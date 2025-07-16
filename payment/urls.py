from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment import views
from payment.views import PaymentViewSet, index

app_name = "payment"

router = DefaultRouter()
router.register("payment", PaymentViewSet, basename="payment")

urlpatterns = [
    path("index/", index, name="index"),
    path("", include(router.urls)),
    path(
        "create-checkout-session/",
        views.create_checkout_session,
        name="create-checkout-session",
    ),
    path("success/", views.success_view, name="success"),
    path("cancel/", views.cancel_view, name="cancel"),
    path("webhook/", views.stripe_webhook, name="stripe-webhook"),
]
