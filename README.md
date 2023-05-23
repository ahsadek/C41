# C41
Génie Logiciel - Équipe 4

Ce jeu a été créer dans le cadre du cours Génie Logiciel C41.
Le serveur ainsi que le code de base a été fourni par Jean-Marc Deschamps.

 -- ORION --

Mise en contexte

Orion est un jeu de conquête spatiale de type RTS (real-time strategy). Il peut accueillir jusqu'à 8 joueurs en plus d'un IA. Chaque joueur commence la partie avec une étoile mère et son but ultime est de conquérir les étoiles sur la carte et d'annihiler ses adversaires. Pour cela, il doit baser sa stratégie sur l'utilisation de ses ressources et de 3 types de vaisseaux: exploration, cargo et combat.

Les vaisseaux

Chaque type de vaisseau effectue une tâche qui permet de prendre le contrôle d'une étoile non colonisée ou d'une étoile déjà colonisée par un autre joueur.

	Coloniser une étoile non colonisée
	
	Le joueur envoi un vaisseau d'exploration sur une étoile non colonisée. Ce dernier va scanner l'étoile et les ressources disponibles seront affichées au joueur. Ceci permet au vaisseau cargo de ce même joueur de pouvoir aller sur l'étoile explorée. Une fois que le cargo se rend sur l'étoile, le joueur devient propriétaire et les ressources de cette étoile sont maintenant à lui.

	Conquérir une étoile colonisée par un autre joueur
	
	Le joueur attaque une étoile colonisée par un autre joueur avec un vaisseau de combat. Le vaisseau de combat va se déplacer à proximité de sa cible et va commencer à tirer. Une fois que les points de vie de l'étoile sont à 0, l'étoile change de propriétaire pour le joueur qui a attaqué. Les ressources sont maintenant au joueur qui a gagné l'attaque.
	


Le combat 
	
	Seul le vaisseau de combat peut attaquer des étoiles et des vaisseaux ennemies. Lorsque les points de vie des vaisseaux descendent à 0, ces derniers sont détruits.

Les étoiles
	
	Chaque joueur commence avec un étoile mère et peut commencer à construire sa flotte de vaisseaux. Chaque étoile qu'il conquiert lui sert de base pour construire des bâtiments et agrandir sa flotte.

Les batiments

	Chaque joueur peut construire de l'infrastructure industrielle sur ses étoiles. Ceci augmente la production de ressources de cette dernière. Toutefois, elles sont dispendieuses. Les 2 types de bâtiments sont les centrales électriques et les mines de métaux. Leurs coûts respectifs sont 

Les ressources

	Le jeu est géré par 2 types de ressources: l'énergie et les métaux. Tous les joueurs commençent avec la même quantité de ressources. La gestion efficace des ressources est importante, car elle permet de construire une flotte considérable et de construire des bâtiments (mines et centrales).

Comment gagner la partie

	Avant de commencer la partie, l'hôte de la partie peut decider combien de temps la partie va durer. le joueur qui a accumulés le plus de points durant la partie gagne lorsque le temps est écoulé. Le calcul pour le pointage se fait en fonction du nombre d'étoiles colonisées et de batiments construits durant la partie.
	
	Une autre façon de gagner la partie serait d'être le seul joueur qui possède au moins une étoile. Donc de conquérir les étoiles de tous ses adversaires.

Autres fonctionnalitées:
	
	Effet parallax subtil.

Comment jouer: 

Coloniser une étoile non colonisée

    cliquer sur un de nos étoiles
    cliquer sur le button "vaisseau exploration" pour créer le vaisseau (si ce n'est pas déjà fait)
    cliquer sur le vaisseau d'exploration
    cliquer sur l'étoile non-contrôlée
    cliquer sur le button "scanner" qui apparait en haut à gauche en cliquant sur l'étoile
    cliquer sur le button "vaisseau cargo" pour créer le vaisseau (si ce n'est pas déjà fait)
    cliquer sur le vaisseau du cargo
    cliquer sur l'étoile non-contrôlée qu'on vient de scanner
    cliquer sur le button "coloniser" qui apparait en haut à gauche en cliquant sur l'étoile


Conquérir une étoile colonisée par un autre joueur / ou attaquer un vaisseau ennemi

        cliquer sur un de nos étoiles
    cliquer sur le button "vaisseau attaque" pour créer le vaisseau (si ce n'est pas déjà fait)
    cliquer sur le vaisseau d'attaque
    cliquer sur l'étoile contrôlée / ou sur le vaisseau ennemi
    cliquer sur le button "attaquer" qui apparait en haut à gauche en cliquant sur l'étoile

Créer un batiment

    cliquer sur un de nos étoiles
    cliquer sur le button "mine metaux" / ou le button "centrale éléctrique"