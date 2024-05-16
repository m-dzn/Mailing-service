import threading
import logging
from django.core.mail import EmailMessage


logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


def send_email_with_attachments(subject, content, from_email, recipient_list, attachments=[]):
    """
    이메일을 보내는 함수
    :param subject: 이메일 제목
    :param content: 이메일 내용
    :param from_email: 발신자 이메일
    :param recipient_list: 수신자 이메일 리스트
    :param attachments: 첨부파일 리스트 (튜플 형태: (파일 이름, 파일 데이터, MIME 타입))
    """
    try:
        email = EmailMessage(subject, content, from_email, recipient_list)

        for attachment in attachments:
            email.attach(attachment[0], attachment[1], attachment[2])

        email.send()
        logging.info(f'Email sent successfully to {", ".join(recipient_list)}')
    except Exception as e:
        logging.error(f'Failed to send email: {str(e)}')


def send_email_async(subject, content, from_email, recipient_list, attachments=[]):
    """
    이메일을 비동기로 보내는 함수
    :param subject: 이메일 제목
    :param content: 이메일 내용
    :param from_email: 발신자 이메일
    :param recipient_list: 수신자 이메일 리스트
    :param attachments: 첨부파일 리스트 (튜플 형태: (파일 이름, 파일 데이터, MIME 타입))
    """
    try:
        thread = threading.Thread(target=send_email_with_attachments, args=(subject, content, from_email, recipient_list, attachments))
        thread.start()
        logging.info('Email sending thread started successfully')
    except Exception as e:
        logging.error(f'Failed to start email sending thread: {str(e)}')


