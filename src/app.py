import os
import requests
import streamlit as st
from google import genai

st.set_page_config(page_title="Kofin - Financial Assistant", page_icon="🪙", layout="wide")

TRANSLATIONS = {
    "EN": {
        "page_title": "💵 Kofin - Financial Assistant",
        "page_caption": "Today's Selic Rate:",
        "api_error": "⚠️ Gemini API key not found! Check your application secrets.",
        "selic_unavailable": "Rate unavailable at the moment",
        "sidebar_settings": "Settings",
        "sidebar_header": "👤 Financial Profile",
        "radio_label": "Select data source:",
        "radio_manual": "Input my data",
        "radio_mock": "Simulated profile",
        "input_name": "Name:",
        "input_income": "Monthly Income (BRL):",
        "input_fixed": "Essential Expenses (BRL):",
        "input_leisure": "Leisure / Desires (BRL):",
        "input_goal": "Main Goal:",
        "btn_save_profile": "Save Profile",
        "default_goal": "Build emergency fund",
        "mock_label": "Select a profile:",
        "mock_1": "John Doe (Beginner)",
        "mock_2": "Mary Smith (Organized)",
        "chat_initial": "Hello! I received your details from the sidebar. What would you like to analyze in your budget today?",
        "chat_input_placeholder": "Type your message...",
        "chat_spinner": "Analyzing...",
        "chat_error": "Error querying the assistant:",
        "sys_prompt_role": "You are Kofin, a practical AI assistant focused on personal finance and budgeting.",
        "sys_prompt_rules": """
RESPONSE RULES:
- Respond in English directly, clearly, and in a friendly tone without overusing emojis or forced slang.
- Explain financial concepts using simple everyday analogies.
- Base your recommendations primarily on the Knowledge Base below.
- Compare the user's income and expenses with the 50/30/20 budget rule whenever relevant.
- NEVER recommend specific stock purchases, cryptocurrencies, or promise financial returns.
- Conclude responses by suggesting a practical next step or asking an objective question.
"""
    },
    "PT": {
        "page_title": "💵 Kofin - Assistente Financeiro",
        "page_caption": "Selic hoje:",
        "api_error": "⚠️ Chave de API do Gemini não encontrada! Verifique os segredos da aplicação.",
        "selic_unavailable": "Taxa indisponível no momento",
        "sidebar_settings": "Configurações",
        "sidebar_header": "👤 Perfil Financeiro",
        "radio_label": "Escolha a origem dos dados:",
        "radio_manual": "Inserir meus dados",
        "radio_mock": "Perfil simulado",
        "input_name": "Nome:",
        "input_income": "Renda mensal (R$):",
        "input_fixed": "Gastos Essenciais (R$):",
        "input_leisure": "Gastos Fúteis/Lazer (R$):",
        "input_goal": "Objetivo principal:",
        "btn_save_profile": "Salvar Perfil",
        "default_goal": "Criar reserva de emergência",
        "mock_label": "Selecione um perfil:",
        "mock_1": "João Silva (Iniciante)",
        "mock_2": "Maria Oliveira (Organizada)",
        "chat_initial": "Olá! Já recebi seus dados na barra lateral. O que gostaria de analisar no seu orçamento hoje?",
        "chat_input_placeholder": "Digite sua mensagem...",
        "chat_spinner": "Analisando...",
        "chat_error": "Erro ao consultar o assistente:",
        "sys_prompt_role": "Você é o Kofin, um assistente prático focado em organização financeira e orçamento pessoal.",
        "sys_prompt_rules": """
REGRAS DE RESPOSTA:
- Responda em Português de forma direta, clara e amigável, sem exagerar em emojis ou gírias forçadas.
- Explique conceitos financeiros com analogias simples do dia a dia.
- Baseie suas recomendações prioritariamente na Base de Conhecimento abaixo.
- Compare a renda e os gastos do usuário com o método 50/30/20 sempre que for pertinente.
- NUNCA recomende compra de ações específicas, criptomoedas ou prometa rentabilidade.
- Finalize as respostas sugerindo um próximo passo prático ou fazendo uma pergunta objetiva.
"""
    }
}

st.sidebar.markdown("### Settings")
selected_lang = st.sidebar.selectbox("🌐 Language / Idioma", ["English (EN)", "Português (PT)"], index=0)
lang_code = "EN" if "English" in selected_lang else "PT"
t = TRANSLATIONS[lang_code]

gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    st.error(t["api_error"])
    st.stop()

client = genai.Client(api_key=gemini_key)

@st.cache_data(ttl=3600)
def obter_taxa_selic():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return f"{res.json()[0]['valor']}% p.a."
    except Exception:
        pass
    return t["selic_unavailable"]

@st.cache_data
def carregar_base_conhecimento():
    caminho = os.path.join("data", "infos_ed_financeira.md")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "Standard Guidelines: 50/30/20 Rule and Emergency Fund targeting 3 to 6 months of fixed expenses."

base_texto = carregar_base_conhecimento()
selic_atual = obter_taxa_selic()

st.sidebar.header(t["sidebar_header"])
opcao_dados = st.sidebar.radio(t["radio_label"], [t["radio_manual"], t["radio_mock"]])

if opcao_dados == t["radio_manual"]:
    with st.sidebar.form("form_dados_usuario"):
        nome = st.text_input(t["input_name"], value="User")
        renda = st.number_input(t["input_income"], min_value=0.0, value=3000.0, step=100.0)
        gastos_fixos = st.number_input(t["input_fixed"], min_value=0.0, value=1500.0, step=50.0)
        gastos_lazer = st.number_input(t["input_leisure"], min_value=0.0, value=900.0, step=50.0)
        meta = st.text_input(t["input_goal"], value=t["default_goal"])
        st.form_submit_button(t["btn_save_profile"])

    contexto_usuario = f"""
    - Name: {nome}
    - Monthly Income: R$ {renda:.2f}
    - Essential Expenses: R$ {gastos_fixos:.2f}
    - Leisure/Wants: R$ {gastos_lazer:.2f}
    - Primary Goal: {meta}
    """
else:
    cliente_mock = st.sidebar.selectbox(t["mock_label"], [t["mock_1"], t["mock_2"]])
    contexto_usuario = f"- Simulated Profile: {cliente_mock}"

system_instruction = f"""
{t['sys_prompt_role']}

{t['sys_prompt_rules']}

KNOWLEDGE BASE:
{base_texto}

CONTEXT DATA:
- Current Selic Rate: {selic_atual}
- User Financial Profile:
{contexto_usuario}
"""

st.title(t["page_title"])
st.caption(f"{t['page_caption']} **{selic_atual}**")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": t["chat_initial"]}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input(t["chat_input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        with st.spinner(t["chat_spinner"]):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config={"system_instruction": system_instruction}
            )
            bot_reply = response.text

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

    except Exception as e:
        st.error(f"{t['chat_error']} {e}")
