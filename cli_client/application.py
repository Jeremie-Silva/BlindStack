from beaupy import select
from rich.console import Console
from enum import Enum
from blind_stack_app.models import Player, Bot
from cli_client.select_bots import cli_select_bots
from cli_client.select_player import cli_select_player


console = Console()

logo: str = r"""
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
    console.print(logo)
    console.print("Bienvenue dans le jeu BlindStack !")

    while True:
        input_choice: str = select(options=[Action.JOUER.value, Action.QUITTER.value])

        if input_choice == Action.JOUER.value:
            player: Player = cli_select_player()
            bots: list[Bot] = cli_select_bots()
            # TODO: reprendre ici
            # game_round: GameRound = cli_start_new_game_round(player=player, bots=bots)
            # game_round.add_cards()
            # game_round.add_stacks()
            # game_round.shuffle_cards()
            # game_round.distribute_cards()
        elif input_choice == Action.QUITTER.value:
            break

    console.print("À bientôt !")