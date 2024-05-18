from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=SocialAccount)
def save_profile_image(sender, instance, **kwargs):
    if instance.provider == 'google':
        picture_url = instance.extra_data['picture']
        user = instance.user
        user.avatar = picture_url
        user.file_receiving_email = instance.extra_data['email']
        user.save()
