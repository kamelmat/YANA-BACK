from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('emotions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedemotion',
            name='latitude',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sharedemotion',
            name='longitude',
            field=models.TextField(),
        ),
    ] 