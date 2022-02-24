pathA = "input_data/a_an_example.in.txt"
pathB = "input_data/b_better_start_small.in.txt"
pathC = "input_data/c_collaboration.in.txt"
pathD = "input_data/d_dense_schedule.in.txt"
pathE = "input_data/e_exceptional_skills.in.txt"
pathF = "input_data/f_find_great_mentors.in.txt"


pourHugo = "D:/code/hashcode/GoogleHashCode/"

class Collaborateur:
    def __init__(self, nom) -> None:
        self.nom = nom
        self.capacites = []
        self.nombre_capacites = 0
        self.disponible = True

    def ajouter_capacite(self, capacite, niveau):
        self.capacites.append((capacite, niveau))
        self.nombre_capacites += 1

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
        self.date_limite_depart = self.best_before - self.jours
    
    def ajouter_activite(self, activite, niveau):
        self.activites.append((activite, niveau))
        self.nombre_activites += 1
    
    def __repr__(self):
        return f"{self.nom} Jours:{self.jours} Score:{self.score} BestBefore:{self.best_before} Nombre activites:{self.nombre_activites} DateLimiteDepart:{self.date_limite_depart}\n {self.activites}"

class Resoudre:
    def __init__(self):
        self.nombre_collaborateurs = 0
        self.nombre_projets = 0
        self.collaborateurs = []
        self.projets = []

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

#Test
resolution = Resoudre()
resolution.generer(pathA)
print(resolution.nombre_collaborateurs, resolution.nombre_projets)
print(resolution.collaborateurs)
print(resolution.projets)