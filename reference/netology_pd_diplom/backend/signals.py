# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
# from django.http import JsonResponse
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User
from netology_pd_diplom.tasks import send_email

# new_user_registered = Signal(
#     providing_args=['user_id'],
# )
#
# new_order = Signal(
#     providing_args=['user_id'],
# )
new_user_registered: Signal = Signal('user_id')

new_order: Signal  = Signal('user_id')

new_contact: Signal  = Signal('user_id')

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    async_result = send_email.delay(reset_password_token.user.email,
                                    f"Password Reset Token for {reset_password_token.user}",
                                    reset_password_token.key
                                    )

    return async_result.task_id


    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {reset_password_token.user}",
    #     # message:
    #     reset_password_token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    async_result = send_email.delay(token.user.email,
                                    f"Password Reset Token for {token.user.email}",
                                    token.key
                                    )

    return async_result.task_id

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {token.user.email}",
    #     # message:
    #     token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [token.user.email]
    # )
    # msg.send()


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    async_result = send_email.delay(user.email,
                                    'Обновление статуса заказа',
                                    'Заказ сформирован'
                                    )
    return async_result.task_id

    #
    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Обновление статуса заказа",
    #     # message:
    #     'Заказ сформирован',
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [user.email]
    # )
    # msg.send()

#< добавляем отправку письма при создании нового адреса доставки
@receiver(new_contact)
def new_contact_signal(user_id, **kwargs):
    """
    отправяем письмо при создании нового адреса доставки
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    async_result = send_email.delay(user.email,
                                    'Добавление нового контакта',
                                    'Новый контакт добавлен'
                                    )
    #? transaction.on_commit(lambda: some_celery_task.delay(obj.id))

    return async_result.task_id
#>