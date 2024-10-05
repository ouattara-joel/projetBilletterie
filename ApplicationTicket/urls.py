from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('', accueil, name='accueil'),
    path('ticket_evenement/<int:evenement_id>/', ticket_evenement, name='ticket_evenement'),

    path('index', index, name='index'),
    path('Dashbord', Dashbord, name='Dashbord'),
    path('evenement', evenement, name='evenement'),
    path('controle_ticket/', controle_ticket, name='controle_ticket'),
    path('message_utilisateur', message_utilisateur, name='message_utilisateur'),
    path('password', password, name='password'),
    path('settings', settings, name='settings'),
    path('connexion', connexion, name='connexion'),
    path('creer_compte', creer_compte, name='creer_compte'),
    path('ticket_detail/<int:ticket_id>/', ticket_detail, name='ticket_detail'),

    path('scan_ticket/<int:evenement_id>/', scan_ticket, name='scan_ticket'),
    path('evenement/supprimer/<int:id>/', supprimer_evenement, name='supprimer_evenement'),
    # path('evenement/Modifier/<int:id>/', modifier_evenement, name='modifier_evenement'),


    path('deconnexion', deconnexion, name='deconnexion'),
    

]
