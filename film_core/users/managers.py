from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """ кастомный менеджер для модели CustomUser  """
    def create_user(self, email, password, **extra_fields):
        user = self.models(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True
        return self.create_user(email, password, **extra_fields)