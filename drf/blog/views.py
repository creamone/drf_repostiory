
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from blog import serializers
from blog.models import Article as ArticleModel
from Django.permissions import RegisterMoreTHanThreeDaysUser,IsAdminOrIsAuthenticatedReadOnly

from blog.serializers import ArticleSerializer

from django.utils import timezone






class ArticleView(APIView):  # CBV 방식

    # permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 로그인 한 사용자의 게시글 목록 return
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        today =timezone.now
        articles = ArticleModel.objects.filter(
            exposure_start_date__lte =today,
            exposure_end_date__gte = today,
        ).order_by("-id")

        serializer = ArticleSerializer(articles, many=True).data
        # titles = [article.title for article in articles]  # list 축약 문법

        # titles = []

        # for article in articles:
        #     titles.append(article.title)

        return Response(articles, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        contents = request.data.get("contents", "")
        categorys = request.data.get("category", [])
        exposure_start_date= request.data.get("exposure_start_date")
        exposure_end_date= request.data.get("exposure_end_date")

        if len(title) <= 5:
            return Response({"error": "타이틀은 5자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(contents) <= 20:
            return Response({"error": "내용은 20자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not categorys:
            return Response({"error": "카테고리가 지정되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)    


        article = ArticleModel(
            user=user,
            title=title,
            contents=contents,
            exposure_start_date=exposure_start_date,
            exposure_end_date=exposure_end_date,
        )


        article.save()
        article.category.add(*categorys)
        return Response({"message":"성공!!"},status=status.HTTP_200_OK)


    #  # 게시글 조회 기능
    # # 로그인한 사용자만 가능
    # def get(self, request):
    #     user = request.user
    #     if not user.is_authenticated:
    #         msg = '로그인을 해주세요.'
    #         return Response({'message': msg})
        
    #     articles = Article.objects.filter(author=user)

    #     # # 현재 시간 기준 : 노출 시작 일자와 종료 일자 사이에 있는 게시글 만 보여주기
    #     # show_date_now = timezone.now()
    #     # # show_date_now = '2022-06-24 14:00:00' # datetime 기준 (현재 시간)
    #     # # print(show_date_now)

    #     # # print(datetime.now())
    #     # # print(timezone.now()) # (django 기준시 기준)

    #     # qyery = Q(author=user) & Q(show_start_date__lte=show_date_now) & Q(show_end_date__gte=show_date_now)
    #     # articles = Article.objects.filter(qyery).order_by("show_start_date")

    #     return Response(ArticleSerializer(articles, many=True).data)