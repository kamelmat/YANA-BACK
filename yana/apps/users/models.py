from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
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
        user = self.model(email=email, user_id=generate_unique_user_id())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_id = models.CharField(max_length=50, unique=True, editable=False, default=generate_unique_user_id)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class formedit(UserCreationForm):
    telefono = forms.IntegerField(label='telefono', required=True)
    direccion = forms.CharField(label='direccion', max_length= 60, required=True)
    sexo = forms.ChoiceField(label='sexo', choices=[('Masculino'), ('Femenino'), ("No binario"), ("Transgenero"), ("Prefiero no responder")])
    
    class Meta:
        model   =   User
        fields  =   ('username', 'email', 'password1', 'password2', 'telefono', 'direccion', 'sexo')