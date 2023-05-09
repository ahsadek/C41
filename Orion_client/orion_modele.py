# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import random
import ast
from id import *
from helper import Helper as hlp
from threading import Timer
from math import hypot


class Mine_metaux():
    def __init__(self, propriataire):
        self.propriataire = propriataire
        self.nom = "mine metaux"
        self.coutMetaux = 50
        self.coutEnergie = 200
        self.coutPopulation = 10
        self.quantite = 1
        self.niveau = 1
        self.augmentationNiveau = 1
        self.tauxProduction = 5

class Centrale_electrique():
    def __init__(self, propriataire):
        self.propriataire = propriataire
        self.nom = "centrale_electrique"
        self.coutMetaux = 200
        self.coutEnergie = 50
        self.coutPopulation = 10
        self.quantite = 2
        self.niveau = 1
        self.augmentationNiveau = 1
        self.tauxProduction = 5

class Usine_vaiseau():
    def __init__(self, propriataire):
        self.propriataire = propriataire
        self.nom = "usine vaiseau"
        self.coutMetaux = 200
        self.coutEnergie = 200
        self.coutPopulation = 30
        self.quantite = 0
        self.niveau = 1
        self.augmentationNiveau = 1

class Laboratoire_recherche ():
    def __init__(self, propriataire):
        self.propriataire = propriataire
        self.nom = "laboratoire recherche"
        self.coutMetaux = 100
        self.coutEnergie = 300
        self.coutPopulation = 40
        self.quantite = 0
        self.niveau = 1
        self.augmentationNiveau = 1

class Systeme_defense ():
    def __init__(self, propriataire):
        self.propriataire = propriataire
        self.nom = "systeme defense"
        self.coutMetaux = 500
        self.coutEnergie = 300
        self.coutPopulation = 30
        self.quantite = 0
        self.niveau = 1
        self.augmentationNiveau = 1

class Porte_de_vers():
    def __init__(self, parent, x, y, couleur, taille):
        self.parent = parent
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.pulsemax = taille
        self.pulse = random.randrange(self.pulsemax)
        self.couleur = couleur

    def jouer_prochain_coup(self):
        self.pulse += 1
        if self.pulse >= self.pulsemax:
            self.pulse = 0


class Trou_de_vers():
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup()
        self.porte_b.jouer_prochain_coup()


class Etoile():
    def __init__(self, parent, x, y):
        self.id = get_prochain_id()
        self.parent = parent
        self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.ressources = {"metal": random.randrange(500, 1000),
                           "energie": random.randrange(5000, 10000),
                           "population": random.randrange(50, 100)}
        self.hp = 1000

        self.batiments = {
            "mines_metaux": Mine_metaux(self.id),
            "centrales_electriques": Centrale_electrique(self.id),
            "usines_vaiseau": Usine_vaiseau(self.id),
            "laboratoires_recherche": Laboratoire_recherche(self.id),
            "systemes_defense": Systeme_defense(self.id)
        }

class Espace():
    def __init__(self, x, y):
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.proprietaire = None

