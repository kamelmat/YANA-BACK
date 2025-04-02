from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import nltk

# Descargar listas de palabras si no están disponibles
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import words

# Filtrar sustantivos y adjetivos
word_list = words.words()
nouns = [word.capitalize() for word in word_list if word.istitle()]  # Sustantivos
adjectives = [word.lower() for word in word_list if word.islower()]  # Adjetivos

def generate_unique_user_id():
    """Genera un user_id único combinando un sustantivo + adjetivo aleatorio."""
    return f"{random.choice(nouns)}{random.choice(adjectives)}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def str(self):
        return self.email
