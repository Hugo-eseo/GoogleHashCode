pathA = "input_data/a_an_example.in.txt"
pathB = "input_data/b_better_start_small.in.txt"
pathC = "input_data/c_collaboration.in.txt"
pathD = "input_data/d_dense_schedule.in.txt"
pathE = "input_data/e_exceptional_skills.in.txt"
pathF = "input_data/f_find_great_mentors.in.txt"

liste_lignes = []
with open(pathA, 'r') as f:
    for line in f:





class Collaborateur:
    def __init__(self, nom):
        self.nom = nom
        self.capacites = []

    
    def ajouter_capacite(self, capacite, niveau):
        self.capacites.append((capacite, niveau))



class Projet:
    def __init__(self, nom, jours, score, best_before, nombre_activites):
        self.nom = nom
        self.jours = jours
        self.score = score
        self.best_before = best_before
        self.nombre_activites = nombre_activites

    

