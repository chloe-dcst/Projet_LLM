import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from upstash_vector import Index

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'index Upstash depuis les secrets
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
        print(f"[DEBUG] Recherche Upstash pour la query : {query}")

        # Rechercher les 10 chunks les plus pertinents
        results = upstash_index.query(
            data=query,
            top_k=10,
            include_metadata=True
        )

        print(f"[DEBUG] Nombre de résultats trouvés : {len(results)}")

        if not results:
            return "Aucune information trouvée dans le portfolio."

        # Formater les résultats sans mentionner les sources
        context = []
        for result in results:
            content = result.metadata.get('text', '')
            context.append(content)

        return "\n\n".join(context)

    except Exception as e:
        print(f"[DEBUG] Erreur lors de la recherche : {e}")
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
- Répondre en français de manière professionnelle et CLAIRE
- Si une information n'est pas dans le portfolio, le dire clairement
- Répond à la question sans passer par 4 chemins et n'ajoute pas des éléments de réponses non attendu

Gestion des questions incompréhensibles :
- Si le message est incompréhensible, réponds : "Je n'ai pas compris votre question. Pouvez-vous la reformuler s'il vous plaît ?"
- Si le message fait référence à la conversation précédente, c'est une question valide
- Ne cherche PAS dans le portfolio si la question n'a pas de sens

Consignes importantes :
- Soit toujours poli
- TOUJOURS utiliser search_portfolio avant de répondre à une question sur Chloé
- Si la première recherche ne donne pas assez de résultats, faire une recherche complémentaire avec des mots-clés différents
- Lister TOUS les projets trouvés, pas seulement les plus pertinents
- Ne pas inventer d'informations qui ne sont pas dans le portfolio
- Ne pas mentionner les sources ou numéros de sources dans ta réponse
- Être concis mais complet""",
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
    print(f"\n[DEBUG] Question posée à l'agent : {question}")
    print("[DEBUG] Agent réfléchit...\n")

    result = Runner.run_sync(portfolio_agent, question)
    answer = result.final_output

    print(f"[DEBUG] Réponse de l'agent : {answer}\n")
    return answer


def get_agent():
    """
    Retourne l'agent configuré pour l'utiliser dans d'autres modules.
    Returns:
        L'agent portfolio_agent
    """
    return portfolio_agent


if __name__ == '__main__':
    print("=" * 80)
    print("PORTFOLIO ASSISTANT - Chloé Découst")
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
