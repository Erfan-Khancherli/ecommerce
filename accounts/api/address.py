from django_countries import countries
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Address
from accounts.serializers import AddressSerializer
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin
class CountryListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(countries, status=HTTP_200_OK)


class AddressListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        print(self.request.query_params)
        address_type = self.request.query_params.get('address_type', None)
        qs = Address.objects.all().filter(user = self.request.user)
        if address_type is None:
            return qs
        return qs.filter(address_type=address_type)


class AddressCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    def post(self , request):
        serializer =AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
class AddressUpdateView(UpdateAPIView , UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data , status=status.HTTP_200_OK)


class AddressDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Address.objects.all()
