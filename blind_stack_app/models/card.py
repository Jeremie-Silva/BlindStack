from django.db.models import Model, PositiveSmallIntegerField, CharField, TextChoices
from django.core.validators import MinValueValidator, MaxValueValidator



class Card(Model):

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
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Values", help_text="Value of the card",
    )

    def __str__(self):
        return f"{self.value}-{self.color}"


    class Meta:
        unique_together = ("color", "value")
        app_label = "blind_stack_app"
        verbose_name = "Carte"
        verbose_name_plural = "Cartes"
