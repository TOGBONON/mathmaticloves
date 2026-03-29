from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from src.manager import AccountManager

# Create your models here.



class UserAccount(AbstractBaseUser,PermissionsMixin): 

    email         = models.EmailField(max_length=255,unique=True, null=False)
    username      = models.CharField(max_length=255,blank=True, null=True)  
    fullname     = models.CharField(max_length=255,null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    tel          = models.fields.CharField(null=False, max_length=255,  default="")
    etablissement          = models.fields.CharField(null=True, blank=True, max_length=255)
    gender          = models.fields.CharField(null=True, blank=True, max_length=255)
 
    picture = models.ImageField( upload_to="files/", verbose_name="Picture",null=True, blank=True)

    type = [
    ('professeur', 'Professeur'),
    ('eleve', 'Elève'),
    ('staff', 'Staff'),
    ] 
   
    typecompte = models.fields.CharField(
        max_length=50,
        choices=type,
        default='professeur',
    ) 

    levelstudy = models.ForeignKey('MT_study_level', related_name='studylevel', null=True, blank=True, on_delete=models.SET_NULL)
    speciality = models.ForeignKey('MT_speciality', related_name='sepecia', null=True, blank=True, on_delete=models.SET_NULL)
    commune = models.ForeignKey('MT_Commune', related_name='comm', null=True, blank=True, on_delete=models.SET_NULL)
    matiere = models.ForeignKey('MT_Matiere', related_name='matier', null=True, blank=True, on_delete=models.SET_NULL)
    note     = models.IntegerField(null=True, blank=True)
    npi     = models.CharField(max_length=255,null=True, blank=True)

    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)

    date_joined   = models.DateTimeField(verbose_name='date_joined',auto_now=True)
    last_login    = models.DateTimeField(auto_now=True)
    is_admin      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tel']

    def __str__(self):
        return self.fullname or self.email
    

class MT_study_level(models.Model):   
    name = models.fields.CharField(null=False, default='', max_length=255, unique=True)
    f_active = models.BooleanField(default=True)
    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)
    userid         = models.ForeignKey(UserAccount,related_name='useridstudylevel', null=True, blank=True, on_delete=models.SET_NULL)
    update_userid         = models.ForeignKey(UserAccount,related_name='useridupstudy', null=True, blank=True, on_delete=models.SET_NULL)
    delete_userid         = models.ForeignKey(UserAccount,related_name='useriddelstudy', null=True, blank=True, on_delete=models.SET_NULL)
    def validate_unique(self, exclude=None):
        try: super().validate_unique(exclude)
        except ValidationError as e:
            if 'name' in e.error_dict: e.error_dict['name'] = ['Cette donnée existe déjà']
            raise e
        
    def __str__(self):
        return self.name
    
class MT_speciality(models.Model):   
    name = models.fields.CharField(null=False, default='', max_length=255, unique=True)
    f_active = models.BooleanField(default=True)
    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)
    userid         = models.ForeignKey(UserAccount,related_name='useridspecia', null=True, blank=True, on_delete=models.SET_NULL)
    update_userid         = models.ForeignKey(UserAccount,related_name='useridupspecia', null=True, blank=True, on_delete=models.SET_NULL)
    delete_userid         = models.ForeignKey(UserAccount,related_name='useriddelspecia', null=True, blank=True, on_delete=models.SET_NULL)
    def validate_unique(self, exclude=None):
        try: super().validate_unique(exclude)
        except ValidationError as e:
            if 'name' in e.error_dict: e.error_dict['name'] = ['Cette donnée existe déjà']
            raise e
        
    def __str__(self):
        return self.name
    
class MT_Commune(models.Model):   
    name = models.fields.CharField(null=False, default='', max_length=255, unique=True)
    f_active = models.BooleanField(default=True)
    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)
    userid         = models.ForeignKey(UserAccount,related_name='useridcom', null=True, blank=True, on_delete=models.SET_NULL)
    update_userid         = models.ForeignKey(UserAccount,related_name='useridupcom', null=True, blank=True, on_delete=models.SET_NULL)
    delete_userid         = models.ForeignKey(UserAccount,related_name='useriddelcom', null=True, blank=True, on_delete=models.SET_NULL)
    def validate_unique(self, exclude=None):
        try: super().validate_unique(exclude)
        except ValidationError as e:
            if 'name' in e.error_dict: e.error_dict['name'] = ['Cette donnée existe déjà']
            raise e
        
    def __str__(self):
        return self.name
    

class MT_Matiere(models.Model):   
    name = models.fields.CharField(null=False, default='', max_length=255, unique=True)
    f_active = models.BooleanField(default=True)
    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)
    userid         = models.ForeignKey(UserAccount,related_name='useridmatier', null=True, blank=True, on_delete=models.SET_NULL)
    update_userid         = models.ForeignKey(UserAccount,related_name='useridupmatier', null=True, blank=True, on_delete=models.SET_NULL)
    delete_userid         = models.ForeignKey(UserAccount,related_name='useriddelmatier', null=True, blank=True, on_delete=models.SET_NULL)
    def validate_unique(self, exclude=None):
        try: super().validate_unique(exclude)
        except ValidationError as e:
            if 'name' in e.error_dict: e.error_dict['name'] = ['Cette données existe déjà']
            raise e
        
    def __str__(self):
        return self.name
    

class DT_Call(models.Model):   
    student_fullname = models.fields.CharField(null=False, default='', max_length=255)
    student_birthday = models.DateField(null=True, blank=True)
    student_tel          = models.fields.CharField(null=False, max_length=255,  default="")
    student_etablissement          = models.fields.CharField(null=True, blank=True, max_length=255)
    student_gender          = models.fields.CharField(null=True, blank=True, max_length=255)
    student_email         = models.EmailField(max_length=255, null=True,  blank=True)
    teacher         = models.ForeignKey(UserAccount,related_name='useridteacher', null=True, blank=True, on_delete=models.SET_NULL)
    type_call          = models.fields.CharField(null=True, blank=True, max_length=255)
    student_commune = models.ForeignKey('MT_Commune', related_name='stdcomm', null=True, blank=True, on_delete=models.SET_NULL)
    matiere = models.ForeignKey('MT_Matiere', related_name='stdmatier', null=True, blank=True, on_delete=models.SET_NULL)

    f_active = models.BooleanField(default=True)
    his_registration_date   = models.DateTimeField(auto_now=True)
    his_update_date   = models.DateTimeField(auto_now=True)
    his_delete_date   = models.DateTimeField(auto_now=True)
    userid  = models.ForeignKey(UserAccount,related_name='useridcall', null=True, blank=True, on_delete=models.SET_NULL)
    update_userid         = models.ForeignKey(UserAccount,related_name='useridupcall', null=True, blank=True, on_delete=models.SET_NULL)
    delete_userid         = models.ForeignKey(UserAccount,related_name='useriddelcall', null=True, blank=True, on_delete=models.SET_NULL)
            
    def __str__(self):
        return self.student_fullname
    
   