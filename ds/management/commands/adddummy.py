import random
from itertools import islice
from faker import Faker

from django.core.management.base import BaseCommand, CommandError
from ds.models import LeaderBoard, ProgrammingLanguage

fak = Faker()
PROGRAMMING_LANGUAGE = ["python", "c", "c++", "java", "R", "GO", "bash", "PyPy", "Pearl", "C#", "swift", "kotlin"]


class GenerateData(object):
    def __init__(self, data_size=100, **kwargs):
        self.data_size = data_size
        self.faker = Faker()

    @staticmethod
    def get_language():
        return {
            "name": random.choice(PROGRAMMING_LANGUAGE)
        }

    @staticmethod
    def get_score():
        return random.uniform(0.0, 95.0)

    @staticmethod
    def generate_data():
        data = {
            "name": fak.name(),
            "email": fak.email(),
            "organizer": fak.company(),
            "country": fak.country(),
            "score": random.uniform(0.0, 95.0),
            "time": "{}:{}".format(random.randint(1, 2000), random.randint(0, 59))
        }
        return data

    def add_data_to_db(self, batch_size=100):
        objects = (LeaderBoard(
                **self.generate_data(),
                language=ProgrammingLanguage.objects.get_or_create(**self.get_language())[0])
                   for i in range(self.data_size))
        while True:
            batch = list(islice(objects, batch_size))
            if not batch:
                break
            LeaderBoard.objects.bulk_create(batch, batch_size)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('batch_size', nargs='+', type=int)

    def handle(self, *args, **options):
        batch_size = options['batch_size'][0]
        g = GenerateData(batch_size)
        g.add_data_to_db()
        self.stdout.write(self.style.SUCCESS('Successfully created dummy entries'))
