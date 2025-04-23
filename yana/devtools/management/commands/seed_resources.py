from django.core.management.base import BaseCommand
from apps.resources.models import HelpResource

class Command(BaseCommand):
    help = 'Seeds the help resources with default organizations'

    def handle(self, *args, **options):
        resources = [
            {
                'name': 'Centro de Atención al Suicida (CAS)',
                'description': 'Brinda contención y asistencia a personas en crisis emocional o en riesgo de suicidio.',
                'url': 'https://www.casbuenosaires.com.ar/',
                'location': 'Buenos Aires',
                'category': 'Crisis',
                'phone': '135',
                'email': 'info@casbuenosaires.com.ar'
            },
            {
                'name': 'Programa Nacional de Prevención del Suicidio',
                'description': 'Ofrece contención, información y asesoramiento a personas en crisis o a quienes buscan ayudar a alguien en esa situación.',
                'url': 'https://www.argentina.gob.ar/salud/mental-y-adicciones/prevencion-del-suicidio',
                'location': 'Nacional',
                'category': 'Prevención',
                'phone': '0800-222-1002',
                'email': 'prevenciondelsuicidio@msal.gov.ar'
            },
            {
                'name': 'Salud Mental',
                'description': 'Ofrece asistencia, acompañamiento y derivación en casos de urgencias en salud mental.',
                'url': 'https://www.argentina.gob.ar/salud/mental-y-adicciones',
                'location': 'Nacional',
                'category': 'Salud Mental',
                'phone': '0800-222-1002',
                'email': 'saludmental@msal.gov.ar'
            },
            {
                'name': 'Atención a Niñas, Niños y Adolescentes',
                'description': 'Brinda contención, asesoramiento y orientación sobre los derechos de niñas, niños y adolescentes.',
                'url': 'https://www.argentina.gob.ar/salud/mental-y-adicciones/linea-102',
                'location': 'Nacional',
                'category': 'Infancia y Adolescencia',
                'phone': '102',
                'email': 'linea102@senaf.gob.ar'
            },
            {
                'name': 'Sistema de Atención Médica de Emergencia (SAME)',
                'description': 'Atiende emergencias médicas y psiquiátricas en la Ciudad Autónoma de Buenos Aires y otras localidades con servicio de SAME.',
                'url': 'https://www.buenosaires.gob.ar/same',
                'location': 'Buenos Aires',
                'category': 'Emergencias',
                'phone': '107',
                'email': 'same@buenosaires.gob.ar'
            }
        ]
        
        for resource_data in resources:
            if HelpResource.objects.filter(name=resource_data['name']).exists():
                self.stdout.write(self.style.WARNING(f'Resource already exists: {resource_data["name"]}'))
            else:
                try:
                    HelpResource.objects.create(**resource_data)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created resource: {resource_data["name"]}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating resource {resource_data["name"]}: {str(e)}')) 