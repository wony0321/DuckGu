import os
import django

# Django 프로젝트 설정 파일을 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pjt.settings')
django.setup()

import requests
import json
from datetime import datetime
from movies.models import Keyword, Movie  
from django.conf import settings
from django.core.management import call_command

API_KEY = settings.API_KEY

genres_dict = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

country_dict = {
    "US": "미국",
    "KR": "대한민국",
    "JP": "일본",
    "FR": "프랑스",
    "CN": "중국",
    "DE": "독일",
    "IN": "인도",
    "GB": "영국",
    "IT": "이탈리아",
    "RU": "러시아",
    "CA": "캐나다",
    "ES": "스페인",
    "MX": "멕시코",
    "BR": "브라질",
    "AU": "오스트레일리아",
    "AR": "아르헨티나",
    "SE": "스웨덴",
    "NL": "네덜란드",
    "TR": "터키",
    "CH": "스위스",
    "EC": "에콰도르",
    "SU": "구소련",
    "IE": "아일랜드",
    "LU": "룩셈부르크",
    "LB": "레바논",
    "HK": "홍콩",
    "DK": "덴마크",
    "AE": "아랍에미리트",
    "NZ": "뉴질랜드",
    "BE": "벨기에",
    "PL": "폴란드",
    "IR": "이란"
}

def create_keywords():
    # 장르 키워드 생성
    for k in genres_dict:
        Keyword.objects.get_or_create(genre=genres_dict[k])
    # 국가 키워드 생성
    for c in country_dict:
        Keyword.objects.get_or_create(origin_country=country_dict[c])
    # 연대 키워드 생성
    eras = [f"{year}년대" for year in range(1900, 2030, 10)]
    for era in eras:
        Keyword.objects.get_or_create(era=era)

def fetch_movies():
    url = 'https://api.themoviedb.org/3/movie/top_rated'
    all_movies = []
    for page in range(1, 21):  # 페이지 범위 조정
        params = {
            'api_key': API_KEY,
            'language': 'ko-KR',
            'region': 'KR',
            'page': page,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            continue
        movies = response.json().get('results', [])
        all_movies.extend(movies)
    return all_movies

def save_movies(all_movies):
    saved_movies = []
    for movie in all_movies:
        if not movie.get('overview'):
            continue  # overview가 없는 영화는 건너뜁니다.

        release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d').date() if movie.get('release_date') else None

        item, created = Movie.objects.get_or_create(
            title=movie['title'],
            defaults={
                'poster_path': movie['poster_path'],
                'vote_average': movie['vote_average'],
                'release_date': release_date,
                'over_view': movie['overview']
            }
        )
        if created:
            for id in movie["genre_ids"]:
                genre = Keyword.objects.get(genre=genres_dict[id])
                item.keywords.add(genre)

            if release_date:
                era_keyword = Keyword.objects.get(era=f"{(release_date.year // 10) * 10}년대")
                item.keywords.add(era_keyword)

            movie_id = movie['id']
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
            detail_params = {'api_key': API_KEY}
            detail_response = requests.get(detail_url, params=detail_params)
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                countries = detail_data.get('origin_country', [])
                for code in countries:
                    if code in country_dict:
                        country_keyword = Keyword.objects.get(origin_country=country_dict[code])
                        item.keywords.add(country_keyword)
                    else:
                        print(f"Unknown country code: {code}")
        saved_movies.append(item)
    return saved_movies

def export_to_json():
    fixtures_dir = os.path.join('movies', 'fixtures')
    os.makedirs(fixtures_dir, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성
    json_path = os.path.join(fixtures_dir, 'movies_keywords.json')

    with open(json_path, 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'movies.Movie', 'movies.Keyword', stdout=f, indent=4, use_natural_primary_keys=True, use_natural_foreign_keys=True)
    
    print(f"JSON 파일이 {json_path}에 성공적으로 생성되었습니다.")

if __name__ == '__main__':
    create_keywords()
    all_movies = fetch_movies()
    saved_movies = save_movies(all_movies)
    export_to_json()
