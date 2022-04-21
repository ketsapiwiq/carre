// Élément HTML du menu d'options
var 	option = document.createElement("div");
		option.id = "option";
		option.classList.add("hidden");
document.body.appendChild(option);

// Ouverture du menu
option.open = function ( element, x, y )
{
	this.target = element;
	this.classList.remove("hidden");
	this.style.left = (x - 20) + "px";
	this.style.top = (y - 10) + "px";
	
	// Affiche/ cache l'option "ouvrir dans un nouvel onglet" si l'élément est une page/ un dossier
	if 	(element.classList.contains("page_title") && option.newTab.classList.contains("hidden"))
		option.newTab.classList.remove("hidden");
	else if (element.classList.contains("folder_title") && !option.newTab.classList.contains("hidden"))
		option.newTab.classList.add("hidden");
}

// Fermeture du menu (lorsqu'appelée ou lorsque la sourie sors de l'élément HTML)
option.close = option.onmouseleave = function ()
{
	this.classList.add("hidden");
}

// Ouvrir dans un nouvel onglet (seulement pour les pages)
option.newTab = document.createElement("div");
option.newTab.link = document.createElement("a");
option.newTab.link.target = "_blank";
option.newTab.link.innerHTML = "Ouvrir dans un nouvel onglet";

option.newTab.onclick = function() 
{
		this.link.href = pad.adress + option.target.id; 
};

option.newTab.appendChild(option.newTab.link);
option.appendChild(option.newTab);

// Renommer un élément
option.rename = document.createElement("div");
option.rename.innerHTML = "Renommer";

option.rename.onclick = function()
{ 
	var name = prompt("Renommer", option.target.innerHTML);
	if (name != null)
	{
		update("newName", name, option.target.path);
	}
}

option.appendChild(option.rename);

// Ajouter une page
option.newPage = document.createElement("div");
option.newPage.innerHTML = "Ajouter une page";

option.newPage.onclick = function()
{ 
	var name = prompt("Titre de la nouvelle page");
	if (name != null)
	{
		update("newPage", name, option.target.path);
	}
}

option.appendChild(option.newPage);

// Ajouter un dossier
option.newFolder = document.createElement("div");
option.newFolder.innerHTML = "Ajouter un dossier";

option.newFolder.onclick = function()
{ 
	var name = prompt("Titre du nouveau dossier");
	if (name != null)
	{
		update("newFolder", name, option.target.path);
	}
}

option.appendChild(option.newFolder);

// Déplacer
option.move = document.createElement("div");
option.move.innerHTML = "Déplacer";
option.move.active = false;

option.move.onclick = function()
{ 
	var elements = menu.getElementsByTagName("li");
	for (var i = 0; i < elements.length; i++)
	{
		elements[i].style.cursor = "s-resize";
	}
	
	option.move.active = true;
	option.close();
}

option.move.from = function (from)
{
	update("move", from.path, option.target.path);
	
	this.stop();
}

option.move.stop = function()
{
	var elements = menu.getElementsByTagName("li");
	for (var i = 0; i < elements.length; i++)
	{
		elements[i].style.cursor = "pointer";
	}
	
	option.move.active = false;
}

option.appendChild(option.move);

// Supprime
option.deleted = document.createElement("div");
option.deleted.innerHTML = "Supprimer";

option.deleted.onclick = function()
{ 
	if (confirm("Voulez-vous vraiment supprimer " + (option.target.classList.contains("page_title") ? "la page" : "le dossier") + " <" + option.target.innerHTML + "> ?"))
		update("delete", "", option.target.path);
	
	option.close();
}

option.appendChild(option.deleted);
