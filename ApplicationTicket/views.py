from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Evenement  # Assurez-vous que le modèle Evenement est bien importé
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from .models import Evenement


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from io import BytesIO
import qrcode
from django.core.files import File
from .models import Evenement, Ticket  # Assure-toi d'importer tes modèles


from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages


from django.core.paginator import Paginator
from django.shortcuts import render



def accueil(request):
    # Récupérer tous les événements
    evenements = Evenement.objects.all()
    
    # Ajouter la pagination (5 événements par page par exemple)
    paginator = Paginator(evenements, 6)  # 5 événements par page
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis l'URL
    page_obj = paginator.get_page(page_number)  # Obtenir la page d'événements

    context = {
        'page_obj': page_obj,  # Passer la page au contexte
    }
    
    return render(request, 'accueil.html', context)


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})



from django.http import HttpResponse
from PIL import Image, ImageDraw
import qrcode

def telecharger_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Récupère l'image de l'événement et le QR code
    evenement_image = Image.open(ticket.evenement.image.path)
    qr_code_image = Image.open(ticket.qr_code.path)

    # Combine les deux images (cela nécessite un ajustement en fonction des tailles)
    evenement_image = evenement_image.resize((300, 300))
    qr_code_image = qr_code_image.resize((150, 150))

    combined_image = Image.new('RGB', (300, 450), 'white')
    combined_image.paste(evenement_image, (0, 0))
    combined_image.paste(qr_code_image, (75, 300))

    # Envoie l'image comme fichier téléchargeable
    response = HttpResponse(content_type="image/png")
    combined_image.save(response, "PNG")
    response['Content-Disposition'] = f'attachment; filename=ticket_{ticket.nom_beneficiaire}.png'
    return response

import re

def ticket_evenement(request, evenement_id):
    # Récupère l'événement avec l'ID
    evenement = get_object_or_404(Evenement, id=evenement_id)
    
    # Vérifie si le formulaire a été soumis
    if request.method == 'POST':
        # Récupère les informations du formulaire
        nom = request.POST.get('Nom', '').strip()
        prenom = request.POST.get('Prénom', '').strip()
        email = request.POST.get('email', '').strip()
        numero_whatsapp = request.POST.get('number', '').strip()

        # Validation des champs requis
        if not nom or not prenom or not email or not numero_whatsapp:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'ticket_evenement.html', {'evenement': evenement})

        # Validation de l'email avec une expression régulière
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "L'email que vous avez entré n'est pas valide.")
            return render(request, 'ticket_evenement.html', {'evenement': evenement})

        # Validation du numéro WhatsApp (vérifier s'il a exactement 10 chiffres)
        if len(numero_whatsapp) != 10 or not numero_whatsapp.isdigit():
            messages.error(request, "Veuillez entrer un numéro de téléphone valide à 10 chiffres.")
            return render(request, 'ticket_evenement.html', {'evenement': evenement})

        # Vérification de l'unicité du ticket
        existing_ticket = Ticket.objects.filter(
            nom_beneficiaire=nom,
            prenom_beneficiaire=prenom,
            numero_whatsapp=numero_whatsapp,
            evenement=evenement
        ).exists()

        if existing_ticket:
            messages.error(request, "Un ticket avec les mêmes informations existe déjà.")
            return render(request, 'ticket_evenement.html', {'evenement': evenement})

        # Si toutes les validations passent, créer un nouveau ticket
        ticket = Ticket.objects.create(
            nom_beneficiaire=nom,
            prenom_beneficiaire=prenom,
            email_beneficiaire=email,
            numero_whatsapp=numero_whatsapp,
            evenement=evenement,
        )

        # Génération du QR code
        qrcode_data = (
            f"Nom: {ticket.nom_beneficiaire}\n"
            f"Prénom: {ticket.prenom_beneficiaire}\n"
            f"Email: {ticket.email_beneficiaire}\n"
            f"Numéro WhatsApp: {ticket.numero_whatsapp}\n"
            f"Événement: {ticket.evenement.titre}"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qrcode_data)
        qr.make(fit=True)

        # Convertir en image
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Sauvegarde du QR code dans le ticket
        ticket.qr_code.save(f'{ticket.nom_beneficiaire}_qrcode.png', File(buffer), save=True)

        # Redirige vers la page de confirmation ou de détails du ticket
        return redirect('ticket_detail', ticket_id=ticket.id)

    # Si c'est une requête GET, affiche simplement le formulaire
    return render(request, 'ticket_evenement.html', {'evenement': evenement})

