"""
Gestion de l'historique des conversations avec Upstash Redis.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from redis import Redis

load_dotenv()


class ConversationManager:
    """Gestionnaire des conversations avec Redis."""
    
    def __init__(self):
        """Initialise la connexion à Upstash Redis."""
        redis_url = os.getenv('UPSTASH_REDIS_REST_URL')
        redis_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
        
        # Si Redis n'est pas configuré, utiliser un stockage en mémoire
        self.redis_available = bool(redis_url and redis_token)
        
        if self.redis_available:
            try:
                self.redis_client = Redis.from_url(
                    f"rediss://default:{redis_token}@{redis_url.replace('https://', '')}",
                    decode_responses=True
                )
                # Test de connexion
                self.redis_client.ping()
                print("✅ Redis connecté")
            except Exception as e:
                print(f"⚠️ Redis non disponible: {e}")
                self.redis_available = False
    
    def save_conversation(self, session_id: str, messages: list):
        """
        Sauvegarde l'historique d'une conversation.
        
        Args:
            session_id: Identifiant unique de la session
            messages: Liste des messages de la conversation
        """
        if not self.redis_available:
            return
        
        try:
            key = f"conversation:{session_id}"
            data = {
                'messages': messages,
                'updated_at': datetime.now().isoformat()
            }
            # Sauvegarder avec expiration de 7 jours
            self.redis_client.setex(
                key,
                7 * 24 * 60 * 60,  # 7 jours en secondes
                json.dumps(data)
            )
        except Exception as e:
            print(f"Erreur sauvegarde Redis: {e}")
    
    def load_conversation(self, session_id: str) -> list:
        """
        Charge l'historique d'une conversation.
        
        Args:
            session_id: Identifiant unique de la session
            
        Returns:
            Liste des messages ou liste vide
        """
        if not self.redis_available:
            return []
        
        try:
            key = f"conversation:{session_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)['messages']
            return []
        except Exception as e:
            print(f"Erreur chargement Redis: {e}")
            return []
    
    def delete_conversation(self, session_id: str):
        """
        Supprime l'historique d'une conversation.
        
        Args:
            session_id: Identifiant unique de la session
        """
        if not self.redis_available:
            return
        
        try:
            key = f"conversation:{session_id}"
            self.redis_client.delete(key)
        except Exception as e:
            print(f"Erreur suppression Redis: {e}")
    
    def list_conversations(self, limit: int = 10) -> list:
        """
        Liste les conversations récentes.
        
        Args:
            limit: Nombre maximum de conversations à retourner
            
        Returns:
            Liste des IDs de session
        """
        if not self.redis_available:
            return []
        
        try:
            keys = self.redis_client.keys("conversation:*")
            return [k.replace("conversation:", "") for k in keys[:limit]]
        except Exception as e:
            print(f"Erreur listage Redis: {e}")
            return []


if __name__ == '__main__':
    # Test du gestionnaire
    manager = ConversationManager()
    
    if manager.redis_available:
        print("Test de sauvegarde...")
        test_messages = [
            {"role": "user", "content": "Bonjour"},
            {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ?"}
        ]
        
        manager.save_conversation("test-session", test_messages)
        loaded = manager.load_conversation("test-session")
        print(f"Messages chargés: {loaded}")
        
        manager.delete_conversation("test-session")
        print("Test terminé")
    else:
        print("⚠️ Redis non configuré - Les conversations ne seront pas sauvegardées")
