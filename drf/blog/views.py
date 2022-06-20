from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from blog.models import Article as ArticleModel
from Django.permissions import RegisterMoreTHanThreeDaysUser

class ArticleView(APIView):  # CBV 방식

    # permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 로그인 한 사용자의 게시글 목록 return
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        articles = ArticleModel.objects.filter(user=user)
        titles = [article.title for article in articles]  # list 축약 문법

        # titles = []

        # for article in articles:
        #     titles.append(article.title)

        return Response({"article_list": titles})


    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        contents = request.data.get("contents", "")
        categorys = request.data.get("category", [])

        if len(title) <= 5:
            return Response({"error": "타이틀은 5자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(contents) <= 20:
            return Response({"error": "내용은 20자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not categorys:
            return Response({"error": "카테고리가 지정되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)    


        article = ArticleModel(
            user=user,
            title=title,
            contents=contents
        )


        article.save()
        article.category.add(*categorys)
        return Response({"message":"성공!!"},status=status.HTTP_200_OK)