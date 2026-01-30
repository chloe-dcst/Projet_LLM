from upstash_vector import Index
import hashlib
from chunk import chunk_file
from load import load_file
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'index Upstash depuis les secrets
index = Index.from_env()

def index_chunks(chunks: list, path: str) -> str:
    """
    Indexe une liste de chunks dans Upstash Vector.
    
    Args:
        chunks: Liste des chunks de texte à indexer
        path: Chemin du fichier source (pour les métadonnées)
        
    Returns:
        Message de confirmation
    """
    vectors_data = []

    print(f"[DEBUG] Indexation du fichier : {path}")
    print(f"[DEBUG] Nombre de chunks à indexer : {len(chunks)}")

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

    print(f"[DEBUG] {len(chunks)} chunks indexés depuis {path}")
    return f"✓ {len(chunks)} chunks indexés depuis {path}"

# Liste des fichiers et leurs paths
files_to_index = [
    "data/experience.md",
    "data/projets.md",
    "data/a-propos.md",
    "data/formation.md"
]

total_chunks_indexed = 0

for file_path in files_to_index:
    # Charger le fichier
    content = load_file(file_path)
    print(f"[DEBUG] Fichier chargé : {file_path} ({len(content)} caractères)")

    # Découper en chunks
    chunks = chunk_file(file_path, content)
    print(f"[DEBUG] Chunks générés : {len(chunks)}")

    # Indexer les chunks
    result = index_chunks(chunks, file_path)
    print(result)

    total_chunks_indexed += len(chunks)

print(f"[DEBUG] Nombre total de chunks indexés : {total_chunks_indexed}")
