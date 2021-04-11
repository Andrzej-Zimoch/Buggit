from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm , UserRegistrationForm, AddProjectForm,AddTicketForm, SignUpForm,AddTeamForm
from django.contrib.auth.decorators import login_required
from .models import Project,Ticket,Profile,Team
from bootstrap_modal_forms.generic import BSModalReadView ,BSModalCreateView , BSModalUpdateView , BSModalDeleteView
from django.urls import reverse_lazy
from django.core import serializers
from itertools import chain
from django.views.generic import View
import json
from django.views.decorators.http import require_POST
import random
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User

def base(request):
    return render(request,'base.html')

# Create your views here.
def user_login(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if (user is not None):
                if (user.is_active):
                    login(request,user)
                    
                    return HttpResponse("Login successfull")
                else:
                    return HttpResponse('Account is blocked')
            else:
                
                return HttpResponse("Wrong login or password")
                
    else:
        form=LoginForm()
    return render(request,'bug/login.html',{'form':form})
    
def project_content(request):
    project= Project.objects.all()
    ticket= Ticket.objects.all()
    return render(request,'bug/projectcon.html',{'ticket':ticket,'project':project})
    # return HttpResponse("haha")

@login_required
def dashboard(request):
    cur_user = request.user.profile
    ticket= Ticket.objects.all()
    project= Project.objects.all()
    profile = Profile.objects.all()
    team = Team.objects.all()

    #Chart 1
    labels = []
    tickets_all = []
    tickets_done=[]
    ticket_colors_1=[]
    ticket_colors_2=[]


    recent_projects = Project.objects.order_by('-project_deadline')[:5]
    for i in recent_projects:
        if (i.manager == request.user.profile):
            
            labels.append(i.name)
            ticket_colors_1.append("#355C7D")
            ticket_colors_2.append("#99B898")
            d_a=0
            d_d=0
            for a in ticket:            
                if( a.project == i) :
                    d_a=d_a+1
                    if (a.status == "Done"):
                        d_d=d_d+1
            tickets_all.append(d_a)
            tickets_done.append(d_d)
    
    #Chart 2
    labels_2 =[]
    data_2=[]
    num = 0
    team_colors=[]
            

    for a in team:
        if (a.team_manager == request.user.profile):
            num = 0
            for i in project:            
                if (i.team == a):
                    num = num + 1        
            data_2.append(num)
            labels_2.append(a.name)
            new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            if new_color in team_colors:
                new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                team_colors.append(new_color)
            else:
                team_colors.append(new_color)
            
    most_recent_project = Project.objects.order_by('-project_deadline')[:1] 
    data_3_list=[]
    for i in most_recent_project:
        data_3_list.append(i.name)
    data_3 = ''.join(data_3_list)

    most_recent_ticket = Ticket.objects.order_by('-ticket_deadline')[:1] 
    data_4_list=[]
    for i in most_recent_ticket:
        data_4_list.append(i.name)
    data_4 = ''.join(data_4_list)
    
        
    return render ( request, 'bug/dashboard.html',{ 'team_colors':team_colors,
                                                    'most_recent_ticket':data_4,
                                                    'most_recent_project':data_3,
                                                    'data_2':data_2,
                                                    'labels_2':labels_2,
                                                    'ticket_colors_1':ticket_colors_1,
                                                    'ticket_colors_2':ticket_colors_2,
                                                    'tickets_all':tickets_all,
                                                    'tickets_done':tickets_done,
                                                    'labels':labels,
                                                    'ticket':ticket,
                                                    'project':project,
                                                    'team':team,
                                                    'profile':profile,
                                                    'cur_user':cur_user},
                                                    {'section':'dashboard'})
   
    


def sign_up_view(request):
    print("test1")
    form = SignUpForm(request.POST)
    if (form.is_valid()):
        print("test2")
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')        
        user.save()
        current_site = get_current_site(request)    
        mail_subject = 'Activate your Buggito account.'
        message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email])
        email.send()
        print("test3")
        print(email)
        return render(request,'activation_progress.html')
        # return HttpResponse('Please confirm your email address to complete the registration')
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password1')
        
        # user = authenticate(username=username,password = password)
        # login(request,user)
        # return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request,'bug/sign_up.html',{'form':form})
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request,'activation_done.html')
        
    else:
        return HttpResponse('Activation link is invalid!')


class ProjectCreateView(BSModalCreateView):
    template_name = 'add_project.html'
    form_class =  AddProjectForm
    success_message = 'Success: Project was added.'
    success_url = reverse_lazy('dashboard')

class ProjectUpdateView(BSModalUpdateView):
    
    model = Project
    template_name = 'update_project.html'
    form_class =  AddProjectForm
    success_message = 'Success: Project was updated.'
    success_url = reverse_lazy('dashboard')

class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = 'delete_project.html'
    success_message = 'Success: Project was deleted.'
    success_url = reverse_lazy('dashboard')

class TicketCreateView(BSModalCreateView):
    template_name = 'add_ticket.html'
    form_class =  AddTicketForm
    success_message = 'Success: Ticket was added.'
    success_url = reverse_lazy('dashboard')

class TeamCreateView(BSModalCreateView):
    template_name = 'add_team.html'
    form_class =  AddTeamForm
    success_message = 'Success: Team was added.'
    success_url = reverse_lazy('dashboard')



# muszę dostac argument w którym będą nazwy ticketów i nowe statusy
@require_POST
def update_ticket(request):
    
    ticket_name_list = request.POST.getlist('key_1_array[]')
    ticket_name_strip=[]
    for i in ticket_name_list:
        a=" ".join(i.split())
        ticket_name_strip.append(a)
    ticket_id_list = request.POST.getlist('key_2_array[]')
    dictionary = dict(zip(ticket_name_strip, ticket_id_list))
    tickets= Ticket.objects.all()
    for i in tickets:
        if i.name in ticket_name_strip:
            num = ticket_name_strip.index(i.name)
            id_t = ticket_id_list[num]
            if (id_t=="To Do"):
                id_t="To Do"
            if (id_t=="In Progress"):
                id_t="In Progress"
            if (id_t=="Done"):
                id_t="Done"
                
            i.status = id_t
            i.save()        
                
    return HttpResponse("Tickets were saved")

@require_POST
def update_profile(request):
    profile = Profile.objects.all()       
    person = request.POST.get('key1')
    a=""
    for i in profile:
        if (i.user.username == person):
            if(i.level == "standard"):
                a = "manager"
                i.level=a
                print("zmiana na managera")
            else:
                a = "standard"
                i.level=a
                print("zmiana na standard")
            
        i.save() 
    return HttpResponse("Test update")



        
    from django.views.decorators.csrf import requires_csrf_token
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
@requires_csrf_token
def my_customized_server_error (request, template_name = '500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response (request, * sys.exc_info ()). content
    return HttpResponseServerError (error_html)

    
