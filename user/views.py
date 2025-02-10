from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer


# Create your views here.
class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


class ManageUser(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