def message_utilisateur(request):
    user = request.user  # Utilisateur connecté
    context = {
        'username': user.username,
        'nom': user.nom,            # Nom
        'prenom': user.prenom,      # Prénom
        'email': user.email,        # Email
        'image': user.image.url if user.image else None,  # Image de profil
    }

    return render(request, 'message_utilisateur.html', context)

# /////////////////////// VUE DE DASHBORD ////////////////////

def Dashbord(request):
   

    return render(request, 'index.html', context)

# views.py

from django.shortcuts import render
from .models import Evenement, Ticket  # Assurez-vous d'importer Ticket

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    evenements = Evenement.objects.filter(utilisateur=request.user)
    
    # Prépare une liste d'événements avec leurs tickets
    evenement_list = []
    for evenement in evenements:
        # Récupérer les tickets associés à chaque événement
        tickets = Ticket.objects.filter(evenement=evenement)

        # Compter les tickets scannés et non scannés
        tickets_scannes = tickets.filter(scanne=True).count()
        tickets_non_scannes = tickets.count() - tickets_scannes
        
        evenement_list.append({
            'evenement': evenement,
            'tickets': tickets,
            'tickets_scannes': tickets_scannes,
            'tickets_non_scannes': tickets_non_scannes,
        })

    user = request.user  # Utilisateur connecté
    context = {
        'evenement_list': evenement_list,  # Liste d'événements avec leurs tickets
        'username': user.username,
        'nom': user.nom,            # Nom
        'prenom': user.prenom,      # Prénom
        'email': user.email,        # Email
        'image': user.image.url if user.image else None,  # Image de profil
    }
    
    return render(request, 'index.html', context)


@login_required
def evenement(request):
    user = request.user

    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.POST.get('titre')
        date = request.POST.get('date')
        heure = request.POST.get('heure')
        lieu = request.POST.get('lieu')
        nombre_places = request.POST.get('places')
        montant = request.POST.get('montant')
        image = request.FILES.get('image')  # Récupérer l'image si elle est téléchargée

        # Validation des données
        if not all([titre, date, heure, lieu, nombre_places, montant]):
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            try:
                # Créer l'objet Evenement
                evenement = Evenement(
                    titre=titre,
                    date=datetime.strptime(date, '%Y-%m-%d').date(),
                    heure=datetime.strptime(heure, '%H:%M').time(),
                    lieu=lieu,
                    nombre_places=int(nombre_places),
                    montant=int(montant),
                    image=image,  # L'image peut être None si non fournie
                    utilisateur=user  # L'utilisateur connecté est lié à l'événement
                )

                # Sauvegarder l'événement dans la base de données
                evenement.save()

                # Message de succès
                messages.success(request, "Événement créé avec succès !")

                # Redirection après création réussie (si nécessaire)
                return redirect('evenement')

            except ValueError as e:
                messages.error(request, f"Erreur de format: {e}")

    # Récupérer tous les événements créés par l'utilisateur connecté
    evenements = Evenement.objects.filter(utilisateur=request.user)


    # Contexte utilisateur et événements pour le rendu du formulaire
    context = {
        'username': user.username,
        'nom': user.nom,
        'prenom': user.prenom,
        'email': user.email,
        'image': user.image.url if user.image else None,
        'evenements': evenements,  # Passer les événements au contexte
    }

    return render(request, 'evenement.html', context)



