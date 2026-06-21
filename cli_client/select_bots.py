from beaupy import select_multiple
from blind_stack_app.models import Bot



def cli_select_bots() -> list[Bot]:
    return select_multiple(options=Bot.objects.unlocked(), minimal_count=3, maximal_count=3)