from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)


# Create your views here.
class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="first_name", type=str, required=False),
            OpenApiParameter(name="last_name", type=str, required=False),
            OpenApiParameter(name="email", type=str, required=True),
            OpenApiParameter(name="password", type=str, required=True),
        ]
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a new user.

        This method handles the HTTP POST request to create a new user
        using the provided data in the request.

        Parameters:
            request (Request): The HTTP request object containing the data
                for the new user creation.

        Returns:
            Response: The HTTP response with the details of the created user.
        """

        return self.create(request, *args, **kwargs)


class ManageUser(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        Retrieves the details of the currently authenticated user.

        Returns:
            Response: The HTTP response with the details of the currently
                authenticated user.
        """
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="first_name", type=str, required=True),
            OpenApiParameter(name="last_name", type=str, required=True),
            OpenApiParameter(name="email", type=str, required=True),
            OpenApiParameter(name="password", type=str, required=True),
        ]
    )
    def put(self, request, *args, **kwargs):
        """
        Updates the details of the currently authenticated user.

        Parameters:
            request (Request): The HTTP request object containing the data to
                update the user's details.

        Returns:
            Response: The HTTP response with the updated details of the user.
        """

        return self.update(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="first_name", type=str, required=False),
            OpenApiParameter(name="last_name", type=str, required=False),
            OpenApiParameter(name="email", type=str, required=False),
            OpenApiParameter(name="password", type=str, required=False),
        ]
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially updates the details of the currently authenticated user.

        Parameters:
            request (Request): The HTTP request object containing the data to
                partially update the user's details.

        Returns:
            Response: The HTTP response with the updated details of the user.
        """
        return self.partial_update(request, *args, **kwargs)
