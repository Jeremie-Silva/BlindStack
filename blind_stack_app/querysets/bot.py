from typing import Self
from django.db.models import QuerySet



class BotQuerySet(QuerySet):
    def unlocked(self) -> Self:
        return self.filter(is_unlocked=True)
