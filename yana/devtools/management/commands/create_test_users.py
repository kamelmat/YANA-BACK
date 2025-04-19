"""
Command to create test users with a specific email pattern.

Usage:
    python manage.py create_test_users [--count N] [--email-pattern PATTERN]

Options:
    --count N              Number of test users to create (default: 50)
    --email-pattern PATTERN  Email pattern to use (default: testing_frontend)

Examples:
    # Create 50 users with default email pattern
    python manage.py create_test_users

    # Create 100 users with custom email pattern
    python manage.py create_test_users --count 100 --email-pattern testing_mobile

    # Create 10 users with default pattern
    python manage.py create_test_users --count 10

The command will create users with:
- Random first and last names
- Emails in format: {pattern}_{number}@example.com
- Same password for all users: testpass123
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random
import re

class Command(BaseCommand):
    help = 'Creates test users with a specific email pattern'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of test users to create (default: 50)'
        )
        parser.add_argument(
            '--email-pattern',
            type=str,
            default='testing_frontend',
            help='Email pattern to use for test users (default: testing_frontend)'
        )

    def get_next_number(self, email_pattern):
        """Find the highest number used for the given pattern and return the next number"""
        User = get_user_model()
        existing_users = User.objects.filter(email__startswith=f"{email_pattern}_")
        
        if not existing_users.exists():
            return 1
            
        # Extract numbers from existing emails
        numbers = []
        for user in existing_users:
            match = re.search(rf"{email_pattern}_(\d+)@", user.email)
            if match:
                numbers.append(int(match.group(1)))
                
        return max(numbers) + 1 if numbers else 1

    def handle(self, *args, **options):
        count = options['count']
        email_pattern = options['email_pattern']
        User = get_user_model()

        first_names = ['John', 'Jane']
        last_names = ['Smith', 'Doe']

        # Get the starting number
        start_number = self.get_next_number(email_pattern)
        
        # Check if we have enough available numbers for the requested count
        existing_users = User.objects.filter(email__startswith=f"{email_pattern}_")
        if existing_users.exists():
            # Get the highest number used
            numbers = []
            for user in existing_users:
                match = re.search(rf"{email_pattern}_(\d+)@", user.email)
                if match:
                    numbers.append(int(match.group(1)))
            highest_number = max(numbers) if numbers else 0
            
            # Check if we have enough available numbers
            if highest_number + count > 999:  # Arbitrary limit to prevent too many users
                raise Exception(f"Cannot create {count} users - would exceed maximum number limit")
            
            # Check if any of the emails we want to create already exist
            for i in range(count):
                email = f"{email_pattern}_{start_number + i}@example.com"
                if User.objects.filter(email=email).exists():
                    raise Exception(f"User with email {email} already exists")
        
        created_count = 0
        for i in range(count):
            try:
                # Generate random user data
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"{email_pattern}_{start_number + i}@example.com"
                password = "testpass123"  # Same password for all test users

                # Create user
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=first_name,
                    last_name=last_name
                )

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created test user: {email} ({first_name} {last_name})'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating user: {str(e)}')
                )
                raise  # Re-raise the exception to stop the command

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} test users with email pattern "{email_pattern}"'
            )
        ) 