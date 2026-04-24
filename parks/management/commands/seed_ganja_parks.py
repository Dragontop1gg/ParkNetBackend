from django.core.management.base import BaseCommand
from parks.models import Park, TreeMarker

class Command(BaseCommand):
    help = "Seed Ganja parks with historical descriptions and media."

    def handle(self, *args, **options):
        parks_data = [
            {
                "name": "Heydər Əliyev Park-Kompleksi",
                "slug": "heydar-aliyev-park",
                "city": "Gəncə",
                "region": "Ganja-Dashkasan",
                "latitude": 40.7128,
                "longitude": 46.3600,
                "acreage": 450,
                "status": Park.Status.HEALTHY,
                "condition_index": 95,
                "total_trees": 50000,
                "description": "Heydər Əliyev Park-Kompleksi — Azərbaycanın və Cənubi Qafqazın ən böyük üç parkından biridir. Ümumi sahəsi 450 hektar (4.5 km²) olan park-kompleksinin əhatə etdiyi ərazidə İncəsənət Muzeyi, Amfiteatr, süni göl yaradılmışdır, parkın girişində Zəfər tağı yerləşir. Park-Kompleksinin açılışı 2014-cü ilin yanvarın 21-də baş tutmuşdur.",
                "hero_image": "parks/Heydər Əliyev Park-Kompleksi.jpeg",
                "markers": [(40.7130, 46.3605), (40.7125, 46.3595)]
            },
            {
                "name": "Xan Bağı",
                "slug": "xan-bagi",
                "city": "Gəncə",
                "region": "Ganja-Dashkasan",
                "latitude": 40.6775,
                "longitude": 46.3603,
                "acreage": 7,
                "status": Park.Status.OPEN_NOW,
                "condition_index": 92,
                "total_trees": 1500,
                "description": "Gəncədə tarixən xanların istirahət guşəsi kimi mövcud olmuş Xan Bağı rus işğalından sonra ləğv edilmiş, oradakı ağacların bir qismi isə Sərdar Bağına köçürülmüşdür. Bağ hal-hazırda gəncəlilərin əsas istirahət guşələrindəndir.",
                "hero_image": "parks/Xan Bağı.jpeg",
                "markers": [(40.6776, 46.3604), (40.6774, 46.3602)]
            },
            {
                "name": "Gəncə Memorial Kompleksi",
                "slug": "ganja-memorial",
                "city": "Gəncə",
                "region": "Ganja-Dashkasan",
                "latitude": 40.6900,
                "longitude": 46.3600,
                "acreage": 2,
                "status": Park.Status.HEALTHY,
                "condition_index": 98,
                "total_trees": 100,
                "description": "Gəncə Memorial Kompleksi — İkinci Qarabağ müharibəsinin gedişatında Ermənistan ordusu tərəfindən törədilən mülki cinayətləri əks etdirən Azərbaycanın Gəncə şəhərində memorial.",
                "hero_image": "parks/Gəncə Memorial Kompleksi.jpeg",
                "markers": [(40.6901, 46.3601)]
            },
            {
                "name": "Əziz Əliyev adına park",
                "slug": "aziz-aliyev-park",
                "city": "Gəncə",
                "region": "Ganja-Dashkasan",
                "latitude": 40.6850,
                "longitude": 46.3550,
                "acreage": 5,
                "status": Park.Status.OPEN_NOW,
                "condition_index": 85,
                "total_trees": 800,
                "description": "Görkəmli dövlət xadimi Əziz Əliyevin adını daşıyan mədəniyyət və istirahət parkı",
                "hero_image": "parks/Əziz Əliyev adına park.jpeg",
                "markers": [(40.6851, 46.3551)]
            }
        ]

        for data in parks_data:
            markers = data.pop("markers")
            park, created = Park.objects.update_or_create(
                slug=data["slug"],
                defaults=data
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{verb} park: {park.name}"))
            
            # Clear existing markers if updating
            park.tree_markers.all().delete()
            for lat, lng in markers:
                TreeMarker.objects.create(park=park, lat=lat, lng=lng)

        self.stdout.write(self.style.SUCCESS("Successfully seeded Ganja parks."))
