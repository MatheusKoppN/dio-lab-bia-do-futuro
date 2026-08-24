# 💵🤖 Kofin - Assistente de Educação e Organização Financeira

> Um assistente virtual inteligente e interativo construído com Python, Streamlit e a API do Google Gemini, focado em ajudar iniciantes a organizarem suas finanças pessoais de forma despojada e sem complicações.

---

## 📌 Sobre o Projeto

O **Kofin** é um chatbot interativo desenvolvido para simplificar a educação financeira. Ele analisa o perfil financeiro do usuário (ou simula dados pré-definidos) e oferece orientações baseadas no método **50/30/20**, além de calcular metas para reserva de emergência e integrar dados de mercado em tempo real, como a **Taxa Selic** obtida via API oficial do Banco Central do Brasil.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.10+](https://www.python.org/)
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Modelo de IA:** Google Gemini API (`google-genai` SDK)
- **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
- **Integração de APIs:** [Requests](https://requests.readthedocs.io/)
- **Gerenciamento de Versão:** Git e GitHub

---

## 📁 Estrutura do Repositório

```text
kofin_bot/
├── .streamlit/
│   └── secrets.toml          # Configuração segura de chaves (ignorado no Git)
├── data/
│   └── infos_ed_financeira.md # Base de conhecimento em Markdown
├── docs/
│   └── documentacao.md        # Documentação e prompt engineering do agente
├── src/
│   └── app.py                 # Código principal da aplicação Streamlit
├── .gitignore                 # Arquivos e pastas ignorados pelo Git
├── README.md                  # Documentação do repositório
└── requirements.txt           # Dependências do projeto
```

***🚀 Como Executar o Projeto***
**Pré-requisitos**
*Python 3.10 ou superior instalado.*

*Chave de API do Google Gemini (obtida no Google AI Studio).*

***Passo a Passo***

**Clone o repositório:**


```
git clone [https://github.com/seu-usuario/kofin_bot.git](https://github.com/seu-usuario/kofin_bot.git)
cd kofin_bot
```
*Crie e ative um ambiente virtual (recomendado):*

# Windows (PowerShell)
```
python -m venv venv
.\venv\Scripts\activate
```

# Linux/Mac
```
python3 -m venv venv
source venv/bin/activate
```

*Instale as dependências:*

```
pip install -r requirements.txt
```

*Configure a Chave de API:*
Crie a pasta .streamlit na raiz e dentro dela o arquivo secrets.toml:

```
GEMINI_API_KEY = "SUA_CHAVE_AQUI"
```
*Rode a aplicação:*

```
python -m streamlit run src/app.py
```

***⚙️ Funcionalidades Principais***

*Perfil Personalizado ou Simulado:* O usuário pode preencher renda e despesas manualmente na barra lateral ou alternar para perfis simulados para testes rápidos.

*Integração com Banco Central:* Consulta automática da taxa Selic atualizada via API do BCB.

*Chat Interativo:* Conversa em tempo real orientada por System Prompt ajustado para garantir respostas educativas, empáticas e seguras (sem recomendações de alto risco).

*Proteção de Dados:* Gerenciamento seguro de credenciais via secrets.toml e regras no .gitignore.

***📜 Licença***
Este projeto foi desenvolvido para fins educacionais e de portfólio.
