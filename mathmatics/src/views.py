from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from src.models import MT_Commune, MT_speciality, MT_study_level, UserAccount
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from src.decorators import unauthenticated_user, allowed_users, admin_only
from src.form_ref import CommuneForm, MatiereForm, SpecialityForm, StudentCallForm, StudyLevelForm, TeacherForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def homefunc(request):   
    return render(request,'src/home.html' )

def pagehome(request):   
    return render(request,'src/page_home.html' )

def blankpage(request):   
    return render(request,'src/contactus.html' )

def sub_registration(request):   
    return render(request,'src/sub_menu/sub_registration.html' )

def sub_list_categorie(request):   
    return render(request,'src/sub_menu/sub_list_categ.html' )

def loginPage(request):  
                   
        if request.method == 'POST':
            
            email = request.POST.get('email')            

            password = request.POST.get('password')
            user = authenticate(request, email=email, password = password)

            if user is not None:
                login(request, user)
                #group = request.user.groups.all()[0].name if request.user.groups.exists() else None 

                

                #request.session['dis_postproject'] = settings.POST_PROJECT_DIS
                #request.session['use_postproject'] = datas.use_postproject
                #request.session['use_support'] = datas.use_support

                #if group == 'professeur':                                    
                return redirect('sub-registration')                  
                # if group =='adminstaff':
                #     return redirect('ss:dash-employee')                        
                # if group == 'staff':                                 
                #     return redirect('ss:dash-employee')
                #return redirect('ss:contactpers-finding') 
               
                   
            else:
                
                messages.info(request, "Incorrect login please try again")
                return redirect('seconnecter')
                

        #context = {}
        #return redirect('ss:create-seller')
        return render(request, 'src/login.html', )
              

def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.typecompte = 'professeur' 
            #obj.userid = request.user.id  
            obj.save()      
                
            #group = Group.objects.get(name='professeur')
            #obj.groups.add(group)

            messages.success(request, 'Données enrégistrées avec succès')
            return redirect('new-teacher')   
        
    else:
        form = TeacherForm()
      
    return render(request,'src/teacher.html' ,  {'form': form})   
    

def StudyLevel(request): 
    if request.method == 'POST':
        form = StudyLevelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.typecompte = 'staff' 
            #obj.userid = UserAccount(1)  
            obj.save() 

            messages.success(request, 'Données enrégistrées avec succès')
            return redirect('sutylevel')   

    else:
        form = StudyLevelForm()
      
    return render(request,'src/category/study_level.html' ,  {'form': form})

def Speciality(request): 
    if request.method == 'POST':
        form = SpecialityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.typecompte = 'staff' 
            #obj.userid = UserAccount(1)  
            obj.save() 

            messages.success(request, 'Données enrégistrées avec succès')
            return redirect('speciality')   

    else:
        form = SpecialityForm()
      
    return render(request,'src/category/speciality.html' ,  {'form': form})


def Commune(request): 
    if request.method == 'POST':
        form = CommuneForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.typecompte = 'staff' 
            #obj.userid = UserAccount(1)  
            obj.save() 

            messages.success(request, 'Données enrégistrées avec succès')
            return redirect('commune')   

    else:
        form = CommuneForm()
      
    return render(request,'src/category/commune.html' ,  {'form': form})


def Matiere(request): 
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.typecompte = 'staff' 
            #obj.userid = UserAccount(1)  
            obj.save() 

            messages.success(request, 'Données enrégistrées avec succès')
            return redirect('matiere')   

    else:
        form = MatiereForm()
      
    return render(request,'src/category/matiere.html' ,  {'form': form})

def find_prof(request): 
    profs =  UserAccount.objects.filter(is_active = 1, typecompte='professeur' ).order_by("-id") 

    return render(request,'src/recent_connect_prof.html' ,  {'profs': profs})

def create_call(request, id):
    if request.method == 'POST':
        form = StudentCallForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            fullname = form.cleaned_data.get('student_fullname')
            birthday = form.cleaned_data.get('student_birthday')
            commune = form.cleaned_data.get('student_commune')
            matiere = form.cleaned_data.get('matiere')

            request.session['ses_fullname'] = fullname
            request.session['ses_birthday'] = birthday.strftime('%Y-%m-%d') if birthday else None
            request.session['ses_tel'] = form.cleaned_data.get('student_tel')
            request.session['ses_etablissment'] = form.cleaned_data.get('student_etablissement')
            request.session['ses_gender'] = form.cleaned_data.get('student_gender')
            request.session['ses_email'] = form.cleaned_data.get('student_email')
            request.session['ses_commune'] = commune.id if commune else None
            request.session['ses_matiere'] = matiere.id if matiere else None
            request.session['ses_teacher_id'] = id
            
            #obj.userid = request.user.id  
            #obj.save()  

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{id}",
                {
                    "type": "incoming_call",
                    "call_id": id,
                    "student_name": fullname,
                }
            )
                
            messages.success(request, 'Données enrégistrées avec succès')
            #return redirect('new-teacher') 
            return render(request, 'src/student_call.html', { 'form': form, 'prof_id': id})  
        
    else:
        form = StudentCallForm()
      
    return render(request,'src/student_call.html' ,  {'form': form, 'prof_id':id})  

def list_commune(request): 
    datalist =  MT_Commune.objects.filter(f_active = 1, ).order_by("-id") 

    return render(request,'src/list/list_commune.html' ,  {'datalist': datalist})

def list_studylevel(request): 
    datalist =  MT_study_level.objects.filter(f_active = 1, ).order_by("-id") 

    return render(request,'src/list/list_studylevel.html' ,  {'datalist': datalist})

def list_speciality(request): 
    datalist =  MT_speciality.objects.filter(f_active = 1, ).order_by("-id") 

    return render(request,'src/list/list_specialite.html' ,  {'datalist': datalist})