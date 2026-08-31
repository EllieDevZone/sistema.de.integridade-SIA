import os
from datetime import datetime
from database import register_file
from integrity import calculate_sha256


def scan_directory(directory_path: str) -> dict:
    """Percorre um diretório recursivamente e registra uma linha de base."""
    if not os.path.isdir(directory_path):
        return {"success": False, "error": f"'{directory_path}' não é um diretório válido."}

    registrados, ja_existentes, erros = 0, 0, 0
    for root, _, files in os.walk(directory_path):
        for filename in files:
            full_path = os.path.abspath(os.path.join(root, filename))
            try:
                file_hash = calculate_sha256(full_path)
            except (PermissionError, OSError):
                erros += 1
                continue

            timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
            if register_file(full_path, file_hash, timestamp):
                registrados += 1
            else:
                ja_existentes += 1

    return {
        "success": True,
        "registered": registrados,
        "existing": ja_existentes,
        "errors": erros,
        "directory": directory_path,
    }
