from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.routers import DefaultRouter



class CardViewSet(ViewSet):
    
    @action(methods=['post'], detail=False, url_path='create', url_name='create-new-card')
    def CreateNewCard(self, request):
        pass
    
    @action(methods=['get'], detail=False, url_path='<int:user_id>', url_name='retrieve-all-cards')
    def RetrieveCardsByUser(self, request, user_id):
        pass
    
    
router = DefaultRouter()
router.register(r'cards', CardViewSet, basename='cards')