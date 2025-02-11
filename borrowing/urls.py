from django.urls import include, path
from borrowing.views import (
    BorrowingDetailAPIView,
    BorrowingListAPIView,
    return_book,
)

from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r"", BorrowingAPIView.as_view(), basename="borrowings")

urlpatterns = [
    path("", BorrowingListAPIView.as_view(), name="borrowing_list"),
    path(
        "<int:pk>/", BorrowingDetailAPIView.as_view(), name="borrowing_detail"
    ),
    path("<int:pk>/return/", return_book, name="return_book"),
]

app_name = "borrowing"
