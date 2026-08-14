from rest_framework import serializers
from .models import CafeModel, CafeStaffModel


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeModel
        fields = ['id', 'name', 'slug', 'logo', 'primary_color', 'cover_image']
        read_only_fields = ('id', 'slug')


class CafeBrandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeModel
        fields = ['name', 'logo', 'cover_image', 'primary_color']


class CafeStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = CafeStaffModel
        fields = ['id', 'username', 'password','first_name', 'last_name', 'role', 'cafe']
        read_only_fields = ('id',)

        def create(self, validated_data):
            password = validated_data.pop('password')
            user = CafeStaffModel(**validated_data)
            user.set_password(password)
            user.save()
            return user