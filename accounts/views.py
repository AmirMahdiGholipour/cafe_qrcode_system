from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignupSerializer
from django.db import transaction
from .models import CafeMembership
from .serializers import CafeSerializer
from rest_framework.generics import get_object_or_404
from .models import CafeModel
from .serializers import StaffCreateSerializer, StaffOutSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(SignupSerializer(user).data, status=status.HTTP_201_CREATED)

class CafeAddView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = CafeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            cafe = serializer.save()
            CafeMembership.objects.create(
                user=request.user,
                cafe=cafe,
                role=CafeMembership.StaffRole.MANAGER,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StaffAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cafe_id):
        cafe = get_object_or_404(CafeModel, id=cafe_id)

        membership = CafeMembership.objects.filter(user=request.user, cafe=cafe).first()
        if membership is None or membership.role == CafeMembership.StaffRole.STAFF:
            return Response(
                {"detail": "شما اجازه‌ی افزودن کارمند در این کافه را ندارید."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = StaffCreateSerializer(
            data=request.data,
            context={"request": request, "creator_role": membership.role, "cafe": cafe},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(StaffOutSerializer(user).data, status=status.HTTP_201_CREATED)
