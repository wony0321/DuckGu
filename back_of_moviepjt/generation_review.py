import os
import django

# Django 프로젝트 설정 파일을 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pjt.settings')

# Django 애플리케이션을 초기화합니다.
django.setup()

import json
import random
from django.contrib.auth import get_user_model
from movies.models import Movie, Review

def generate_reviews():
    # 사용자 및 영화 목록 가져오기
    User = get_user_model()
    users = User.objects.all()
    movies = Movie.objects.all()

    # 0.5 단위 평점 리스트 생성
    rates = [i * 0.5 for i in range(11)]  # 0, 0.5, 1, ..., 4.5, 5

    # Review 인스턴스 생성하여 JSON 데이터 구성
    reviews_data = []
    for i in range(100):  # 100개의 리뷰 생성
        user = random.choice(users)
        movie = random.choice(movies)
        rate = random.choice(rates)  # 0.5 단위로 임의의 평점 생성
        content = f"{user.username}이 쓴 {movie.title} 리뷰입니다."

        review_data = {
            "model": "movies.review",
            "pk": i + 1,  # primary key 값을 설정
            "fields": {
                "movie": movie.id,
                "user": user.id,
                "rate": rate,  # 소수점 첫째 자리까지 반올림
                "content": content,
            }
        }
        reviews_data.append(review_data)

    # JSON 파일로 저장
    fixtures_dir = os.path.join('movies', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성
    json_path = os.path.join(fixtures_dir, 'reviews.json')

    with open(json_path, 'w') as f:
        json.dump(reviews_data, f, indent=4)

    print(f"JSON 파일이 {json_path}에 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    generate_reviews()
