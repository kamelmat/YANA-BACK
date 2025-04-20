from django.core.management.base import BaseCommand
from apps.emotions.models import SharedEmotion

class Command(BaseCommand):
    help = 'Clears all user emotions from the database. Usage: python manage.py clear_user_emotions --confirm'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion of all emotions'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL user emotions from the database. '
                    'Run with --confirm to proceed.'
                )
            )
            return

        count = SharedEmotion.objects.count()
        SharedEmotion.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {count} user emotions'
            )
        ) 