from blog.models import Category as CategoryModel
from blog.models import Category as ArticleModel
from blog.models import Comment as CommentModel

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from rest_framework import serializers

from blog.serializers import ArticleSerializer, CommentSerializer


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age"]


class UserSerializer(serializers.ModelSerializer):
    # One-to-one 관계에서는 fk처럼 사용 가능하다.
    userprofile = UserProfileSerializer()
    articles = ArticleSerializer(many=True, source="article_set")
    comments = CommentSerializer(many=True, source="comment_set")
    # 사용자의 게시글 user's article

    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email", "userprofile"]


class HobbySerializer(serializers.ModelSerializer):
    # serializers.SerializerMethodField()를 사용해 원하는 필드를 생성한다.
    same_hobby_users = serializers.SerializerMethodField()

    def get_same_hobby_users(self, obj):
        user_list = []
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)

        return user_list

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]
