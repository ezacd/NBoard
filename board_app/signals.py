from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from .models import PostResponses
from django.conf import settings


@receiver(pre_save, sender=PostResponses)
def send_response_mail(sender, instance, **kwargs):
    user = instance.user.username
    to_email = instance.post.author.email
    from_email = settings.DEFAULT_FROM_EMAIL

    # send_mail(
    #     subject=f'Пользователь {user} откликнулся на ваше объявление',
    #     message=instance.text,
    #     from_email=from_email,
    #     recipient_list=[to_email, ]
    # )
