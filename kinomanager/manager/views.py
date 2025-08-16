from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.views.generic import CreateView 
from django.contrib.auth.views import LoginView

from django.contrib.auth import login, logout
from .forms import *
from .models import KinoUsers, Message, Chat

# Create your views here.
def main_page(request):
    return render(request, "manager/index.html")

def contacts(request):
    return render(request, "manager/contacts.html")

def get_chat_history(user, name=False) -> list:
    chat_history = []
    
    if name:
        user = KinoUsers.objects.get(username=user)

    curr_chat = Chat.objects.get(user_main=user)
        
    chat_history = Message.objects.filter(chat=curr_chat).order_by("-timestamp")
    
    return chat_history

def help(request):
    if request.user.is_support:
        chat = Chat.objects.get(user_support=request.user)
        return redirect("help_forsup", clientname=chat.user_main.username)
    
    elif request.user.is_authenticated:
        chat_history=get_chat_history(request.user)
        return render(request, "manager/help.html", context={"chat_history":chat_history})
    return redirect("login")

def help_forsup(request, clientname):
    if request.user.is_authenticated and request.user.is_support:
        
        print("This is from", request.user)
        chats_list = Chat.objects.filter(user_support=request.user)
        users_list = []
        for i in chats_list:
            users_list.append(i.user_main.username)
        print(users_list)
        
        chat_history=get_chat_history(clientname, True)
    
        return render(request, "manager/help.html", context = {"users_list": users_list, "clientname":clientname, "chat_history":chat_history})
    return redirect("login")



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "manager/register.html"
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user) 
        return super().form_valid(form)

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "manager/login.html"
    
    def get_success_url(self):
        return reverse_lazy('main_page')

def logout_user(request):
    logout(request)
    return redirect('login')