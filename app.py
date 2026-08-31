from pathlib import Path
import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog

import streamlit as st

from auditor import audit_files
from database import create_database, delete_all_files, get_all_files, update_file_hash
from scanner import scan_directory

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="SI-AIA | Auditoria e Integridade", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
create_database()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0b1020; }
[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #263248; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
.block-container { padding-top: 2rem; max-width: 1400px; }
.hero { padding: 1.2rem 1.4rem; border: 1px solid #263248; border-radius: 16px; background: linear-gradient(135deg,#121a2d,#0f172a); margin-bottom: 1.2rem; }
.hero h1 { margin: 0; font-size: 2rem; }
.hero p { color: #9ca3af; margin: .35rem 0 0; }
.metric { border: 1px solid #263248; border-radius: 14px; padding: 1rem; background: #111827; min-height: 115px; }
.metric .label { color: #9ca3af; font-size: .86rem; }
.metric .value { font-size: 2rem; font-weight: 700; margin-top: .2rem; }
.status-ok { color:#34d399; font-weight:700; }
.status-bad { color:#f87171; font-weight:700; }
.status-warn { color:#fbbf24; font-weight:700; }
.small { color:#9ca3af; font-size:.82rem; }
code { color:#c4b5fd !important; }
</style>
""", unsafe_allow_html=True)


def choose_folder() -> str:
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title="Selecione o diretório para monitorar")
    root.destroy()
    return folder or ""


def metric(label: str, value: int):
    st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>', unsafe_allow_html=True)


def short_path(path: str, max_len: int = 90) -> str:
    return path if len(path) <= max_len else "…" + path[-(max_len-1):]

st.markdown('<div class="hero"><h1>🛡️ SI-AIA</h1><p>Sistema de Auditoria e Integridade de Arquivos · SHA-256 · SQLite</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## SI-AIA")
    page = st.radio("Navegação", ["Dashboard", "Escanear diretório", "Auditar integridade", "Arquivos monitorados", "Configurações"])
    st.divider()
    st.caption("Aplicação local")
    st.caption(f"Banco: {Path(BASE_DIR / 'audit.db').name}")

registros = get_all_files()

if page == "Dashboard":
    st.subheader("Visão geral")
    result = st.session_state.get("last_audit")
    total = len(registros)
    intact = len(result["intact"]) if result and result.get("success") else 0
    modified = len(result["modified"]) if result and result.get("success") else 0
    missing = len(result["missing"]) if result and result.get("success") else 0

    cols = st.columns(4)
    with cols[0]: metric("Arquivos monitorados", total)
    with cols[1]: metric("Íntegros (última auditoria)", intact)
    with cols[2]: metric("Alterados", modified)
    with cols[3]: metric("Ausentes / removidos", missing)

    st.write("")
    if not registros:
        st.info("Nenhum arquivo está na linha de base. Vá em **Escanear diretório** para começar.")
    elif result and result.get("success"):
        if modified or missing:
            st.error("⚠️ Foram encontradas anomalias na última auditoria.")
        else:
            st.success("✓ Integridade verificada: nenhuma anomalia encontrada na última auditoria.")
        st.caption(f"Última auditoria: {result['timestamp']}")
    else:
        st.warning("A linha de base existe, mas ainda não foi executada uma auditoria nesta sessão.")

    st.markdown("### Fluxo recomendado")
    st.markdown("1. **Escanear diretório** → cria a linha de base SHA-256.  \n2. Alterações nos arquivos podem ser feitas normalmente.  \n3. **Auditar integridade** → compara os hashes atuais com a linha de base.")

elif page == "Escanear diretório":
    st.subheader("Escanear diretório")
    st.write("Selecione uma pasta. O SI-AIA percorre os arquivos recursivamente e registra o SHA-256 de cada arquivo novo.")
    col1, col2 = st.columns([5,1])
    with col1:
        directory = st.text_input("Caminho do diretório", placeholder=r"C:\Users\SeuNome\Documentos")
    with col2:
        st.write("")
        st.write("")
        if st.button("📁 Procurar", use_container_width=True):
            selected = choose_folder()
            if selected:
                st.session_state["directory"] = selected
                st.rerun()
    if "directory" in st.session_state and not directory:
        directory = st.session_state["directory"]
        st.info(f"Diretório selecionado: `{directory}`")
    if st.button("🔎 Iniciar escaneamento", type="primary", use_container_width=True):
        if not directory:
            st.error("Informe ou selecione um diretório.")
        else:
            with st.spinner("Calculando hashes SHA-256..."):
                result = scan_directory(directory)
            if result["success"]:
                st.success("Escaneamento concluído.")
                a,b,c = st.columns(3)
                with a: metric("Novos registrados", result["registered"])
                with b: metric("Já existentes", result["existing"])
                with c: metric("Erros de leitura", result["errors"])
                st.caption(f"Diretório: {result['directory']}")
            else:
                st.error(result["error"])

elif page == "Auditar integridade":
    st.subheader("Auditoria de integridade")
    st.write("Compara o SHA-256 atual de cada arquivo com a linha de base armazenada no SQLite.")
    if not registros:
        st.warning("Não existem arquivos monitorados. Faça um escaneamento primeiro.")
    elif st.button("🛡️ Executar auditoria agora", type="primary", use_container_width=True):
        with st.spinner("Verificando integridade..."):
            result = audit_files()
        st.session_state["last_audit"] = result
        st.rerun()

    result = st.session_state.get("last_audit")
    if result and result.get("success"):
        st.divider()
        a,b,c,d = st.columns(4)
        with a: metric("Total", result["total"])
        with b: metric("Íntegros", len(result["intact"]))
        with c: metric("Alterados", len(result["modified"]))
        with d: metric("Ausentes", len(result["missing"]))
        if not result["modified"] and not result["missing"] and not result["errors"]:
            st.success("✓ Nenhuma anomalia detectada.")
        if result["modified"]:
            st.error(f"ALTERAÇÕES DETECTADAS: {len(result['modified'])}")
            for item in result["modified"]:
                st.write(f"**{short_path(item['path'])}**")
                st.caption(f"Original: {item['original']}  |  Atual: {item['current']}")
        if result["missing"]:
            st.warning(f"ARQUIVOS AUSENTES/REMOVIDOS: {len(result['missing'])}")
            for path in result["missing"]:
                st.write(f"- `{path}`")
        if result["errors"]:
            st.warning(f"Erros de leitura: {len(result['errors'])}")

elif page == "Arquivos monitorados":
    st.subheader("Arquivos monitorados")
    st.caption(f"{len(registros)} arquivo(s) registrado(s) na linha de base.")
    if registros:
        for _id, path, sha, registered_at in registros:
            with st.expander(f"#{_id} · {short_path(path)}"):
                st.write(f"**Caminho:** `{path}`")
                st.write(f"**SHA-256:** `{sha}`")
                st.write(f"**Registrado em:** {registered_at}")
                if os.path.exists(path):
                    st.markdown('<span class="status-ok">● Arquivo presente</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-bad">● Arquivo ausente</span>', unsafe_allow_html=True)
    else:
        st.info("Nenhum arquivo registrado.")

elif page == "Configurações":
    st.subheader("Configurações")
    st.warning("A linha de base é uma evidência. Não altere os hashes automaticamente após uma auditoria.")
    st.markdown("**Local do banco:**")
    st.code(str(BASE_DIR / "audit.db"))
    st.divider()
    st.markdown("### Recriar linha de base")
    st.write("Use esta opção somente quando quiser apagar a linha de base atual e começar outra.")
    confirm = st.checkbox("Entendo que esta ação apagará todos os registros atuais.")
    if st.button("🗑️ Apagar linha de base", disabled=not confirm):
        delete_all_files()
        st.session_state.pop("last_audit", None)
        st.success("Linha de base apagada. Faça um novo escaneamento.")
        st.rerun()

st.divider()
st.caption("SI-AIA · Auditoria e Integridade de Arquivos · Python + Streamlit + SQLite + SHA-256")
