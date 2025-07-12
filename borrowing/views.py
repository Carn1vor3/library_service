from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingSerializer, BorrowingDetailSerializer


class ListBorrowingsView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related("book", "user")


class CreateBorrowingsView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)


class RetrieveBorrowingView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)
