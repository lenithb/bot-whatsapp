"""
Manejo del historial de conversación por usuario.

Para aprender: usamos un diccionario en memoria.
En producción usarías Redis o una base de datos.
"""

from collections import defaultdict
from typing import List, Dict

# Historial en memoria: { "whatsapp:+549..." : [ {role, content}, ... ] }
_histories: Dict[str, List[Dict]] = defaultdict(list)

# Máximo de mensajes a recordar por usuario (para no pasarse del contexto)
MAX_HISTORY = 20


def get_history(sender: str) -> List[Dict]:
    """Devuelve copia del historial del usuario."""
    return list(_histories[sender])


def save_message(sender: str, role: str, content: str):
    """Agrega un mensaje al historial y recorta si es necesario."""
    _histories[sender].append({"role": role, "content": content})

    # Mantener solo los últimos MAX_HISTORY mensajes
    if len(_histories[sender]) > MAX_HISTORY:
        _histories[sender] = _histories[sender][-MAX_HISTORY:]


def clear_history(sender: str):
    """Borra el historial completo de un usuario."""
    _histories[sender] = []


def get_all_users() -> List[str]:
    """Lista todos los usuarios con historial activo."""
    return list(_histories.keys())
