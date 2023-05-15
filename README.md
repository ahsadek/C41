# C41
Génie Logiciel - Équipe 4

Ce jeu a été créer dans le cadre du cours Génie Logiciel C41.
Le serveur ainsi que le code de base a été fourni par Jean-Marc Deschamps.

 -- ORION --

Mise en contexte

Orion est un jeu de conquête spatiale de type RTS (real-time strategy). Il peut accueillir jusqu'à 8 joueurs en plus d'un IA.
Chaque joueur commence la partie avec une étoile mère et son but ultime est de conquérir les étoiles sur la carte et d'annihiler ses adversaires. Pour cela, il doit baser sa stratégie sur l'utilisation de ses ressources et de 3 types de vaisseaux: exploration, cargo et combat.

Les vaisseaux

Chaque type de vaisseau effectue une tâche qui permet de prendre le contrôle d'une étoile non colonisée ou d'une étoile déjà colonisée par un autre joueur.

	Coloniser une étoile non colonisée
	
	Le joueur envoi un vaisseau d'exploration sur une étoile non colonisée. Ceci permet au vaisseau de cargo de ce même joueur de pouvoir aller sur l'étoile explorée. Une fois que le cargo se rend sur la planète, le joueur devient propriétaire et les ressources de cette étoile sont maintenant à lui.

	Conquérir une étoile colonisée par un autre joueur
	
	Le joueur attaque une étoile colonisée par un autre joueur avec un vaisseau de combat. Une fois que le points de vie de l'étoile sont à 0, l'étoile change de propriétaire pour le joueur qui a attaqué. Les ressources sont maintenant au joueur qui a gagné l'attaque.
	



Le combat 



Les étoiles



Les batiments



Les ressources



Comment gagner la partie

