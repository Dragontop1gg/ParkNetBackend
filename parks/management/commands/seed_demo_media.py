"""
Fill DB with demo entities and attach images from backend/seed_assets/.
See seed_assets/README.txt for filenames and folders.
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from parks.models import ImprovementProject, Park, TreeMarker
from reports.models import Report

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def _find_image(seed_dir: Path, subdir: str, basename: str) -> Path | None:
    folder = seed_dir / subdir
    for ext in IMAGE_EXTENSIONS:
        p = folder / f"{basename}{ext}"
        if p.is_file():
            return p
    return None


def _attach_file(model, field_name: str, path: Path) -> bool:
    field = getattr(model, field_name)
    with path.open("rb") as f:
        field.save(path.name, File(f), save=True)
    return True


class Command(BaseCommand):
    help = "Create/update demo parks, projects, reports; attach images from seed_assets/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-reports",
            action="store_true",
            help="Skip demo reports (only parks, markers, projects and their images).",
        )

    def handle(self, *args, **options):
        seed_dir: Path = settings.SEED_ASSETS_DIR
        if not seed_dir.is_dir():
            self.stdout.write(self.style.WARNING(f"Folder missing: {seed_dir} - create it and add images."))

        cp, _ = Park.objects.update_or_create(
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
        sp, _ = Park.objects.update_or_create(
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
        oc, _ = Park.objects.update_or_create(
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

        proj_north, _ = ImprovementProject.objects.update_or_create(
            title="North Park Reforestation",
            park=cp,
            defaults={
                "progress_percent": 75,
                "reward_points": 120,
                "is_active": True,
            },
        )
        proj_trail, _ = ImprovementProject.objects.update_or_create(
            title="Trail Lighting Upgrade",
            park=sp,
            defaults={
                "progress_percent": 40,
                "reward_points": 80,
                "is_active": True,
            },
        )

        attached = 0
        for park, slug in [(cp, "central-park"), (sp, "silverwood-park"), (oc, "oak-creek-path")]:
            img = _find_image(seed_dir, "parks", slug)
            if img:
                _attach_file(park, "hero_image", img)
                attached += 1
                self.stdout.write(f"  hero_image ← {img}")
            else:
                self.stdout.write(self.style.WARNING(f"  Missing: parks/{slug}.jpg (or .png/.webp)"))

        for project, key in [
            (proj_north, "north-park-reforestation"),
            (proj_trail, "trail-lighting-upgrade"),
        ]:
            img = _find_image(seed_dir, "projects", key)
            if img:
                _attach_file(project, "thumbnail", img)
                attached += 1
                self.stdout.write(f"  project thumb ← {img}")
            else:
                self.stdout.write(self.style.WARNING(f"  Missing: projects/{key}.jpg (or .png/.webp)"))

        if not options["skip_reports"]:
            user, created = User.objects.get_or_create(
                username="parknet_demo",
                defaults={"email": "demo@parknet.local", "first_name": "Elena"},
            )
            if created or not user.has_usable_password():
                user.set_password("demo12345")
                user.save()

            bench_img = _find_image(seed_dir, "reports", "broken-bench")
            graf_img = _find_image(seed_dir, "reports", "graffiti-cleaned")

            report_bench, _ = Report.objects.update_or_create(
                user=user,
                park=sp,
                category=Report.Category.BROKEN_PATH,
                description="Broken bench near the east entrance — wood split, bolts loose.",
                defaults={
                    "status": Report.Status.IN_PROGRESS,
                    "latitude": sp.latitude,
                    "longitude": sp.longitude,
                },
            )
            if bench_img:
                _attach_file(report_bench, "image", bench_img)
                attached += 1
                self.stdout.write(f"  report image ← {bench_img}")
            else:
                self.stdout.write(self.style.WARNING("  Missing: reports/broken-bench.*"))

            report_graf, _ = Report.objects.update_or_create(
                user=user,
                park=oc,
                category=Report.Category.VANDALISM,
                description="Graffiti removed along Oak Creek trail — wall cleaned.",
                defaults={
                    "status": Report.Status.RESOLVED,
                    "latitude": oc.latitude,
                    "longitude": oc.longitude,
                },
            )
            if graf_img:
                _attach_file(report_graf, "image", graf_img)
                attached += 1
                self.stdout.write(f"  report image ← {graf_img}")
            else:
                self.stdout.write(self.style.WARNING("  Missing: reports/graffiti-cleaned.*"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Images attached: {attached}. Demo user: parknet_demo / demo12345"
            )
        )
