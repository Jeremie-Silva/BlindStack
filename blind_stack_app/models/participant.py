from django.db.models import Model, ForeignKey, CASCADE, UniqueConstraint, CheckConstraint, Q, DateTimeField
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from blind_stack_app.models import Player, Bot



class Participant(Model):
    player = ForeignKey(
        to="Player", on_delete=CASCADE,
        null=True, blank=True,
        related_name="participations",
        verbose_name="Players", help_text="Players of the GameRound",
    )
    bot = ForeignKey(
        to="Bot", on_delete=CASCADE,
        null=True, blank=True,
        related_name="participations",
        verbose_name="Bots", help_text="Bots of the GameRound",
    )
    game_round = ForeignKey(
        to="GameRound", on_delete=CASCADE,
        null=True, blank=True,
        related_name="participants",
        verbose_name="GameRounds", help_text="Participant of a GameRound",
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.id} {self.player or self.bot}"


    @property
    def owner(self) -> "Player | Bot":
        return self.player or self.bot


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        constraints = [
            UniqueConstraint(fields=["bot", "game_round"], name="unique_bot_per_game_round"),
            UniqueConstraint(fields=["player", "game_round"], name="unique_player_per_game_round"),
            CheckConstraint(
                condition=Q(player__isnull=True) ^ Q(bot__isnull=True),
                name="participant_is_player_or_bot_not_both"
            )
        ]
