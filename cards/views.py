from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from . models import Card
from . serializers import CardSerializer

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def card_list_create(request):

    if request.method == 'GET':
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def card_detail(request, pk):
    try:
        card = Card.objects.get(pk=pk, user=request.user)
    except Card.DoesNotExist:
        return Response({'errors': 'card not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        card.delete()
        return Response({'message': 'card deleted'}, status=status.HTTP_204_NO_CONTENT)


