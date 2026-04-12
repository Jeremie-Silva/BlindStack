import questionary
from blind_stack_app.models import Bot



def cli_select_bots() -> list[Bot]:
    return questionary.checkbox(
        message="Veuillez sélectionner des bots",
        choices=[questionary.Choice(title=str(bot), value=bot) for bot in Bot.objects.unlocked().all()],
        validate=lambda x: len(x) == 3
    ).ask()
