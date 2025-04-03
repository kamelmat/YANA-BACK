import random

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_words():
    """Carga sustantivos y adjetivos desde un archivo JSON."""
    with open(os.path.join(BASE_DIR, "words.json"), "r", encoding="utf-8") as file:
        words = json.load(file)
    return words["nouns"], words["adjectives"]

NOUNS, ADJECTIVES = load_words()

def generate_random_user_id():
    """Genera un user_id aleatorio sin verificar en la BD."""
    return f"{random.choice(NOUNS)}{random.choice(ADJECTIVES)}"

def generate_unique_user_id():
    """Genera un user_id único en la base de datos."""
    from django.db import connection  # ← Evita importar modelos directamente
    if 'users_customuser' not in connection.introspection.table_names():
        return generate_random_user_id()  # ← Si la tabla no existe, devuelve un ID sin verificar

    from .models import CustomUser  # ← Importación dentro de la función para evitar errores al iniciar Django

    while True:
        user_id = generate_random_user_id()
        if not CustomUser.objects.filter(user_id=user_id).exists():
            return user_id
