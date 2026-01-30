import streamlit as st
import sys
from pathlib import Path
from agents import Runner
from agent import get_agent

# configuration du path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

st.title("Portfolio IA de Chloé DECOUST")


# style CSS
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0.4rem 0.6rem;
    font-size: 0.9rem;
}

/* Resserre l’espace entre les colonnes */
#quick-buttons [data-testid="column"] {
    padding: 0 0.15rem !important;
}

/* Réserver de la place pour boutons + input */
.main .block-container {
    padding-bottom: 220px !important;
}

/* Espacement propre des messages */
.stChatMessage {
    margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# initialisation de la session
if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# boutton : nouvelle conversation
if st.button("Nouvelle conversation"):
    st.session_state.messages = []
    st.rerun()

# affichage du chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction de récupération et traitement des questions / réponses bouttons
def process_question(question):
    """
    Traite une question posée par l'utilisateur et génère une réponse de l'agent.
    
    Cette fonction gère l'ensemble du cycle de traitement d'une question :
    - Ajoute la question à l'historique de la conversation
    - Récupère le contexte des messages récents (4 derniers échanges)
    - Construit un prompt enrichi avec l'historique pour maintenir la cohérence
    - Interroge l'agent OpenAI qui utilise la recherche vectorielle Upstash
    - Ajoute la réponse à l'historique et actualise l'interface
    
    Args:
        question (str): La question posée par l'utilisateur, soit via les boutons 
                       prédéfinis, soit via la barre de saisie
    
    Returns:
        None: La fonction met à jour directement st.session_state.messages 
              et provoque un rechargement de la page avec st.rerun()
    """
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    context_messages = []
    recent_messages = (
        st.session_state.messages[-5:-1]
        if len(st.session_state.messages) > 1
        else []
    )

    for msg in recent_messages:
        context_messages.append(
            f"{msg['role'].capitalize()}: {msg['content']}"
        )

    full_prompt = (
        "Historique récent:\n"
        + "\n".join(context_messages)
        + f"\n\nQuestion actuelle: {question}"
        if context_messages
        else question
    )

    result = Runner.run_sync(st.session_state.agent, full_prompt)
    response = (
        result.final_output
        if hasattr(result, "final_output")
        else str(result)
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.rerun()

# Boutton : questions proposées
st.markdown('<div id="quick-buttons">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Quelle est sa passion ?"):
        process_question("Quelle est sa passion ?")

with col2:
    if st.button("Quelle est sa formation ?"):
        process_question("Quelle est sa formation ?")

with col3:
    if st.button("Quelles sont ses compétences ?"):
        process_question("Quelles sont ses compétences ?")

st.markdown('</div>', unsafe_allow_html=True)

# Chat classique
if prompt := st.chat_input("Posez votre question..."):
    process_question(prompt)
