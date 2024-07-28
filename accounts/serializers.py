from rest_framework import serializers
from . models import CustomUser , Address
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email'  ,'first_name' , 'last_name','password' ]

        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    # def validate_password(self , value):
    #     return make_password(value)
    

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self , value):
        validate_password(value)
        return value  
    
class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = [
            'id',
            'user',
            'street_address',
            'apartment_address',
            'country',
            'zip',
            'address_type',
            'phone_number',
            ]
        read_only_fields = ['user']
# class UpdateAddressSerializer(serializers.Serializer):
#     class Meta:
#         model = Address
#         fields = [
#             'id',
#             'user',
#             'street_address',
#             'apartment_address',
#             'country',
#             'zip',
#             'address_type',
#             'phone_number',
#             ]
#     def update(self, instance, validated_data):
#         shop = validated_data.pop('shop')
#         shop_obj = Address.objects.filter(pk=validated_data['id']).first()
#         if shop_obj:
#             instance.shop = shop_obj
#         return super().update(instance, validated_data)
