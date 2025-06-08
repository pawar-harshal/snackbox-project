from django.core.management.base import BaseCommand
from core.models import Snack

class Command(BaseCommand):
    help = 'Categorizes existing snacks based on their names'

    def handle(self, *args, **kwargs):
        # Define category mappings based on keywords in snack names
        category_mappings = {
            'chips': 'chips_crisps',
            'crisps': 'chips_crisps',
            'bars': 'bars_bites',
            'bites': 'bars_bites',
            'popcorn': 'popcorn_puffs',
            'puffs': 'popcorn_puffs',
            'crackers': 'crackers_clusters',
            'clusters': 'crackers_clusters',
            'dried': 'dried_fruits',
            'fruits': 'dried_fruits',
            'roasted': 'roasted_spiced',
            'spiced': 'roasted_spiced',
            'cookies': 'cookies_sweets',
            'sweets': 'cookies_sweets',
        }

        snacks = Snack.objects.all()
        if not snacks:
            self.stdout.write(self.style.WARNING('No snacks found in the database'))
            return

        updated_count = 0
        for snack in snacks:
            # Skip if already categorized (not 'specialty')
            if snack.category != 'specialty':
                continue

            # Normalize snack name for matching
            snack_name = snack.name.lower()
            assigned = False

            # Check for keywords in the snack name
            for keyword, category in category_mappings.items():
                if keyword in snack_name:
                    snack.category = category
                    snack.save()
                    self.stdout.write(self.style.SUCCESS(f"Categorized '{snack.name}' as '{category}'"))
                    updated_count += 1
                    assigned = True
                    break

            if not assigned:
                self.stdout.write(self.style.WARNING(f"Could not categorize '{snack.name}', leaving as 'specialty'"))

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} snacks with categories"))