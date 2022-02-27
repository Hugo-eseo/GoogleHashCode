pathA = "input_data/a_an_example.in.txt"
pathB = "input_data/b_better_start_small.in.txt"
pathC = "input_data/c_collaboration.in.txt"
pathD = "input_data/d_dense_schedule.in.txt"
pathE = "input_data/e_exceptional_skills.in.txt"
pathF = "input_data/f_find_great_mentors.in.txt"

from tqdm import tqdm
import time

pourHugo = "D:/code/hashcode/GoogleHashCode/"

class Collaborateur:
    def __init__(self, nom):
        self.nom = nom
        self.capacites = []
        self.nombre_capacites = 0
        self.activite_en_cours = None
        self.disponible = True
    
    def ajouter_capacite(self, capacite, niveau):
        self.capacites.append([capacite, niveau])
        self.nombre_capacites += 1

    def indexCapacite(self, capacite):
        for i in range(self.nombre_capacites):
            if capacite[0] == self.capacites[i][0]:
                return i
        return None

    def amelioration(self):
        indexC = self.indexCapacite(self.activite_en_cours)
        if self.capacites[indexC][1] <= self.activite_en_cours[1]:
            self.capacites[indexC][1] += 1

    def __repr__(self):
        return f"{self.nom} {self.capacites}"

class Projet:
    def __init__(self, nom, jours, score, best_before, nombre_activites):
        self.nom = nom
        self.jours = jours
        self.score = score
        self.best_before = best_before
        self.nombre_activites = nombre_activites
        self.activites = []
        self.collaborateurs = []
        self.date_limite_depart = self.best_before - self.jours
        self.niveauMoyen = 0
    
    def ajouter_activite(self, activite, niveau):
        self.activites.append([activite, niveau])
 
    def calulNiveauMoyen(self):
        totalNiveau = 0
        for activite in self.activites:
            totalNiveau += activite[1]
        self.niveauMoyen = totalNiveau/self.nombre_activites

    def ajouterCollaborateur(self, collabo, activite):
        collabo.activite_en_cours = activite
        collabo.disponible = False
        self.collaborateurs.append(collabo)

    def supprimerTousLesCollaborateurs(self):
        # Pertinent ?
        for collabo in self.collaborateurs:
            collabo.activite_en_cours = None
            collabo.disponible = True
        self.collaborateurs = []
    
    def demarrerProjet(self):
        with open("solution", "a") as fichier:
            fichier.write("\n"+self.nom + "\n")
            for collabo in self.collaborateurs:
                fichier.write(collabo.nom + " ")

    def diminuerJour(self):
        self.jours -= 1

    def __repr__(self):
        #return f"Nom : {self.nom} ; Niveau Moyen : {round(self.niveauMoyen,2)}"
        return f"Nom : {self.nom} ; Nombre d'activités : {self.nombre_activites}"
        #return f"{self.nom} Jours:{self.jours} Score:{self.score} BestBefore:{self.best_before} Nombre activites:{self.nombre_activites} DateLimiteDepart:{self.date_limite_depart}\n {self.activites}\n"

