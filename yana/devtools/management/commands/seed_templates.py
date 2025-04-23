from django.core.management.base import BaseCommand
from apps.message.models import SupportMessageTemplate

class Command(BaseCommand):
    help = 'Seeds the support message templates with default phrases'

    def handle(self, *args, **options):
        templates = [
            "¡Ánimo!",
            "Cuentas con todo mi apoyo",
            "Estoy contigo, comparto lo que sientes"
        ]
        
        for template_text in templates:
            if SupportMessageTemplate.objects.filter(text=template_text).exists():
                self.stdout.write(self.style.WARNING(f'Template already exists: {template_text}'))
            else:
                try:
                    SupportMessageTemplate.objects.create(text=template_text)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created template: {template_text}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating template {template_text}: {str(e)}')) 