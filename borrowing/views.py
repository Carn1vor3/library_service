from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingSerializer, BorrowingDetailSerializer


class ListBorrowingsView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer


class CreateBorrowingsView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class RetrieveBorrowingView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
