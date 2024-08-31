import os
from django.core.management import call_command
from core.models import Region, District

def seed_regions_and_districts():
    # Create some regions
    regions = [
        Region(name="Ashanti Region", code="AR"),
        Region(name="Bono Region", code="BR"),
        Region(name="Bono East Region", code="BE"),
        Region(name="Ahafo Region", code="AH"),
        Region(name="Central Region", code="CR"),
        Region(name="Eastern Region", code="ER"),
        Region(name="Greater Accra Region", code="GA"),
        Region(name="Northern Region", code="NR"),
        Region(name="Savannah Region", code="SR"),
        Region(name="North East Region", code="NE"),
        Region(name="Upper East Region", code="UE"),
        Region(name="Upper West Region", code="UW"),
        Region(name="Volta Region", code="VR"),
        Region(name="Oti Region", code="OR"),
        Region(name="Western Region", code="WR"),
        Region(name="Western North Region", code="WN")
    ]
    Region.objects.bulk_create(regions)

    # Create some districts for Greater Accra
    greater_accra = Region.objects.get(name="Greater Accra")
    districts = [
        District(name="Accra Metro", region=greater_accra),
        District(name="Tema Metro", region=greater_accra),
        District(name="Ga East", region=greater_accra),
    ]
    District.objects.bulk_create(districts)

    # ... Add more districts for other regions

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    call_command('migrate')
    seed_regions_and_districts()
