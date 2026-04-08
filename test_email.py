import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhivaya_kniga.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    try:
        send_mail(
            'Тестовое письмо от Живой книги',
            'Привет! Это тестовое письмо для проверки работы почты через Яндекс.',
            settings.DEFAULT_FROM_EMAIL,
            ['aryanova.sofia@yandex.ru'],  # Замените на ваш тестовый email
            fail_silently=False,
        )
        print("✅ Письмо успешно отправлено!")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

if __name__ == "__main__":
    test_email()