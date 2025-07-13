from django.utils import timezone  # Правильний timezone для Django
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.permissions import BorrowingPermissions
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingListAdminSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = (BorrowingPermissions,)

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)

            user_id = self.request.query_params.get("user_id")
            if self.request.user.is_staff and user_id:
                user_ids = [int(uid) for uid in user_id.split(",") if uid.isdigit()]
                queryset = queryset.filter(user_id__in=user_ids)

            is_active = self.request.query_params.get("is_active")
            if is_active is not None:
                if is_active.lower() in ["true", "1"]:
                    queryset = queryset.filter(actual_return_date__isnull=True)
                elif is_active.lower() in ["false", "0"]:
                    queryset = queryset.filter(actual_return_date__isnull=False)
        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListAdminSerializer if self.request.user.is_staff else BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingListSerializer

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(BorrowingPermissions,),
        url_path="return",
    )
    def return_borrowing(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response(
            {"status": "Book returned successfully"},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type=int,
                description="The ID of the user who borrowed",
            ),
            OpenApiParameter(
                "is_active",
                type=bool,
                description="Whether the borrowing is active",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """List of all borrowings"""
        return super().list(request, *args, **kwargs)
