from typing import Self
from django.db.models import Model, DateTimeField, ForeignKey, CASCADE, CheckConstraint, Q, F, BooleanField
from blind_stack_app.models.bot import Bot
from blind_stack_app.models.player import Player



class GameRound(Model):
    player_1 = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_one",
        verbose_name="Players", help_text="Player One of the GameRound",
    )
    player_2 = ForeignKey(
        to=Bot, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_two",
        verbose_name="Players", help_text="Player Two of the GameRound (Bot)",
    )
    player_3 = ForeignKey(
        to=Bot, on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_player_three",
        verbose_name="Players", help_text="Player Three of the GameRound (Bot)",
    )
    player_4 = ForeignKey(
        to=Bot, on_delete=CASCADE,
        blank=True, null=True,
        related_name="game_as_player_four",
        verbose_name="Players", help_text="Player Four of the GameRound (Bot)",
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
                    ~Q(player_2=F("player_3")) &  # le bot 2 doit être différent du 3
                    (
                        Q(player_4__isnull=True) |  # le bot 4 n'est pas présent (ou)
                            (
                                ~Q(player_2=F("player_4")) &  # le bot 2 doit être différent du 4
                                ~Q(player_3=F("player_4"))    # le bot 3 doit être différent du 4
                            )
                    )
                ),
                name="unique_bots_in_game_round"
            )
        ]


    @property
    def active_players(self) -> list["Player"]:
        all_possible_players: list["Player" | "Bot"] = [self.player_1, self.player_2, self.player_3, self.player_4]
        return list(filter(lambda player: player is not None, all_possible_players))


    def add_cards(self) -> Self:
        from blind_stack_app.models.card import Card
        if self.cards.all().count() > 0:
            return self
        Card.objects.generate_cards_of_game_round(game_round=self)
        return self


    def add_stacks(self) -> Self:
        from blind_stack_app.models.stack import Stack
        if self.stacks.all().count() > 0:
            return self
        Stack.objects.generate_stacks_of_game_round(game_round=self)
        return self


    def shuffle_cards(self) -> Self:
        if self.cards and self.cards.filter(order_in_deck__isnull=False).exists():
            return self
        self.cards.shuffle_cards(game_round=self)
        return self


    def distribute_cards(self) -> Self:
        from blind_stack_app.models import Card
        if self.cards and self.cards.filter(player__isnull=False).exists():
            return self
        Card.objects.distribute_cards(game_round=self)
        return self
