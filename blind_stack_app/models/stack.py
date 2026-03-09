from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, PositiveSmallIntegerField, DateTimeField, ForeignKey, CASCADE, CheckConstraint, Q
from blind_stack_app.models.game_round import GameRound



STACK_RANK_MIN: int = 1
STACK_RANK_MAX: int = 6



class Stack(Model):
    STACK_RANK_MIN: int = STACK_RANK_MIN
    STACK_RANK_MAX: int = STACK_RANK_MAX

    rank = PositiveSmallIntegerField(
        blank=False, null=False,
        validators=[MinValueValidator(STACK_RANK_MIN), MaxValueValidator(STACK_RANK_MAX)],
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
        constraints = [
            CheckConstraint(
                condition=Q(rank__gte=STACK_RANK_MIN) & Q(rank__lte=STACK_RANK_MAX),
                name="check_stack_rank"
            )
        ]
