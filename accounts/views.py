from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserMeSerializer


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        display_name = request.data.get("display_name")
        if display_name is not None:
            profile.display_name = display_name
            profile.save(update_fields=["display_name"])
        return Response(UserMeSerializer(user).data)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(UserMeSerializer(user).data, status=status.HTTP_201_CREATED)
