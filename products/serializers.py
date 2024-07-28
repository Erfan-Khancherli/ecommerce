from rest_framework import serializers

from products.models import  Item, Price , Category , ItemImage




# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brands
#         fields = ['id', 'title']
        
        
class ItemSerializer(serializers.ModelSerializer):
    # brand = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'
        depth = 1
        ordering = ['id']
        
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Price
        fields = [
            'id',
            'amount',
            'currencycode',
        ]
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'category_title',
            'category_path'
        ]
class ItemImageSerializer(serializers.ModelSerializer):
    # images = serializers.ImageField(many=True)
    class Meta:
        model = ItemImage
        fields = [
            'id',
            'image',
            'alt_text'
        ]
class CreateItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    price = PriceSerializer()
    image = ItemImageSerializer()
    class Meta:
        model = Item
        fields = [
            'title',
            'price',
            # 'brand',
            'availableForSale', 
            'category',
            'description',
            'image',
            'color',
            'size',
        ]
    def create(self, validated_data):
        price_data = validated_data.pop('price')
        category_data = validated_data.pop('category')
        item_image_data = validated_data.pop('image')
        price_instance = Price.objects.create(**price_data)
        category_instance = Category.objects.create(**category_data)
        image_instance = ItemImage.objects.create(**item_image_data)
        item = Item.objects.create(price=price_instance,category=category_instance,image=image_instance,**validated_data)
        return item


    def update(self, instance, validated_data):
        price_data = validated_data.pop('price', None)
        category_data = validated_data.pop('category', None)
        item_image_data = validated_data.pop('image' , None)
        if price_data:
            # Update price instance
            Price.objects.filter(id=instance.price.id).update(**price_data)

        if category_data:
            # Update or get existing Category instance
            category_instance, created = Category.objects.get_or_create(**category_data)
            instance.category = category_instance
        if item_image_data:
            ItemImage.objects.filter(id = instance.image.id).update(**item_image_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance