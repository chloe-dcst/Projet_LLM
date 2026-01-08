"""
Interface Streamlit pour interagir avec l'agent portfolio.
"""

import streamlit as st
from agent import portfolio_agent
from agents import Runner

# Configuration de la page
st.set_page_config(
    page_title="Portfolio Chloé Découst",
    page_icon="💼",
    layout="centered"
)

# Titre et description
st.title("💼 Portfolio Assistant - Chloé Découst")
st.markdown("""
Posez-moi des questions sur le parcours, les compétences et les projets de Chloé !

**Exemples de questions :**
- Quelles sont ses compétences en Python ?
- Parle-moi de son expérience avec le basket-ball
- Quels projets a-t-elle réalisés ?
""")

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Posez votre question..."):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Afficher la réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            # Construire le contexte avec les derniers messages
            context_prompt = prompt
            if len(st.session_state.messages) > 0:
                # Inclure les 2 derniers échanges pour le contexte
                recent_messages = st.session_state.messages[-4:] if len(st.session_state.messages) >= 4 else st.session_state.messages
                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
                context_prompt = f"Contexte de la conversation précédente:\n{context}\n\nQuestion actuelle: {prompt}"
            
            # Exécuter l'agent
            result = Runner.run_sync(portfolio_agent, context_prompt)
            response = result.final_output
            
            # Afficher la réponse
            st.markdown(response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Bouton pour effacer l'historique
if st.session_state.messages:
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
