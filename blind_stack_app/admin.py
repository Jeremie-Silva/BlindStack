from django.contrib.admin import register, ModelAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action
from blind_stack_app.models import CardValue



@register(CardValue)
class CardValueAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ("id", "value", "color",)
    search_fields = ("id", "value", "color",)
    list_filter = ("color", "value",)


    @action(label="Générer toutes les valeurs de cartes possibles", description="Création initiale")
    def generate_all_cards_values(self, request: HttpRequest, queryset: QuerySet[CardValue]):
        CardValue.objects.generate_all_cards_values()


    changelist_actions = ("generate_all_cards_values",)
