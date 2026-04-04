from typing import TYPE_CHECKING, Self
from django.db.models import QuerySet


if TYPE_CHECKING:
    from blind_stack_app.models import GameRound



class StackQuerySet(QuerySet):
    def generate_stacks_of_game_round(self, game_round: "GameRound") -> Self:
        from blind_stack_app.models.stack import STACK_RANK_MIN, STACK_RANK_MAX
        for rank in range(STACK_RANK_MIN, STACK_RANK_MAX + 1):
            self.create(rank=rank, game_round=game_round)
        return self
