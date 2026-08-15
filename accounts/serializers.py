from rest_framework import serializers
from .models import CafeModel, CafeStaffModel, CafeMembership


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeModel
        fields = ['id', 'name', 'slug', 'logo', 'primary_color', 'cover_image']
        read_only_fields = ('id', 'slug')


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CafeModel
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'phone_number', 'national_code', 'address', 'province', 'city', 'gender',
        ]
        extra_kwargs = {
            "first_name": {'required': True},
            "last_name": {'required': True},
            "phone_number": {'required': True},
            "national_code": {'required': True},
            "address": {'required': True},
            "province": {'required': True},
            "city": {'required': True},
            "gender": {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CafeStaffModel(**validated_data)
        user.set_password(password)
        user.save()
        return user

class StaffCreateSerializer(SignupSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=CafeMembership.StaffRole.choices)

    class Meta:
        model = CafeStaffModel
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'role', 'gender']

    def validate_role(self, value):
        creator = self.context['request'].user
        creator_role = self.context['creator_role']

        allowed = {
            CafeMembership.StaffRole.MANAGER: {CafeMembership.StaffRole.ADMIN, CafeMembership.StaffRole.STAFF},
            CafeMembership.StaffRole.ADMIN: {CafeMembership.StaffRole.STAFF},
        }

        if value not in allowed.get(creator_role, set()):
            raise serializers.ValidationError("Role must be one of {}".format(allowed.get(creator_role)))
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        cafe = self.context['cafe']

        user = CafeStaffModel(**validated_data)
        user.set_password(password)
        user.save()

        CafeMembership.objects.create(user=user, cafe=cafe, role=role)
        return user


class CafeMembershipSerializer(serializers.ModelSerializer):
    cafe_name = serializers.CharField(source="cafe.name", read_only=True)

    class Meta:
        model = CafeMembership
        fields = ["id", "cafe", "cafe_name", "role", "created_at"]