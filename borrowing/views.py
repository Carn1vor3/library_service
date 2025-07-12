from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer, BorrowingListAdminSerializer,
)


class ListBorrowingsView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        queryset = Borrowing.objects.select_related("book", "user")

        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                user_ids = [int(uid) for uid in user_id.split(",") if uid.isdigit()]
                queryset = queryset.filter(user_id__in=user_ids)
        else:
            queryset = queryset.filter(user=self.request.user)

        if is_active is not None:
            if is_active.lower() in ["true", "1"]:
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() in ["false", "0"]:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return BorrowingListAdminSerializer
        else:
            return BorrowingListSerializer


class CreateBorrowingsView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAuthenticated,)


class RetrieveBorrowingView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)