@login_required
def controle_ticket(request):
    evenements = Evenement.objects.filter(utilisateur=request.user)  # Récupérer les événements de l'utilisateur connecté

    # Pagination
    paginator = Paginator(evenements, 5)  # 5 événements par page (ajuste ce nombre si nécessaire)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'username': request.user.username,
        'nom': request.user.nom,
        'prenom': request.user.prenom,
        'email': request.user.email,
        'image': request.user.image.url if request.user.image else None,
        'page_obj': page_obj,  # Passer l'objet de pagination à ton template
    }

    return render(request, 'controle_ticket.html', context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def scan_ticket(request, evenement_id):
    if request.method == 'POST':
        decoded_text = request.POST.get('decoded_text')  # Obtenez le texte décodé du ticket
        
        # Vérifier si le ticket existe
        ticket = get_object_or_404(Ticket, code=decoded_text)

        # Récupérer l'événement associé à l'identifiant
        evenement = get_object_or_404(Evenement, id=evenement_id)
        
        # Vérifier si le ticket appartient à l'événement
        if ticket.evenement != evenement:
            return JsonResponse({'success': False, 'message': "Ce ticket n'appartient pas à cet événement."})

        # Vérifier si le ticket a déjà été scanné
        if ticket.scanne:
            return JsonResponse({'success': False, 'message': "Ce ticket a déjà été scanné."})
        
        # Si toutes les vérifications passent, marquez le ticket comme scanné
        ticket.scanne = True
        ticket.save()

        return JsonResponse({'success': True, 'message': "Ticket scanné avec succès.", 'event': evenement.nom})

    # Retourne une réponse si la méthode n'est pas POST
    return JsonResponse({'success': False, 'message': "Méthode non autorisée. Veuillez utiliser POST."})



@login_required
def password(request):
    user = request.user  # Utilisateur connecté
    context = {
        'username': user.username,
        'nom': user.nom,            # Nom
        'prenom': user.prenom,      # Prénom
        'email': user.email,        # Email
        'image': user.image.url if user.image else None,  # Image de profil
    }
    return render(request, 'password.html', context)


@login_required
def settings(request):
    user = request.user  # Utilisateur connecté
    context = {
        'username': user.username,
        'nom': user.nom,            # Nom
        'prenom': user.prenom,      # Prénom
        'email': user.email,        # Email
        'image': user.image.url if user.image else None,  # Image de profil
    }
    return render(request, 'settings.html',context)

@login_required
def deconnexion(request):
    user = request.user  # Utilisateur connecté
    context = {
        'username': user.username,
        'nom': user.nom,            # Nom
        'prenom': user.prenom,      # Prénom
        'email': user.email,        # Email
        'image': user.image.url if user.image else None,  # Image de profil
    }
    return render(request, 'deconnexion.html',context)

# /////////////////////// VUE DE CONNEXION ////////////////////

def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('index')  # Redirection vers la page d'accueil ou une autre page
        else:
            messages.error(request, "Identifiants invalides")
            
    return render(request, 'connexion.html')


# /////////////////////// VUE DE CREATION DE COMPTE UTILISATEUR ////////////////////

def creer_compte(request):
    if request.method == 'POST':
        nom = request.POST.get('Nom')
        prenom = request.POST.get('Prénom')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')
        image = request.FILES.get('image')

        # Initialisation d'un dictionnaire pour stocker les erreurs par champ
        errors = {
            'email': None,
        }

        # Vérification des champs requis
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Cet email est déjà utilisé'

        if any(errors.values()):  # Si au moins une erreur est présente
            return render(request, 'creer_compte.html', {'errors': errors})

        utilisateur = CustomUser(
            username=email,
            nom=nom,
            prenom=prenom,
            email=email,
            image=image
        )
        utilisateur.set_password(mot_de_passe)
        utilisateur.save()

        login(request, utilisateur)
        messages.success(request, "Compte créé avec succès")

        return redirect('connexion')

    return render(request, 'creer_compte.html')





def supprimer_evenement(request, id):
    # Tente de récupérer l'événement ou renvoie une 404 s'il n'existe pas
    evenement = get_object_or_404(Evenement, id=id)

    if request.method == 'POST':
        # Supprime l'événement
        evenement.delete()
        # Ajoute un message de succès
        messages.success(request, 'Événement supprimé avec succès !')
        # Redirige vers la vue de la liste des événements
        return redirect('evenement')  # Assurez-vous que cette URL est correcte

    # Rendre le template de confirmation
    return render(request, 'supprimer_evenement.html', {'evenement': evenement})

def modifier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.POST.get('titre')
        date = request.POST.get('date')
        heure = request.POST.get('heure')
        lieu = request.POST.get('lieu')
        places = request.POST.get('places')
        montant = request.POST.get('montant')
        image = request.FILES.get('image')

        # Mettre à jour l'événement
        evenement.titre = titre
        evenement.date = date
        evenement.heure = heure
        evenement.lieu = lieu
        evenement.nombre_places = places
        evenement.montant = montant

        if image:  # Si une nouvelle image est téléchargée
            evenement.image = image

        evenement.save()  # Enregistrer les modifications
        messages.success(request, "L'événement a été modifié avec succès.")
        return redirect('evenement')  # Rediriger vers la liste des événements

    return render(request, 'modifier_evenement.html', {'evenement': evenement})