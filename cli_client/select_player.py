import questionary
from blind_stack_app.models import Player



def cli_select_player() -> Player:
    while True:
        return questionary.select(
            message="Veuillez sélectionner un joueur",
            choices=[questionary.Choice(title=str(player), value=player) for player in Player.objects.all()],
        ).ask()
