"""
Command to restore the missing European emotions that were overwritten.

Usage:
    python manage.py restore_european_emotions

This command will restore the original 100 European emotions:
- Spain (20 emotions)
- Argentina (20 emotions) 
- France (20 emotions)
- UK (20 emotions)
- India (20 emotions)

Uses existing testing_frontend users and creates NEW emotions for European locations.
"""

from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Restores missing European emotions that were overwritten'

    def handle(self, *args, **options):
        # Get testing_frontend users (original test users)
        User = get_user_model()
        testing_users = list(User.objects.filter(email__contains='testing_frontend'))
        
        if not testing_users:
            self.stdout.write(self.style.ERROR('No testing_frontend users found'))
            return

        # Get available emotions
        available_emotions = list(Emotion.objects.filter(id__in=[20, 21, 22, 23, 24]))
        
        if len(available_emotions) < 5:
            self.stdout.write(self.style.ERROR(f'Expected 5 emotions, found {len(available_emotions)}'))
            return

        # Original European countries that got overwritten
        european_countries = {
            '🇪🇸 SPAIN': [
                ('Madrid', 40.4168, -3.7038),
                ('Barcelona', 41.3851, 2.1734),
                ('Valencia', 39.4699, -0.3763),
                ('Seville', 37.3891, -5.9845),
                ('Bilbao', 43.2627, -2.9253),
                ('Málaga', 36.7213, -4.4214),
                ('Las Palmas', 28.1248, -15.4300),
                ('Zaragoza', 41.6488, -0.8891),
                ('Murcia', 37.9922, -1.1307),
                ('Palma', 39.5696, 2.6502),
                ('Vigo', 42.2406, -8.7207),
                ('Gijón', 43.5322, -5.6611),
                ('A Coruña', 43.3623, -8.4115),
                ('Granada', 37.1773, -3.5986),
                ('Córdoba', 37.8882, -4.7794),
                ('Santander', 43.4623, -3.8099),
                ('Toledo', 39.8628, -4.0273),
                ('Badajoz', 38.8794, -6.9707),
                ('Salamanca', 40.9701, -5.6635),
                ('Pamplona', 42.8125, -1.6458),
            ],
            '🇦🇷 ARGENTINA': [
                ('Buenos Aires', -34.6118, -58.3960),
                ('Córdoba', -31.4201, -64.1888),
                ('Rosario', -32.9442, -60.6505),
                ('Mendoza', -32.8895, -68.8458),
                ('La Plata', -34.9215, -57.9545),
                ('Tucumán', -26.8241, -65.2226),
                ('Mar del Plata', -38.0055, -57.5426),
                ('Salta', -24.7821, -65.4232),
                ('Santa Fe', -31.6107, -60.6973),
                ('San Juan', -31.5375, -68.5364),
                ('Resistencia', -27.4514, -58.9867),
                ('Neuquén', -38.9516, -68.0591),
                ('Formosa', -26.1775, -58.1781),
                ('San Luis', -33.2949, -66.3356),
                ('Catamarca', -28.4696, -65.7852),
                ('La Rioja', -29.4331, -66.8563),
                ('Jujuy', -24.1858, -65.2995),
                ('Santiago del Estero', -27.7951, -64.2615),
                ('San Salvador', -24.7793, -65.4107),
                ('Posadas', -27.3621, -55.8981),
            ],
            '🇫🇷 FRANCE': [
                ('Paris', 48.8566, 2.3522),
                ('Lyon', 45.7640, 4.8357),
                ('Marseille', 43.2965, 5.3698),
                ('Toulouse', 43.6047, 1.4442),
                ('Nice', 43.7102, 7.2620),
                ('Nantes', 47.2184, -1.5536),
                ('Montpellier', 43.6110, 3.8767),
                ('Strasbourg', 48.5734, 7.7521),
                ('Bordeaux', 44.8378, -0.5792),
                ('Lille', 50.6292, 3.0573),
                ('Rennes', 48.1173, -1.6778),
                ('Reims', 49.2583, 4.0317),
                ('Toulon', 43.1242, 5.9280),
                ('Saint-Étienne', 45.4397, 4.3872),
                ('Le Havre', 49.4944, 0.1079),
                ('Grenoble', 45.1885, 5.7245),
                ('Dijon', 47.3220, 5.0415),
                ('Angers', 47.4784, -0.5632),
                ('Nîmes', 43.8367, 4.3601),
                ('Villeurbanne', 45.7733, 4.8794),
            ],
            '🇬🇧 UK': [
                ('London', 51.5074, -0.1278),
                ('Birmingham', 52.4862, -1.8904),
                ('Manchester', 53.4808, -2.2426),
                ('Glasgow', 55.8642, -4.2518),
                ('Liverpool', 53.4084, -2.9916),
                ('Leeds', 53.8008, -1.5491),
                ('Sheffield', 53.3811, -1.4701),
                ('Edinburgh', 55.9533, -3.1883),
                ('Bristol', 51.4545, -2.5879),
                ('Newcastle', 54.9783, -1.6178),
                ('Belfast', 54.5973, -5.9301),
                ('Cardiff', 51.4816, -3.1791),
                ('Leicester', 52.6369, -1.1398),
                ('Coventry', 52.4068, -1.5197),
                ('Bradford', 53.7960, -1.7594),
                ('Nottingham', 52.9548, -1.1581),
                ('Plymouth', 50.3755, -4.1427),
                ('Wolverhampton', 52.5873, -2.1285),
                ('Southampton', 50.9097, -1.4044),
                ('Derby', 52.9225, -1.4746),
            ],
            '🇮🇳 INDIA': [
                ('Mumbai', 19.0760, 72.8777),
                ('Delhi', 28.7041, 77.1025),
                ('Bangalore', 12.9716, 77.5946),
                ('Chennai', 13.0827, 80.2707),
                ('Kolkata', 22.5726, 88.3639),
                ('Hyderabad', 17.3850, 78.4867),
                ('Pune', 18.5204, 73.8567),
                ('Ahmedabad', 23.0225, 72.5714),
                ('Surat', 21.1702, 72.8311),
                ('Jaipur', 26.9124, 75.7873),
                ('Lucknow', 26.8467, 80.9462),
                ('Kanpur', 26.4499, 80.3319),
                ('Nagpur', 21.1458, 79.0882),
                ('Indore', 22.7196, 75.8577),
                ('Thane', 19.2183, 72.9781),
                ('Bhopal', 23.2599, 77.4126),
                ('Visakhapatnam', 17.6868, 83.2185),
                ('Pimpri', 18.6298, 73.8093),
                ('Patna', 25.5941, 85.1376),
                ('Vadodara', 22.3072, 73.1812),
            ]
        }

        # Clear any existing emotions for testing_frontend users to avoid duplicates
        existing_count = SharedEmotion.objects.filter(user__email__contains='testing_frontend').count()
        self.stdout.write(f'Found {existing_count} existing emotions for testing_frontend users')
        
        # Delete them to avoid having users with multiple emotions
        SharedEmotion.objects.filter(user__email__contains='testing_frontend').delete()
        self.stdout.write(self.style.WARNING(f'Cleared {existing_count} existing emotions to avoid duplicates'))

        created_count = 0
        total_locations = sum(len(cities) for cities in european_countries.values())
        user_index = 0
        
        self.stdout.write(f'Restoring {total_locations} European emotions using {len(testing_users)} frontend users...')
        
        for country, cities in european_countries.items():
            self.stdout.write(f'\n{country}:')
            
            for city, lat, lng in cities:
                try:
                    # Use frontend users sequentially to ensure distribution
                    if user_index < len(testing_users):
                        user = testing_users[user_index]
                        user_index += 1
                    else:
                        # Wrap around if we run out of users
                        user_index = 0
                        user = testing_users[user_index]
                        user_index += 1
                    
                    emotion = random.choice(available_emotions)
                    
                    # Create timestamp within last few hours
                    hours_ago = random.uniform(0, 6)
                    created_at = datetime.now() - timedelta(hours=hours_ago)
                    
                    # Create the shared emotion
                    shared_emotion = SharedEmotion.objects.create(
                        user=user,
                        emotion=emotion,
                        latitude=f"{lat:.4f}",
                        longitude=f"{lng:.4f}",
                        created_at=created_at,
                        is_active=True
                    )
                    
                    created_count += 1
                    self.stdout.write(
                        f'  ✅ {city}: {emotion.name} (ID:{emotion.id}) @ ({lat:.4f}, {lng:.4f}) - User: {user.email[:25]}...'
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ {city}: Error - {str(e)}')
                    )

        # Summary
        self.stdout.write(f'\n🎯 SUCCESS: Restored {created_count} European emotions')
        
        # Show emotion distribution
        emotion_counts = {}
        for emotion in available_emotions:
            count = SharedEmotion.objects.filter(
                emotion=emotion, 
                user__email__contains='testing_frontend'
            ).count()
            emotion_counts[emotion.name] = count
            
        self.stdout.write('\n📊 Restored European Emotion Distribution:')
        for emotion_name, count in emotion_counts.items():
            self.stdout.write(f'  {emotion_name}: {count} locations')
            
        # Total counts
        frontend_count = SharedEmotion.objects.filter(user__email__contains='testing_frontend').count()
        extended_count = SharedEmotion.objects.filter(user__email__contains='testing_extended').count()
        total_count = SharedEmotion.objects.filter(is_active=True).count()
        
        self.stdout.write(f'\n📈 Database Summary:')
        self.stdout.write(f'  European emotions (testing_frontend): {frontend_count}')
        self.stdout.write(f'  Extended emotions (testing_extended): {extended_count}')
        self.stdout.write(f'  Total active emotions: {total_count}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ European emotions restored! Now you should see ALL countries on the map!'))
