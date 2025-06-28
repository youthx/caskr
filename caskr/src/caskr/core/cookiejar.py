# The `CookieJar` class manages storing, retrieving, and clearing cookies for different client IDs,
# with the ability to set a priority client.
from typing import Dict, Optional

class CookieJar:
    def __init__(self):
        # Maps client_id (like session_id) to cookie dict {cookie_name: cookie_value}
        self._store: Dict[str, Dict[str, str]] = {}
        self.priority_client: Optional[str] = None
        
    def set_priority_client(self, client_id: str):
        self.priority_client = client_id 
        
    def load(self, client_id: str) -> Dict[str, str]:
        """Return stored cookies for a client_id, or empty dict."""
        return self._store.get(client_id, {})

    def save(self, client_id: str, cookies: Dict[str, str]):
        """Save cookies for a client_id."""
        if client_id not in self._store:
            self._store[client_id] = {}
        self._store[client_id].update(cookies)

    def get_cookie(self, client_id: str, key: str) -> Optional[str]:
        return self._store.get(client_id, {}).get(key)

    def set_cookie(self, client_id: str, key: str, value: str):
        if client_id not in self._store:
            self._store[client_id] = {}
        self._store[client_id][key] = value

    def clear_cookies(self, client_id: str):
        self._store.pop(client_id, None)
