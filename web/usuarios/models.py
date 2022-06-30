from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username,run,email,nombre, password=None):
        if not run:
            raise ValueError('El usuario debe tener un run')
        usuario = self.model(
            username=username,
            run = run,
            email = self.normalize_email(email),
            nombre = nombre,

        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username,run,email,nombre, password):
        usuario = self.create_user(
            username=username,
            run = run,
            email = email,                        
            nombre = nombre,
            password=password

        )
        usuario.usuario_admin = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario',unique = True,max_length=100)
    run = models.CharField('Run',unique = True,max_length=10)
    email = models.EmailField('Correo Electronico',unique=True,max_length=150)
    nombre = models.CharField('Nombre',max_length=100, blank=True, null=True)
    apellido = models.CharField('Apellido',max_length=100, blank=True,null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_admin = models.BooleanField(default=False)
    objects = UserManager()


    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['nombre','email','run']

    def __str__(self):
        return f'{self.username}'
    
    def has_perm(self, perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_admin
