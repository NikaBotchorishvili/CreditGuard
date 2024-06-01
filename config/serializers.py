from rest_framework.serializers import Serializer, CharField 

class ErrorResponseSerializer(Serializer):
    detail = CharField()