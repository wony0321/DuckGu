import os
import django

# Django 프로젝트 설정 파일을 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pjt.settings')
django.setup()

import json
import random
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from movies.models import Meet, Keyword



User = get_user_model()

def generate_meet_fixtures():
    users = list(User.objects.all())
    keywords = list(Keyword.objects.all())

    if len(users) < 100:
        raise ValueError("There must be at least 100 users to generate the fixtures.")

    fixtures = []

    for i in range(1, 101):
        meet_name = f"둥지{i}"

        # 임의의 유저 5명을 선택
        selected_users = random.sample(users, k=5)

        # 첫 번째 유저를 meet의 admin으로 설정
        admin_user = selected_users[0]

        # Meet 객체 생성
        meet = Meet.objects.create(name=meet_name, admin=admin_user)

        # 임의의 키워드 5개를 선택
        selected_keywords = random.sample(keywords, k=5)
        meet.keywords.set(selected_keywords)
        meet.users.set(selected_users)

        # fixtures 데이터 작성
        meet_fixture = {
            "model": "movies.Meet",
            "pk": meet.pk,
            "fields": {
                "name": meet.name,
                "keywords": [keyword.pk for keyword in meet.keywords.all()],
                "users": [user.pk for user in meet.users.all()],
                "admin": admin_user.pk,
            }
        }
        fixtures.append(meet_fixture)

    # 'movies/fixtures' 디렉토리에 파일 저장
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'movies', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)
    file_path = os.path.join(fixtures_dir, 'meets.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=4)

    print(f'Successfully generated {file_path}')

if __name__ == "__main__":
    generate_meet_fixtures()
