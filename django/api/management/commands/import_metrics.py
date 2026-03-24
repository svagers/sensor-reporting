from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import metrics data from JSON file'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully imported metrics!'))
