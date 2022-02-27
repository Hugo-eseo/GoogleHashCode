pathA = "input_data/a_an_example.in.txt"
pathB = "input_data/b_better_start_small.in.txt"
pathC = "input_data/c_collaboration.in.txt"
pathD = "input_data/d_dense_schedule.in.txt"
pathE = "input_data/e_exceptional_skills.in.txt"
pathF = "input_data/f_find_great_mentors.in.txt"

pourHugo = "D:/code/hashcode/GoogleHashCode/"

class Collaborateur:
    def __init__(self, nom):
        self.nom = nom
        self.capacites = []
        self.nombre_capacites = 0
        self.disponible = True
        self.activite_en_cours = None
    
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
        self.index_activite_recherchee = -1
        self.collaborateurs = []
        self.date_limite_depart = self.best_before - self.jours
        self.en_cours = False
        self.fini = False
    
    def ajouter_activite(self, activite, niveau):
        self.activites.append([activite, niveau])

    def ajouterCollaborateur(self, collabo, activite):
        collabo.disponible = False
        collabo.activite_en_cours = activite
        self.collaborateurs.append(collabo)
        if len(self.collaborateurs) == self.nombre_activites:
            self.en_cours = True
            with open("solution", "a") as fichier:
                fichier.write("\n"+self.nom + "\n")
                for collabo in self.collaborateurs:
                    fichier.write(collabo.nom + " ")
            #print("Projet démarré !")

    def diminuerJour(self):
        if self.en_cours and not self.fini:
            self.jours -= 1
            if self.jours == 0:
                self.fini = True
                for collabo in self.collaborateurs:
                    collabo.disponible = True
                    collabo.amelioration()

    def rechercheActivite(self):
        self.index_activite_recherchee += 1
        return self.activites[self.index_activite_recherchee]

    def __repr__(self):
        return f"{self.nom} Jours:{self.jours} Score:{self.score} BestBefore:{self.best_before} Nombre activites:{self.nombre_activites} DateLimiteDepart:{self.date_limite_depart}\n {self.activites}\n Fini:{self.fini}"

class Resoudre:
    def __init__(self):
        self.nombre_collaborateurs = 0
        self.nombre_projets = 0
        self.collaborateurs = []

        # Skills des collaborateurs
        self.skills = []
        self.collaborateursSkills = []

        self.projets = []
        self.day = 0

        self.nombreDeProjetNonRealisable = 0

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
                self.collaborateurs.append(collabo)
            #Génération des projets
            for i in range(self.nombre_projets):
                ligne = fichier.readline().strip().split(" ")
                proj = Projet(ligne[0], int(ligne[1]), int(ligne[2]), int(ligne[3]), int(ligne[4]))
                for j in range(int(ligne[4])):
                    ligneActivite = fichier.readline().strip().split(" ")
                    proj.ajouter_activite(ligneActivite[0], int(ligneActivite[1]))
                self.projets.append(proj)

    def processDay(self):
        # On met à jour la liste des projets en cours
        for projet in self.projets:
            projet.diminuerJour()
    
        # On parcours les projets
        for projet in self.projets:
            if projet.fini or projet.en_cours:
                continue
            # Si on arrive à la date limite du projet
            if self.day < projet.date_limite_depart + projet.score:
                collaborateurSurProjet = []
                collaborateurSurProjeBis = []
                # On parcours les activités du projet
                for activite in projet.activites:
                    #print("Acitvité : ", activite)
                    collaborateurTrouve = False
                    # On parcours la liste des collaborateurs
                    for collaborateur in self.collaborateurs:
                        if collaborateur.disponible:
                            # On parcours la liste des capacités du collaborateur
                            for capacite in collaborateur.capacites:
                                # Colaborateur disponible avec compétence correspondante
                                if capacite[0] == activite[0] and capacite[1] >=  activite[1]:
                                    if(collaborateur in collaborateurSurProjeBis):
                                        break
                                    collaborateurSurProjet.append((collaborateur, activite))
                                    collaborateurSurProjeBis.append((collaborateur))
                                    #print("Colaborateur trouvé : ", collaborateur.nom)
                                    collaborateurTrouve = True
                                    break # Sortie de la boucle capacite
                        if collaborateurTrouve:
                            break # Sortie de la boucle Collaborateur
                if(len(collaborateurSurProjet)==projet.nombre_activites):
                    for collaborateur in collaborateurSurProjet:
                        collaborateur[0].disponible = False
                        projet.ajouterCollaborateur(collaborateur[0], collaborateur[1])
        self.day+=1

    def newPorcessDay(self):
        # On met à jour la liste des projets en cours
        for projet in self.projets:
            projet.diminuerJour()
        # On parcours les porjts
        for projet in self.projets:
            if projet.fini or projet.en_cours:
                continue
            # Tant que le projet est intéréssant à débuter
            if self.day < projet.date_limite_depart + projet.score:
                collaborateurSurProjet = []
                collaborateurSurProjeBis = []
                # On parcours la liste des activités
                for activite in projet.activites:
                    try:
                        index = self.skills.index(activite[0])
                    except:
                        print("Pas normal")
                        return
                    # On cherche un collaborateur ayant les compétences requises
                    for collaborateur in self.collaborateursSkills[index]:
                        if(collaborateur.disponible):
                            #print(activite)
                            for i in range(len(collaborateur.capacites)):
                                if collaborateur.capacites[i][0] == activite[0]:
                                    break
                            # Si il a la capacité recherchée
                            if(collaborateur.capacites[i][1] >= activite[1]):
                                # Si il est déjà sur le projet
                                if(collaborateur in collaborateurSurProjeBis):
                                        break
                                collaborateurSurProjet.append((collaborateur, activite))
                                collaborateurSurProjeBis.append((collaborateur))
                                break # Sortie de la boucle activites
                if(len(collaborateurSurProjet)==projet.nombre_activites):
                    for collaborateur in collaborateurSurProjet:
                        collaborateur[0].disponible = False
                        projet.ajouterCollaborateur(collaborateur[0], collaborateur[1])
            else:
                self.nombreDeProjetNonRealisable +=1

        self.day+=1



    def processColloratteur(self):
        for collaborateur in self.collaborateurs:
            for capacite in collaborateur.capacites:
                try:
                    index = self.skills.index(capacite[0])
                except:
                    index = -1
                if(index == -1):
                    self.skills.append(capacite[0])
                    self.collaborateursSkills.append([collaborateur])
                else:
                    self.collaborateursSkills[index].append(collaborateur)


#Test
resolution = Resoudre()
resolution.generer(pathB)
resolution.projets.sort(key=lambda x: x.date_limite_depart)

dateStop = resolution.projets[-1].best_before + resolution.projets[-1].jours
print(dateStop)
#print(resolution.nombre_collaborateurs, resolution.nombre_projets)
#print(resolution.collaborateurs)
#print(resolution.projets)

resolution.processColloratteur()
#print(resolution.skills)
#print("==========================")
#print(resolution.collaborateursSkills)
#print("==========================")

for i in range(dateStop):
    resolution.newPorcessDay()
    #resolution.processDay()
    pass

nbProjetFini = 0
for projet in resolution.projets:
    if projet.fini:
        nbProjetFini += 1

print("Nombre de projet impossible : ", resolution.nombreDeProjetNonRealisable)
print("Nombre de projet fini : ", nbProjetFini)
