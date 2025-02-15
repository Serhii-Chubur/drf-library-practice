from django.urls import include, path
from book.views import BookViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"", BookViewSet, basename="books")

urlpatterns = [path("", include(router.urls))]

app_name = "book"
