from rest_framework.serializers import ModelSerializer, Serializer, ValidationError, CharField, IntegerField, BooleanField
from cards.models import Card

class CreateCardSerializer(Serializer):
    title = CharField(max_length=100)
    card_number = CharField(write_only=True, max_length=16)
    ccv = IntegerField(write_only=True)
    isValid = BooleanField(read_only=True)
    def validate_ccv(self, value):
        if value < 100 or value > 999:
            raise ValidationError("CVV must be a 3 digit number")
        return value

    def validate_card_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise ValidationError("Card number must be 16 digits")
        return value
    
    def validate(self, data: dict):
        cardNumber = data.get('card_number')
        cvv = data.get('ccv')
        pairs = [(int(cardNumber[i:i+2]), int(cardNumber[i+2:i+4])) for i in range(0, 16, 4)]
        
        for x, y in pairs:
            if pow(x, pow(y, 3), cvv) % 2 != 0:
                data["isValid"] = False
                return data
        data["isValid"] = True
        return data
    
class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ["id", "user", "title", "censoredNumber", "isValid", "created_at"]
        read_only_fields = ['user', 'censored_number', 'is_valid', 'created_at']