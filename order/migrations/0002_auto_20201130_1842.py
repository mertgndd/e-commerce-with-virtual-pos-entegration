# Generated by Django 2.2.12 on 2020-11-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='beden',
            field=models.CharField(choices=[('', 'Beden Seçiniz.'), ('S-M', 'S-M'), ('L-XL', 'L-XL'), ('Tek Ebat', 'Tek Ebat')], max_length=10),
        ),
    ]
