from rest_framework import serializers
from .models import Movie, Meet, Review, Keyword
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# 전체 모임 조회용
User = get_user_model()


class MeetListSerializer(serializers.ModelSerializer):
    keywords_list = serializers.SerializerMethodField()

    class Meta:
        # 이름, user(회원 수 반환), 키워드, 커스텀 키워드
        model = Meet
        fields = ('id', 'name', 'users', 'keywords', 'keywords_list', )

    def get_keywords_list(self, obj):
        return [self.get_keyword_value(keyword) for keyword in obj.keywords.all()]

    def get_keyword_value(self, keyword):
        if keyword.genre:
            return keyword.genre
        elif keyword.era:
            return keyword.era
        else:
            return keyword.origin_country


# 모임 생성, 수정용

class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = '__all__'
        read_only_fields = ('admin', 'users', 'movie',)


# 모임 상세 페이지용
class MeetDetailSerializer(serializers.ModelSerializer):
    keywords_list = serializers.SerializerMethodField()

    class Meta:
        model = Meet
        fields = '__all__'

    def get_keywords_list(self, obj):
        return [self.get_keyword_value(keyword) for keyword in obj.keywords.all()]

    def get_keyword_value(self, keyword):
        if keyword.genre:
            return keyword.genre
        elif keyword.era:
            return keyword.era
        else:
            return keyword.origin_country


# 영화
class MovieSerializer(serializers.ModelSerializer):
    keywords_list = serializers.SerializerMethodField()

    class ReviewForMovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('id',)

    review_set = ReviewForMovieSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_keywords_list(self, obj):
        return [self.get_keyword_value(keyword) for keyword in obj.keywords.all()]

    def get_keyword_value(self, keyword):
        if keyword.genre:
            return keyword.genre
        elif keyword.era:
            return keyword.era
        else:
            return keyword.origin_country


# 리뷰
class ReviewSerializer(serializers.ModelSerializer):

    class UserInReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'id',)

    user = UserInReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie')

    def validate_rate(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("평점은 0점에서 5점 사이어야 합니다")
        if (value * 2) % 1 != 0:
            raise serializers.ValidationError("평점은 0.5점 단위로만 입력 가능합니다.")
        return value

    def validate(self, data):
        if self.instance is None:
            movie = self.context['movie']
            user = self.context['user']

            # movie와 user의 조합이 중복되지 않도록 검증
            if Review.objects.filter(movie=movie, user=user).exists():
                raise serializers.ValidationError("이미 평가한 영화입니다.")

            data['movie'] = movie
            data['user'] = user
        return data



# 키워드

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
        read_only_fields = ('users', )
