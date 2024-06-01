from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.routers import DefaultRouter
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from cards.serializers import CardSerializer, CreateCardSerializer
from config.serializers import ErrorResponseSerializer
from rest_framework.permissions import IsAuthenticated
from cards.models import Card
from rest_framework.request import Request

@extend_schema_view(
    CreateNewCard=extend_schema(
        request=CreateCardSerializer,
        responses={201: CardSerializer, 400: ErrorResponseSerializer}
    ),
    RetrieveCardsByUser=extend_schema(
        request=None,
        responses={200: CardSerializer(many=True)}
    )
)
class CardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(methods=['post'], detail=False, url_path='create', url_name='create-new-card')
    def CreateNewCard(self, request: Request):
        serializer = CreateCardSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            card_number = request.data["card_number"]
            title = request.data["title"]
            isValidCreditCard = serializer["isValid"].value
            newCard = Card.objects.create(
                user=user,
                title=title,
                censoredNumber=card_number,
                isValid=isValidCreditCard
            )
            try:
                newCard.save()
            except Exception as e:
                return Response(data={"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            serializedCard = CardSerializer(newCard)
            return Response(data=serializedCard.data, status=status.HTTP_201_CREATED)            
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['get'], detail=False, url_path='', url_name='retrieve-all-cards')
    def RetrieveCardsByUser(self, request):
        user = request.user
        cards = Card.objects.filter(user=user)
        serializedCards = CardSerializer(cards, many=True)
        return Response(data=serializedCards.data, status=status.HTTP_200_OK)
    
    
router = DefaultRouter()
router.register(r'cards', CardViewSet, basename='cards')