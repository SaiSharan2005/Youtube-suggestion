# Generated by Django 5.0.3 on 2024-03-20 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_documentation_documentationdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentation',
            old_name='topic_name',
            new_name='DocumentName',
        ),
    ]