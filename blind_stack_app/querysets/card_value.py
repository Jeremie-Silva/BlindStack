from typing import TYPE_CHECKING
from django.db.models import QuerySet


if TYPE_CHECKING:
    from blind_stack_app.models import CardValue



class CardValueQuerySet(QuerySet):
    def generate_all_cards_values(self) -> QuerySet["CardValue"]:
        if self.all().count() > 0:
            return self
        for color in self.model.Color.values:
            for value in range(self.model.CARD_VALUE_MIN, self.model.CARD_VALUE_MAX + 1):
                self.create(color=color, value=value)
        return self
