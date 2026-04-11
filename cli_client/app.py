import questionary
import typer
from enum import Enum



class Action(Enum):
    JOUER = "JOUER"
    QUITTER = "QUITTER"



def cli_application() -> None:
    typer.echo("Bienvenue dans le jeu BlindStack !")

    while True:
        response: str = questionary.select(
            message="Qu'est-ce que vous voulez faire?",
            choices=[Action.JOUER.value, Action.QUITTER.value],
        ).ask()

        if response == Action.JOUER.value:
            pass
        elif response == Action.QUITTER.value:
            break
        else:
            typer.echo("Action inconnue")

    typer.echo("À bientôt !")
