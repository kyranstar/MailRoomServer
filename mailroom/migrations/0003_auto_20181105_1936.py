# Generated by Django 2.0.4 on 2018-11-06 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailroom', '0002_emailtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]