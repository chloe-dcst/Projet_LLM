from upstash_vector import Index
import hashlib
from chunk import chunk_file
from load import load_file
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# import des informations d'identification
index = Index.from_env()

def index_chunks(chunks:list, path:str) -> str:
    """
    Indexe une liste de chunks dans Upstash Vector.
    
    Args:
        chunks: Liste des chunks de texte à indexer
        path: Chemin du fichier source (pour les métadonnées)
        
    Returns:
        Message de confirmation
    """
    vectors_data = []
    
    for i, chunk in enumerate(chunks):
        # Créer un ID unique pour chaque chunk
        chunk_id = hashlib.md5(f"{path}_{i}_{chunk[:50]}".encode()).hexdigest()
        
        # Métadonnées associées au chunk
        metadata = {
            "text": chunk,
            "source": path,
            "chunk_index": i
        }
        
        # Ajouter le chunk à la liste (Upstash génère l'embedding automatiquement)
        vectors_data.append({
            'id': chunk_id,
            'data': chunk,
            'metadata': metadata
        })
    
    # Indexer les chunks
    index.upsert(vectors=vectors_data)
    
    return f"✓ {len(chunks)} chunks indexés depuis {path}"

chunks = chunk_file('data/experience.md', load_file('data/experience.md'))
result = index_chunks(chunks, 'data/experience.md')
print(result)