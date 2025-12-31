📅 AgendaDesk
Sua agenda desktop simples, elegante e eficiente

AgendaDesk é uma aplicação desktop em Python criada para quem busca organização, produtividade e praticidade no dia a dia.
Com ela, você gerencia tarefas, compromissos e pautas de conteúdo em um só lugar — com lembretes automáticos, dark mode e funcionamento em segundo plano.

Ideal para estudantes, profissionais, criadores de conteúdo e qualquer pessoa que precise manter a rotina sob controle. ✅

✨ Principais Funcionalidades

✔️ Cadastro de tarefas com data e hora
📝 Campo exclusivo para pauta de conteúdos
🔔 Lembretes automáticos, mesmo com a interface fechada
💾 Persistência de dados local em JSON
🌙 Interface moderna em Dark Mode
✏️ Edição e exclusão de tarefas
📌 Marcação de tarefas como concluídas
🖥️ Aplicação desktop leve, simples e intuitiva

🛠️ Tecnologias Utilizadas

Python 3.10+

Tkinter – Interface gráfica

tkcalendar – Seleção de datas

JSON – Armazenamento local

Pillow (PIL) – Ícones e imagens

Threading – Execução de lembretes em segundo plano

📂 Estrutura do Projeto
AgendaDesk/
│
├── assets/
│   ├── logo.png
│   └── logo.ico
│
├── tarefas.json
├── agendadesk.py
├── lembrete_background.py
└── README.md

📄 Descrição dos Arquivos
🖥️ agendadesk.py

Responsável pela interface principal da aplicação.
Permite cadastrar, editar, excluir, visualizar e marcar tarefas como concluídas.

🔔 lembrete_background.py

Script que roda em segundo plano, verificando os horários das tarefas e exibindo alertas automáticos, mesmo com a interface fechada.

💾 tarefas.json

Arquivo onde todas as tarefas são armazenadas localmente.

🎨 assets/

Contém os ícones e imagens utilizadas na aplicação.

▶️ Como Executar o Projeto
1️⃣ Clone o repositório
git clone https://github.com/seu-usuario/agendadesk.git
cd agendadesk

2️⃣ Instale as dependências
pip install tkcalendar pillow

3️⃣ Execute a aplicação principal
python agendadesk.py

4️⃣ Execute o lembrete em segundo plano
python lembrete_background.py


💡 Dica: o lembrete_background.py pode ser configurado para iniciar automaticamente junto com o sistema operacional.

🔔 Como Funcionam os Lembretes

Baseados nas tarefas salvas no tarefas.json

Funcionam mesmo com a interface fechada

Verificação periódica de horários

Exibição de pop-ups centralizados na tela

🎯 Objetivo do Projeto

O AgendaDesk foi criado para facilitar a organização pessoal e profissional, oferecendo uma solução desktop prática, leve e eficiente para:

Estudos 📚

Trabalho 💼

Produção de conteúdo 🎥

Rotinas diárias 📆

🚀 Possíveis Melhorias Futuras

🔔 Notificações nativas do sistema

📄 Exportação de tarefas (PDF / CSV)

🔍 Filtros por prioridade e data

👤 Suporte a múltiplos perfis

🗄️ Integração com banco de dados

💙 Contribuições

Sinta-se à vontade para abrir issues, sugerir melhorias ou contribuir com o projeto.
Toda ajuda é bem-vinda! 😊