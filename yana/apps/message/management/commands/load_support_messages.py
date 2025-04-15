# apps/message/management/commands/load_support_messages.py
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.message.models import SupportMessageTemplate


class Command(BaseCommand):
    help = 'Carga mensajes de apoyo desde un archivo JSON'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'apps', 'message', 'data', 'messages.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"No se encontró el archivo en {file_path}"))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                messages = json.load(file)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error al leer el archivo JSON: {e}"))
            return

        new_count = 0
        existing_count = 0
        invalid_count = 0

        for msg in messages:
            if 'text' not in msg:
                self.stdout.write(self.style.WARNING(f"Mensaje inválido (falta 'text'): {msg}"))
                invalid_count += 1
                continue

            text = msg['text'].strip()
            if not text:
                self.stdout.write(self.style.WARNING(f"Mensaje con texto vacío: {msg}"))
                invalid_count += 1
                continue

            obj, created = SupportMessageTemplate.objects.get_or_create(text=text)
            if created:
                new_count += 1
            else:
                existing_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {new_count} nuevos mensajes cargados. 🗃️ {existing_count} ya existían. ⚠️ {invalid_count} inválidos."
        ))
