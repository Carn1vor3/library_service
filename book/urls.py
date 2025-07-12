from django.urls import include, path
from rest_framework.routers import DefaultRouter

from book import views

app_name = "book"
router = DefaultRouter()
router.register("books", views.BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
