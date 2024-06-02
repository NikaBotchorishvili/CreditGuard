from cards.models import Card
from django_filters import FilterSet # type: ignore

class CardFilter(FilterSet):
    class Meta:
        model = Card
        fields = ['title']