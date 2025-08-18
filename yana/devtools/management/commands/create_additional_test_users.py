"""
Command to create additional test users for new countries without affecting existing ones.

Usage:
    python manage.py create_additional_test_users

This will create 200 additional test users specifically for:
- United States (50 users)
- Canada (40 users) 
- Brazil (20 users)
- Japan (20 users)
- Australia (40 users)
- Buffer users (30 users)

These users will have pattern: testing_extended_{number}@example.com
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

class Command(BaseCommand):
    help = 'Creates additional test users for extended countries without affecting existing ones'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check existing test users
        existing_users = User.objects.filter(email__contains='testing_frontend').count()
        self.stdout.write(f'Existing testing_frontend users: {existing_users}')
        
        existing_extended = User.objects.filter(email__contains='testing_extended').count()
        self.stdout.write(f'Existing testing_extended users: {existing_extended}')
        
        # Create 200 additional users for new countries
        first_names = [
            'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella', 'William',
            'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia', 'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander',
            'Abigail', 'Michael', 'Emily', 'Daniel', 'Elizabeth', 'Jacob', 'Sofia', 'Logan', 'Avery', 'Jackson',
            'Ella', 'Sebastian', 'Madison', 'Jack', 'Scarlett', 'Owen', 'Victoria', 'Samuel', 'Aria', 'Matthew',
            'Grace', 'Carter', 'Chloe', 'Luke', 'Camila', 'Jayden', 'Penelope', 'Gabriel', 'Riley', 'Anthony'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
            'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
            'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
            'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
            'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts'
        ]
        
        created_count = 0
        target_count = 200  # 50+40+20+20+40+30
        
        for i in range(1, target_count + 1):
            try:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f'testing_extended_{i:03d}@example.com'
                
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    self.stdout.write(f'User {email} already exists, skipping...')
                    continue
                
                user = User.objects.create_user(
                    email=email,
                    name=first_name,
                    last_name=last_name,
                    password='testpass123'
                )
                
                created_count += 1
                if created_count % 20 == 0:
                    self.stdout.write(f'Created {created_count}/{target_count} users...')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {i}: {str(e)}'))
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} additional test users')
        )
        
        # Summary
        total_testing_users = User.objects.filter(
            email__contains='testing_frontend'
        ).count() + User.objects.filter(
            email__contains='testing_extended'
        ).count()
        
        self.stdout.write(f'Total test users now: {total_testing_users}')
        self.stdout.write('Email patterns:')
        self.stdout.write(f'  - testing_frontend_*: {User.objects.filter(email__contains="testing_frontend").count()}')
        self.stdout.write(f'  - testing_extended_*: {User.objects.filter(email__contains="testing_extended").count()}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Ready to create emotions for extended countries without affecting existing ones!')
        )
