# Generated by Django 2.2.10 on 2020-03-30 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercury', '0017_agevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gfconfig',
            name='gf_db_grafana_name',
        ),
    ]
