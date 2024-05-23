from django.conf import settings
from django.contrib.auth import get_user_model
from pathlib import Path
import random
import json
import django
import os

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pjt.settings')
django.setup()

User = get_user_model()

first_name_samples = '김이박최정강조윤장임'
middle_name_samples = '민서예지도하주윤채현지'
last_name_samples = '준윤우원호후서연아은진'


def random_name(existing_names):
    while True:
        name = random.choice(first_name_samples) + random.choice(
            middle_name_samples) + random.choice(last_name_samples)
        if name not in existing_names:
            return name


def generate_user_data(num_users=100):
    users = []
    existing_names = set()

    for i in range(num_users):
        last_name = random.choice(first_name_samples)
        first_name = random.choice(
            middle_name_samples) + random.choice(last_name_samples)
        password = "rkskekfk"

        user = User(
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        # username을 user{user.pk} 형식으로 설정
        user.username = f"user{user.pk}"
        user.save()

        user_fixture = {
            "model": "accounts.User",  # app 부분을 실제 앱 이름으로 변경해주세요.
            "pk": user.pk,
            "fields": {
                "username": user.username,
                "first_name": first_name,
                "last_name": last_name,
                "password": user.password,  # 해시된 비밀번호 저장
                "followings": []
            }
        }
        users.append(user_fixture)
    return users


def save_to_fixture(data, filename='users.json'):
    Path("accounts/fixtures").mkdir(parents=True, exist_ok=True)
    with open(f'accounts/fixtures/{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    user_data = generate_user_data(100)
    save_to_fixture(user_data)
    print(f"{len(user_data)} user records have been saved to 'accounts/fixtures/users.json'")
