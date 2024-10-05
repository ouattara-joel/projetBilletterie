from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


# ///////////////////// MODEL UTILISATEUR /////////////////////////////////

class CustomUser(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Assure que l'email est unique
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.username
# ///////////////////// MODEL EVENEMENT /////////////////////////////////

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    heure = models.TimeField()
    lieu = models.CharField(max_length=255)
    nombre_places = models.IntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='evenements/', null=True, blank=True)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Clé étrangère vers l'utilisateur

    def __str__(self):
        return self.titre


class Ticket(models.Model):
    nom_beneficiaire = models.CharField(max_length=100)
    prenom_beneficiaire = models.CharField(max_length=100)
    email_beneficiaire = models.EmailField()
    numero_whatsapp = models.CharField(max_length=10)
    evenement = models.ForeignKey('Evenement', on_delete=models.CASCADE)  # Clé étrangère vers l'événement
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    scanne = models.BooleanField(default=False)  # Champ pour le statut du scan

    def __str__(self):
        return f"Ticket pour {self.nom_beneficiaire} {self.prenom_beneficiaire} - {self.evenement.titre}"
    