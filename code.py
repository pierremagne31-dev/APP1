import tkinter as tk
from tkinter import messagebox

class MorpionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion - Tic Tac Toe")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # Variables du jeu
        self.tour = "X"
        self.board = [" " for _ in range(9)] # Liste pour stocker l'état du jeu
        self.boutons = []

        # Création de l'interface
        self.creer_widgets()

    def creer_widgets(self):
        # Label pour afficher le tour
        self.label_info = tk.Label(self.root, text=f"Au tour de : {self.tour}", font=("Arial", 20))
        self.label_info.pack(pady=20)

        # Frame pour la grille
        frame_grille = tk.Frame(self.root)
        frame_grille.pack()

        # Création des 9 boutons
        for i in range(9):
            btn = tk.Button(frame_grille, text=" ", font=("Arial", 24, "bold"), width=5, height=2,
                            command=lambda index=i: self.jouer(index))
            
            # Positionnement en grille (3x3)
            # i // 3 donne la ligne (0, 0, 0, 1, 1, 1...)
            # i % 3 donne la colonne (0, 1, 2, 0, 1, 2...)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.boutons.append(btn)
        
        # Bouton Rejouer
        btn_reset = tk.Button(self.root, text="Recommencer", font=("Arial", 12), command=self.reset_jeu)
        btn_reset.pack(pady=20)

    def jouer(self, index):
        # Si la case est déjà prise, on ne fait rien
        if self.board[index] != " ":
            return

        # Mise à jour du modèle (board) et de la vue (bouton)
        self.board[index] = self.tour
        self.boutons[index].config(text=self.tour, fg="blue" if self.tour == "X" else "red")

        # Vérification victoire ou nul
        if self.verifier_victoire():
            messagebox.showinfo("Victoire !", f"Le joueur {self.tour} a gagné !")
            self.reset_jeu()
        elif " " not in self.board:
            messagebox.showinfo("Match Nul", "Personne n'a gagné !")
            self.reset_jeu()
        else:
            # Changement de joueur
            self.tour = "O" if self.tour == "X" else "X"
            self.label_info.config(text=f"Au tour de : {self.tour}")

    def verifier_victoire(self):
        combinaisons = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Lignes
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Colonnes
            (0, 4, 8), (2, 4, 6)             # Diagonales
        ]
        
        for a, b, c in combinaisons:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != " ":
                self.colorier_gagnant([a, b, c])
                return True
        return False

    def colorier_gagnant(self, indices):
        for index in indices:
            self.boutons[index].config(bg="#90EE90") # Vert clair

    def reset_jeu(self):
        self.tour = "X"
        self.board = [" " for _ in range(9)]
        self.label_info.config(text=f"Au tour de : {self.tour}")
        for btn in self.boutons:
            btn.config(text=" ", bg="SystemButtonFace") # Remet la couleur par défaut

if __name__ == "__main__":
    root = tk.Tk()
    app = MorpionApp(root)
    root.mainloop()
