# Trading Bot - Sistema Completo com IA

Este projeto consiste em um sistema de trading automatizado que utiliza inteligência artificial para tomar decisões de compra e venda de criptomoedas na exchange Binance. O sistema é composto por um backend em Python (Flask) que contém a lógica do bot e a API, e um frontend em React (Next.js) que serve como um dashboard para controle e monitoramento.

## Arquitetura e Funcionalidades

- **Backend (Python/Flask):**
  - **API RESTful:** Para comunicação com o frontend, com endpoints para autenticação, controle do bot e visualização de dados.
  - **Lógica de Trading com IA:** Utiliza modelos de Machine Learning (XGBoost e RandomForest) treinados com dados históricos para prever movimentos de preço.
  - **Análise Técnica:** Incorpora uma vasta gama de indicadores técnicos (RSI, Bandas de Bollinger, ADX, etc.) para filtrar e confirmar os sinais da IA.
  - **Gerenciamento de Risco:** Implementa estratégias de Take Profit e Stop Loss dinâmicos para otimizar saídas e proteger o capital.
  - **Persistência de Dados:** Utiliza um banco de dados PostgreSQL para armazenar usuários, chaves de API (criptografadas), histórico de trades e configurações do bot.
  - **Segurança:** Autenticação baseada em tokens JWT e criptografia das chaves da API da Binance.

- **Frontend (React/Next.js):**
  - **Dashboard Interativo:** Interface para monitorar o status do bot, posições abertas, performance do portfólio e sinais de trading em tempo real.
  - **Autenticação de Usuário:** Telas de login e registro seguras.
  - **Controle Remoto:** Botões para iniciar e parar o bot de forma segura.
  - **Visualização de Dados:** Gráficos e tabelas para análise de performance e histórico de operações.

- **Banco de Dados (PostgreSQL):**
  - Estrutura robusta para garantir a persistência e a integridade dos dados, permitindo que o bot recupere seu estado mesmo após reinicializações.

## Stack Tecnológica

- **Backend:** Python, Flask, SQLAlchemy, Psycopg2, Flask-JWT-Extended, Flask-Cors, python-binance, TA, Scikit-learn, XGBoost.
- **Frontend:** TypeScript, React, Next.js, Tailwind CSS, Recharts, Axios.
- **Banco de Dados:** PostgreSQL.

## Pré-requisitos

- Python 3.11 ou superior
- Node.js e npm
- PostgreSQL
- Git

## Guia de Instalação e Execução

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento.

### 1. Configuração do Banco de Dados

1.  **Instale o PostgreSQL** no seu sistema.
2.  Inicie o serviço do PostgreSQL.
3.  Crie o banco de dados e o usuário para a aplicação:

    ```sql
    CREATE DATABASE trading_bot_db;
    CREATE USER trading_bot_user WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE trading_bot_db TO trading_bot_user;
    ```

4.  Execute o script `setup_db.sql` (localizado na raiz do projeto) para criar as tabelas necessárias. Pode ser necessário fornecer a senha (`password`) durante a execução.

    ```bash
    psql -h localhost -d trading_bot_db -U trading_bot_user -f setup_db.sql
    ```

### 2. Configuração do Backend

1.  Navegue até a raiz do projeto.
2.  Instale as dependências do Python:

    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Um arquivo `requirements.txt` será gerado na próxima etapa)*

3.  Gere o arquivo `requirements.txt` (opcional, mas recomendado):

    ```bash
    pip freeze > requirements.txt
    ```

4.  Inicie o servidor do backend:

    ```bash
    python run.py
    ```

    O servidor estará em execução em `http://localhost:5000`.

### 3. Configuração do Frontend

1.  Navegue até o diretório do frontend:

    ```bash
    cd frontend/trading-bot-dashboard
    ```

2.  Crie um arquivo de ambiente `.env.local` na raiz do diretório `frontend/trading-bot-dashboard` e adicione a URL da API do backend:

    ```
    NEXT_PUBLIC_API_URL=http://localhost:5000/api
    ```

3.  Instale as dependências do Node.js. Pode ser necessário usar a flag `--legacy-peer-deps` devido a conflitos de versão entre as bibliotecas.

    ```bash
    npm install --legacy-peer-deps
    ```

4.  Inicie o servidor de desenvolvimento do frontend:

    ```bash
    npm run dev
    ```

    A aplicação estará acessível em `http://localhost:3000` (ou outra porta, caso a 3000 esteja em uso).

## Uso

1.  Abra o navegador e acesse `http://localhost:3000`.
2.  Crie uma nova conta na tela de **Registro**, fornecendo um nome de usuário, senha e suas chaves da API da Binance.
3.  Faça **Login** com as credenciais que você acabou de criar.
4.  Você será redirecionado para o dashboard, onde poderá iniciar/parar o bot e monitorar sua atividade.

## Estrutura do Projeto

```
/
├── backend/                # Código-fonte do backend (Flask)
│   ├── api/                # Módulo da API (rotas)
│   ├── bot/                # Lógica do bot de trading
│   ├── utils/              # Funções utilitárias (segurança)
│   ├── __init__.py         # Fábrica da aplicação Flask
│   ├── config.py           # Configurações
│   ├── database.py         # Configuração do banco de dados
│   └── models.py           # Modelos de dados (SQLAlchemy)
├── frontend/               # Código-fonte do frontend (Next.js)
│   └── trading-bot-dashboard/
│       ├── app/            # Páginas e layouts
│       ├── components/     # Componentes React
│       ├── lib/            # Módulos auxiliares (ex: api.ts)
│       └── ...
├── run.py                  # Script para iniciar o servidor backend
├── setup_db.sql            # Script de inicialização do banco de dados
└── README.md               # Esta documentação
```

