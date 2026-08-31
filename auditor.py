import os
from datetime import datetime
from database import get_all_files
from integrity import calculate_sha256


def audit_files() -> dict:
    registros = get_all_files()
    if not registros:
        return {"success": False, "error": "Nenhum arquivo registrado. Faça um escaneamento primeiro."}

    intactos, alterados, removidos, erros = [], [], [], []
    for _id, file_path, hash_original, registrado_em in registros:
        if not os.path.exists(file_path):
            removidos.append(file_path)
            continue
        try:
            hash_atual = calculate_sha256(file_path)
        except (PermissionError, OSError) as exc:
            erros.append({"path": file_path, "error": str(exc)})
            continue
        if hash_atual == hash_original:
            intactos.append(file_path)
        else:
            alterados.append({"path": file_path, "original": hash_original, "current": hash_atual})

    return {
        "success": True,
        "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
        "total": len(registros),
        "intact": intactos,
        "modified": alterados,
        "missing": removidos,
        "errors": erros,
    }


def run_audit() -> None:
    result = audit_files()
    if not result["success"]:
        print(result["error"])
        return
    print(f"\n=== Relatório de Auditoria — {result['timestamp']} ===")
    print(f"Íntegros: {len(result['intact'])}")
    print(f"Alterados: {len(result['modified'])}")
    print(f"Ausentes/removidos: {len(result['missing'])}")
    if result["errors"]:
        print(f"Erros de leitura: {len(result['errors'])}")
