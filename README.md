# SI-AIA — Sistema de Auditoria e Integridade de Arquivos

Aplicação local para criar uma linha de base criptográfica de arquivos e verificar posteriormente sua integridade usando **SHA-256**. A interface é feita com **Streamlit** e os registros são armazenados em **SQLite**.

## Recursos

- Escaneamento recursivo de diretórios
- Cálculo de hash SHA-256
- Linha de base persistente em SQLite
- Detecção de arquivos alterados
- Detecção de arquivos ausentes/removidos
- Listagem dos arquivos monitorados
- Interface web local
- Interface de terminal original preservada em `main.py`

## Instalação

Recomendado: Python 3.10+.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar a interface

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador. Ela roda localmente no computador.

## Fluxo de uso

1. Abra **Escanear diretório**.
2. Selecione a pasta que deseja monitorar.
3. Execute o escaneamento para criar a linha de base.
4. Faça as alterações normalmente.
5. Abra **Auditar integridade** e execute a auditoria.
6. Arquivos alterados ou ausentes serão destacados.

## Segurança e GitHub

A linha de base **não é atualizada automaticamente** quando um arquivo muda. Isso é deliberado: uma alteração deve ser detectada antes de qualquer rebaseline.
