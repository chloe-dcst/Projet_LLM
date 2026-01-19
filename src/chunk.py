from load import load_file
import re

def chunk_file(path:str, content_file:str) -> list:
    """
    Découpe le contenu d'un fichier texte en chunks basés sur les titres de niveau 1, 2 et 3.
    Args:
        path: Chemin vers le fichier à lire 
        content_file: Contenu du fichier à découper  
    Returns:
        Liste des chunks extraits du fichier
    """

    content = load_file(path)
    chunks = []
    lines = content.split('\n')
    current_chunk = []
    h1_context = ""
    
    for line in lines:
        if re.match(r'^# ', line):
            if current_chunk: 
                chunks.append('\n'.join(current_chunk).strip())
            h1_context = line
            current_chunk = []
        elif re.match(r'^## ', line):
            if current_chunk: 
                chunks.append('\n'.join(current_chunk).strip())
            h2_context = line
            current_chunk = [h1_context, h2_context] if h1_context else [line]
        elif re.match(r'^### ', line):
            if current_chunk:
                chunks.append('\n'.join(current_chunk).strip())
            current_chunk = [h1_context, h2_context, line] if h2_context else [h1_context, line] if h1_context else [line]
        else:
            current_chunk.append(line)
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk).strip())
    
    # Filtrer les chunks vides
    chunks = [chunk for chunk in chunks if chunk]
    
    return chunks    

chunks = chunk_file('data/experience.md', load_file('data/experience.md'))
for i, chunk in enumerate(chunks, 1):
    print(f"\n{'='*60}\nCHUNK {i}\n{'='*60}")
    print(chunk)

    
