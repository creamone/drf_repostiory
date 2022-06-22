from rest_framework import serializers

from product.models import Product as ProductModel

class ProductSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username' #email도 가능
    )

    class Meta:
        model = ProductModel
        fields = ["user","title","thumbnail","description","created","exposure_start_date","exposure_end_date",]