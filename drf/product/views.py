from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Product as ProductModel
from product.serializers import ProductSerializer

from datetime import datetime
from django.db.models import Q
from Django.permissions import RegisteredMoreThanThreeDaysUser
# Create your views here.


class ProductView(APIView):

    permission_classes = [RegisteredMoreThanThreeDaysUser]

    def get(self, request):
        today = datetime.now()
        products = ProductModel.objects.filter(
            Q(exposure_end_date__gte=today, is_active=True) |
            Q(user=request.user)
        )

        serialized_data = ProductSerializer(products, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.user
        request.data['user'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            Response(product_serializer.errors,
                     status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        product_serializer = ProductSerializer(
            product, data=request.data, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            Response(product_serializer.errors,
                     status=status.HTTP_400_BAD_REQUEST)
