from django.contrib.admin import register, ModelAdmin, TabularInline
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action
from blind_stack_app.models import CardValue, Player, GameRound, Card



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



@register(GameRound)
class GameRoundAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("pk", "completed", "player_1", "player_2", "player_3", "player_4", "created_at", "updated_at",)
    search_fields = ("pk", "completed", "player_1", "player_2", "player_3", "player_4", "created_at", "updated_at",)
    list_filter = ("completed", "player_1", "player_2", "player_3", "player_4",)
    inlines = [CardInline]

    @action(label="Générer toutes les cartes de la partie", description="Création des cartes")
    def add_cards(self, request: HttpRequest, obj: GameRound):
        return obj.add_cards()

    change_actions = ("add_cards",)
