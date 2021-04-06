from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core import serializers
import datetime
from smart_selects.db_fields import ChainedManyToManyField,ChainedForeignKey

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    level_choices = (('standard','standard'),('manager','manager'),('admin','admin'))
    level = models.CharField(max_length=240,choices=level_choices,default=level_choices[0][0])
    email = models.EmailField(max_length=250)
    def __str__(self):
        return self.user.username


@receiver(post_save,sender=User)
def update_profile_signal(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Team(models.Model):
    name = models.CharField(max_length=250, default="")
    members = models.ManyToManyField('Profile',limit_choices_to={'level':'standard'},blank=True,related_name="members")
    team_manager = models.ForeignKey('Profile',limit_choices_to={'level':'manager'},blank=True,related_name="team_manager",on_delete=models.CASCADE,null=True,default=None)
    # add manager
    def __str__(self):
        return self.name

class Project (models.Model):
    name = models.CharField(max_length=250, default="")
    description = models.TextField(default="")
    team = models.ForeignKey(Team,on_delete=models.CASCADE,blank=True,default=None,null=True)
    # project manager to chained z team
    manager = ChainedForeignKey(
        "Profile",
        chained_field="team",
        chained_model_field="team_manager",
        show_all=False,
        auto_choose=True,
        related_name="p_manager",
        default=None
    ) 
    
  
    project_deadline = models.DateField(default=None)

    def __str__(self):
        return self.name

class Ticket (models.Model):
    name = models.CharField(max_length=250, default="")
    description = models.TextField(default="")
    
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    assigned_team =ChainedForeignKey(
        "Team",
        chained_field="project",
        chained_model_field="project",
        show_all=False,
        auto_choose=True,
        related_name="t_team"
    ) 
    
    assigned_member = ChainedForeignKey(
        "Profile",
        chained_field="assigned_team",
        chained_model_field="members",
        show_all=False,
        auto_choose=True,
        
    ) 

    ticket_deadline = models.DateField(default=None,blank=True,null=True)

   
    status_choices = (('To Do','To Do'),('In Progress','In Progress'),('Done','Done'))
    status = models.CharField(max_length=240,choices=status_choices,default=status_choices[0][0])
    def __str__(self):
        return self.name

