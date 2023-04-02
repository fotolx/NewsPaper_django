from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Post, UsersSubscribed
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from NewsPaper.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL
from django.template.loader import render_to_string

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Post)
def mail_to_subscribers(sender, instance, created, **kwargs):
    try:
        post = instance
        category = post.category.get().id
        header = post.header
        main_text = post.main_text[:50]
        subscribers_list = UsersSubscribed.objects.filter(category=category)
        for each in subscribers_list:
            print(each)
            hello_text = f'Здравствуй, {each.user}. Новая статья в твоём любимом разделе!\n'
            html_content = render_to_string('account/email/mail_to_subscribers.html', {'header': header, 'main_text': main_text, 'hello_text': hello_text,})
            msg = EmailMultiAlternatives(
            subject=f'{header}',
            body=hello_text+main_text,
            from_email=EMAIL_HOST_USER,
            to=[each.user.email],
            )
            msg.attach_alternative(html_content, "text/html") # добавляем html
            msg.send()

    except ObjectDoesNotExist:
        pass