from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, PositiveSmallIntegerField, CharField, TextChoices, DateTimeField



class CardValue(Model):

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
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.id} {self.value}-{self.color}"


    class Meta:
        unique_together = ("color", "value")
        app_label = "blind_stack_app"
        verbose_name = "Valeur des Cartes"
        verbose_name_plural = "Valeurs des cartes"
