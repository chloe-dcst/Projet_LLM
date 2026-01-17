# Chargement des fichiers

def load_file(path:str) -> str:
    """
    Charge et lit le contenu d'un fichier texte.
    Args:
        path: Chemin vers le fichier à lire   
    Returns:
        Contenu du fichier sous forme de chaîne de caractères
    """
    with open(path, 'r', encoding='utf-8') as file:
        content_file = file.read()

    return content_file

content = load_file('data/projets.md')
print(content)