# Generated by Django 2.1.4 on 2019-05-20 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_ocrmodel_script'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentprocesssettings',
            name='document',
        ),
        migrations.RemoveField(
            model_name='documentprocesssettings',
            name='ocr_model',
        ),
        migrations.RemoveField(
            model_name='documentprocesssettings',
            name='train_model',
        ),
        migrations.RemoveField(
            model_name='documentprocesssettings',
            name='typology',
        ),
        migrations.DeleteModel(
            name='DocumentProcessSettings',
        ),
    ]
