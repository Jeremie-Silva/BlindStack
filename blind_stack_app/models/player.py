from django.contrib.auth.models import User
from django.db.models import Model, CharField, OneToOneField, PROTECT, DateTimeField



class Player(Model):
    user = OneToOneField(
        to=User, on_delete=PROTECT,
        blank=False, null=False,
        verbose_name="Users", help_text="Utilisateur",
    )
    username = CharField(
        max_length=30,
        blank=False, null=False,
        verbose_name="Pseudos", help_text="Pseudo"
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.id} {self.username}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Joueur"
        verbose_name_plural = "Joueurs"
