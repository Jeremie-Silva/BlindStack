import questionary
import typer
from enum import Enum
from blind_stack_app.models import Player, GameRound
from cli_client.select_player import cli_select_player
from cli_client.start_new_game_round import cli_start_new_game_round



logo: str = """
    $$$$$$$\  $$\       $$$$$$\ $$\   $$\ $$$$$$$\   $$$$$$\ $$$$$$$$\  $$$$$$\   $$$$$$\  $$\   $$\ 
    $$  __$$\ $$ |      \_$$  _|$$$\  $$ |$$  __$$\ $$  __$$\\__$$  __|$$  __$$\ $$  __$$\ $$ | $$  |
    $$ |  $$ |$$ |        $$ |  $$$$\ $$ |$$ |  $$ |$$ /  \__|  $$ |   $$ /  $$ |$$ /  \__|$$ |$$  / 
    $$$$$$$\ |$$ |        $$ |  $$ $$\$$ |$$ |  $$ |\$$$$$$\    $$ |   $$$$$$$$ |$$ |      $$$$$  /  
    $$  __$$\ $$ |        $$ |  $$ \$$$$ |$$ |  $$ | \____$$\   $$ |   $$  __$$ |$$ |      $$  $$<   
    $$ |  $$ |$$ |        $$ |  $$ |\$$$ |$$ |  $$ |$$\   $$ |  $$ |   $$ |  $$ |$$ |  $$\ $$ |\$$\  
    $$$$$$$  |$$$$$$$$\ $$$$$$\ $$ | \$$ |$$$$$$$  |\$$$$$$  |  $$ |   $$ |  $$ |\$$$$$$  |$$ | \$$\ 
    \_______/ \________|\______|\__|  \__|\_______/  \______/   \__|   \__|  \__| \______/ \__|  \__|
"""



class Action(Enum):
    JOUER = "JOUER"
    QUITTER = "QUITTER"



def cli_application() -> None:
    typer.echo(logo)
    typer.echo("Bienvenue dans le jeu BlindStack !")

    while True:
        input_choice: Action = questionary.select(
            message="Qu'est-ce que vous voulez faire?",
            choices=[Action.JOUER.value, Action.QUITTER.value],
        ).ask()

        if response == Action.JOUER.value:
            pass
        elif response == Action.QUITTER.value:
        if input_choice == Action.JOUER.value:
            player: Player = cli_select_player()
            game_round: GameRound = cli_start_new_game_round(player=player)
        elif input_choice == Action.QUITTER.value:
            break
        else:
            typer.echo("Action inconnue")

    typer.echo("À bientôt !")
