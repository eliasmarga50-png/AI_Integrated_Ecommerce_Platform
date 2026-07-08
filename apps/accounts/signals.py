


from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    Executes after a User object is saved.
    """

    if created:
        print(
            f"New user created: {instance.username}"
        )