# Installation

1- Récupérer le code 

	git clone gitlab@git.laquadrature.net:Oncela5eva/PadWikIRC.git
	cd PadWikIRC

2- Créer un dossier "server"

	mkdir server

3- Récupérer le nom d'utilisateur d'Apache (probablement "www-data")

	ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1
	
4- Rendre Apache propriétarie du dossier "server" et lui donner tous les droits

	sudo chown www-data server
	sudo chmod 770 server
	
5- Définir dans pad.js le début de l'URL des etherpad à créer/utiliser. Exemple :

	pad.adress = "https://pad.lqdn.fr/p/test_padwikirc";
	
6- Facultatif : protéger l'accès au dossier "admin" via htaccess (pour protéger la modification du menu)
