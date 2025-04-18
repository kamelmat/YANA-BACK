from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils import generate_unique_user_id

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name, password=None, user_id = None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        name = name.capitalize()
        last_name = last_name.capitalize()

        user_id = user_id or generate_unique_user_id()
        user = self.model(
            email=email, 
            user_id=user_id, 
            name=name,
            last_name=last_name,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name="Admin", last_name = "user", password=None):
        user = self.create_user(
        email=email,
        name=name,
        last_name=last_name,
        password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_id = models.CharField(
        max_length=50, 
        unique=True, 
        default=generate_unique_user_id, 
        null=True,
        blank=True
    )
    avatar_id = models.IntegerField(default=34)
    unread_messages = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = generate_unique_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """
        Retorna True si el usuario tiene un permiso específico.
        En este caso, los superusuarios tienen todos los permisos.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Retorna True si el usuario tiene permisos para ver una aplicación específica.
        En este caso, los superusuarios tienen acceso a todas las aplicaciones.
        """
        return self.is_admin