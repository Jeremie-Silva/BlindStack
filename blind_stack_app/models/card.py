from django.db.models import Model, PositiveSmallIntegerField, DateTimeField, ForeignKey, CASCADE
from blind_stack_app.models.stack import Stack
from blind_stack_app.models.game_round import GameRound
from blind_stack_app.models.player import Player
from blind_stack_app.models.card_value import CardValue
from blind_stack_app.querysets import CardsQuerySet



class Card(Model):
    value = ForeignKey(
        to=CardValue, on_delete=CASCADE,
        blank=False, null=False,
        related_name="cards",
        verbose_name="Cards", help_text="Cards of the GameRound",
    )
    player = ForeignKey(
        to=Player, on_delete=CASCADE,
        blank=True, null=True,
        related_name="cards",
        verbose_name="Players", help_text="Players of the GameRound",
    )
    stack = ForeignKey(
        to=Stack, on_delete=CASCADE,
        blank=True, null=True,
        related_name="cards",
        verbose_name="Stacks", help_text="Players of the GameRound",
    )
    game_round = ForeignKey(
        to=GameRound, on_delete=CASCADE,
        blank=False, null=False,
        related_name="cards",
        verbose_name="GameRounds", help_text="GameRound",
    )
    order_in_stack = PositiveSmallIntegerField(
        blank=True, null=True,
        verbose_name="Orders in Stack", help_text="Order of the Card in the Stack",
    )
    order_in_deck = PositiveSmallIntegerField(
        blank=True, null=True,
        verbose_name="Orders in Deck", help_text="Order of the Card in the Deck",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects: CardsQuerySet = CardsQuerySet.as_manager()

    def __str__(self):
        return f"{self.id=} {self.value}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Carte"
        verbose_name_plural = "Cartes"
