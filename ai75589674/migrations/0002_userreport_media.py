# Generated by Django 4.2.7 on 2023-11-29 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai75589674', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreport',
            name='media',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
