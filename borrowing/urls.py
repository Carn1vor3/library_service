from django.urls import path

from borrowing.views import CreateBorrowingsView, ListBorrowingsView, RetrieveBorrowingView

app_name = "borrowing"

urlpatterns = [
    path("create/", CreateBorrowingsView.as_view(), name="borrowing_create"),
    path("list/", ListBorrowingsView.as_view(), name="borrowing_list"),
    path("<int:pk>/", RetrieveBorrowingView.as_view(), name="borrowing_retrieve"),
]