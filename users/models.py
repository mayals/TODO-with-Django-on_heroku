from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    P_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='U_profile', null=True)
    P_image = models.ImageField(verbose_name='Profile Image', upload_to='prof_image/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return f'{self.P_user} profile'




# https: // docs.djangoproject.com/en/3.2/topics/signals/
# If this behavior is problematic 
# (such as when using signals to send an email whenever a model is saved),
#  pass a unique identifier as the dispatch_uid argument 
# to identify your receiver function. 
# This identifier will usually be a string, 
# although any hashable object will suffice. 
# The end result is that your receiver function will only be bound to the signal once for each unique dispatch_uid value




def create_profile(sender, instance, created, **kwargs):
    """
       Creates the user profile for a given User instance.

       Args: sender, instance, created,
       Sender: The model class,
       Instance: The actual instance being saved,
       Created: Boolean that defaults to True if user is created
    """


    if created:
        Profile.objects.create(P_user = instance)


post_save.connect(create_profile, sender=User, dispatch_uid=create_profile)
                     




# same way >> also work :)
# def create_profile(sender, **kwarg):
#     if kwarg['created']:
#         Profile.objects.create(user=kwarg['instance'])


# post_save.connect(create_profile, sender=User)
