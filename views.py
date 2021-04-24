from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .forms import signupform,Loginform,PostForm,edituserprofileform,editadminprofileform

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from osj.models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.models import User



#Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'osj/home.html',{'posts':posts})
# About
def about(request):
    return render(request, 'osj/about.html')
def busniess(request):
    return render(request,'osj/Busniess.html')
# Contruct
def contact(request):
    return render(request,'osj/contact.html')
# Login
def user_login(request):
 if not request.user.is_authenticated:
    if request.method == "POST":
        form=Loginform(request=request,data=request.POST)
        if form.is_valid():
            uname= form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user= authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in sucessfully')
                return HttpResponseRedirect('/dashboard/')
    else:
        form=Loginform()
    return render(request,'osj/login.html',{'form':form})  
 else:
    return HttpResponseRedirect('/login/')        
 

    

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
# signup
def user_signup(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations You have become a Author.')
            user= form.save()
            group= Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = signupform()
    return render(request,'osj/signup.html',{'form':form})
# Add  New post
def add_post(request):
    if request.user.is_authenticated:
     if request.method == 'POST':
           form = PostForm(request.POST)
           if form.is_valid():
              title = form.cleaned_data['title']
              desc = form.cleaned_data['desc']
              pst =Post(title=title,desc=desc)
              pst.save()
              form = PostForm()
     else:
           form =PostForm() 
     return render(request,'osj/dashboard.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
# Update Post
def update_post(request,id):
    if request.user.is_authenticated:
     if request.method == 'POST':
           pi=Post.objects.get(pk=id)
           form = PostForm(request.POST,instance=pi)
           if form.is_valid():
              
              form.save()
              
     else:
           form =PostForm()
           pi=Post.objects.get(pk=id)
           form =PostForm(instance=pi)
          
     return render(request,'osj/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
# Delete Post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
#Health
def health(request):
    return render(request,'osj/health.html')
#Singel
def singel(request):
    return render(request,'osj/singel.html')
#Admin
def dashboard(request):
    if request.user.is_authenticated:
      posts = Post.objects.all()
      user=request.user
      full_name=user.get_full_name()
      gps=user.groups.all()
      return render(request,'osj/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
      return HttpResponseRedirect('/login/')   
def admin_profile(request):

    if request.user.is_authenticated:
      if request.method=="POST":
          if request.user.is_superuser == True:
           fm=editadminprofileform(request.POST,instance=request.user)
           users=User.objects.all()

          else:
            fm=edituserprofileform(request.POST,instance=request.user) 
        
          if fm.is_valid():
            messages.success(request,'profile updated')
            fm.save()
      else:
       
        if request.user.is_superuser == True:
            fm=editadminprofileform(instance=request.user)
            users=User.objects.all()
         
        else:
            fm=edituserprofileform(instance=request.user)
            users=None
      return render(request,'osj/admin-templates/admin_profile.html',{'name':request.user,'form':fm,'users':users})

    else:
      return HttpResponseRedirect('/login/') 
#Changepass
def user_change_pass(request):
  if request.user.is_authenticated:  
    if request.method=="POST":
        fm=PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'Password Change Successfully')
            return HttpResponseRedirect('/admin_profile/')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request,'osj/admin-templates/admin_changepass.html',{'form':fm})  
  else:
    return HttpResponseRedirect('/login/')

def user_profile(request):

    if request.user.is_authenticated:
      if request.method=="POST":
        if request.user.is_superuser==True:
              users=User.objects.all()
              fm=editadminprofileform(request.POST,instance=request.user)
        else:
              fm=edituserprofileform(request.POST,instance=request.user)
        if fm.is_valid():
            messages.success(request,'profile updated')
            fm.save()
      else:
        if request.user.is_superuser == True:
            fm=editadminprofileform(instance=request.user)
        else:
            users=None
            fm=edituserprofileform(instance=request.user)
      return render(request,'osj/admin-templates/user_profile',{'name':request.user,'form':fm,'users':users})

    else:
      return HttpResponseRedirect('/login/')
def user_detail(request,id):
    if request.user.is_authenticated:
       pi=User.objects.get(pk=id)
       fm=editadminprofileform(instance=pi)
       return render(request,'osj/admin-templates/userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')