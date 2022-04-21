// Iframe du pad
var 	pad = document.createElement("iframe");
		pad.adress = "https://pad.lqdn.fr/p/carre-";
		pad.id = "pad";
		pad.current = null; 								// pad actuellement ouvert, celui  dans l'URL
		pad.def = null;											// pad ouvert par défaut

// Ouvre une nouvelle page dans le pad
pad.open = function (element)
{
	this.src = this.adress + element.id;

	if (this.current != null)
	{
		this.current.classList.remove("selected");
	}
	this.current = element;
	this.current.classList.add("selected");

	window.location.hash = element.id;
}

// Démarre le pad
pad.start = function()
{
	// Intègre l'iframe
	document.body.appendChild(pad);

	// Si aucune page n'est visée dans le hash de l'URL
	if (this.current == null)
	{
		// Vise la page par défaut
		this.current = this.def;
	}

	// Ouvre la page
	pad.open(this.current);

	// Déplie les dossiers correspondants dans le menu
	var child = this.current;
	for (var i = 0; i < this.current.path.length-1; i++)
	{
		var parent = child.parentNode.previousSibling;
		parent.classList.add("open");
		child = parent;
	}
}
