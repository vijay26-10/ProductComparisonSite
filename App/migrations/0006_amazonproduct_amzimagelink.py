# Generated by Django 3.2.7 on 2021-10-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20211001_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazonproduct',
            name='amzImageLink',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]