class Vaisseau():   # vaisseau de combat, classe faite donc implementer a faire
    def __init__(self, parent, nom, x, y):
        self.parent = parent
        self.id = get_prochain_id()
        self.proprietaire = nom
        self.x = x
        self.y = y
        self.espace_cargo = 0
        self.hp = 100
        self.delai_tir = 100        #delai en ms entre les tirs de lasers du vaisseau
        self.portee = 500
        self.en_tir = False
        self.taille = 5
        self.vitesse = 10
        self.cible = 0
        self.type_cible = None
        self.angle_cible = 0
        self.angle_cible_tir = 0
        self.cible_tir = None
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Porte_de_vers": self.arriver_porte,
                        "Espace": self.arriver_espace}
        self.liste_laser = []
        self.firing = False
    def jouer_prochain_coup(self, trouver_nouveau=0):
        #lasers
        for laser in self.liste_laser:
            if laser.cible.hp <= 0:
                self.firing = False
                self.liste_laser.remove(laser)
                continue
            laser.avancer()
            if hlp.calcDistance(laser.x, laser.y, laser.cible.x, laser.cible.y) <= laser.vitesse:
                laser.cible.hp -= laser.puissance
                if laser.cible.hp <= 0:
                    self.firing = False
                    if laser.type_cible == "Cargo":
                        del laser.cible.parent.flotte["Cargo"][laser.cible.id]
                    elif laser.type_cible == "Combat":
                        del laser.cible.parent.flotte["Combat"][laser.cible.id]
                    elif laser.type_cible == "Explo":
                        del laser.cible.parent.flotte["Explo"][laser.cible.id]
                    elif laser.type_cible == "Etoile":
                        ancien_proprietaire = laser.cible.proprietaire
                        laser.cible.proprietaire = laser.proprietaire
                        self.parent.etoilescontrolees.append(laser.cible)
                        ancien_joueur = self.parent.parent.joueurs[ancien_proprietaire]
                        ancien_joueur.etoilescontrolees.remove(laser.cible)
                        self.parent.parent.parent.afficher_etoile(self.parent.nom, laser.cible)
                        laser.cible.hp = 1000
                self.liste_laser.remove(laser)
                    
        if self.cible != 0:
            return self.avancer()
        elif trouver_nouveau:
            cible = random.choice(self.parent.parent.etoiles)
            self.acquerir_cible(cible, "Etoile")

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def acquerir_cible_espace(self, posDestinationX, posDestinationY, type_cible):
        self.type_cible = type_cible
        self.cible = Espace(posDestinationX, posDestinationY)
        self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def avancer(self):
        if self.firing:
            self.firing = False
        if self.cible != 0:
            x = self.cible.x
            y = self.cible.y
            self.angle_cible = hlp.calcAngle(self.x, self.y, self.cible.x, self.cible.y)
            self.x, self.y = hlp.getAngledPoint(self.angle_cible, self.vitesse, self.x, self.y)
            distance = hypot(self.cible.x - self.x, self.cible.y - self.y)
            #continuer, ne pas re appele la methode avancer
            if self.firing and distance <= self.portee * 0.80:
                self.tirer_laser(self.cible, self.cible.__class__.__name__)
            elif hlp.calcDistance(self.x, self.y, x, y) <= self.vitesse:
                self.x = x
                self.y = y
                type_obj = type(self.cible).__name__
                rep = self.arriver[type_obj]()
                return rep
        
        
    def avancer_combat(self):
        if self.cible_tir != None:
            x = self.cible_tir.x
            y = self.cible_tir.y
            self.angle_cible_tir = hlp.calcAngle(self.x, self.y, x, y)
            self.x, self.y = hlp.getAngledPoint(self.angle_cible_tir, self.vitesse, self.x, self.y)
            distance = hypot(self.cible_tir.x - self.x, self.cible_tir.y - self.y)
            if self.firing and distance >= self.portee * 0.80:
                next = Timer(0.075, self.tirer_laser, args=(self.cible_tir, self.cible_tir.__class__.__name__))
                next.start()
            

    def arriver_etoile(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Etoile", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire and isinstance(self, Cargo):
            self.cible.proprietaire = self.proprietaire
            self.parent.update_points([self.parent.nom, 15])
        cible = self.cible
        self.cible = 0
        return ["Etoile", cible]

    def arriver_espace(self):
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Espace", self.id, self.cible.id, self.cible.proprietaire])
        cible = self.cible
        self.cible = 0
        return ["Espace", cible]

    def arriver_porte(self):
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]
    
    def tirer_laser(self, cible, type_cible):
        self.cible_tir = cible
        distance = hypot(cible.x - self.x, cible.y - self.y)
        if self.firing == True and cible.proprietaire != self.proprietaire:
            if (self.portee >= distance):
                self.liste_laser.append(Laser(self, self.proprietaire, self.x, self.y, cible, type_cible))
                tir = Timer(0.25, self.tirer_laser, args=(cible, type_cible))
                tir.start()
            else:
                self.avancer_combat()


