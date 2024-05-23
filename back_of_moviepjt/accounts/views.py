from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

User = get_user_model()


@api_view(['POST'])
def follow_user(request, user_id):
    you = get_object_or_404(User, id=user_id)
    me = request.user
    if me != you:
        if me in you.followings.all():
            you.followers.remove(me)
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        else:
            you.followwers.add(me)
            return Response({'status': 'followed'}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'자기자신은 팔로우할 수 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userInfo(request, user_name):
    user = get_object_or_404(User, username=user_name)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
