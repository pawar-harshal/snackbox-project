# Generated by Django 5.2.1 on 2025-05-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_passwordresettoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snack',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='snack',
            name='stock',
        ),
        migrations.AddField(
            model_name='snack',
            name='category',
            field=models.CharField(choices=[('chips_crisps', 'Chips & Crisps'), ('bars_bites', 'Bars & Bites'), ('popcorn_puffs', 'Popcorn & Puffs'), ('crackers_clusters', 'Crackers & Clusters'), ('dried_fruits', 'Dried Fruits & Slices'), ('roasted_spiced', 'Roasted & Spiced Snacks'), ('cookies_sweets', 'Cookies & Sweets'), ('specialty', 'Specialty Snacks')], default='specialty', max_length=50),
        ),
        migrations.AlterField(
            model_name='snack',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='snacks/'),
        ),
        migrations.AlterField(
            model_name='snack',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
