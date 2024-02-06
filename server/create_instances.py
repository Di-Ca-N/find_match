from accounts.models import User
from teams.models import Team
from competition.models import Competition, CompetitionSubscription
from sports.models import Sport, Modality
from django.contrib.auth.models import Group

def create_sports():
    sports = {
        "Futebol": [
            ("Futebol de Campo", 11),
            ("Futsal", 5),
            ("Futebol de 7", 7)
        ],
        "Vôlei": [
            ("Vôlei de praia", 2),
            ("Vôlei de quadra", 6),
        ],
        "Xadrez": [
            ("Rápido", 1),
            ("Blitz", 1),
            ("Clássico", 1)
        ],
        "Natação": [
            ("400m rasos", 1),
            ("Revezamento 4x100", 4)
        ]
    }
    for sport, modalities in sport.items():
        obj = Sport.objects.create(name=sport)
        for mname, tsize in modalities:
            Modality.objects.create(sport=obj, name=mname, team_size=tsize)

def create_users():
    leaders = ["lider1", "lider2", "lider3"]
    for leader in leaders:
        l = User.objects.create_user(
            username=leader,
            email=f"{leader}@gmail.com",
            password="testeteste"
        )
        l.groups.add(Group.objects.get(name="leaders"))
    l = User.objects.
    organizers = ["organizador1", "organizador2"]

def main():
    create_sports()
    create_users


    
