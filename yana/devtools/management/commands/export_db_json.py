from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Model
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime

class Command(BaseCommand):
  help = 'Exports the contents of all database tables to a JSON file'

  def handle(self, *args, **options):
    # Create a dictionary to store all data
    db_data = {}
    
    # Get all models from all installed apps
    for app_config in apps.get_app_configs():
      app_data = {}
      
      for model in app_config.get_models():
        if issubclass(model, Model):
          try:
            # Get table name
            table_name = model._meta.db_table
            
            # Get all records
            records = model.objects.all()
            
            if records.exists():
              # Get field names
              field_names = [f.name for f in model._meta.fields]
              
              # Store records
              table_data = []
              for record in records:
                record_data = {}
                for field in field_names:
                  value = getattr(record, field)
                  record_data[field] = str(value)
                table_data.append(record_data)
              
              app_data[table_name] = {
                'records': table_data,
                'count': records.count()
              }
            else:
              app_data[table_name] = {
                'records': [],
                'count': 0
              }
              
          except Exception as e:
            app_data[table_name] = {
              'error': str(e)
            }
      
      db_data[app_config.label] = app_data

    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'db_export_{timestamp}.json'

    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(db_data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)

    self.stdout.write(self.style.SUCCESS(f'Database exported successfully to {filename}')) 