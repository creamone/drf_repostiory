from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from django.contrib.auth import login, logout, authenticate

from user.serializers import UserSignupSerializer, UserSerializer, UserProfileSerializer


# Create your views here.

# CBV Class Base View


# def sum_numbers(num1, num2):
#     return num1+num2


class UserView(APIView):  # CBV 방식
    # permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    permission_classes = [permissions.IsAuthenticated]

    # 사용자 정보 조회
    # def get(self, request):
    #     return Response({"message": "get method"})

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!!"})
        else:
            print(serializer.errors)
            return Response({"message": "가입실패!!"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})

# FBV Function Base View
# def user_view(request):
#     if request.method == "get":
#         pass


class UserAPIView(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "login success!!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})


# 서버에서 -> 클라이언트로 object를 보내주고싶을떄
# ex) 서버에서 회원정보를 클라이언트로 보내주고싶다.
#   user = request.user
#   serializer(user) => 클라이언트에서 알아들을 수 있게됨 (json 형태)
#   user = request.user
#   (object) --(serializer) --> (json)
#   return Response(serializer(user))
#   return Response({'user':user})
