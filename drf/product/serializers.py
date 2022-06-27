from rest_framework import serializers

from product.models import Product as ProductModel
from product.models import Review as ReviewModel

from django.db.models import Avg

from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.fullname
    
    class Meta:
        model = ReviewModel
        fields = ["user","content","created",'rating',]


class ProductSerializer(serializers.ModelSerializer):

    review = serializers.SerializerMethodField()

    def get_review(self, obj):
        reviews = obj.review_set
        return {
            "last_review":ReviewSerializer(reviews.last()).data,
            "average_rating":reviews.aggregate(Avg("rating"))["avg"]
        }

    def validate(self, data): 
        exposure_end_date = data.get("exposure_end_date","")
        if exposure_end_date and exposure_end_date < datetime.now().date():
            raise serializers.ValidationError (
                detail = {"error": "유효하지 않은 노출 종료 날짜입니다."},
            )
        return data

    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()
        product.description += f"\n\n{product.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
        product.save()

        return product

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "description":
                value += f"\n\n{instance.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
            setattr(instance, key, value)
        instance.save()
        instance.description = f"{instance.modified.replace(microsecond=0, tzinfo=None)}에 수정되었습니다. \n\n" + instance.description      
        
        instance.save()
        return instance


    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username' #email도 가능
    )

    class Meta:
        model = ProductModel
        fields = ["user","thumbnail","description","created","modified","exposure_end_date","is_active","price","review"]


       