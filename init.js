// Lorsque la page et ses scripts sont chargés
onload = function ()
{

	// Ajoute un ément HTML pour contenir le menu
	menu = document.createElement("menu");
	menu.id = "menu";
	menu.path= "";
	document.body.appendChild(menu);
	
	// Établie une connexion avec le serveur
	server = new XMLHttpRequest();
	server.open("POST", 'updateClient.php', true);
	server.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

	// Demande au serveur le contenu du menu
	server.send("updateClient=1");

	// Lorsque la réponse à la requête est reçue
	server.onreadystatechange = function() 
	{
			
		if (this.readyState == XMLHttpRequest.DONE && this.status == 200) 
		{
			// Récupère le menu et le parse dans un tableau
			var response = JSON.parse(server.responseText);
		
			// Construit le menu à partir de chacun de ses éléments de premier niveau
			response.forEach(construct, menu);
			
			// Initialise le pad
			pad.start();
			
			// Initialise l'applet IRC
			irc.start();
		}
	}
}
