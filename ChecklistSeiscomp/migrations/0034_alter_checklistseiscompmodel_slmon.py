# Generated by Django 4.0.6 on 2023-03-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChecklistSeiscomp', '0033_checklistseiscompmodel_slmon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistseiscompmodel',
            name='slmon',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
    ]
