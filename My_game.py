# Créé par Waîl Yeager, le 14/01/2024 en Python 3.7
# Créé par Waîl Yeager, le 11/01/2024 en Python 3.7
import pyxel
import random
import time as t

"""Gameplay: Fleches : 4 directions , espace : tirs basiques , Bouton X : Laser (attention le laser n'affecte pas les bonus , echap: abandonner , Q : quitter le jeu , C : charge , V : bombe  """
#ralentir le temps

class Jeu:
    def __init__(self):


        pyxel.init(128, 128, title="Spaceship Survive")  #affiche un fenetre de 128x128 avec le titre du jeu

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 60
        self.vaisseau_y = 60

        # vies
        self.vies = 5

        self.score = 0

        self.kill = 0

        self.laser_liste = []

        self.nb_bonus = 0

        # initialisation des tirs
        self.tirs_liste = []

        # initialisation des ennemis
        self.ennemis_liste = []

        # initialisation des explosions
        self.explosions_liste = []

        self.bonusliste = []

        self.charge = 3

        self.nucleaire = 1

        #self.bouclier = 2
        self.temps = 2
        self.est_actif = False

        pyxel.run(self.update, self.draw)


    def deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x < 120:   #les conditions sont la pour ne pas depasser la resolution et prend en compte la taille du joueur (8) donc 128-8=120
            self.vaisseau_x += 6
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x > 0:
            self.vaisseau_x -= 6
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y < 120:
            self.vaisseau_y += 6
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y > 0:
            self.vaisseau_y -= 6

    """ bouclier """
    """
    def boucliers(self):
        if pyxel.btn(pyxel.KEY_B) and self.bouclier > 0:
            self.est_actif = True
            tps = 5
            while tps > 0:
                t.sleep(1)
                tps -= 1
            self.est_actif = False
            self.bouclier -= 1
    """
    def wait(self):
        i = 0
        while i < 38800000:

                i += 1

    """
    def wait(self):
        i = 0
        while i < 100000:
            self.deplacement()
            i += 1
            time.sleep(0.001)
    """
    def tps(self):
        if pyxel.btn(pyxel.KEY_B) and self.temps > 0:
            self.est_actif = True
            self.wait()
            self.est_actif = False
            self.temps -= 1

            """
            tps = 5
            while tps > 0:
                t.sleep(1)
                tps -= 1
            self.est_actif = False
            self.temps -= 1
            """


    def retry(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()


    def dash(self):
        if self.charge > 0:
            if pyxel.btn(pyxel.KEY_C) and self.vaisseau_y > 0:
                self.vaisseau_y -= 20
                self.charge -= 1

    def tirs_creation(self):
        """création d'un tir avec la barre d'espace"""

        if pyxel.btnr(pyxel.KEY_SPACE):
            self.tirs_liste.append([self.vaisseau_x + 4, self.vaisseau_y - 4])

    def laser_creation(self):
        if pyxel.btnr(pyxel.KEY_X):
            self.laser_liste.append([self.vaisseau_x + 4, self.vaisseau_y - 4])

    def tirs_deplacement(self):     #<-->
        """déplacement des tirs vers le haut et suppression quand ils sortent du cadre"""

        for tir in self.tirs_liste:
            tir[1] -= 1
            if tir[1] < -8:
                self.tirs_liste.remove(tir)

    def laser_deplacement(self):
        for laser in self.laser_liste:
            laser[1] -= 1
            if laser[1] < -8:
                self.laser_liste.remove(laser)

    def ennemis_creation(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if pyxel.frame_count % 20 == 0:
            self.ennemis_liste.append([random.randint(0, 120), 0])



    def bonus_creation(self):
        if pyxel.frame_count % 100 == 0:
            self.bonusliste.append([random.randint(0,120),0])



    def ennemis_deplacement(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

        for ennemi in self.ennemis_liste:
            ennemi[1] += 1
            if ennemi[1] > 128:
                self.ennemis_liste.remove(ennemi)


    def bonus_deplacement(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

        for b in self.bonusliste:
            b[1] += 2
            if b[1] > 128:
                self.bonusliste.remove(b)


    def vaisseau_suppression(self):
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:
            if (
                ennemi[0] <= self.vaisseau_x + 8
                and ennemi[1] <= self.vaisseau_y + 8
                and ennemi[0] + 8 >= self.vaisseau_x
                and ennemi[1] + 8 >= self.vaisseau_y
            ):
                self.ennemis_liste.remove(ennemi)
                self.vies -= 1
                self.score -= 12
                # on ajoute l'explosion
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)


    def ennemis_suppression(self):
        """disparition d'un ennemi et d'un tir si contact"""

        for ennemi in self.ennemis_liste:
            for tir in self.tirs_liste:
                if (
                    ennemi[0] <= tir[0] + 8
                    and ennemi[0] + 8 >= tir[0]
                    and ennemi[1] + 8 >= tir[1]
                ):
                    self.ennemis_liste.remove(ennemi)
                    self.tirs_liste.remove(tir)

                    self.score += 15
                    self.kill += 1
                    # on ajoute l'explosion
                    self.explosions_creation(ennemi[0], ennemi[1])


    def bonus_suppression(self):
        """disparition d'un ennemi et d'un tir si contact"""

        for bon in self.bonusliste:
            for tir in self.tirs_liste:
                if (
                    bon[0] <= tir[0] + 8
                    and bon[0] + 8 >= tir[0]
                    and bon[1] + 8 >= tir[1]
                ):
                    self.bonusliste.remove(bon)
                    self.tirs_liste.remove(tir)
                    self.vies += 1
                    self.nb_bonus += 1
                    self.score += 25
                    # on ajoute l'explosion
                    self.explosions_creation(bon[0], bon[1])

    def ennemis_suppression_bis(self):
        for ennemi in self.ennemis_liste:
            for las in self.laser_liste:
                if (
                    ennemi[0] <= las[0] + 8
                    and ennemi[0] + 8 >= las[0]
                    and ennemi[1] + 8 >= las[1]
                ):
                    self.ennemis_liste.remove(ennemi)
                    self.laser_liste.remove(las)

                    self.score += 15
                    self.kill += 1
                    # on ajoute l'explosion
                    self.explosions_creation(ennemi[0], ennemi[1])

    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])

    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] += 1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    # =====================================================
    # == UPDATE
    # =====================================================

    def quitter_jeu(self):
        if pyxel.btnp(pyxel.ESC):
            self.vie = 0

    def nucleaires(self):
        if pyxel.btn(pyxel.KEY_V):
            self.nucleaire -= 1
            self.ennemis_liste = []

    def update(self):
        if self.est_actif == False:
            """mise à jour des variables (30 fois par seconde)"""

            # deplacement du vaisseau
            self.deplacement()

            # creation des tirs en fonction de la position du vaisseau

            self.tirs_creation()

            # mise a jour des positions des tirs
            self.tirs_deplacement()

            self.laser_creation()

            self.laser_deplacement()

            # creation des ennemis
            if self.nucleaire > 0:
                self.nucleaires()

            #if self.est_actif == False:
            self.ennemis_creation()


            # mise a jour des positions des ennemis
            if not self.dash():
                self.ennemis_deplacement()


            self.dash()

            self.tps()
            #self.boucliers()

            # suppression des ennemis et tirs si contact
            self.ennemis_suppression()

            self.ennemis_suppression_bis()

            # suppression du vaisseau et ennemi si contact
            self.vaisseau_suppression()

            # evolution de l'animation des explosions
            self.explosions_animation()

            self.bonus_creation()

            self.bonus_deplacement()

            self.bonus_suppression()

            self.retry()
        else:
            self.deplacement()


    # =====================================================
    # == DRAW
    # =====================================================

    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)

        # si le vaisseau possede des vies le jeu continue
        if self.vies > 0:

            pyxel.text(3, 120, "Scores:" + str(self.score), 5)
            # affichage des vies
            pyxel.text(3, 5, "VIES x" + str(self.vies), 7)

            pyxel.text(3, 110, "Kills:" + str(self.kill), 8)

            pyxel.text(3,100,"Bonus:" + str(self.nb_bonus),9)

            pyxel.text(60,120,"Saut restant:"+str(self.charge),2)

            pyxel.text(60,110,"Bombes:"+str(self.nucleaire),3)

            pyxel.text(60,100,"Arret tps:"+str(self.temps),6)

            #pyxel.text(60,100,"Bouclier:"+str(self.bouclier),6)

            # vaisseau (carre 8x8)

            pyxel.rect(self.vaisseau_x, self.vaisseau_y, 8, 8, 1)



            # tirs
            for tir in self.tirs_liste:
                pyxel.rect(tir[0], tir[1], 1, 4, 10)

            for las in self.laser_liste:
                pyxel.rect(las[0], las[1], 10, 2, 20)

            # ennemis
            for ennemi in self.ennemis_liste:
                pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

            for bonus in self.bonusliste:
                pyxel.rect(bonus[0], bonus[1], 5, 5, 11)



            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:
                pyxel.circb(
                    explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3
                )

        # sinon: GAME OVER
        else:

            pyxel.text(50, 64, "GAME OVER", 7)

Jeu()

