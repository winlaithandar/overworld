from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework. response import Response
from rest_framework.exceptions import PermissionDenied
from knox.models import AuthToken
from libgravatar import Gravatar
from actions.serializers import RatingSerializer
from actions.models import Ratings, Journal
from .models import CustomUser
from .serializers import UserSerializer, ProfileSerializer, RegisterSerializer, LoginSerializer, RecentActivitySerializer
from rest_framework.parsers import MultiPartParser

class RatingsView(generics.GenericAPIView):
    """Endpoint for getting ratings by user for all games.

    Supports only GET.
    Returns:
        data: [{game, user_id, rating}...]
    """
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        user = CustomUser.objects.get(username=username)
        ratings = Ratings.objects.filter(user=user)
        serializer = RatingSerializer(ratings, many=True).data
        
        return Response(serializer)


class RegisterView(generics.GenericAPIView):
    """Endpoint for signing up to Overworld.

    All authentication related functionality in Overworld is handled by
    django-rest-knox.

    Returns:
        user: object with user-related data.
        token: JWT token for handling the session in the browser.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user, context=self.get_serializer_context())

        return Response({
            'user': user_data.data,
            'token': AuthToken.objects.create(user)[1]
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Endpoint for login in to Overworld.

    All authentication related functionality in Overworld is handled by
    django-rest-knox.

    Returns:
        user: object with user-related data.
        token: JWT token for handling the session in the browser.
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_data = UserSerializer(user, context=self.get_serializer_context())

        return Response({
            'user': user_data.data,
            'token': AuthToken.objects.create(user)[1]
        })


class UserView(generics.RetrieveAPIView):
    """Endpoint for obtaining basic user data.

    Returns:
        user: object with user ID, username and email.
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileView(generics.GenericAPIView):
    """Endpoint for obtaining a user's profile.

    The profile consists of the user's activity, favorite games, bio, reviews,
    contact information, stats, lists, followers and other stuff. This endpoint
    accepts both GET and POST methods.
    """
    def post(self, request, *args, **kwargs):
        """Method for updating your profile."""
        me = get_object_or_404(CustomUser, id=request.user.id)
        parser_classes = (MultiPartParser,)


        #if 'refreshAvatar' in request.data:
         #   g = Gravatar(me.email)
          #  me.gravatar = g.get_image(size=120, default='retro', use_ssl=True)

        for key in request.data:
          setattr(me, key, request.data[key])

        me.save()
        serializer = ProfileSerializer(me).data

        return Response(serializer)

    def get(self, request, *args, **kwargs):
        """Method for getting the profile."""
        user = get_object_or_404(CustomUser, username=kwargs['username'])
        serializer = ProfileSerializer(user).data

        if not request.user.is_anonymous:
            # handle follow logic for showing the following/follow/unfollow
            # buttons in the frontend
            me = CustomUser.objects.get(id=request.user.id)
            serializer['me'] = UserSerializer(me).data
            if user in me.following.all():
                serializer['followingUser'] = True

        return Response(serializer)


class RecentActivityView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        limit = int(request.GET.get('limit', 0))
        if limit <= 0:
            limit = None

        user = CustomUser.objects.get(username=kwargs['username'])
        entries = Journal.objects.filter(user=user).order_by('-date')[:limit]
        serializer = RecentActivitySerializer(entries, many=True)

        return Response(serializer.data)


class FollowView(generics.GenericAPIView):
    """Endpoint to follow a user.

    This adds a user to the current user's `following` field, and adds the
    current user to that user's `followers` field. These fields are a
    many-to-many relationship.

    The user calling this endpoint must be authenticated.

    Args:
        username: the user to follow.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        me = CustomUser.objects.get(id=request.user.id)
        try:
            user = CustomUser.objects.get(username=request.data['username'])
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User does not exist'},
                            status.HTTP_404_NOT_FOUND)

        me.following.add(user)
        user.followers.add(me)

        return Response([])


class UnfollowView(generics.GenericAPIView):
    """Endpoint to unfollow a user.

    This removes a user from the current user's `following` field, and removes
    the current user from that user's `followers` field. These fields are a
    many-to-many relationship.

    The user calling this endpoint must be authenticated.

    Args:
        username: the user to unfollow.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        me = CustomUser.objects.get(id=request.user.id)
        try:
            user = CustomUser.objects.get(username=request.data['username'])
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User does not exist'},
                            status.HTTP_404_NOT_FOUND)

        me.following.remove(user)
        user.followers.remove(me)

        return Response([])
