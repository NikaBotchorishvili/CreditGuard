from django.contrib.admin import register, ModelAdmin
from cards.models import Card


@register(Card)
class Card(ModelAdmin):
    list_display = ["user", "title", "censoredNumber", "isValid", "created_at"]
