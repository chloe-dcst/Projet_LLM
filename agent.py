"""
Agent IA pour répondre aux questions sur le portfolio.
Utilise openai-agents avec une tool de recherche vectorielle (RAG).
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from upstash_vector import Index


# Charger les variables d'environnement
load_dotenv()

# Initialiser l'index Upstash
upstash_index = Index(
    url=os.getenv('UPSTASH_VECTOR_REST_URL'),
    token=os.getenv('UPSTASH_VECTOR_REST_TOKEN')
)


@function_tool
def search_portfolio(query: str) -> str:
    """
    Recherche des informations dans le portfolio de Chloé.
    Utilise la recherche vectorielle pour trouver les informations pertinentes.
    
    Args:
        query: La question ou le sujet à rechercher dans le portfolio
        
    Returns:
        Les informations trouvées dans le portfolio
    """
    try:
        # Rechercher les 5 chunks les plus pertinents
        results = upstash_index.query(
            data=query,
            top_k=5,
            include_metadata=True
        )
        
        if not results:
            return "Aucune information trouvée dans le portfolio."
        
        # Formater les résultats
        context = []
        for i, result in enumerate(results, 1):
            title = result.metadata.get('title', 'N/A')
            content = result.metadata.get('content', '')
            context.append(f"[Source {i}: {title}]\n{content}\n")
        
        return "\n---\n".join(context)
        
    except Exception as e:
        return f"Erreur lors de la recherche: {e}"


# Créer l'agent
portfolio_agent = Agent(
    name="Portfolio Assistant",
    model="gpt-4.1-nano",
    instructions="""Tu es un assistant IA spécialisé pour répondre aux questions sur le portfolio de Chloé Découst.

Ton rôle :
- Répondre aux questions sur ses compétences, projets, expériences et formations
- Utiliser la tool 'search_portfolio' pour chercher des informations précises
- Être précis et factuel en te basant sur les informations trouvées
- Répondre en français de manière professionnelle et claire
- Si une information n'est pas dans le portfolio, le dire clairement

Consignes importantes :
- TOUJOURS utiliser search_portfolio avant de répondre à une question sur Chloé
- Si la première recherche ne donne pas assez de résultats, faire une recherche complémentaire avec des mots-clés différents
- Par exemple, pour "projets en data visualisation", chercher aussi "plotly", "power bi", "graphiques", "tableaux de bord"
- Lister TOUS les projets trouvés, pas seulement les plus pertinents
- Citer les sources quand tu mentionnes des informations spécifiques
- Ne pas inventer d'informations qui ne sont pas dans le portfolio
- Être concis mais complet dans tes réponses""",
    tools=[search_portfolio]
)


def ask_agent(question: str) -> str:
    """
    Pose une question à l'agent.
    
    Args:
        question: La question à poser
        
    Returns:
        La réponse de l'agent
    """
    print(f"\n❓ Question: {question}")
    print("🤖 Agent réfléchit...\n")
    
    result = Runner.run_sync(portfolio_agent, question)
    
    answer = result.final_output
    print(f"💬 Réponse: {answer}\n")
    
    return answer


if __name__ == '__main__':
    print("=" * 80)
    print("🤖 PORTFOLIO ASSISTANT - Chloé Découst")
    print("=" * 80)
    
    # Exemples de questions
    questions = [
        "Quelles sont les compétences techniques de Chloé ?",
        "Parle-moi de son expérience avec le basket-ball",
        "Quels projets a-t-elle réalisés en data visualisation ?"
    ]
    
    for question in questions:
        ask_agent(question)
        print("-" * 80)
