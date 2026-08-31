import argparse
from database import create_database, get_all_files
from scanner import scan_directory
from auditor import run_audit


def cmd_init(args):
    create_database()
    print("Banco de dados inicializado.")


def cmd_scan(args):
    scan_directory(args.directory)


def cmd_audit(args):
    run_audit()


def cmd_list(args):
    registros = get_all_files()
    if not registros:
        print("Nenhum arquivo registrado.")
        return
    for _id, path, hash_val, registrado_em in registros:
        print(f"[{_id}] {path}\n    hash: {hash_val}\n    registrado em: {registrado_em}\n")


def main():
    parser = argparse.ArgumentParser(description="Sistema de Auditoria e Integridade de Arquivos")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    subparsers.add_parser("init", help="Cria o banco de dados").set_defaults(func=cmd_init)

    p_scan = subparsers.add_parser("scan", help="Escaneia um diretório e registra a linha de base")
    p_scan.add_argument("directory", help="Caminho do diretório a escanear")
    p_scan.set_defaults(func=cmd_scan)

    subparsers.add_parser("audit", help="Verifica a integridade dos arquivos registrados").set_defaults(func=cmd_audit)
    subparsers.add_parser("list", help="Lista os arquivos registrados").set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()