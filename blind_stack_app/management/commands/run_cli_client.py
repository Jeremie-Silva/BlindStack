from django.core.management import BaseCommand
from cli_client.application import cli_application


class Command(BaseCommand):
    def handle(self, *args, **options):
        cli_application()