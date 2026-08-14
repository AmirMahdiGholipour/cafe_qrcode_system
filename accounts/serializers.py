from rest_framework import serializers
from models import CafeModel


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeModel
        fields = ['id', 'name', 'slug', 'logo', 'primary_color', 'cover_image']
        read_only_fields = ('id', 'slug')


class CafeBrandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeModel
        fields = ['name', 'logo', 'cover_image', 'primary_color']