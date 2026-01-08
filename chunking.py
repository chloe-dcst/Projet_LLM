"""
Module de découpage (chunking) de documents Markdown pour l'indexation vectorielle.
Permet de diviser les documents en morceaux cohérents pour améliorer la récupération d'information.
"""

import os
import re
from typing import List, Dict
from pathlib import Path


class MarkdownChunker:
    """Classe pour découper des documents Markdown en chunks cohérents."""
    
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        """
        Initialise le chunker.
        
        Args:
            max_chunk_size: Taille maximale d'un chunk en caractères
            overlap: Nombre de caractères de chevauchement entre chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_by_sections(self, content: str, file_path: str) -> List[Dict[str, str]]:
        """
        Découpe le contenu Markdown par sections (titres H1, H2, H3).
        
        Args:
            content: Contenu du fichier Markdown
            file_path: Chemin du fichier source
            
        Returns:
            Liste de dictionnaires contenant les chunks avec leurs métadonnées
        """
        chunks = []
        
        # Diviser le contenu par lignes
        lines = content.split('\n')
        
        current_chunk = []
        current_metadata = {
            'file': file_path,
            'h1': '',
            'h2': '',
            'h3': ''
        }
        
        for line in lines:
            # Détecter les titres
            h1_match = re.match(r'^# (.+)$', line)
            h2_match = re.match(r'^## (.+)$', line)
            h3_match = re.match(r'^### (.+)$', line)
            
            if h1_match:
                # Sauvegarder le chunk précédent si non vide
                if current_chunk:
                    chunks.append(self._create_chunk(current_chunk, current_metadata.copy()))
                
                # Commencer un nouveau chunk avec le nouveau H1
                current_metadata['h1'] = h1_match.group(1).strip()
                current_metadata['h2'] = ''
                current_metadata['h3'] = ''
                current_chunk = [line]
                
            elif h2_match:
                # Sauvegarder le chunk précédent si trop grand
                if self._chunk_size(current_chunk) > self.max_chunk_size and current_chunk:
                    chunks.append(self._create_chunk(current_chunk, current_metadata.copy()))
                    current_chunk = []
                
                current_metadata['h2'] = h2_match.group(1).strip()
                current_metadata['h3'] = ''
                current_chunk.append(line)
                
            elif h3_match:
                # Sauvegarder le chunk précédent si trop grand
                if self._chunk_size(current_chunk) > self.max_chunk_size and current_chunk:
                    chunks.append(self._create_chunk(current_chunk, current_metadata.copy()))
                    current_chunk = []
                
                current_metadata['h3'] = h3_match.group(1).strip()
                current_chunk.append(line)
                
            else:
                current_chunk.append(line)
                
                # Si le chunk devient trop grand, le sauvegarder
                if self._chunk_size(current_chunk) > self.max_chunk_size:
                    chunks.append(self._create_chunk(current_chunk, current_metadata.copy()))
                    current_chunk = []
        
        # Ajouter le dernier chunk
        if current_chunk:
            chunks.append(self._create_chunk(current_chunk, current_metadata.copy()))
        
        return chunks
    
    def _chunk_size(self, lines: List[str]) -> int:
        """Calcule la taille d'un chunk en caractères."""
        return sum(len(line) for line in lines)
    
    def _create_chunk(self, lines: List[str], metadata: Dict[str, str]) -> Dict[str, str]:
        """
        Crée un chunk avec son contenu et ses métadonnées.
        
        Args:
            lines: Lignes du chunk
            metadata: Métadonnées du chunk
            
        Returns:
            Dictionnaire contenant le chunk et ses métadonnées
        """
        content = '\n'.join(lines).strip()
        
        # Créer un titre descriptif pour le chunk
        title_parts = []
        if metadata['h1']:
            title_parts.append(metadata['h1'])
        if metadata['h2']:
            title_parts.append(metadata['h2'])
        if metadata['h3']:
            title_parts.append(metadata['h3'])
        
        title = ' > '.join(title_parts) if title_parts else os.path.basename(metadata['file'])
        
        return {
            'content': content,
            'title': title,
            'file': metadata['file'],
            'h1': metadata['h1'],
            'h2': metadata['h2'],
            'h3': metadata['h3'],
            'size': len(content)
        }
    
    def process_directory(self, directory: str) -> List[Dict[str, str]]:
        """
        Traite tous les fichiers Markdown d'un répertoire.
        
        Args:
            directory: Chemin du répertoire à traiter
            
        Returns:
            Liste de tous les chunks créés
        """
        all_chunks = []
        data_path = Path(directory)
        
        # Trouver tous les fichiers .md
        md_files = list(data_path.rglob('*.md'))
        
        print(f"📂 Traitement de {len(md_files)} fichiers Markdown...")
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Ignorer les fichiers vides
                if not content.strip():
                    continue
                
                # Découper le fichier
                relative_path = md_file.relative_to(data_path.parent)
                chunks = self.chunk_by_sections(content, str(relative_path))
                all_chunks.extend(chunks)
                
                print(f"  ✓ {relative_path}: {len(chunks)} chunks créés")
                
            except Exception as e:
                print(f"  ✗ Erreur lors du traitement de {md_file}: {e}")
        
        print(f"\n📊 Total: {len(all_chunks)} chunks créés\n")
        return all_chunks


def main():
    """Fonction principale pour tester le chunking."""
    chunker = MarkdownChunker(max_chunk_size=1000, overlap=100)
    
    # Traiter le répertoire data
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    chunks = chunker.process_directory(data_dir)
    
    # Afficher un exemple de chunks
    if chunks:
        print("=" * 80)
        print("EXEMPLES DE CHUNKS")
        print("=" * 80)
        
        for i, chunk in enumerate(chunks[:3]):  # Afficher les 3 premiers
            print(f"\n--- CHUNK {i+1} ---")
            print(f"Titre: {chunk['title']}")
            print(f"Fichier: {chunk['file']}")
            print(f"Taille: {chunk['size']} caractères")
            print(f"Contenu (extrait):\n{chunk['content'][:200]}...")
            print()


if __name__ == '__main__':
    main()
