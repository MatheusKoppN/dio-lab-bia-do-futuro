import os
import requests
import streamlit as st
from google import genai

# 1. Configuração da página
st.set_page_config(page_title="Kofin - Finanças Pessoais", page_icon="🪙", layout="wide")

# 2. Autenticação na API
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("⚠️ Chave de API do Gemini não encontrada! Verifique os segredos da aplicação.")
    st.stop()

client = genai.Client(api_key=gemini_key)

# 3. Consulta da Taxa Selic
@st.cache_data(ttl=3600)
def obter_taxa_selic():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return f"{res.json()[0]['valor']}% a.a."
    except Exception:
        pass
    return "Taxa indisponível no momento"

# 4. Base de Conhecimento
@st.cache_data
def carregar_base_conhecimento():
    caminho = os.path.join("data", "infos_ed_financeira.md")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "Diretrizes padrão: Regra 50/30/20 e Reserva de Emergência de 3 a 6 meses de custos fixos."

base_texto = carregar_base_conhecimento()
selic_atual = obter_taxa_selic()

# 5. Barra Lateral
st.sidebar.header("👤 Perfil Financeiro")
opcao_dados = st.sidebar.radio("Escolha a origem dos dados:", ["Inserir meus dados", "Perfil simulado"])

if opcao_dados == "Inserir meus dados":
    with st.sidebar.form("form_dados_usuario"):
        nome = st.text_input("Nome:", value="Usuário")
        renda = st.number_input("Renda mensal (R$):", min_value=0.0, value=3000.0, step=100.0)
        gastos_fixos = st.number_input("Gastos Essenciais (R$):", min_value=0.0, value=1500.0, step=50.0)
        gastos_lazer = st.number_input("Gastos Fúteis/Lazer (R$):", min_value=0.0, value=900.0, step=50.0)
        meta = st.text_input("Objetivo principal:", value="Criar reserva de emergência")
        st.form_submit_button("Salvar Perfil")

    contexto_usuario = f"""
    - Nome: {nome}
    - Renda Mensal: R$ {renda:.2f}
    - Gastos Essenciais: R$ {gastos_fixos:.2f}
    - Lazer/Desejos: R$ {gastos_lazer:.2f}
    - Meta Principal: {meta}
    """
else:
    cliente_mock = st.sidebar.selectbox("Selecione um perfil:", ["João Silva (Iniciante)", "Maria Oliveira (Organizada)"])
    contexto_usuario = f"- Perfil Simulado: {cliente_mock}"

# 6. Prompt do Sistema (Ajustado para tom natural)
system_instruction = f"""
Você é o Kofin, um assistente prático focado em organização financeira e orçamento pessoal.

REGRAS DE RESPOSTA:
- Responda de forma direta, clara e amigável, sem exagerar em emojis ou gírias forçadas.
- Explique conceitos financeiros com analogias simples do dia a dia.
- Baseie suas recomendações prioritariamente na Base de Conhecimento abaixo.
- Compare a renda e os gastos do usuário com o método 50/30/20 sempre que for pertinente.
- NUNCA recomende compra de ações específicas, criptomoedas ou prometa rentabilidade.
- Finalize as respostas sugerindo um próximo passo prático ou fazendo uma pergunta objetiva.

BASE DE CONHECIMENTO:
{base_texto}

DADOS DE CONTEXTO:
- Selic Atual: {selic_atual}
- Dados do Usuário:
{contexto_usuario}
"""

# 7. Interface
st.title("💵 Kofin")
st.caption(f"Selic hoje: **{selic_atual}**")

# 8. Inicialização das Mensagens e da Sessão do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Já recebi seus dados na barra lateral. O que gostaria de analisar no seu orçamento hoje?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 9. Loop do Chat
if user_input := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        with st.spinner("Analisando..."):
            # Chamada utilizando o modelo Flash estável
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input,
                config={"system_instruction": system_instruction}
            )
            bot_reply = response.text

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)

    except Exception as e:
        st.error(f"Erro ao consultar o assistente: {e}")
