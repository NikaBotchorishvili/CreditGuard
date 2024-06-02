from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.routers import DefaultRouter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from cards.serializers import CardSerializer, CreateCardSerializer
from config.serializers import ErrorResponseSerializer
from rest_framework.permissions import IsAuthenticated
from cards.models import Card
from rest_framework.request import Request
from cards.filters import CardFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


@extend_schema_view(
    CreateNewCard=extend_schema(
        request=CreateCardSerializer,
        responses={201: CardSerializer, 400: ErrorResponseSerializer},
       
    ),
    RetrieveCardsByUser=extend_schema(
        request=None,
        responses={200: CardSerializer(many=True)}
    )
)
class CardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CardFilter
    queryset = Card.objects.none()
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    @action(methods=['post'], detail=False, url_path='create', url_name='create-new-card')
    def CreateNewCard(self, request: Request):
        serializer = CreateCardSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            card_number = request.data["card_number"]
            title = request.data["title"]
            isValidCreditCard = serializer["isValid"].value
            print(isValidCreditCard)
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
    
    
    @action(methods=['get'], detail=False, url_path='byUser', url_name='retrieve-all-cards')
    def RetrieveCardsByUser(self, request):
        user = request.user
        queryset = Card.objects.filter(user=user.id)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        serializedCards = CardSerializer(queryset, many=True)
        return Response(data=serializedCards.data, status=status.HTTP_200_OK)
    

router = DefaultRouter()
router.register(r'', CardViewSet, basename='card')