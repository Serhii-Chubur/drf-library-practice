from django.urls import path
from borrowing.views import (
    BorrowingDetailAPIView,
    BorrowingListCreateAPIView,
    return_book,
)


urlpatterns = [
    path("", BorrowingListCreateAPIView.as_view(), name="borrowing_list"),
    path(
        "<int:pk>/", BorrowingDetailAPIView.as_view(), name="borrowing_detail"
    ),
    path("<int:pk>/return/", return_book, name="return_book"),
]

app_name = "borrowing"
