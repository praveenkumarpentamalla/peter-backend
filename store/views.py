from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import products_table
import uuid

class ProductList(APIView):
    def get(self, request):
        response = products_table.scan()
        return Response(response.get('Items', []))
    
    def post(self, request):
        product_id = str(uuid.uuid4())
        item = {
            'product_id': product_id,
            'name': request.data.get('name'),
            'price': str(request.data.get('price')),
            'description': request.data.get('description', ''),
            'image_url': request.data.get('image_url', ''),
        }
        products_table.put_item(Item=item)
        return Response(item, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, product_id):
        response = products_table.get_item(Key={'product_id': product_id})
        return Response(response.get('Item', {}))
    
    def put(self, request, product_id):
        item = {
            'product_id': product_id,
            'name': request.data.get('name'),
            'price': str(request.data.get('price')),
            'description': request.data.get('description', ''),
            'image_url': request.data.get('image_url', ''),
        }
        products_table.put_item(Item=item)
        return Response(item)
    
    def delete(self, request, product_id):
        products_table.delete_item(Key={'product_id': product_id})
        return Response(status=status.HTTP_204_NO_CONTENT)