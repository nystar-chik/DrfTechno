from rest_framework import serializers
from apps.models import Product, Category, Characteristics
from account.serializer import DateUserSerializer

class ProductSerializer(serializers.ModelSerializer):
    user = DateUserSerializer()
    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
    #     characteristic = validated_data.pop('characteristic', [])
    #     product = Product.objects.create(**validated_data)
    #     product.characteristic.set(characteristic)
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.price = validated_data.get('price', instance.price)
    #     characteristic = validated_data.get('characteristic')
    #     instance.save()
    #     if characteristic is not None:
    #         instance.characteristic.set(characteristic)         
    #     return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = '__all__'






