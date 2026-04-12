from blind_stack_app.models import Player, Bot, GameRound



def cli_start_new_game_round(player: Player, bots: list[Bot]) -> GameRound:
    return GameRound.objects.create(
        player_1=player,
        player_2=bots[0],
        player_3=bots[1],
        player_4=bots[2],
    )
