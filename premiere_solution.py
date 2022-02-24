from preprocessing import liste_collaborateurs, liste_projets



liste_projets_triee = sorted(liste_projets, key=lambda x: x.date_limite_depart)


liste_collaborateurs_dispo = []
def collaborateurs_dispo(liste_collaborateurs):
    for collaborateur in liste_collaborateurs:
        if collaborateur.disponible:
            liste_collaborateurs_dispo.append(collaborateur)


jours = 100
for i in range(jours):
    