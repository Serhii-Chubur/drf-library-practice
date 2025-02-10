from django.urls import include, path
from book.views import BookViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"books", BookViewSet, basename="books")
app_name = "book"

urlpatterns = [path("", include(router.urls))]
