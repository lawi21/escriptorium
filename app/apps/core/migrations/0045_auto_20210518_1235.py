# Generated by Django 2.2.19 on 2021-05-18 12:35

from django.db import migrations, models
import django.db.models.deletion


def populate_m2m(apps, schema_editor):
    OcrModel = apps.get_model('core', 'OcrModel')
    OcrModelDocument = apps.get_model('core', 'OcrModelDocument')

    OcrModelDocument.objects.bulk_create([
        OcrModelDocument(
            document_id = model.document_id,
            ocr_model_id = model.id,
            trained_on = False,
            executed_on = True,
        ) for model in OcrModel.objects.exclude(document__isnull=True)
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20210520_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='OcrModelDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('trained_on', models.BooleanField()),
                ('executed_on', models.BooleanField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_model_documents', to='core.Document')),
                ('ocr_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_model_documents', to='core.OcrModel')),
            ],
            options={
                'unique_together': {('document', 'ocr_model')},
            },
        ),
        migrations.AddField(
            model_name='ocrmodel',
            name='documents',
            field=models.ManyToManyField(related_name='ocr_models', through='core.OcrModelDocument', to='core.Document'),
        ),
        migrations.RunPython(
            populate_m2m,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='ocrmodel',
            name='document',
        ),
    ]
