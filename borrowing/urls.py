from django.urls import path
from borrowing.views import (
    BorrowingDetailAPIView,
    BorrowingListCreateAPIView,
    return_book,
)


urlpatterns = [
    path("", BorrowingListCreateAPIView.as_view(), name="borrowing-list"),
    path(
        "<int:pk>/", BorrowingDetailAPIView.as_view(), name="borrowing-detail"
    ),
    path("<int:pk>/return/", return_book, name="return-book"),
]

app_name = "borrowing"
