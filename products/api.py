from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from products.models import Item
from products.serializers import ItemSerializer , CreateItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , IsAdminUser
class ItemListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class CreateItem(APIView):
    permission_classes = (IsAdminUser,)
    
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404
    def post(self , request):
        
        serializer = CreateItemSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def get(self, request, format=None):
    #     qs = Item.objects.all()
    #     serializer = ItemSerializer(qs, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     item = self.get_object(pk)
    #     serializer = CreateItemSerializer(item, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        if item is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        print(item)
        # Extract the specific parameter you want to update
        parameter_to_update = request.data.get('parameter_name')
        # print(parameter_to_update)
        for attr, value in request.data.items():
            if hasattr(item, attr):
                setattr(item, attr, value)

        item.save()
        serializer = CreateItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
# class ItemDetailView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = ItemDetailSerializer
#     queryset = Item.objects.all()
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)