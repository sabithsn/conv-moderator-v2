# Generated by Django 3.2.11 on 2022-02-08 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textAnnotation', '0008_alter_annotations_selection'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotations',
            name='context_helpful',
            field=models.IntegerField(default=0),
        ),
    ]
