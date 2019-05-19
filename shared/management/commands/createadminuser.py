from django.core.management.base import BaseCommand, CommandError
from shared.models import BaseProfile

class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies password for the admin user.',
        )
        parser.add_argument(
            '--email', dest='email', default=None,
            help='Specifies email for the admin user.',
        )

    def handle(self, *args, **options):
        password = options.get('password')
        email = options.get('email')

        if not password or not email:
            raise CommandError('--email and --password are required')

        BaseProfile.objects.create(
            email=email,
            password=password,
            is_staff=True,
        )
