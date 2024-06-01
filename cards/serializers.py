from rest_framework.serializers import ModelSerializer, ValidationError, CharField, IntegerField
from cards.models import Card

class CardSerializer(ModelSerializer):
    card_number = CharField(write_only=True)
    ccv = IntegerField(write_only=True)

    class Meta:
        model = Card
        fields = ["id", "user", "title", "censoredNumber", "isValid", "created_at"]
        
    def validate_cvv(self, value):
        if value < 100 or value > 999:
            raise ValidationError("CVV must be a 3 digit number")
        return value

    def validate_card_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise ValidationError("Card number must be 16 digits")
        return value
    
    def validate(self, data: dict):
        cardNumber = data.get('card_number')
        cvv = data.get('cvv')
        pairs = [(int(cardNumber[i:i+2]), int(cardNumber[i+2:i+4])) for i in range(0, 16, 4)]
        
        for x, y in pairs:
            if pow(x, pow(y, 3), cvv) % 2 == 0:
                data["isValid"] = True
                return data
        data["isValid"] = False
        return data
    
    def create(self, validated_data):
        card_number = validated_data.pop('card_number')

        censoredNumber = card_number[:4] + "****" + card_number[-4:]
        validated_data["censoredNumber"] = censoredNumber
        return super().create(validated_data)