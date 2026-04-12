from django.db.models import Model, PositiveSmallIntegerField, DateTimeField, ForeignKey, CASCADE
from blind_stack_app.querysets import CardQuerySet



class Card(Model):
    value = ForeignKey(
        to="CardValue", on_delete=CASCADE,
        blank=False, null=False,
        related_name="cards",
        verbose_name="Cards", help_text="Cards of the GameRound",
    )
    participant = ForeignKey(
        to="Participant", on_delete=CASCADE,
        blank=True, null=True,
        related_name="cards",
        verbose_name="Participants", help_text="Participants of the GameRound",
    )
    stack = ForeignKey(
        to="Stack", on_delete=CASCADE,
        blank=True, null=True,
        related_name="cards",
        verbose_name="Stacks", help_text="Players of the GameRound",
    )
    game_round = ForeignKey(
        to="GameRound", on_delete=CASCADE,
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

    objects: CardQuerySet = CardQuerySet.as_manager()


    def __str__(self) -> str:
        return f"{self.id} {self.value}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Carte"
        verbose_name_plural = "Cartes"
