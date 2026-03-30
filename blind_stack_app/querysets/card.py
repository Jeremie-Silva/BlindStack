from random import shuffle
from typing import TYPE_CHECKING
from django.db.models import QuerySet


if TYPE_CHECKING:
    from blind_stack_app.models import Card



class CardsQuerySet(QuerySet):
    def shuffle_cards(self) -> QuerySet["Card"]:
        deck_positions: list[int] = list(range(1, self.count() + 1))
        shuffle(deck_positions)
        for position, card in zip(deck_positions, self.all()):
            card.order_in_deck = position
            card.save()
        return self
