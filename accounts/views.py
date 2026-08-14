from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from serializers import CafeSerializer


class CafeView(APIView):
    def post(self, request):
        serializer = CafeSerializer(data=request.data)