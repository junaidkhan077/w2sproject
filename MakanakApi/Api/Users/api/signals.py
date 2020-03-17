import django.dispatch
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django_rest_passwordreset.signals import reset_password_token_created

reset_password_token_created = django.dispatch.Signal(
    providing_args=["reset_password_token", "request"],
)

pre_password_reset = django.dispatch.Signal(providing_args=["user", "request"])

post_password_reset = django.dispatch.Signal(
    providing_args=["user", "request"])


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
        'reset_password_url': "http://3.6.160.132/pages/auth/reset-password/?token={token}".format(token=reset_password_token.key)
    }

    # render email text
    print(context)
    email_html_message = render_to_string('email/reset_password.html', context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)
    print('render email text2')
    msg = EmailMultiAlternatives(
        # title:
        ("Password Reset for {title}".format(title="Makanak")),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    print('email html msg:'+email_html_message)
    msg.send()
