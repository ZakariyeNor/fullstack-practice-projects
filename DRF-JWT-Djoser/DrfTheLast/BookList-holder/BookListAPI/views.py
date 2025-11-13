from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

@api_view(['POST', 'GET'])
def books(request):
    if request.method == 'GET':
        return Response('Get list of the books', status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response('Post list of the books', status=status.HTTP_200_OK)

class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if(author):
            return Response({'message': 'Get list of the books by' + author}, status=status.HTTP_200_OK)
        return Response({'message': 'Get list of the books by'}, status=status.HTTP_200_OK)
    def post(self, request):
        return Response('Post list of the books', status=status.HTTP_200_OK)
      
