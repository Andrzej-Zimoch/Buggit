from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #path('login/',views.user_login, name='login')
        
    path('', lambda request: redirect('login/', permanent=False)),
    
    path ('',auth_views.LoginView.as_view(),name='login'),
    path ('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    path('dashboard/',views.dashboard, name='dashboard'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),



    #new register
    path('sign_up/',views.sign_up_view,name='sign_up'),
    #old register
    # path('register/', views.register,name='register'),
    path('base/',views.base,name="base"),

     # asyncSettings.dataUrl
    path('add/', views.ProjectCreateView.as_view(), name='add_project'),

    path('update_project/<int:pk>', views.ProjectUpdateView.as_view(), name='update_project'),
    path('delete/<int:pk>', views.ProjectDeleteView.as_view(), name='delete_project'),

    path('add_ticket/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('add_team/', views.TeamCreateView.as_view(), name='add_team'),

    path('update_ticket/',views.update_ticket,name='update_ticket'),

    path('update_profile/',views.update_profile,name='update_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
] 

from map.views import my_customized_server_error
handler500 = my_customized_server_error
