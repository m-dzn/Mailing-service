import os
from django.http import HttpResponse
from app.thread import send_email_async
from app.utils import get_file


def send_email_test(request):
    file = get_file('bc1ac9b8-44dd-45db-8a82-9efdb82bb7b4.pdf', 'learning-material')

    send_email_async(
        'Test Email',
        'This is a test email sent from Django.',
        f'{os.getenv('EMAIL_HOST_USER')}',
        ['88yangkh@gmail.com'],
        [('test.pdf', file, 'application/pdf')],
    )

    return HttpResponse('Email sent successfully.')
