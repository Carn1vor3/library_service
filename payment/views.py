from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from borrowing.models import Borrowing
from library_service import settings
from payment.models import Payment
from payment.permissions import PaymentPermission
from payment.serializers import PaymentDetailSerializer, PaymentSerializer
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = (PaymentPermission,)

    def get_queryset(self):
        qs = Payment.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(borrowing__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentSerializer
        elif self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer


def success_view(request):
    return HttpResponse("Thank you fo purchasing! ✅")


def cancel_view(request):
    return HttpResponse("You declined the payment ❌")


@csrf_exempt
def create_checkout_session(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    borrowing_id = request.POST.get("borrowing_id")
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)

    amount_cents = 2000

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": f"Payment fo borrowing №{borrowing.id}",
                    },
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/api/success/",
        cancel_url="http://localhost:8000/api/cancel/",
    )

    Payment.objects.create(
        status=Payment.Status.PENDING,
        type=Payment.Type.PAYMENT,
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=amount_cents / 100,
    )

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        try:
            payment = Payment.objects.get(session_id=session["id"])
            payment.status = Payment.Status.PAID
            payment.save()
            print(f"Payment {payment.id} marked as PAID")
        except Payment.DoesNotExist:
            print("Payment with session_id not found")

    return HttpResponse(status=200)


def index(request):
    borrowing = Borrowing.objects.first()
    return render(request, "index.html", {"borrowing": borrowing})
