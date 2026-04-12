from django.db.models import Model, CharField, DateTimeField, BooleanField
from blind_stack_app.querysets import BotQuerySet



class Bot(Model):
    username = CharField(
        max_length=30,
        blank=False, null=False,
        verbose_name="Pseudos", help_text="Pseudo"
    )
    is_unlocked = BooleanField(
        default=False, blank=False, null=False,
        verbose_name="Is unlocked", help_text="Is unlocked ?"
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = BotQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} {self.username}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Bot"
        verbose_name_plural = "Bots"
