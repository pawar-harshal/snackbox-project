# Generated by Django 5.2.1 on 2025-05-29 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_userprofile_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snack',
            name='category',
            field=models.CharField(choices=[('chips_crisps', 'Chips & Crisps'), ('bars_bites', 'Bars & Bites'), ('popcorn_puffs', 'Popcorn & Puffs'), ('crackers_clusters', 'Crackers & Clusters'), ('dried_fruits', 'Dried Fruits & Slices'), ('roasted_spiced', 'Roasted & Spiced Snacks'), ('cookies_sweets', 'Cookies & Sweets'), ('specialty', 'Specialty Snacks')], max_length=20),
        ),
    ]
