# Installation

1- Récupérer le code 

	git clone gitlab@git.laquadrature.net:Oncela5eva/PadWikIRC.git
	cd PadWikIRC

2- Créer un dossier "server" et permettre à Apache d'écrire dedans

	mkdir server
	sudo chown www-data server
	sudo chmod 770 server
	
3- Définir dans pad.js le début de l'URL des etherpad à créer/utiliser. Exemple :

	pad.adress = "https://pad.lqdn.fr/p/test_padwikirc";
	
4- Facultatif : protéger l'accès au dossier "admin" via htaccess (pour protéger la modification du menu)
