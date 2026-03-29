import datetime
from pickle import FALSE
from django import forms
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput, TimePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from django.forms import TextInput
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from src.models import DT_Call, MT_Commune, MT_Matiere, UserAccount, MT_study_level, MT_speciality
from django.core.validators import RegexValidator

# custom_filters.py

#from django import template

#register = template.Library()

#@register.filter
#def customrange(number):
#    return range(number)

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class DateInput(forms.DateInput): 
    input_type = 'date'

class TimeInput(forms.DateInput):
   input_type = 'time'
   TIME_INPUT_FORMATS = '%H:%i'
    


gender_choice = [
    ('M', 'Masculin'),
    ('F', 'Féminin'),   
   ]   
class TeacherForm(forms.ModelForm):
   class Meta:
      model = UserAccount
      fields = ['email', 'fullname', 'etablissement', 'tel', 'birthday', 'gender', 'levelstudy', 'speciality', 'commune', 'matiere' , 'npi']
      #exclude = ('username', 'picture', 'typecompte', 'his_update_date', 'his_delete_date',  'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser')  
      widgets = {  
         'birthday': DatePickerInput(
            options=FlatpickrOptions(
                  altFormat="Y-m-d",  # altFormat="F j, Y", for February 10, 2026
                  #locale="ja",
                  yearSelectorType="dropdown",
                  #defaultDate="2000-01-01", 
                  minDate= "1950-01-01",
                  maxDate= "today"
            ),
            attrs={
               "placeholder": "YYYY-MM-DD",
               
            }
         ),
         
         #'tel': TextInput(attrs={'data-mask': "000-0000-0000"}),  
         #'npi': TextInput(attrs={ 'maxlength': '10', 'minlength': '10','pattern': '[0-9]*', 'inputmode': 'numeric', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}),           
       }
      labels = {'email':'', 'fullname':'', 'etablissement':'', 'tel':'', 'birthday':'' , 'gender':'', 'levelstudy':'', 'speciality':'', 'commune':'' , 'matiere':'' , 'npi':''}

   #password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
   #password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, help_text=("Enter the same password as above, for verification."))
   fullname= forms.CharField(required=True, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   etablissement= forms.CharField(required=False, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   tel= forms.CharField(required=True, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   levelstudy= forms.ModelChoiceField(required=True, queryset = MT_study_level.objects.filter(f_active=1).order_by("-id")  )
   speciality= forms.ModelChoiceField(required=True, queryset = MT_speciality.objects.filter(f_active=1).order_by("-id"))
   commune= forms.ModelChoiceField(required=True, queryset = MT_Commune.objects.filter(f_active=True).order_by("-id"))
   matiere= forms.ModelChoiceField(required=True, queryset = MT_Matiere.objects.filter(f_active=True).order_by("-id"))
   gender = forms.ChoiceField(choices=gender_choice, widget=forms.RadioSelect,label="", required=True, initial='M')
   npi = forms.CharField( max_length=10, min_length=10, validators=[RegexValidator(r'^\d{10}$', 'NPI must be exactly 10 digits') ] )
   #npi= forms.IntegerField(required=True, label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   #birthday = forms.DateField(widget=DateInput)
   

   def save(self, commit=True):
         user = super(TeacherForm, self).save(commit=False)
         #pwdset = "Abcd" + self.cleaned_data['seller_code'] + "ss"
         pwdset = 'mathlove'  
         
         if self.instance.pk is None:  
            user.set_password(pwdset) 
     
         if commit:
               user.save()
         return user


class StudentCallForm(forms.ModelForm):
   class Meta:
      model = DT_Call
      fields = ['student_fullname', 'student_birthday', 'student_tel', 'student_etablissement', 'student_gender', 'student_email', 'student_commune', 'matiere']
      #exclude = ('username', 'picture', 'typecompte', 'his_update_date', 'his_delete_date',  'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser')  
      widgets = {  
         'student_birthday': DatePickerInput(
            options=FlatpickrOptions(
                  altFormat="Y-m-d",  # altFormat="F j, Y", for February 10, 2026
                  #locale="ja",
                  yearSelectorType="dropdown",
                  #defaultDate="2000-01-01", 
                  minDate= "1950-01-01",
                  maxDate= "today"
            ),
            attrs={
               "placeholder": "YYYY-MM-DD",
               
            }
         ),
                  
       }
      labels = {'student_email':'', 'student_fullname':'', 'student_etablissement':'', 'student_tel':'', 'student_birthday':'' , 'student_gender':'', 'student_commune':'' , 'matiere':'' }

   #password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
   #password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, help_text=("Enter the same password as above, for verification."))
   student_fullname= forms.CharField(required=True, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   student_etablissement= forms.CharField(required=False, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   student_tel= forms.CharField(required=True, max_length=255 , label='' ,widget=forms.TextInput(attrs={'class': 'validate'}))
   student_commune= forms.ModelChoiceField(required=True, queryset = MT_Commune.objects.filter(f_active=True).order_by("-id"))
   matiere= forms.ModelChoiceField(required=True, queryset = MT_Matiere.objects.filter(f_active=True).order_by("-id"))
   student_gender = forms.ChoiceField(choices=gender_choice, widget=forms.RadioSelect,label="", required=True, initial='M')

  
class StudyLevelForm(forms.ModelForm):
   class Meta:
     model = MT_study_level
     fields = ['name',]
     labels = { 'name':''} 
     widgets = { 'name': forms.TextInput(attrs={ 'class': 'validate' }) }


class SpecialityForm(forms.ModelForm):
   class Meta:
     model = MT_speciality
     fields = ['name',]
     labels = { 'name':''} 
     widgets = { 'name': forms.TextInput(attrs={ 'class': 'validate' }) }


class CommuneForm(forms.ModelForm):
   class Meta:
     model = MT_Commune
     fields = ['name',]
     labels = { 'name':''} 
     widgets = { 'name': forms.TextInput(attrs={ 'class': 'validate' }) }

class MatiereForm(forms.ModelForm):
   class Meta:
     model = MT_Matiere
     fields = ['name',]
     labels = { 'name':''} 
     widgets = { 'name': forms.TextInput(attrs={ 'class': 'validate' }) }





