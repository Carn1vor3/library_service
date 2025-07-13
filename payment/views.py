from rest_framework import viewsets
from payment.models import Payment
from payment.permissions import PaymentPermission
from payment.serializers import PaymentDetailSerializer, PaymentSerializer


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