# back_of_moviepjt/keyword-user.py

import random
import json
import os
import django
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.conf import settings

# Django 설정을 로드합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pjt.settings')
django.setup()

from movies.models import Keyword  # Django 설정 로드 후 모델 임포트

def generate_keyword_user_fixtures():
    User = get_user_model()
    users = User.objects.all()
    keywords = Keyword.objects.all()

    # Create random Keyword-User relationships
    for keyword in keywords:
        num_users = random.randint(1, 10)
        selected_users = random.sample(list(users), num_users)
        for user in selected_users:
            keyword.users.add(user)
            print(f'Added User {user.id} to Keyword {keyword.id}')

    # Export data to JSON
    keyword_data = serialize('json', keywords)
    fixtures_dir = 'movies/fixtures'
    os.makedirs(fixtures_dir, exist_ok=True)
    fixtures_path = os.path.join(fixtures_dir, 'keyword_user.json')
    with open(fixtures_path, 'w') as json_file:
        json.dump(json.loads(keyword_data), json_file, indent=4)

    print(f'Successfully created random Keyword-User relationships and exported to {fixtures_path}')

if __name__ == '__main__':
    generate_keyword_user_fixtures()
