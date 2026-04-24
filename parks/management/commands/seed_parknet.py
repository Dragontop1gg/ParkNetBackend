from django.core.management.base import BaseCommand

from parks.models import ImprovementProject, Park, TreeMarker


class Command(BaseCommand):
    help = "Seed demo parks, tree markers, and improvement projects"

    def handle(self, *args, **options):
        if Park.objects.exists():
            self.stdout.write(self.style.WARNING("Parks already exist; skipping seed."))
            return

        cp, _ = Park.objects.get_or_create(
            slug="central-park",
            defaults={
                "name": "Central Park",
                "city": "New York",
                "region": "NY",
                "latitude": 40.7829,
                "longitude": -73.9654,
                "acreage": 843,
                "status": Park.Status.HEALTHY,
                "condition_index": 94,
                "total_trees": 18240,
            },
        )
        sp, _ = Park.objects.get_or_create(
            slug="silverwood-park",
            defaults={
                "name": "Silverwood Park",
                "city": "Austin",
                "region": "TX",
                "latitude": 30.2672,
                "longitude": -97.7431,
                "acreage": 120,
                "status": Park.Status.OPEN_NOW,
                "condition_index": 88,
                "total_trees": 2100,
            },
        )
        oc, _ = Park.objects.get_or_create(
            slug="oak-creek-path",
            defaults={
                "name": "Oak Creek Path",
                "city": "Portland",
                "region": "OR",
                "latitude": 45.5152,
                "longitude": -122.6784,
                "acreage": 45,
                "status": Park.Status.BUSY,
                "condition_index": 79,
                "total_trees": 890,
            },
        )

        for p, coords in [
            (cp, [(40.785, -73.968), (40.78, -73.96), (40.775, -73.97)]),
            (sp, [(30.268, -97.744), (30.266, -97.742)]),
            (oc, [(45.516, -122.68), (45.514, -122.677)]),
        ]:
            for lat, lng in coords:
                TreeMarker.objects.get_or_create(
                    park=p, lat=lat, lng=lng, defaults={"label": ""}
                )

        ImprovementProject.objects.get_or_create(
            title="North Park Reforestation",
            park=cp,
            defaults={
                "progress_percent": 75,
                "reward_points": 120,
                "is_active": True,
            },
        )
        ImprovementProject.objects.get_or_create(
            title="Trail Lighting Upgrade",
            park=sp,
            defaults={
                "progress_percent": 40,
                "reward_points": 80,
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo parks and markers created."))
