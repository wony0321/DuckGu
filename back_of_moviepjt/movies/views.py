from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from .models import Movie, Keyword, Review, Meet
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import MeetListSerializer, MeetDetailSerializer, MeetSerializer, ReviewSerializer, KeywordSerializer, MovieSerializer
from django.db.models import Count, Q

@api_view(['GET', 'POST'])
# get은 로그인 안해도 가능/ post는 로그인해야함
def meet(request):
    if request.method == 'GET':
        meets = Meet.objects.all()
        serializer = MeetListSerializer(meets, many=True)

        # 전체 키워드 가져오기
        keywords = Keyword.objects.all()
        kw_serializer = KeywordSerializer(keywords, many=True)

        response_data = {
            'meets': serializer.data,
            'keywords_list': kw_serializer.data
        }
        return Response(response_data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = MeetSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                meet = serializer.save(admin=request.user)
                if request.user not in meet.users.all():
                    meet.users.add(request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# 내가 가입한 그룹 보게하는 함수
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def joined_meets(request):
    if request.user.is_authenticated:
        meets = Meet.objects.filter(users=request.user)
        serializer = MeetListSerializer(meets, many=True)

        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def join_or_leave_meet(request, meet_id):
    try:
        meet = Meet.objects.get(id=meet_id)
    except Meet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        meet.users.add(request.user)
        meet.save()
        serializer = MeetSerializer(meet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        meet.users.remove(request.user)
        meet.save()
        serializer = MeetSerializer(meet)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def meet_detail(request, meet_id):
    print(f'🐸🐸🐸🐸🐸🐸🐸🐸🐸🐸🐸request user는 {request.user}')
    meet = get_object_or_404(Meet, pk=meet_id)

    if request.method == 'GET':
        serializer = MeetDetailSerializer(meet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user == meet.admin:
            serializer = MeetSerializer(meet, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        if request.user == meet.admin:
            meet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reiview_list(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == 'GET':
        reviews = movie.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={
                                      'request': request, 'movie': movie, 'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, movie_pk, review_pk):
    movie = Movie.objects.get(pk=movie_pk)
    review = Review.objects.get(pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if request.user == review.user:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        if request.user == review.user:
            serializer = ReviewSerializer(review, data=request.data, partial=True, context={'movie': movie, 'user': review.user})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# def movie_list(request):
#     if request.method == 'GET':
#         keywords_str = request.query_params.get('keywords')
#         if keywords_str:
#             keywords = list(map(int, keywords_str.split(',')))
#         else:
#             keywords = []

#         print(f'request는 {request}')
#         for keyword in keywords:
#             print(f'keyword는 {keyword}')

#         if keywords:
#             movies = Movie.objects.filter(
#                 keywords__id__in=keywords).distinct().order_by('-vote_average')[:50]
#         else:
#             movies = Movie.objects.all().order_by('-vote_average')[:50]

#         print("Number of movies retrieved:", len(movies))

#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        keywords_str = request.query_params.get('keywords')
        if keywords_str:
            keyword_ids = list(map(int, keywords_str.split(',')))
        else:
            keyword_ids = []

        if keyword_ids:
            # 사용자 키워드와 영화 키워드 간의 유사도를 계산하여 관련도 높은 순으로 정렬
            movies = Movie.objects.annotate(
                match_count=Count('keywords', filter=Q(keywords__id__in=keyword_ids))
            ).order_by('-match_count', '-vote_average')[:50]
        else:
            movies = Movie.objects.all().order_by('-vote_average')[:50]

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user in movie.like_users.all():
        movie.like_users.remove(request.user)
        isLikeMovie = False
    else:
        movie.like_users.add(request.user)
        isLikeMovie = True

    like_count = movie.like_users.count()
    context = {
        'isLikeMovie': isLikeMovie,
        'like_count': like_count
    }
    return Response(context, status=status.HTTP_200_OK)
