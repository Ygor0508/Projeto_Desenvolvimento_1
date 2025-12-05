# 🤖 Robô de Trading de Criptomoedas com IA (MVP)

> Projeto de Desenvolvimento 1 - Sistema automatizado para execução de estratégias de trading na Binance utilizando Análise Técnica e Machine Learning.

## 📋 Sobre o Projeto

Este projeto visa democratizar o acesso a ferramentas de trading automatizado. Diferente de bots simples que usam apenas indicadores fixos, este sistema implementa uma **estratégia híbrida** que combina análise técnica clássica com modelos de Inteligência Artificial (XGBoost) para validar entradas, além de uma gestão de risco dinâmica baseada na volatilidade do mercado (ATR).

### 🚀 Principais Funcionalidades

* **Dashboard Interativo:** Monitoramento em tempo real de saldo, P&L (Lucro/Prejuízo) e posições abertas.
* [cite_start]**Gestão de Risco Dinâmica:** Stop-Loss e Take-Profit calculados via **ATR (Average True Range)**, adaptando-se automaticamente se o mercado está calmo ou agitado.
* [cite_start]**Inteligência Artificial:** Classificador **XGBoost** treinado para filtrar sinais falsos e calcular probabilidade de lucro antes da entrada.
* [cite_start]**Segurança:** Chaves de API da Binance armazenadas com criptografia simétrica (Fernet) no banco de dados.
* **Backtesting:** Motor de simulação que utiliza dados históricos para validar a eficácia da estratégia antes da operação real.
* **Arquitetura Desacoplada:** Frontend (Next.js) e Backend (Python/Flask) independentes.

---

## 🛠️ Tecnologias Utilizadas

### Backend (Inteligência e API)
* **Linguagem:** Python 3.8+
* **Framework:** Flask (API RESTful)
* **IA & Dados:** Scikit-learn, XGBoost, Pandas, TA-Lib
* **Integração:** python-binance
* **Segurança:** Fernet (Cryptography)

### Frontend (Interface)
* **Framework:** Next.js 14 (React)
* **Linguagem:** TypeScript
* **Estilização:** Tailwind CSS
* **Componentes:** Shadcn/UI
* **Gráficos:** Recharts

### Banco de Dados
* **SGBD:** PostgreSQL (NeonDB)
* **ORM:** SQLAlchemy

---

## ⚙️ Instalação e Execução

Como o projeto possui uma arquitetura desacoplada, é necessário rodar o servidor (Back-end) e a interface (Front-end) simultaneamente.

### Pré-requisitos
* Python 3.8+ e Node.js instalados.
* Banco de dados PostgreSQL criado (local ou nuvem).
* Conta na Binance (para obter API Key e Secret Key).

### Passo 1: Configuração do Back-end

1. Acesse a pasta do backend:
   ```bash
   cd backend

2. Crie e ative o ambiente virtual:
    # Windows
    python -m venv venv
        venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

3. Instale as bibliotecas:
    pip install -r requirements.txt

4. Configure como variáveis ​​de ambiente:
    Crie um arquivo .envna pasta backend.

    Adicione a URL do seu banco de dados:DATABASE_URL=postgresql://user:password@host:port/dbname

5. Inicialize o banco e rode o servidor:
    python criar_tabelas.py
    python run.py

    O servidor iniciará emhttp://localhost:5000

### Passo 2: Configuração do Front-end

1. Em um novo terminal, acesse a pasta do frontend:
    cd frontend/trading-bot-dashboard

2. Instale as partes:
    npm install

3. Execute o servidor de desenvolvimento:
    npm run dev

4. Acesse o aplicativo no navegador:
    Abrahttp://localhost:3000

📊 Backtest vs. Produção
O sistema foi projetado para garantir a consistência entre a simulação e a realidade:

![alt text](image.png)

Nota: Embora a interface permita definir porcentagens fixas, o núcleo matemático do robô prioriza o uso do ATR para garantir a segurança estatística em mercados voláteis

🔒 Segurança
A segurança é prioridade neste projeto:

Criptografia: As credenciais da Binance (API Key e Secret) nunca são salvas em texto plano. Elas são criptografadas antes da persistência no banco.

Comunicação: O Backend e Frontend se comunicam via JSON/HTTPS.

Execução Local: As chaves permanecem no ambiente do usuário (ou servidor privado), não sendo compartilhadas com terceiros.

📝 Autor
Desenvolvido por Ygor Campos da Rosa como parte do Projeto de Desenvolvimento 1.