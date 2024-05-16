import os

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 기본 세팅
EMAIL_BACKEND = 'app.backends.email_backend.EmailBackend' # SSL 인증 비활성화 세팅
# 메일을 호스트하는 서버
EMAIL_HOST = 'smtp.gmail.com'
# Gmail과 통신하는 포트
EMAIL_PORT = 587
# TLS 보안 설정
EMAIL_USE_TLS = True
# SSL 보안 설정
EMAIL_USE_SSL = False
# 발신할 이메일
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# 발신할 메일의 구글 비밀번호
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# 사이트와 관련된 자동 응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 버그 해결법 : ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)
# https://www.youtube.com/watch?v=ZbrJjkOX8Ro