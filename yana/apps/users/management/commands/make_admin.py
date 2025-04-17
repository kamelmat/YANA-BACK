from django.core.management.base import BaseCommand
from apps.users.models import CustomUser

#run command: python manage.py make_admin <email>
class Command(BaseCommand):
    help = 'Makes a user an admin'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to make admin')

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = CustomUser.objects.get(email=email)
            user.is_admin = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully made {email} an admin'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} does not exist')) 