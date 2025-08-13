"""
Command to populate help resources database with location-sensitive mental health contacts and hotlines.

Usage:
    python manage.py add_help_resources

This command will create help resources including:
- Spanish mental health services and crisis lines (priority)
- International mental health resources by country
- Emergency contacts and online resources
"""

from django.core.management.base import BaseCommand
from apps.resources.models import HelpResource


class Command(BaseCommand):
    help = 'Populates the database with location-sensitive help resources and mental health contacts'

    def handle(self, *args, **options):
        # Complete help resources organized by country
        all_resources = [
            # 🇪🇸 SPAIN - Priority resources
            {
                'name': 'Línea 024 - Atención a la Conducta Suicida',
                'description': 'Línea telefónica gratuita de ayuda a personas con pensamientos suicidas, 24/7, confidencial.',
                'url': 'https://www.sanidad.gob.es/linea024/home.htm',
                'location': 'España',
                'category': 'Crisis Support',
                'phone': '024',
                'email': None
            },
            {
                'name': 'Fundación Española para la Prevención del Suicidio (FSME)',
                'description': 'Organización dedicada a la prevención del suicidio y formación de profesionales.',
                'url': 'https://www.fsme.es/',
                'location': 'España',
                'category': 'Prevention',
                'phone': '91 083 43 93',
                'email': 'fsme@fsme.es'
            },
            {
                'name': 'Cruz Roja - Línea 024 Chat',
                'description': 'Chat online de atención a la conducta suicida por Cruz Roja Española.',
                'url': 'https://www2.cruzroja.es/linea024',
                'location': 'España',
                'category': 'Crisis Support',
                'phone': '024',
                'email': None
            },
            {
                'name': 'Fundación ANAR',
                'description': 'Ayuda a niños y adolescentes en riesgo, línea de ayuda para menores.',
                'url': 'https://www.anar.org/',
                'location': 'España',
                'category': 'Youth Support',
                'phone': '900 20 20 10',
                'email': 'anar@anar.org'
            },
            {
                'name': 'Teléfono de la Esperanza',
                'description': 'Servicio de orientación y ayuda a personas en crisis emocional.',
                'url': 'https://telefonodelaesperanza.org',
                'location': 'España',
                'category': 'Crisis Support',
                'phone': '717 003 717',
                'email': 'madrid@telefonodelaesperanza.org'
            },

            # 🇺🇸 UNITED STATES
            {
                'name': '988 Suicide & Crisis Lifeline',
                'description': 'Free and confidential emotional support for people in suicidal crisis, 24/7.',
                'url': 'https://988lifeline.org/',
                'location': 'United States',
                'category': 'Crisis Support',
                'phone': '988',
                'email': None
            },
            {
                'name': 'Crisis Text Line',
                'description': 'Free 24/7 support via text message for those in crisis.',
                'url': 'https://www.crisistextline.org/',
                'location': 'United States',
                'category': 'Crisis Support',
                'phone': '741741',
                'email': None
            },
            {
                'name': 'NAMI - National Alliance on Mental Illness',
                'description': 'Support, education and advocacy for people affected by mental illness.',
                'url': 'https://www.nami.org/',
                'location': 'United States',
                'category': 'Mental Health',
                'phone': '1-800-950-6264',
                'email': 'info@nami.org'
            },

            # 🇫🇷 FRANCE
            {
                'name': 'SOS Amitié',
                'description': 'Service d\'écoute par téléphone pour les personnes en détresse, 24h/24.',
                'url': 'https://www.sos-amitie.com/',
                'location': 'France',
                'category': 'Crisis Support',
                'phone': '09 72 39 40 50',
                'email': None
            },
            {
                'name': 'Suicide Écoute',
                'description': 'Ligne nationale de prévention du suicide, écoute et orientation.',
                'url': 'https://www.suicide-ecoute.fr/',
                'location': 'France',
                'category': 'Crisis Support',
                'phone': '01 45 39 40 00',
                'email': None
            },

            # 🇩🇪 GERMANY
            {
                'name': 'Telefonseelsorge',
                'description': 'Kostenlose Beratung und Seelsorge per Telefon, rund um die Uhr.',
                'url': 'https://www.telefonseelsorge.de/',
                'location': 'Germany',
                'category': 'Crisis Support',
                'phone': '0800 111 0 111',
                'email': None
            },
            {
                'name': 'Deutsche Gesellschaft für Suizidprävention',
                'description': 'Nationale Arbeitsgemeinschaft zur Suizidprävention und Hilfe in Lebenskrisen.',
                'url': 'https://www.suizidprophylaxe.de/',
                'location': 'Germany',
                'category': 'Prevention',
                'phone': None,
                'email': 'info@suizidprophylaxe.de'
            },

            # 🇬🇧 UNITED KINGDOM
            {
                'name': 'Samaritans',
                'description': 'Free support for anyone in emotional distress, struggling to cope, or at risk of suicide.',
                'url': 'https://www.samaritans.org/',
                'location': 'United Kingdom',
                'category': 'Crisis Support',
                'phone': '116 123',
                'email': 'jo@samaritans.org'
            },
            {
                'name': 'Mind',
                'description': 'Mental health charity providing advice and support to empower anyone experiencing mental health problems.',
                'url': 'https://www.mind.org.uk/',
                'location': 'United Kingdom',
                'category': 'Mental Health',
                'phone': '0300 123 3393',
                'email': 'info@mind.org.uk'
            },

            # 🇵🇹 PORTUGAL
            {
                'name': 'SOS Voz Amiga',
                'description': 'Linha de apoio emocional e prevenção do suicídio, disponível 24 horas.',
                'url': 'https://www.sosvozamiga.org/',
                'location': 'Portugal',
                'category': 'Crisis Support',
                'phone': '213 544 545',
                'email': 'sosvozamiga@sosvozamiga.org'
            },
            {
                'name': 'SNS 24',
                'description': 'Linha de Saúde 24 do Serviço Nacional de Saúde para apoio em saúde mental.',
                'url': 'https://www.sns24.gov.pt/',
                'location': 'Portugal',
                'category': 'Health Support',
                'phone': '808 24 24 24',
                'email': None
            },

            # 🇦🇷 ARGENTINA
            {
                'name': 'Centro de Asistencia al Suicida (CAS)',
                'description': 'Centro de prevención del suicidio en Buenos Aires, atención telefónica gratuita.',
                'url': 'https://www.casbuenosaires.com.ar/',
                'location': 'Argentina',
                'category': 'Crisis Support',
                'phone': '135',
                'email': 'info@casbuenosaires.com.ar'
            },
            {
                'name': 'Línea de Vida',
                'description': 'Servicio de contención telefónica para prevención del suicidio.',
                'url': 'https://www.argentina.gob.ar/salud/mental',
                'location': 'Argentina',
                'category': 'Crisis Support',
                'phone': '0800 999 0091',
                'email': None
            },

            # 🇧🇪 BELGIUM
            {
                'name': 'Centre de Prévention du Suicide',
                'description': 'Centre de prévention du suicide en Belgique, aide et écoute.',
                'url': 'https://www.preventionsuicide.be/',
                'location': 'Belgium',
                'category': 'Prevention',
                'phone': '0800 32 123',
                'email': 'info@preventionsuicide.be'
            },
            {
                'name': 'Zelfmoordlijn 1813',
                'description': 'Hulplijn voor mensen met zelfmoordgedachten, 24/7 beschikbaar.',
                'url': 'https://www.zelfmoord1813.be/',
                'location': 'Belgium',
                'category': 'Crisis Support',
                'phone': '1813',
                'email': None
            },

            # 🇺🇾 URUGUAY
            {
                'name': 'Vida',
                'description': 'Centro de prevención del suicidio en Uruguay, línea de crisis 24 horas.',
                'url': 'https://www.msp.gub.uy/',
                'location': 'Uruguay',
                'category': 'Crisis Support',
                'phone': '*8483',
                'email': None
            },

            # 🇧🇷 BRAZIL
            {
                'name': 'Centro de Valorização da Vida (CVV)',
                'description': 'Apoio emocional e prevenção do suicídio, atendimento gratuito 24 horas.',
                'url': 'https://www.cvv.org.br/',
                'location': 'Brazil',
                'category': 'Crisis Support',
                'phone': '188',
                'email': None
            },
            {
                'name': 'CAPS - Centro de Atenção Psicossocial',
                'description': 'Rede de centros de atenção psicossocial do Sistema Único de Saúde.',
                'url': 'https://www.gov.br/saude/pt-br',
                'location': 'Brazil',
                'category': 'Mental Health',
                'phone': '136',
                'email': None
            }
        ]

        created_count = 0
        for resource_data in all_resources:
            # Check if resource already exists
            if not HelpResource.objects.filter(name=resource_data['name']).exists():
                HelpResource.objects.create(**resource_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created help resource: {resource_data["name"]} ({resource_data["location"]})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Help resource already exists: {resource_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} help resources across multiple countries')
        )
        
        # Summary by country
        countries = {}
        for resource in all_resources:
            country = resource['location']
            countries[country] = countries.get(country, 0) + 1
        
        self.stdout.write(self.style.SUCCESS('\nResources created by country:'))
        for country, count in countries.items():
            flag = {'España': '🇪🇸', 'United States': '🇺🇸', 'France': '🇫🇷', 'Germany': '🇩🇪', 
                   'United Kingdom': '🇬🇧', 'Portugal': '🇵🇹', 'Argentina': '🇦🇷', 
                   'Belgium': '🇧🇪', 'Uruguay': '🇺🇾', 'Brazil': '🇧🇷'}.get(country, '🌍')
            self.stdout.write(f'{flag} {country}: {count} resources') 