class Cargo(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.cargo = 1000
        self.hp = 300
        self.taille = 6
        self.vitesse = 5
        self.cible = 0
        self.ang = 0
        self.prixMetal = 9000
        self.prixEnergie = 8000
        self.prixPopulation = 100

class Combat(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.combat = 1000
        self.energie = 500
        self.hp = 150
        self.taille = 6
        self.vitesse = 12
        self.cible = 0
        self.ang = 0
        self.prixMetal = 10000
        self.prixEnergie = 9000
        self.prixPopulation = 120

class Exploration(Vaisseau):
    def __init__(self, parent, nom, x, y):
        Vaisseau.__init__(self, parent, nom, x, y)
        self.exploration = 1000
        self.hp = 75
        self.energie = 500
        self.taille = 6
        self.vitesse = 25
        self.cible = 0
        self.ang = 0
        self.prixMetal = 7000
        self.prixEnergie = 6000
        self.prixPopulation = 80
        
        
class Laser(Vaisseau):
    def __init__(self, parent, nom, x, y, cible, type_cible):
        super().__init__(parent, nom, x, y)
        self.puissance = 5
        self.taille = 2
        self.vitesse = 25
        self.cible = cible
        self.type_cible = type_cible
        self.arriver = {"Etoile": self.arriver_etoile,
                        "Combat": self.arriver_vaisseau,
                        "Cargo": self.arriver_vaisseau,
                        "Exploration": self.arriver_vaisseau}


    def arriver_etoile(self):
        cible = self.cible
        return ["Etoile", cible]


    def arriver_vaisseau(self):
        cible = self.cible
        return ["Vaisseau", cible]
    
    
class Joueur():
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoileselect = None
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.coloniser = None
        self.etoilescontrolees = [etoilemere]
        self.id_etoile = None
        self.flotte = {"Explo": {},
                       "Cargo": {},
                       "Combat": {}}
        self.actions = {"creervaisseau": self.creervaisseau,
                        "ciblerflotte": self.ciblerflotte,
                        "ciblerflotteespace": self.ciblerFlotteEspace,
                        "creerlaser": self.creerlaser,
                        "update_points": self.update_points,
                        "update_coloniser": self.update_coloniser,
                        "lancer_timer": self.lancer_timer}

        self.nbrPoints = 0
        self.nbrMetal = 10000
        self.nbrEnergie = 10000
        self.nbrPopulation = 500

        self.batiments = {
            "mines_metaux": Mine_metaux(self.nom),
            "centrales_electriques": Centrale_electrique(self.nom),
            "usines_vaiseau": Usine_vaiseau(self.nom),
            "laboratoires_recherche": Laboratoire_recherche(self.nom),
            "systemes_defense": Systeme_defense(self.nom)
        }
        
        
    def lancer_timer(self, params):
        nb_minutes = params[0]
        self.parent.minutes = nb_minutes
        self.parent.update_timer()
        
        
    def update_points(self, params):
        joueur, points = params
        self.parent.joueurs[joueur].nbrPoints += points
    
    
    def update_coloniser(self, params):
        joueur, action = params
        self.parent.joueurs[joueur].coloniser = action
        
        
    def creervaisseau(self, params):
        type_vaisseau = params[0]
        
        id_etoilecourante = params[1]
        etoilecourante = None

        if id_etoilecourante == self.etoilemere.id:
            etoilecourante = self.etoilemere
        else:
            for etoile in self.parent.etoiles:
                if etoile.id == id_etoilecourante:
                    etoilecourante = etoile
                    break
        
        if type_vaisseau == "Cargo":
            v = Cargo(self, self.nom, etoilecourante.x + 10, etoilecourante.y)
        elif type_vaisseau == "Explo":
            v = Exploration(self, self.nom, etoilecourante.x + 10, etoilecourante.y)
        elif type_vaisseau == "Combat":
            v = Combat(self, self.nom, etoilecourante.x + 10, etoilecourante.y)
        # else:
        #     v = Vaisseau(self, self.nom, self.etoilemere.x + 10, self.etoilemere.y)

        self.flotte[type_vaisseau][v.id] = v

        if self.nom == self.parent.parent.mon_nom:
            self.parent.parent.lister_objet(self)
        return v
    
    
    def creerlaser(self, params):
        id_parent, id_cible, proprietaire_cible, type_cible = params
        
        vaisseau_parent = self.parent.joueurs[self.nom].flotte["Combat"][id_parent]
        if type_cible == "Etoile":
            for etoile in self.parent.etoiles:
                if etoile.id == id_cible:
                    cible = etoile
                    break
            for joueur in self.parent.joueurs:
                for etoile in self.parent.joueurs[joueur].etoilescontrolees:
                    if etoile.id == id_cible:
                        cible = etoile
                        break
        else:
            if self.parent.joueurs[proprietaire_cible].flotte[type_cible][id_cible] != None:
                cible = self.parent.joueurs[proprietaire_cible].flotte[type_cible][id_cible]
        
        vaisseau_parent.firing = True
        vaisseau_parent.tirer_laser(cible, type_cible)
        
    

    def ciblerflotte(self, ids):
        idori, iddesti, type_cible, type_origine = ids
        ori = None
        
        if type_origine == "Combat":
            self.parent.joueurs[self.nom].flotte["Combat"][idori].firing = False

        if idori in self.flotte["Cargo"]:       # laisser ce bout de code ici, sinon tout casse
            ori = self.flotte["Cargo"][idori]

        if idori in self.flotte["Explo"]:  # laisser ce bout de code ici, sinon tout casse
            ori = self.flotte["Explo"][idori]

        for i in self.flotte:   # code prof, fonctionne seulement pour vaisseau
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        # if ori: # deplacements entre des objets avec des id
            if ori != None:
                if type_cible == "Etoile":
                    for j in self.parent.etoiles:
                        if j.id == iddesti:
                            ori.acquerir_cible(j, type_cible)
                            return
                elif type_cible == "Porte_de_ver":
                    cible = None
                    for j in self.parent.trou_de_vers:
                        if j.porte_a.id == iddesti:
                            cible = j.porte_a
                        elif j.porte_b.id == iddesti:
                            cible = j.porte_b
                        if cible:
                            ori.acquerir_cible(cible, type_cible)
                            return
                else:
                    pass

    def ciblerFlotteEspace(self, params):
        idOrigine, posDestinationX, posDestinationY, typeCible, type_origine = params
        if type_origine == "Combat":
            self.parent.joueurs[self.nom].flotte["Combat"][idOrigine].firing = False
        ori = None
        for i in self.flotte.keys():
            if idOrigine in self.flotte[i]:
                ori = self.flotte[i][idOrigine]
        if ori != None:
            ori.acquerir_cible_espace(posDestinationX, posDestinationY, "Espace")
        return

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile":
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoilescontrolees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        if self.coloniser == "Coloniser":
                            print("test")
                            self.etoilescontrolees.append(rep[1])
                            self.parent.parent.afficher_etoile(self.nom, rep[1])
                        #########################################################################################################################################################
                        for etoile in self.etoilescontrolees:
                            if etoile.id == self.id_etoile or self.id_etoile == rep[1].id:
                                self.parent.parent.afficher_ressources(self.id_etoile)
                        #########################################################################################################################################################
                        
                        #########################################################################################################################################################
                    elif rep[0] == "Porte_de_ver":
                        pass                        


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoilemere, couleur):
        Joueur.__init__(self, parent, nom, etoilemere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20

    def jouer_prochain_coup(self):
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            # , self.etoilemere.id
            v = self.creervaisseau(["Explo", self.etoilemere.id])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1

class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)
        self.minutes = 00
        self.secondes = 00
        self.jeu_actif = True
        
        
    
        
        
    def update_timer(self):
        if self.minutes == 0 and self.secondes == 0:
            
            self.parent.afficher_fin_jeu(self.select_joueur_gagnant())
            pass
        else:
            if self.secondes > 0:
                self.secondes -= 1
            else:
                self.minutes -= 1
                self.secondes = 59

            self.boucle_timer = Timer(1.0, self.update_timer)
            self.parent.update_timer_vue()
            self.boucle_timer.start()  
            
            
    def select_joueur_gagnant(self):
        joueur_gagnant = []
        for joueur in self.joueurs:
            if len(joueur_gagnant) == 0:
                joueur_gagnant.append(self.joueurs[joueur])
            else:
                if self.joueurs[joueur].nbrPoints > joueur_gagnant[0].nbrPoints:
                    joueur_gagnant = [self.joueurs[joueur]]
                elif self.joueurs[joueur].nbrPoints == joueur_gagnant[0].nbrPoints:
                        joueur_gagnant.append(self.joueurs[joueur])
        return joueur_gagnant
    
    
    def production_ressource(self):
        for joueur in self.joueurs:
            for etoile in self.joueurs[joueur].etoilescontrolees:
                #etoile.batiments["mines_metaux"]
                self.joueurs[joueur].nbrMetal += etoile.batiments["mines_metaux"].quantite * etoile.batiments["mines_metaux"].tauxProduction
                self.joueurs[joueur].nbrEnergie += etoile.batiments["centrales_electriques"].quantite * etoile.batiments["centrales_electriques"].tauxProduction
                pointsMetaux = self.joueurs[joueur].nbrMetal * 0.000025
                pointsEnergie = self.joueurs[joueur].nbrEnergie * 0.000025
                self.joueurs[joueur].nbrPopulation += round(pointsMetaux + pointsEnergie)

    def production_pointage(self):
        for joueur in self.joueurs:
            # if joueur == self.joueurs:
            for etoile in self.joueurs[joueur].etoilescontrolees:
                pointsMetaux = self.joueurs[joueur].nbrMetal * 0.001
                pointsEnergie = self.joueurs[joueur].nbrEnergie * 0.001
                self.joueurs[joueur].nbrPoints += round(pointsMetaux + pointsEnergie)

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creeretoiles(self, joueurs, ias=0):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.etoiles.append(Etoile(self, x, y))
        np = len(joueurs) + ias
        etoile_occupee = []
        while np:
            p = random.choice(self.etoiles)
            if p not in etoile_occupee:
                etoile_occupee.append(p)
                self.etoiles.remove(p)
                np -= 1

        couleurs = ["#F49F0A", "#7f827d", "#5FA550", "#4894FE", "#8B5588", "#EB5C68",
                     "#85130f", "#735645"]
        # jaune, gris, vert, bleu, mauve, rose, rouge, brun
        for i in joueurs:
            etoile = etoile_occupee.pop(0)
            self.joueurs[i] = Joueur(self, i, etoile, couleurs.pop(0))
            x = etoile.x
            y = etoile.y
            dist = 500
            for e in range(5):
                x1 = random.randrange(x - dist, x + dist)
                y1 = random.randrange(y - dist, y + dist)
                self.etoiles.append(Etoile(self, x1, y1))

        # IA- creation des ias
        couleursia = ["SeaGreen1", "green", "cyan",
                      "orange", "turquoise1", "firebrick1"]
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), etoile_occupee.pop(0), couleursia.pop(0))

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        
        
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet représentant le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        #### Debut Eric
        joueur_sans_etoile = 0
        joueur_avec_etoile = 0
        for joueur in self.joueurs:
            if len(self.joueurs[joueur].etoilescontrolees) == 0:
                joueur_sans_etoile += 1
            else:
                joueur_gagnant = joueur
                joueur_avec_etoile += 1
            
        if joueur_avec_etoile == 1:
            print("Partie finiiiiiiiiiiiiiiiiiieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            print("Le joueur " + joueur_gagnant + " a gagné")
            self.parent.afficher_fin_jeu(joueur_gagnant)
            self.jeu_actif = False
        #### Fin Eric
        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for i in self.joueurs:
            self.joueurs[i].jouer_prochain_coup()

        # NOTE si le modele (qui représente l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

    #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, actionsrecues):
        cadrecle = None
        for i in actionsrecues:
            cadrecle = i[0]
            if cadrecle:
                if (self.parent.cadrejeu - 1) > int(cadrecle):
                    print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                action = ast.literal_eval(i[1])

                if cadrecle not in self.actions_a_faire.keys():
                    self.actions_a_faire[cadrecle] = action
                else:
                    self.actions_a_faire[cadrecle].append(action)
    # NE PAS TOUCHER - FIN
##############################################################################
