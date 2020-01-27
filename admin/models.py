from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# user permission data ...
class AdminUserPermission(models.Model):

    user_can_view = models.BooleanField(default=False)
    user_can_delete = models.BooleanField(default=False)
    user_can_update = models.BooleanField(default=False)
    user_can_active = models.BooleanField(default=False)
    user_can_makesuperuser = models.BooleanField(default=False)
    user_can_create_user = models.BooleanField(default=False)
    created_at = models.DateField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "AdminUserPermission"


# @receiver(post_save, sender=User)
# def user_is_created(sender, instance, created, **kwargs):
#     if created:
#         AdminUserPermission.objects.create(user=instance)
#     else:
#         instance.AdminUserPermission.save()