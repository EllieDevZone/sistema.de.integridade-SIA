SI-AIA — Sistema de Auditoria e Integridade de Arquivos

«Um sistema de vigilância para arquivos.

O SI-AIA é uma aplicação desenvolvida para monitorar a integridade de arquivos e identificar possíveis alterações dentro de uma pasta.

De forma simples: você seleciona uma pasta, o sistema registra o estado original dos arquivos e, posteriormente, pode verificar se algo foi modificado, removido ou apresenta alguma anomalia.

O projeto foi desenvolvido com foco em aplicações relacionadas à Computação Forense 🕵️‍♀️ e Cibersegurança 🛡️.

---

Como funciona?

Imagine que o sistema tira uma “impressão digital” de cada arquivo da pasta.

Essa impressão digital é criada usando o algoritmo criptográfico SHA-256.

Depois, quando uma auditoria é realizada, o sistema cria uma nova impressão digital dos arquivos e compara com o registro original.

Resultado:

🟢 Íntegro — o arquivo continua igual ao original.

🟡 Alterado — o arquivo foi modificado desde o último registro.

🔴 Ausente — um arquivo que existia anteriormente não foi encontrado.

⚠️ Anomalia — foi identificada uma diferença entre o estado atual e a linha de base original.

---

 Fluxo do sistema

 Escanear o diretório

O usuário seleciona uma pasta que deseja monitorar.

O sistema analisa todos os arquivos presentes no diretório e cria uma linha de base de integridade utilizando hashes SHA-256.

Pasta selecionada
        ↓
Escaneamento dos arquivos
        ↓
Geração dos hashes SHA-256
        ↓
Armazenamento da linha de base

---

2️⃣ Os arquivos podem ser utilizados normalmente

Após criar a linha de base, os arquivos continuam podendo ser modificados normalmente.

Por exemplo:

- Um documento pode ser editado;
- Um arquivo pode ser removido;
- arquivos podem sofrer alterações.

O sistema não bloqueia as modificações.

Ele registra o estado original para que seja possível verificar posteriormente se algo mudou.

---

3️⃣ Auditar a integridade

Durante uma auditoria, o sistema escaneia novamente os arquivos e compara os hashes atuais com os hashes armazenados na linha de base.

  Hash original
        VS
  Hash atual

Se houver diferença, o sistema identifica a alteração.

---

 Tecnologias utilizadas

- 🐍 Python — lógica e processamento do sistema
- 🗄️ SQLite — armazenamento dos registros e da linha de base
- 🖥️ Streamlit — interface web local
- 🔐 SHA-256 — verificação da integridade dos arquivos

---

  Funcionalidades

- 📁 Escaneamento recursivo de diretórios
- 🔐 Geração de hashes SHA-256
- 🗄️ Criação de linha de base de integridade
- 🔍 Auditoria dos arquivos monitorados
- ⚠️ Detecção de arquivos alterados
- 🗑️ Detecção de arquivos removidos ou ausentes
- 📋 Listagem dos arquivos monitorados
- 🖥️ Interface gráfica local com Streamlit
- 💻 Interface de terminal disponível

---

 Instalação

É recomendado utilizar Python 3.10 ou superior.

Clone o repositório:

git clone https://github.com/EllieDevZone/sistema.de.integridade-SIA.git

Entre na pasta do projeto:

cd sistema.de.integridade-SIA

Crie um ambiente virtual:

python -m venv .venv

Windows PowerShell

.\.venv\Scripts\Activate.ps1

Instale as dependências:

pip install -r requirements.txt

---

▶️ Executando o sistema

Para iniciar a interface:

streamlit run app.py

A aplicação será aberta no navegador e funcionará localmente no computador.

---

Aplicações

Este tipo de sistema pode ser utilizado em contextos como:

- 🛡️ Cibersegurança
- 🕵️ Computação Forense
- 🔍 Auditoria de arquivos
- 📁 Monitoramento de integridade
- 🚨 Identificação de alterações não autorizadas
- 💻 Análise de possíveis incidentes de segurança

---

  Segurança

A linha de base não é atualizada automaticamente quando um arquivo sofre uma alteração.

Isso é intencional.

Se o sistema atualizasse automaticamente os hashes após uma modificação, uma possível alteração suspeita poderia ser aceita como legítima.

Por isso, o objetivo da auditoria é primeiro identificar e registrar diferenças, permitindo que o usuário analise o que aconteceu antes de criar uma nova linha de base.

---

  Objetivo do projeto

O SI-AIA foi desenvolvido como um projeto prático voltado para o estudo e aplicação de conceitos de:

Python • Cibersegurança • Criptografia • Integridade de Dados • Computação Forense

---

  Desenvolvido por

EllieDevZone

Projeto desenvolvido para fins de estudo, portfólio e exploração de tecnologias relacionadas à Computação Forense e Cibersegurança.