class Resoudre:
    def __init__(self):
        # Données fournis
        self.nombre_collaborateurs = 0
        self.nombre_projets = 0
        self.projets = []
        self.collaborateurs = []

        # Collaborateurs Disponibles / non disponibles
        self.skills = []
        self.collaborateursDisponibles = []

        # Projets en cours/terminés
        self.projetsEnCours = []
        self.projetsFini =[]
        self.nombreProjetNonFiniATemps = 0

        # Jour courant
        self.day = 0

    def generer(self, path):
        with open(path, "r") as fichier:
            ligne = fichier.readline().strip().split(" ")
            self.nombre_collaborateurs = int(ligne[0])
            self.nombre_projets = int(ligne[1])
            #Génération des collaborateurs
            for i in range(self.nombre_collaborateurs):
                ligne = fichier.readline().strip().split(" ")
                collabo = Collaborateur(ligne[0])
                for j in range(int(ligne[1])):
                    ligneCapacite = fichier.readline().strip().split(" ")
                    collabo.ajouter_capacite(ligneCapacite[0], int(ligneCapacite[1]))
                    # Tri des collaborateurs par capacités
                    try:
                        index = self.skills.index(ligneCapacite[0])
                        self.collaborateursDisponibles[index].append(collabo)
                    except:
                        self.skills.append(ligneCapacite[0])
                        self.collaborateursDisponibles.append([collabo])
                        #self.collaborateursNonDisponibles.append([])
                self.collaborateurs.append(collabo)

            #Génération des projets
            for i in range(self.nombre_projets):
                ligne = fichier.readline().strip().split(" ")
                proj = Projet(ligne[0], int(ligne[1]), int(ligne[2]), int(ligne[3]), int(ligne[4]))
                for j in range(int(ligne[4])):
                    ligneActivite = fichier.readline().strip().split(" ")
                    proj.ajouter_activite(ligneActivite[0], int(ligneActivite[1]))
                proj.calulNiveauMoyen()
                self.projets.append(proj)

    def PorcessDay(self):
        #print("===== Jour n° ", self.day, " =====")
        # On met à jour la liste des projets en cours
        for projet in self.projetsEnCours:
            # Si le projet est terminé
            if projet.jours == 0:
                # On libère et on améliore les collaborateurs
                for collaborateur in projet.collaborateurs:
                    collaborateur.amelioration()
                projet.supprimerTousLesCollaborateurs()
                # On marque le projet comme terminé
                self.projetsFini.append(projet)
                self.projetsEnCours.remove(projet)
            # Sinon, on diminue la date de fin du projet
            else:
                projet.diminuerJour()

        # On parcours la liste des projets non débutés
        for projet in self.projets:
            # Tant que le projet est intéréssant à débuter
            if self.day < projet.date_limite_depart + projet.score:
                #print("Projet étudié : ", projet)
                # On parcours la liste des activités
                for activite in projet.activites:
                    index = self.skills.index(activite[0])
                    # On cherche un collaborateur disponible ayant les compétences requises
                    collaborateurDeCote = None
                    collaborateurSelectionne = None
                    for collaborateur in self.collaborateursDisponibles[index]:
                        # Dès qu'on arrive aux collaborateurs indisponibles, on sort de la boucle
                        if(collaborateur.disponible):
                            # On cherche sa capacité dans sa propre liste de capacités
                            for i in range(len(collaborateur.capacites)):
                                if collaborateur.capacites[i][0] == activite[0]:
                                    break
                            # Si il a parfaitement le niveau requis
                            if(collaborateur.capacites[i][1] == activite[1]):
                                # Si il n'est pas déjà sur le projet
                                if(collaborateur in projet.collaborateurs):
                                    continue # Collaborateur suivant
                                # Sinon il est sélectionné
                                collaborateurSelectionne = collaborateur
                                break # On sort de la boucle collaborateur

                            # Si il a un niveau supérieur à celui demandé
                            elif (collaborateur.capacites[i][1] > activite[1]):
                                # Si il n'est pas déjà sur le projet
                                if(collaborateur in projet.collaborateurs):
                                    continue # Collaborateur suivant
                                # Si il à un niveau inférieur à celui déjà de côté
                                try:
                                    if(collaborateurDeCote[1] > collaborateur.capacites[i][1]):
                                        collaborateurDeCote = [collaborateur, collaborateur.capacites[i][1]]
                                except:
                                    # On le met de côté !
                                    collaborateurDeCote = [collaborateur, collaborateur.capacites[i][1]]
                    if(collaborateurDeCote is not None or collaborateurSelectionne is not None):
                        if(collaborateurSelectionne is None):
                            collaborateurSelectionne = collaborateurDeCote[0]
                        projet.ajouterCollaborateur(collaborateurSelectionne, activite)
                    else:
                        break # Sortie de la boucle activité

                # Si le projet trouve tous ses collaborateurs
                if(len(projet.collaborateurs)==projet.nombre_activites):
                    # On met à jour la liste des collaborateurs disponibles
                    self.projetsEnCours.append(projet)
                    projet.demarrerProjet()
                    #print("Projet réalisable : ", projet)
                    self.projets.remove(projet)
                # Sinon, on raz les collaborateurs du projet
                else:
                    projet.supprimerTousLesCollaborateurs()
            # Si le projet n'est plus réalisable (temps passé, on le supprime)
            else:
                self.projets.remove(projet)
                self.nombreProjetNonFiniATemps += 1

        self.day+=1

start = time.time()
resolution = Resoudre()
resolution.generer(pathE)
resolution.projets.sort(key=lambda x: x.date_limite_depart)
dateStop = resolution.projets[-1].best_before + resolution.projets[-1].jours

resolution.projets.sort(key=lambda x: x.niveauMoyen)
#print(resolution.projets)
#print(resolution.collaborateurs)

print("Dernier jour : ", dateStop)
print("Nombre total de projets : ", resolution.nombre_projets)
print("Nombre total de collaborateurs : ", resolution.nombre_collaborateurs)

for i in tqdm(range(dateStop)):
    if(len(resolution.projets)==0 and len(resolution.projetsEnCours)==0):
        break
    resolution.PorcessDay()

print("Nombre de jours utilisés : ", i)
print("Nombre de projet fini : ", len(resolution.projetsFini))
print("Nombre de projet non commancés à temps : ", resolution.nombreProjetNonFiniATemps)

end = time.time()
print("Temps d'execution :", end - start, "s")

# Idée : prendre en priorité les collaborateurs ayant juste le niveau requis pour les faire level up !!