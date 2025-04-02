from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils import generate_unique_user_id

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_id = None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user_id = user_id or generate_unique_user_id()
        user = self.model(email=email, user_id=user_id)
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
    user_id = models.CharField(
        max_length=50, 
        unique=True, 
        default=generate_unique_user_id, 
        null=True,
        blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = generate_unique_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
