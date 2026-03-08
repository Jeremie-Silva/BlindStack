from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, PositiveSmallIntegerField, DateTimeField, ForeignKey, CASCADE
from blind_stack_app.models.game_round import GameRound



class Stack(Model):
    rank = PositiveSmallIntegerField(
        blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name="Ranks", help_text="Rank of the stack",
    )
    game_round = ForeignKey(
        to=GameRound, on_delete=CASCADE,
        blank=False, null=False,
        related_name="stacks",
        verbose_name="GameRounds", help_text="GameRound",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.id} {self.rank}-{self.game_round}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Pile de carte"
        verbose_name_plural = "Piles de cartes"
