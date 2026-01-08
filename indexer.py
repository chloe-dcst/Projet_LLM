"""
Script d'indexation des chunks dans Upstash Vector.
"""

import os
from dotenv import load_dotenv
from upstash_vector import Index
from chunking import MarkdownChunker
import hashlib


def create_chunk_id(chunk: dict) -> str:
    """
    Crée un ID unique pour un chunk.
    
    Args:
        chunk: Dictionnaire contenant les informations du chunk
        
    Returns:
        ID unique (hash MD5)
    """
    content = f"{chunk['file']}_{chunk['title']}_{chunk['content'][:50]}"
    return hashlib.md5(content.encode()).hexdigest()


def index_documents():
    """Indexe tous les documents Markdown dans Upstash Vector."""
    # Charger les variables d'environnement
    load_dotenv()
    
    upstash_url = os.getenv('UPSTASH_VECTOR_REST_URL')
    upstash_token = os.getenv('UPSTASH_VECTOR_REST_TOKEN')
    
    if not upstash_url or not upstash_token:
        raise ValueError("❌ Les variables UPSTASH_VECTOR_REST_URL et UPSTASH_VECTOR_REST_TOKEN doivent être dans le .env")
    
    print("🔗 Connexion à Upstash Vector...")
    index = Index(url=upstash_url, token=upstash_token)
    
    print("📄 Découpage des documents...")
    chunker = MarkdownChunker(max_chunk_size=1000, overlap=100)
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    chunks = chunker.process_directory(data_dir)
    
    print(f"\n📤 Indexation de {len(chunks)} chunks dans Upstash...")
    
    # Préparer les données pour l'indexation
    vectors_data = []
    for chunk in chunks:
        chunk_id = create_chunk_id(chunk)
        
        # Métadonnées du chunk
        metadata = {
            'title': chunk['title'],
            'file': chunk['file'],
            'h1': chunk['h1'],
            'h2': chunk['h2'],
            'h3': chunk['h3'],
            'content': chunk['content']
        }
        
        vectors_data.append({
            'id': chunk_id,
            'data': chunk['content'],  # Upstash génère l'embedding automatiquement
            'metadata': metadata
        })
    
    # Indexer par batch de 10
    batch_size = 10
    success_count = 0
    
    for i in range(0, len(vectors_data), batch_size):
        batch = vectors_data[i:i + batch_size]
        try:
            index.upsert(vectors=batch)
            success_count += len(batch)
            print(f"  ✓ Batch {i//batch_size + 1}/{(len(vectors_data)-1)//batch_size + 1} indexé ({success_count}/{len(vectors_data)})")
        except Exception as e:
            print(f"  ✗ Erreur sur le batch {i//batch_size + 1}: {e}")
    
    print(f"\n✅ Indexation terminée : {success_count}/{len(vectors_data)} chunks indexés")
    
    # Statistiques de l'index
    try:
        info = index.info()
        print(f"\n📊 Statistiques de l'index:")
        print(f"   - Vecteurs totaux: {info.vector_count}")
        print(f"   - Dimension: {info.dimension}")
        print(f"   - Similarité: {info.similarity_function}")
    except Exception as e:
        print(f"\n⚠️ Impossible de récupérer les stats: {e}")


def test_search(query: str, top_k: int = 3):
    """
    Teste la recherche dans l'index.
    
    Args:
        query: Requête de recherche
        top_k: Nombre de résultats à retourner
    """
    load_dotenv()
    
    upstash_url = os.getenv('UPSTASH_VECTOR_REST_URL')
    upstash_token = os.getenv('UPSTASH_VECTOR_REST_TOKEN')
    
    index = Index(url=upstash_url, token=upstash_token)
    
    print(f"\n🔍 Recherche: '{query}'")
    print("=" * 80)
    
    results = index.query(
        data=query,
        top_k=top_k,
        include_metadata=True
    )
    
    if not results:
        print("Aucun résultat trouvé")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n--- RÉSULTAT {i} (Score: {result.score:.4f}) ---")
        print(f"Titre: {result.metadata.get('title', 'N/A')}")
        print(f"Fichier: {result.metadata.get('file', 'N/A')}")
        content = result.metadata.get('content', '')
        print(f"Extrait: {content[:200]}...")


if __name__ == '__main__':
    # Indexation
    index_documents()
    
    # Tests de recherche
    print("\n" + "=" * 80)
    print("TESTS DE RECHERCHE")
    print("=" * 80)
    
    test_search("Quelles sont les compétences en Python ?", top_k=2)
    test_search("Parle-moi du basket", top_k=2)
