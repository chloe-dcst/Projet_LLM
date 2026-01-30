import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier src au path
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from agents import Runner
from agent import get_agent

st.title("Portfolio IA de Chloé DECOUST")

# Initialiser l'agent
if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Boutton : nouvelle conversation
if st.button("Nouvelle conversation"):
    st.session_state.messages = []
    st.rerun()

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Posez votre question..."):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Afficher la réponse de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                # Construire le contexte avec l'historique récent
                context_messages = []
                # Prendre les 4 derniers messages (2 échanges) pour ne pas surcharger
                recent_messages = st.session_state.messages[-4:] if len(st.session_state.messages) > 4 else st.session_state.messages[:-1]
                for msg in recent_messages:
                    context_messages.append(f"{msg['role'].capitalize()}: {msg['content']}")
                
                # Construire le prompt avec contexte
                if context_messages:
                    full_prompt = "Historique récent:\n" + "\n".join(context_messages) + f"\n\nQuestion actuelle: {prompt}"
                else:
                    full_prompt = prompt
                
                # Exécuter l'agent
                result = Runner.run_sync(st.session_state.agent, full_prompt)
                
                # Extraire la réponse
                response = result.final_output if hasattr(result, 'final_output') else str(result)
                
                # Afficher la réponse
                st.markdown(response)
                
                # Ajouter à l'historique
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Erreur : {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})