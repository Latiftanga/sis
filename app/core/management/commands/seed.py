# from django.core.management.base import BaseCommand
# import random

# MODE_REFRESH = 'refresh'
# MODE_CLEAR = 'clear'

# class Command(BaseCommand):
#     help = "Seed database for testing and development."

#     def add_arguments(self, parser):
#         parser.add_argument('--mode', type=str, help="Mode")

#     def handle(self, *args, **options):
#         self.stdout.write('Seeding data...')
#         run_seed(self, options['mode'])
#         self.stdout.write('Done.')

# def clear_data():
#     # Delete all table data
#     Address.objects.all().delete()

# def create_address():
#     # Create an address object with random data
#     # (customize this as needed)
#     # Example: street_flats, street_localities, pincodes
#     address = Address(
#         street_flat=random.choice(street_flats),
#         street_locality=random.choice(street_localities),
#         pincode=random.choice(pincodes),
#     )
#     address.save()

# def run_seed(self, mode):
#     # Clear data from tables
#     clear_data()
#     if mode == MODE_CLEAR:
#         return
#     # Create 15 addresses (customize as needed)
#     for i in range(15):
#         create_address()