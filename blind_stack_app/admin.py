from django.contrib.admin import register, ModelAdmin
from blind_stack_app.models import Card



@register(Card)
class PermissionManagerAdmin(ModelAdmin):
    list_display = ("id", "value", "color")
    search_fields = ("id", "value", "color")
    list_filter = ("color", "value",)
