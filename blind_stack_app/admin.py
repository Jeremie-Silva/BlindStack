from django.contrib.admin import register, ModelAdmin, TabularInline
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action
from blind_stack_app.models import CardValue, Player, GameRound, Card, Stack


@register(CardValue)
class CardValueAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "value", "color", "created_at", "updated_at",)
    search_fields = ("pk", "value", "color", "created_at", "updated_at",)
    list_filter = ("color", "value",)

    @action(label="Générer toutes les valeurs de cartes possibles", description="Création initiale")
    def generate_all_cards_values(self, request: HttpRequest, queryset: QuerySet[CardValue]):
        return CardValue.objects.generate_all_cards_values()

    changelist_actions = ("generate_all_cards_values",)



@register(Player)
class PlayerAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "username", "user", "created_at", "updated_at",)
    search_fields = ("pk", "username", "user", "created_at", "updated_at",)
    list_filter = ("user", "username",)



class CardInline(TabularInline):
    model = Card
    extra = 0



class StackInline(TabularInline):
    model = Stack
    extra = 0



@register(GameRound)
class GameRoundAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "completed", "player_1", "player_2", "player_3", "player_4", "created_at", "updated_at",)
    search_fields = ("pk", "completed", "player_1", "player_2", "player_3", "player_4", "created_at", "updated_at",)
    list_filter = ("completed", "player_1", "player_2", "player_3", "player_4",)
    inlines = [CardInline, StackInline]

    @action(label="1 - Générer les cartes", description="Création de toutes les cartes de la partie")
    def add_cards(self, request: HttpRequest, obj: GameRound):
        return obj.add_cards()

    @action(label="2 - Générer les piles", description="Création de toutes les piles de la partie")
    def add_stacks(self, request: HttpRequest, obj: GameRound):
        return obj.add_stacks()

    @action(label="3 - Mélanger les cartes", description="Mélanger toutes les cartes de la partie")
    def shuffle_cards(self, request: HttpRequest, obj: GameRound):
        return obj.shuffle_cards()

    @action(label="4 - Distribuer les cartes", description="Distribuer toutes les cartes de la partie")
    def distribute_cards(self, request: HttpRequest, obj: GameRound):
        return obj.distribute_cards()

    change_actions = ("add_cards", "add_stacks", "shuffle_cards", "distribute_cards")



@register(Card)
class CardAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "value", "player", "stack", "game_round_id", "order_in_deck", "order_in_stack", "created_at", "updated_at",)
    search_fields = ("pk", "value", "player", "stack", "game_round_id", "order_in_deck", "order_in_stack", "created_at", "updated_at",)
    list_filter = ("value", "player", "stack", "game_round_id", "order_in_deck", "order_in_stack",)



@register(Stack)
class StackAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "rank", "game_round_id", "created_at", "updated_at",)
    search_fields = ("pk", "rank", "game_round_id", "created_at", "updated_at",)
    list_filter = ("rank", "game_round_id",)

