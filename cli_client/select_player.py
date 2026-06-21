from beaupy import select
from blind_stack_app.models import Player



def cli_select_player() -> Player:
    return select(options=Player.objects.all())