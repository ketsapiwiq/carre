// Envoie au serveur des information à mettre à jour
function update (type, info, path)
{
	// Envoie des information au serveur
	server.open("POST", "admin/updateServer.php", true);
	server.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	server.send(encodeURI("updateServer=" + type + "&info=" + info + "&path=" + path));
	
	// Réponse du serveur
	server.onreadystatechange = function() 
	{
		if (this.readyState == XMLHttpRequest.DONE && this.status == 200 && server.responseText) 
		{
		
			// Liste des dossiers déjà dépliés par l'utilisateur
			var openFolders = [];
			var folders = menu.getElementsByClassName("folder_title");
			for (var i = 0; i < folders.length; i++)
			{
				if (folders[i].classList.contains("open"))
					openFolders.push(folders[i].id);
			}
				
			// Retire tous les éléments HTML du menu
			while (menu.firstChild) 
			{
				menu.firstChild.remove();
			}
	
			// Récupère le menu envoyé par le serveur et le parse dans un tableau
			var response = JSON.parse(server.responseText);

			// Construit le menu à partir de chacun de ses éléments de premier niveau
			response.forEach(construct, menu);
			
			// Déplie les dossiers qui étaient dépliés avant la mise à jour
			var folders = menu.getElementsByClassName("folder_title");
			for (var i = 0; i < folders.length; i++)
			{
				if (openFolders.includes(folders[i].id))
				{
					folders[i].classList.add("open");
				}
			}
			
			// Chage la classe CSS de la page qui était ouverte
			pad.current.classList.add("selected");
		}
	}
}
