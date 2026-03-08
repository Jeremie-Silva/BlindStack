from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, PositiveSmallIntegerField, CharField, TextChoices, DateTimeField, CheckConstraint, Q
from blind_stack_app.querysets import CardValueQuerySet



CARD_VALUE_MIN: int = 1
CARD_VALUE_MAX: int = 12



class CardValue(Model):
    CARD_VALUE_MIN: int = CARD_VALUE_MIN
    CARD_VALUE_MAX: int = CARD_VALUE_MAX

    class Color(TextChoices):
        BLACK = "Black", "Noir"
        WHITE = "White", "Blanc"

    color = CharField(
        choices=Color.choices,
        max_length=12,
        blank=False, null=False,
        verbose_name="Colors", help_text="Color of the card",
    )
    value = PositiveSmallIntegerField(
        blank=False, null=False,
        validators=[MinValueValidator(CARD_VALUE_MIN), MaxValueValidator(CARD_VALUE_MAX)],
        verbose_name="Values", help_text="Value of the card",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = CardValueQuerySet.as_manager()


    def __str__(self):
        return f"{self.id} {self.value}-{self.color}"


    class Meta:
        unique_together = ("color", "value")
        app_label = "blind_stack_app"
        verbose_name = "Valeur des Cartes"
        verbose_name_plural = "Valeurs des cartes"
        constraints = [
            CheckConstraint(
                condition=Q(value__gte=CARD_VALUE_MIN) & Q(value__lte=CARD_VALUE_MAX),
                name="check_card_value"
            )
        ]
