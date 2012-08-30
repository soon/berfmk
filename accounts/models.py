# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.db                  import models
from django.db.models.signals   import post_save
from django.contrib.auth.models import User, Group
#-------------------------------------------------------------------------------
class UserProfile(models.Model):
    user    = models.OneToOneField(User)
    group   = models.ForeignKey(Group)
    #---------------------------------------------------------------------------
    def set_group(self, group):
        self.group.user_set.remove(self.user)
        self.group = group
        self.group.user_set.add(self.user)
        self.save()
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.user.username + ': ' + self.group.name
#-------------------------------------------------------------------------------
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name = 'Пользователь')
        user = UserProfile.objects.create(user = instance, group = group)
        group.user_set.add(instance)
#-------------------------------------------------------------------------------
post_save.connect(create_user_profile, sender = User)
#-------------------------------------------------------------------------------