# Generated by Django 3.2.11 on 2022-02-08 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textAnnotation', '0003_annotations_annotated'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotations',
            name='author',
            field=models.CharField(default='default_val', max_length=100),
        ),
    ]
