function click (e)
{
	// Si le clic est fait alors que l'option de déplacement est en cours
	if (option.move.active)
	{
		// Clic gauche
		if (e.button == 0)
		{
			// Active le déplacement à partir de l'élément cliqué
			option.move.from(this);
		}

		// Autre
		else
		{
			e.preventDefault();
			option.move.stop();
		}
	}

	// Clic gauche
	else if (e.button == 0)
	{
		// Si l'élément cliqué est le titre d'une page
		if (this.classList.contains("page_title"))
		{
			// Ouvre la page dans l'iframe du pad
			pad.open(this);
		}

		// Si l'élément cliqué est le titre d'un dossier
		else if (this.classList.contains("folder_title"))
		{
			// Change la classe CSS du dossier
			if (!this.classList.contains("open"))
			{
				this.classList.add("open");
			}
			else
			{
				this.classList.remove("open");
			}
		}
	}

	// Clic droit
	else if (e.button == 2)
	{
		// Empêche l'option du navigateur de s'ouvrir (le clic droit par défaut)
		e.preventDefault();

		// Ouvre l'option, en lui passant l'élément cliqué et la position de la sourie
		option.open(this, e.clientX, e.clientY);
		// TODO : Remplacer le clientX par MouseX pour correspondre à la position du curseur.
	}
}
