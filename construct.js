// Construit chaque élément HTML du menu, à partir de son parent ("element") et de sa place sous ce parent ("index")
function construct ( element , index )
{
		// Crée le <li> qui contiendra le titre de l'élément, et lui donne comme classe CSS le type de l'élément ("page" ou "folder")
		var 	item = document.createElement("li");
				item.innerHTML = element.title;
				item.classList.add(element.type + "_title");

		// Retient la position de l'élément dans la hiérarchie du menu, à partir de la position de l'élément parent ("this")
		// Ici, la construction du path se fait sur des ints, ce qui fait que deux sous-éléments peuvent se retrouver
		// avec le même id, et donc on as une limite de 10 sous-éléments. On l'élement "1" avec le sous élément "0"  qui
		// possède le même chemin l'élément 10.
		item.path = this.path + "/" + index;

		console.log('creation' + item.path);	

		// Associe le clic (gauche ou droite) à la fonction appropriée (définie dans < clickMenu.js >)
		item.onclick = item.oncontextmenu = click;

		// Intègre le <li> dans le <div> de son parent ("this")
		this.appendChild(item);

		// Donne à l'élément son ID
		item.id = element.id;

		// Si l'élément est une page
		if (element.type == "page")
		{
			// Si aucune page par défaut n'est encore définit
			if ( pad.def == null )
			{
				// Fait de la première page rencontrée celle ouverte par défaut
				pad.def = item;
			}

			// Si l'ID de la page est celui indiqué dans l'URL
			if ( element.id == parseInt ( window.location.hash.slice (1) ) )
			{
				// Fait de la page celle ouverte au démarage
				pad.current = item;
			}
		}

		// Si l'élément est un dossier
		else if (element.type == "folder")
		{
			// Crée le <ul> qui contiendra les éléments du dossier
			item.folder = document.createElement("ul");

			// Donne à <ul> la classe CSS appropriée
			item.folder.classList.add("folder_content");

			// Conserve dans <ul> la même position que l'élément principal (pour le transmettre aux enfants)
			item.folder.path = item.path;

			// Construit les éléments du dossier, l'un après l'autre, en passant l'élément <ul> en paramètre
			element.content.forEach(construct, item.folder);

			// Intègre l'élement <ul> du dossier à l'élément
			this.appendChild(item.folder);
		}
}
