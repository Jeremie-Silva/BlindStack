import typer
import sys
from django.core.management import BaseCommand
from cli_client import cli_application



class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.argv: list[str] = [sys.argv[0]]  # juste pour typer
        typer.run(cli_application)
