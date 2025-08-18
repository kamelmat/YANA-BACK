"""
Command to populate global test emotions for frontend testing across major regions.

Usage:
    python manage.py populate_global_test_emotions

This command will create 270 test emotions distributed across:
- Spain (20 emotions)
- Argentina (20 emotions) 
- France (20 emotions)
- UK (20 emotions)
- India (20 emotions)
- United States (50 emotions)
- Canada (40 emotions)
- Brazil (20 emotions)
- Japan (20 emotions)
- Australia (40 emotions)

Requirements:
- Existing test users with emails containing 'testing_frontend'
- Emotions: sadness(21), loneliness(22), distress(23), tranquility(24), reluctance(25)
- Current timestamp for 24-hour filter compatibility
"""

from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populates global test emotions across major regions for frontend testing'

    def handle(self, *args, **options):
        # Get all test users and emotions
        User = get_user_model()
        testing_users = list(User.objects.filter(email__contains='testing_frontend'))
        
        if not testing_users:
            self.stdout.write(self.style.ERROR('No testing users found. Create test users first with: python manage.py create_test_users'))
            return

        # Get available emotions - using the current IDs from database
        available_emotions = list(Emotion.objects.filter(id__in=[20, 21, 22, 23, 24]))  # sadness, distress, loneliness, reluctance, tranquility
        
        if len(available_emotions) < 5:
            self.stdout.write(self.style.ERROR(f'Expected 5 emotions, found {len(available_emotions)}. Available: {[e.name for e in available_emotions]}'))
            return

        # Global test locations organized by country
        locations = {
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
            ],
            '🇺🇸 UNITED STATES': [
                ('New York', 40.7128, -74.0060),
                ('Los Angeles', 34.0522, -118.2437),
                ('Chicago', 41.8781, -87.6298),
                ('Houston', 29.7604, -95.3698),
                ('Phoenix', 33.4484, -112.0740),
                ('Philadelphia', 39.9526, -75.1652),
                ('San Antonio', 29.4241, -98.4936),
                ('San Diego', 32.7157, -117.1611),
                ('Dallas', 32.7767, -96.7970),
                ('Austin', 30.2672, -97.7431),
                ('San Jose', 37.3382, -121.8863),
                ('Jacksonville', 30.3322, -81.6557),
                ('Fort Worth', 32.7555, -97.3308),
                ('Columbus', 39.9612, -82.9988),
                ('Charlotte', 35.2271, -80.8431),
                ('San Francisco', 37.7749, -122.4194),
                ('Indianapolis', 39.7684, -86.1581),
                ('Seattle', 47.6062, -122.3321),
                ('Denver', 39.7392, -104.9903),
                ('Washington DC', 38.9072, -77.0369),
                ('Boston', 42.3601, -71.0589),
                ('El Paso', 31.7619, -106.4850),
                ('Nashville', 36.1627, -86.7816),
                ('Detroit', 42.3314, -83.0458),
                ('Oklahoma City', 35.4676, -97.5164),
                ('Portland', 45.5152, -122.6784),
                ('Las Vegas', 36.1699, -115.1398),
                ('Memphis', 35.1495, -90.0490),
                ('Louisville', 38.2527, -85.7585),
                ('Baltimore', 39.2904, -76.6122),
                ('Milwaukee', 43.0389, -87.9065),
                ('Albuquerque', 35.0844, -106.6504),
                ('Tucson', 32.2226, -110.9747),
                ('Fresno', 36.7378, -119.7871),
                ('Mesa', 33.4164, -111.8315),
                ('Sacramento', 38.5816, -121.4944),
                ('Atlanta', 33.7490, -84.3880),
                ('Kansas City', 39.0997, -94.5786),
                ('Colorado Springs', 38.8339, -104.8214),
                ('Raleigh', 35.7796, -78.6382),
                ('Omaha', 41.2565, -95.9345),
                ('Miami', 25.7617, -80.1918),
                ('Long Beach', 33.7701, -118.1937),
                ('Virginia Beach', 36.8529, -75.9780),
                ('Oakland', 37.8044, -122.2711),
                ('Minneapolis', 44.9778, -93.2650),
                ('Tulsa', 36.1540, -95.9928),
                ('Tampa', 27.9506, -82.4572),
                ('Arlington', 32.7357, -97.1081),
                ('New Orleans', 29.9511, -90.0715),
            ],
            '🇨🇦 CANADA': [
                ('Toronto', 43.6532, -79.3832),
                ('Montreal', 45.5017, -73.5673),
                ('Vancouver', 49.2827, -123.1207),
                ('Calgary', 51.0447, -114.0719),
                ('Edmonton', 53.5461, -113.4938),
                ('Ottawa', 45.4215, -75.6972),
                ('Winnipeg', 49.8951, -97.1384),
                ('Quebec City', 46.8139, -71.2080),
                ('Hamilton', 43.2557, -79.8711),
                ('Kitchener', 43.4516, -80.4925),
                ('London', 42.9849, -81.2453),
                ('Victoria', 48.4284, -123.3656),
                ('Halifax', 44.6488, -63.5752),
                ('Oshawa', 43.8971, -78.8658),
                ('Windsor', 42.3149, -83.0364),
                ('Saskatoon', 52.1332, -106.6700),
                ('St. Catharines', 43.1594, -79.2469),
                ('Regina', 50.4452, -104.6189),
                ('Sherbrooke', 45.4042, -71.8929),
                ('Kelowna', 49.8880, -119.4960),
                ('Barrie', 44.3894, -79.6903),
                ('Guelph', 43.5448, -80.2482),
                ('Kanata', 45.3002, -75.9195),
                ('Abbotsford', 49.0504, -122.3045),
                ('Trois-Rivières', 46.3432, -72.5420),
                ('Kingston', 44.2312, -76.4860),
                ('Milton', 43.5183, -79.8774),
                ('Moncton', 46.0878, -64.7782),
                ('White Rock', 49.0258, -122.8028),
                ('Nanaimo', 49.1659, -123.9401),
                ('Brantford', 43.1394, -80.2644),
                ('Chicoutimi', 48.4269, -71.0662),
                ('Saint John', 45.2733, -66.0633),
                ('Peterborough', 44.3091, -78.3197),
                ('Thunder Bay', 48.3809, -89.2477),
                ('Kamloops', 50.6745, -120.3273),
                ('Sudbury', 46.4917, -80.9930),
                ('Sault Ste. Marie', 46.5197, -84.3467),
                ('Sarnia', 42.9994, -82.4066),
                ('Red Deer', 52.2681, -113.8112),
            ],
            '🇧🇷 BRAZIL': [
                ('São Paulo', -23.5558, -46.6396),
                ('Rio de Janeiro', -22.9068, -43.1729),
                ('Brasília', -15.8267, -47.9218),
                ('Salvador', -12.9714, -38.5014),
                ('Fortaleza', -3.7172, -38.5433),
                ('Belo Horizonte', -19.9167, -43.9345),
                ('Manaus', -3.1190, -60.0217),
                ('Curitiba', -25.4244, -49.2654),
                ('Recife', -8.0476, -34.8770),
                ('Goiânia', -16.6869, -49.2648),
                ('Belém', -1.4558, -48.5044),
                ('Porto Alegre', -30.0346, -51.2177),
                ('Guarulhos', -23.4538, -46.5333),
                ('Campinas', -22.9099, -47.0626),
                ('São Luís', -2.5387, -44.2825),
                ('São Gonçalo', -22.8305, -43.0531),
                ('Maceió', -9.6658, -35.7353),
                ('Duque de Caxias', -22.7858, -43.3054),
                ('Natal', -5.7945, -35.2110),
                ('Teresina', -5.0892, -42.8019),
            ],
            '🇯🇵 JAPAN': [
                ('Tokyo', 35.6762, 139.6503),
                ('Yokohama', 35.4437, 139.6380),
                ('Osaka', 34.6937, 135.5023),
                ('Nagoya', 35.1815, 136.9066),
                ('Sapporo', 43.0642, 141.3469),
                ('Fukuoka', 33.5904, 130.4017),
                ('Kobe', 34.6901, 135.1956),
                ('Kawasaki', 35.5308, 139.7029),
                ('Kyoto', 35.0116, 135.7681),
                ('Saitama', 35.8617, 139.6455),
                ('Hiroshima', 34.3853, 132.4553),
                ('Sendai', 38.2682, 140.8694),
                ('Kitakyushu', 33.8834, 130.8751),
                ('Chiba', 35.6074, 140.1065),
                ('Sakai', 34.5732, 135.4825),
                ('Niigata', 37.9161, 139.0364),
                ('Hamamatsu', 34.7108, 137.7261),
                ('Okayama', 34.6551, 133.9195),
                ('Sagamihara', 35.5761, 139.3739),
                ('Kumamoto', 32.8031, 130.7079),
            ],
            '🇦🇺 AUSTRALIA': [
                ('Sydney', -33.8688, 151.2093),
                ('Melbourne', -37.8136, 144.9631),
                ('Brisbane', -27.4698, 153.0251),
                ('Perth', -31.9505, 115.8605),
                ('Adelaide', -34.9285, 138.6007),
                ('Gold Coast', -28.0167, 153.4000),
                ('Newcastle', -32.9267, 151.7789),
                ('Canberra', -35.2809, 149.1300),
                ('Sunshine Coast', -26.6500, 153.0667),
                ('Wollongong', -34.4278, 150.8931),
                ('Hobart', -42.8821, 147.3272),
                ('Geelong', -38.1499, 144.3617),
                ('Townsville', -19.2590, 146.8169),
                ('Cairns', -16.9186, 145.7781),
                ('Toowoomba', -27.5598, 151.9507),
                ('Darwin', -12.4634, 130.8456),
                ('Launceston', -41.4332, 147.1441),
                ('Ballarat', -37.5622, 143.8503),
                ('Bendigo', -36.7570, 144.2794),
                ('Albury', -36.0737, 146.9135),
                ('Mackay', -21.1550, 149.1844),
                ('Rockhampton', -23.3781, 150.5136),
                ('Bunbury', -33.3267, 115.6441),
                ('Bundaberg', -24.8661, 152.3489),
                ('Coffs Harbour', -30.2963, 153.1185),
                ('Wagga Wagga', -35.1082, 147.3598),
                ('Hervey Bay', -25.2990, 152.8553),
                ('Mildura', -34.2090, 142.1614),
                ('Shepparton', -36.3820, 145.4015),
                ('Port Macquarie', -31.4333, 152.9000),
                ('Orange', -33.2839, 149.0988),
                ('Tamworth', -31.0927, 150.9279),
                ('Dubbo', -32.2571, 148.6017),
                ('Geraldton', -28.7774, 114.6145),
                ('Kalgoorlie', -30.7489, 121.4648),
                ('Gladstone', -23.8499, 151.2587),
                ('Warrnambool', -38.3799, 142.4819),
                ('Busselton', -33.6500, 115.3333),
                ('Alice Springs', -23.6980, 133.8807),
                ('Mount Gambier', -37.8282, 140.7821),
            ]
        }

        # Clear existing test emotions first (optional - remove if you want to keep them)
        # SharedEmotion.objects.filter(user__email__contains='testing_frontend').delete()
        # self.stdout.write(self.style.WARNING('Cleared existing test emotions'))

        created_count = 0
        total_locations = sum(len(cities) for cities in locations.values())
        
        self.stdout.write(f'Creating {total_locations} test emotions across {len(locations)} countries...')
        
        for country, cities in locations.items():
            self.stdout.write(f'\n{country}:')
            
            for city, lat, lng in cities:
                try:
                    # Select random user and emotion
                    user = random.choice(testing_users)
                    emotion = random.choice(available_emotions)
                    
                    # Create timestamp within last few hours (ensures 24h filter compatibility)
                    hours_ago = random.uniform(0, 6)  # Within last 6 hours
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
                        f'  ✅ {city}: {emotion.name} (ID:{emotion.id}) @ ({lat:.4f}, {lng:.4f}) - User: {user.email[:20]}...'
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ {city}: Error - {str(e)}')
                    )

        # Summary
        self.stdout.write(f'\n🎯 SUCCESS: Created {created_count} test emotions across {len(locations)} countries')
        
        # Show emotion distribution
        emotion_counts = {}
        for emotion in available_emotions:
            count = SharedEmotion.objects.filter(emotion=emotion, user__email__contains='testing_frontend').count()
            emotion_counts[emotion.name] = count
            
        self.stdout.write('\n📊 Emotion Distribution:')
        for emotion_name, count in emotion_counts.items():
            self.stdout.write(f'  {emotion_name}: {count} locations')
            
        self.stdout.write(f'\n🌍 Total test emotions in database: {SharedEmotion.objects.filter(user__email__contains="testing_frontend").count()}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Global test emotions population complete! Ready for frontend testing.'))
