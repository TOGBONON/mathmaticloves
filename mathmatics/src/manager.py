from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class AccountManager(BaseUserManager):
    def create_user(self,email,password,**other_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
        
        email=self.normalize_email(email)
        user=self.model(email=email,**other_fields)
        user.set_password(password)
        user.save()

    def create_superuser(self,email,password,**other_fields):
            other_fields.setdefault('is_staff',True)
            other_fields.setdefault('is_superuser',True)
            other_fields.setdefault('is_active',True)
            if other_fields.get('is_staff') is not True:
                raise ValueError('is_staff is set to False')
            if other_fields.get('is_superuser') is not True:
                raise ValueError('is_superuser is set to False')
            return self.create_user(email,password,**other_fields)