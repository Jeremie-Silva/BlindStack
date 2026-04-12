from typing import Self
from django.db.models import Model, DateTimeField, ForeignKey, CASCADE, CheckConstraint, Q, F, BooleanField
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from blind_stack_app.models.participant import Participant



class GameRound(Model):
    participant_1 = ForeignKey(
        to="Participant", on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_participant_one",
        verbose_name="Participants", help_text="Participant One of the GameRound",
    )
    participant_2 = ForeignKey(
        to="Participant", on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_participant_two",
        verbose_name="Participants", help_text="Participant Two of the GameRound",
    )
    participant_3 = ForeignKey(
        to="Participant", on_delete=CASCADE,
        blank=False, null=False,
        related_name="game_as_participant_three",
        verbose_name="Participants", help_text="Participant Three of the GameRound",
    )
    participant_4 = ForeignKey(
        to="Participant", on_delete=CASCADE,
        blank=True, null=True,
        related_name="game_as_participant_four",
        verbose_name="Participants", help_text="Participant Four of the GameRound",
    )
    completed = BooleanField(
        default=False,
        blank=False, null=False,
        verbose_name="Completeds", help_text="The GameRound is completed ?",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.id} {self.completed} {self.participant_1}-{self.participant_2}-{self.participant_3}-{self.participant_4} {self.created_at}"


    class Meta:
        app_label = "blind_stack_app"
        verbose_name = "Partie de jeu"
        verbose_name_plural = "Parties de jeu"
        constraints = [
            CheckConstraint(
                condition=(
                    ~Q(participant_1=F("participant_2")) &  # le participant 1 doit être différent du 2
                    ~Q(participant_1=F("participant_3")) &  # le participant 2 doit être différent du 3
                    ~Q(participant_2=F("participant_3")) &  # le participant 2 doit être différent du 3
                    (
                        Q(participant_4__isnull=True) |  # le participant 4 n'est pas présent (ou)
                            (
                                ~Q(participant_2=F("participant_4")) &  # le participant 2 doit être différent du 4
                                ~Q(participant_3=F("participant_4"))    # le participant 3 doit être différent du 4
                            )
                    )
                ),
                name="unique_participants_in_game_round"
            ),

        ]


    @property
    def active_participants(self) -> list["Participant"]:
        all_possible_participants: list["Participant"] = [self.participant_1, self.participant_2, self.participant_3, self.participant_4]
        return list(filter(None, all_possible_participants))


    def add_cards(self) -> Self:
        from blind_stack_app.models.card import Card
        if self.cards.all().count() > 0:
            return self
        Card.objects.generate_cards_of_game_round(game_round=self)
        return self


    def add_stacks(self) -> Self:
        from blind_stack_app.models.stack import Stack
        if self.stacks.all().count() > 0:
            return self
        Stack.objects.generate_stacks_of_game_round(game_round=self)
        return self


    def shuffle_cards(self) -> Self:
        if self.cards and self.cards.filter(order_in_deck__isnull=False).exists():
            return self
        self.cards.shuffle_cards(game_round=self)
        return self


    def distribute_cards(self) -> Self:
        from blind_stack_app.models import Card
        if self.cards and self.cards.filter(player__isnull=False).exists():
            return self
        Card.objects.distribute_cards(game_round=self)
        return self
