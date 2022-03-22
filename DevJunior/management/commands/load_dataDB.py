from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from DevJunior.models import Specialty, Company, Vacancy
from DevJunior.data import specialties, companies, jobs


class Command(BaseCommand):
    def handle(self, *args, **options):
        Specialty.objects.all().delete()
        Company.objects.all().delete()
        Vacancy.objects.all().delete()

        for specialty in specialties:
            Specialty.objects.create(**specialty)

        for company in companies:
            Company.objects.create(
                name=company['title'],
                location=company['location'],
                logo=company['logo'],
                description=company['description'],
                employee_count=int(company['employee_count']),
                owner=User.objects.get(id=company['owner']),
            )

        for job in jobs:
            Vacancy.objects.create(
                title=job['title'],
                specialty=Specialty.objects.get(code=job['specialty']),
                company=Company.objects.get(id=int(job['company'])),
                skills=job['skills'],
                description=job['description'],
                salary_min=float(job['salary_from']),
                salary_max=float(job['salary_to']),
                published_at=job['posted'],
            )
