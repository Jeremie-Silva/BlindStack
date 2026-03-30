from typing import Self
from django.db.models import Model, DateTimeField, ForeignKey, CASCADE, CheckConstraint, Q, F, BooleanField
from blind_stack_app.models.player import Player



class GameRound(Model):
    player_1 = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_one",
        verbose_name="Players", help_text="Player One of the GameRound",
    )
    player_2 = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_two",
        verbose_name="Players", help_text="Player Two of the GameRound",
    )
    player_3 = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_three",
        verbose_name="Players", help_text="Player Three of the GameRound",
    )
    player_4 = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=True, null=True,
        related_name="game_as_player_four",
        verbose_name="Players", help_text="Player Four of the GameRound",
    )
    completed = BooleanField(
        default=False,
        blank=False, null=False,
        verbose_name="Completeds", help_text="The GameRound is completed ?",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.id} {self.completed} {self.player_1}-{self.player_2}-{self.player_3}-{self.player_4} {self.created_at}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Partie de jeu"
        verbose_name_plural = "Parties de jeu"
        constraints = [
            CheckConstraint(
                condition=(
                    ~Q(player_1=F("player_2")) &  # le joueur 1 doit être différent du 2
                    ~Q(player_1=F("player_3")) &  # le joueur 1 doit être différent du 3
                    ~Q(player_2=F("player_3")) &  # le joueur 2 doit être différent du 3
                    (
                        Q(player_4__isnull=True) |  # le joueur 4 n'est pas présent (ou)
                            (
                                ~Q(player_1=F("player_4")) &  # le joueur 4 est différent du 1
                                ~Q(player_2=F("player_4")) &  # le joueur 4 est différent du 2
                                ~Q(player_3=F("player_4"))    # le joueur 4 est différent du 3
                            )
                    )
                ),
                name="unique_players_in_game_round"
            )
        ]


    def add_cards(self) -> Self:
        from blind_stack_app.models.card import Card
        from blind_stack_app.models.card_value import CardValue
        if self.cards.all().count() > 0:
            return self
        for card_value in CardValue.objects.all():
            self.cards.add(Card.objects.create(value=card_value, game_round=self))
        return self


    def add_stacks(self) -> Self:
        from blind_stack_app.models.stack import Stack
        if self.stacks.all().count() > 0:
            return self
        for rank in range(Stack.STACK_RANK_MIN, Stack.STACK_RANK_MAX + 1):
            self.stacks.add(Stack.objects.create(rank=rank, game_round=self))
        return self


    def shuffle_cards(self) -> Self:
        if self.cards.filter(order_in_deck__isnull=False).exists():
            return self
        self.cards.shuffle_cards()
        return self

# TODO: distribuer les cartes
