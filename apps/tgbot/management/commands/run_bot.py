from django.core.management.base import BaseCommand

from ...bot import Bot


class Command(BaseCommand):
    help = 'Run telegram bot'

    def add_arguments(self, parser):
        parser.add_argument(
            'token',
            type=str,
            help='bot token'
        )

    def handle(self, token, *args, **options):
        Bot(token).forever_run()
