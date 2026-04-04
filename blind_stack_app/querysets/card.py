from random import shuffle
from typing import TYPE_CHECKING, Self
from django.db.models import QuerySet


if TYPE_CHECKING:
    from blind_stack_app.models import Card, GameRound



class CardQuerySet(QuerySet):
    def shuffle_cards(self) -> Self:
        game_round_ids: QuerySet["Card"] = self.values_list("game_round_id", flat=True).distinct()
        if game_round_ids.count() != 1:
            raise ValueError("All cards must belong to the same GameRound to be shuffled.")
        deck_positions: list[int] = list(range(1, self.count() + 1))
        shuffle(deck_positions)
        for position, card in zip(deck_positions, self.all()):
            card.order_in_deck = position
            card.save()
        return self


    def generate_cards_of_game_round(self, game_round: "GameRound") -> Self:
        from blind_stack_app.models import CardValue
        for card_value in CardValue.objects.all():
            self.create(value=card_value, game_round=game_round)
        return self
