import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class MorpionSimple(QWidget):
    def __init__(self):
        """ Initialise la fenêtre principale et les variables de base du jeu. """
        super().__init__()
        self.setWindowTitle("Morpion Simple")
        self.setFixedSize(400, 550) 
        self.setStyleSheet("background-color: #2b2d42; color: white;") 

        self.plateau = [""] * 9   
        self.jeu_en_cours = True  
        self.humain = "X"
        self.ia = "O"
        self.mode_ia_vs_ia = False 

        self.creer_interface() 

    def creer_interface(self):
        """ Crée les éléments visuels de l'interface graphique (textes, grille, boutons). """
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        self.info = QLabel("C'est à toi de jouer (X) !")
        self.info.setFont(QFont("Arial", 16, QFont.Bold))
        self.info.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.info)

        grille_layout = QGridLayout()
        layout_principal.addLayout(grille_layout)

        self.boutons = [] 
        
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(100, 100)
            btn.setFont(QFont("Arial", 36, QFont.Bold))
            btn.setStyleSheet("background-color: #8d99ae; border-radius: 10px; color: black;")
            
            btn.clicked.connect(lambda checked, index=i: self.clic_joueur(index))
            
            ligne, colonne = divmod(i, 3) 
            grille_layout.addWidget(btn, ligne, colonne)
            self.boutons.append(btn)

        layout_boutons = QHBoxLayout()

        btn_reset = QPushButton("Jouer vs IA")
        btn_reset.setFont(QFont("Arial", 12))
        btn_reset.setStyleSheet("background-color: #ef233c; padding: 10px; border-radius: 5px;")
        btn_reset.clicked.connect(self.recommencer)
        layout_boutons.addWidget(btn_reset)

        btn_ia_vs_ia = QPushButton("IA vs IA")
        btn_ia_vs_ia.setFont(QFont("Arial", 12))
        btn_ia_vs_ia.setStyleSheet("background-color: #f77f00; padding: 10px; border-radius: 5px;")
        btn_ia_vs_ia.clicked.connect(self.lancer_ia_vs_ia)
        layout_boutons.addWidget(btn_ia_vs_ia)

        layout_principal.addLayout(layout_boutons)

    def clic_joueur(self, index):
        """ Gère le clic d'un joueur humain sur une case de la grille. """
        # Si les bots jouent entre eux, on bloque tes clics
        if self.mode_ia_vs_ia:
            return

        if self.plateau[index] == "" and self.jeu_en_cours:
            self.jouer_un_coup(index, self.humain) 
            
            if self.jeu_en_cours:
                self.info.setText("L'IA réfléchit...")
                QTimer.singleShot(100, self.tour_de_lia) 

    def tour_de_lia(self):
        """ Déclenche le tour classique de l'IA (symbole O) quand tu joues contre elle. """
        meilleur_coup = self.trouver_meilleur_coup(self.ia)
        if meilleur_coup != -1:
            self.jouer_un_coup(meilleur_coup, self.ia) 
        
        if self.jeu_en_cours:
            self.info.setText("C'est à toi de jouer (X) !")

    def lancer_ia_vs_ia(self):
        """ Initialise et démarre le mode de jeu automatique IA contre IA. """
        self.recommencer()
        self.mode_ia_vs_ia = True
        self.boucle_ia_vs_ia()

    def boucle_ia_vs_ia(self):
        """ Gère le tour par tour automatique en mode combat de bots. """
        if not self.jeu_en_cours or not self.mode_ia_vs_ia:
            return
        
        nb_vides = self.plateau.count("")
        joueur_actuel = self.humain if nb_vides % 2 != 0 else self.ia
        
        self.info.setText(f"L'IA ({joueur_actuel}) réfléchit...")
        
        QTimer.singleShot(100, lambda: self.executer_coup_ia(joueur_actuel))

    def executer_coup_ia(self, joueur):
        """ Calcule et joue le meilleur coup pour l'IA en cours, puis relance la boucle. """
        if not self.jeu_en_cours or not self.mode_ia_vs_ia:
            return
        
        coup = self.trouver_meilleur_coup(joueur)
        if coup != -1:
            self.jouer_un_coup(coup, joueur)
            
        if self.jeu_en_cours:
            QTimer.singleShot(500, self.boucle_ia_vs_ia)
    
    def trouver_meilleur_coup(self, joueur):
        """ Parcours les cases vides pour trouver le coup parfait adapté au joueur donné. """
        meilleur_coup = -1
        
        if joueur == self.ia: 
            meilleur_score = -math.inf
            for i in range(9):
                if self.plateau[i] == "":
                    self.plateau[i] = self.ia
                    score = self.minimax(self.plateau, False) 
                    self.plateau[i] = ""
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = i
        else: 
            meilleur_score = math.inf
            for i in range(9):
                if self.plateau[i] == "":
                    self.plateau[i] = self.humain
                    score = self.minimax(self.plateau, True) 
                    self.plateau[i] = ""
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = i
        return meilleur_coup

    def minimax(self, plateau_virtuel, c_est_le_tour_de_lia):
        """ Simule récursivement tous les futurs possibles pour évaluer une grille de jeu. """
        vainqueur = self.verifier_victoire(plateau_virtuel)
        if vainqueur == self.ia: return 1      
        if vainqueur == self.humain: return -1 
        if "" not in plateau_virtuel: return 0 

        if c_est_le_tour_de_lia:
            score_max = -math.inf
            for i in range(9):
                if plateau_virtuel[i] == "":
                    plateau_virtuel[i] = self.ia
                    score = self.minimax(plateau_virtuel, False) 
                    plateau_virtuel[i] = ""
                    score_max = max(score, score_max)
            return score_max
        
        else:
            score_min = math.inf
            for i in range(9):
                if plateau_virtuel[i] == "":
                    plateau_virtuel[i] = self.humain
                    score = self.minimax(plateau_virtuel, True) 
                    plateau_virtuel[i] = ""
                    score_min = min(score, score_min)
            return score_min

    def jouer_un_coup(self, index, joueur):
        """ Inscrit le symbole en mémoire, modifie le bouton visuel et vérifie la victoire. """
        self.plateau[index] = joueur
        self.boutons[index].setText(joueur)
        
        if joueur == "X":
            self.boutons[index].setStyleSheet("background-color: #8d99ae; border-radius: 10px; color: #ef233c;") 
        else:
            self.boutons[index].setStyleSheet("background-color: #8d99ae; border-radius: 10px; color: black;")

        vainqueur = self.verifier_victoire(self.plateau)
        if vainqueur:
            self.jeu_en_cours = False
            self.info.setText(f"{vainqueur} a gagné la partie !")
        elif "" not in self.plateau:
            self.jeu_en_cours = False
            self.info.setText("Match nul !")

    def verifier_victoire(self, plateau):
        """ Regarde si 3 cases identiques sont alignées (lignes, colonnes ou diagonales). """
        lignes_gagnantes = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], 
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]             
        ]
        for combo in lignes_gagnantes:
            a, b, c = combo
            if plateau[a] == plateau[b] == plateau[c] and plateau[a] != "":
                return plateau[a] 
        return None

    def recommencer(self):
        """ Remet la grille à zéro et désactive le mode IA vs IA pour te rendre la main. """
        self.plateau = [""] * 9
        self.jeu_en_cours = True
        self.mode_ia_vs_ia = False 
        self.info.setText("C'est à toi de jouer (X) !")
        for btn in self.boutons:
            btn.setText("")
            btn.setStyleSheet("background-color: #8d99ae; border-radius: 10px; color: black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MorpionSimple()
    fenetre.show()
    sys.exit(app.exec_())