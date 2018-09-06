<?php

/* ----------------------
Mise à jour du serveur
---------------------- */

// L'emplacement du fichier contenant le menu
$file = "../server/menu.json";

// L'emplacement du fichier contenant les éléments supprimés
$deletedFile = "../server/deleted.json";

// Lorsque reçoit une demande de mise à jour du serveur
if (isset($_POST['updateServer']))
{
	// Recupère l'objet principal contenu dans le fichier
	$content = json_decode(file_get_contents($file));
	
	// Recupère le type de la modification, spécifié par la demande
	$type = $_POST['updateServer'];
	
	// Recupère le contenu de la modification, spécifié par la demande
	$info = $_POST['info'];
	
	// Recupère la position de l'élément du menu à partir duquel faire la modification, spécifiée par la demande
	$path = str_split($_POST['path']);
	
	// Renomme
	if ($type == "newName")
		$content = newName($content, $info, $path);
	
	// Ajoute
	else if ($type == "newPage" || $type == "newFolder")
		$content = addElement($content, $info, $path, $type);
	
	// Déplace
	else if ($type == "move")
		$content = moveElement($content, $info, $path);
	
	// Supprime
	else if ($type == "delete")
		$content = deleteElement($content, $path);
	
	// Met à jour l'objet principal du fichier
	file_put_contents ($file, json_encode($content));
	
	// Envoie au client le contenu du tableau de l'objet principal
	echo json_encode($content->content);
}

/* ----------------------
Créer un élément
---------------------- */

function createElement($title, $type)
{
	// Crée un nouvel élément
	$element = new stdClass;
	
	// Donne au nouvel élément le titre celui indiquée par la demande
	$element->title = $title;
	
	// Donne au nouvel élément un ID aléatoire
	$element->id = rand(10000000, 99999999);
	
	// Si la demande concerne l'ajout d'une page
	if ($type == "newPage")
	{
		// Donne à l'élément le type "page"
		$element->type = "page";
	}
	
	// Si la demande concerne l'ajout d'un dossier
	else if ($type == "newFolder")
	{
		// Donne à l'élément le type "folder"
		$element->type = "folder";
		
		// Donne à l'élément un tableau qui contiendra ses sous-éléments
		$element->content = [];
	}
	
	return $element;
}

/* ----------------------
Récupérer un élément
---------------------- */

function getElement($content, $path)
{
	$element = $content;
	for ($i = 0; $i < count($path); $i++)
	{
		$element = $element->content[$path[$i]];
	}
	return $element;
}

/* ----------------------
Récupérer le parent d'un élément
---------------------- */

function getParent($content, $path)
{
	$element = $content;
	for ($i = 0; $i < count($path) -1; $i++)
	{
		$element = $element->content[$path[$i]];
	}
	return $element;
}

/* ----------------------
Renomer
---------------------- */

function newName($content, $info, $path)
{
	// Recupère l'élément
	$element = getElement($content, $path);
	
	// Donne à l'élément le titre indiqué
	$element->title = $info;
	
	// Renvoie l'objet principal modifié
	return $content;
}

/* ----------------------
Insérer
---------------------- */

function insertElement($content, $path, $element)
{
	// Recupère l'élément cliqué (en fonction duquel le nouvel élément doit être ajouté)
	$syb = getElement($content, $path);
	
	// Si l'élément cliqué est un dossier
	if ($syb->type == "folder")
	{
		// Ajoute le nouvel élément au début du dossier
		array_unshift($syb->content, $element);
	}
	
	// Si l'élément cliqué est une page
	else if ($syb->type == "page")
	{
		// Recupère le dossier parent de la page cliquée
		$parent = getParent($content, $path);
	
		// Ajoute le nouvel élément dans le dossier parent, après la page cliquée
		array_splice( $parent->content, $path[ count($path) -1 ] +1 , 0, array ( $element ) );
	}
	
	return $content;
}


/* ----------------------
Ajouter un nouvel élément
---------------------- */

function addElement($content, $info, $path, $type)
{
	// Crée un nouvel élément
	$newElement = createElement($info, $type);
	
	return insertElement($content, $path, $newElement);
}

/* ----------------------
Déplacer
---------------------- */

function moveElement($content, $pathTo, $path)
{

	$pathTo=str_split($pathTo);

	// Vérifie que l'élément à déplacer n'est pas un parent du dossier où on cherche à le déplacer
	$continue = false;
	
	if ( count($pathTo) >= count($path) )
	{
		
		for ($i = 0; $i < count($path) AND $continue == false; $i++)
		{
			if ( $pathTo[$i] != $path[$i] ) 
				$continue = true;
		}
	}
	else
	{
		$continue = true;
	}

	if ($continue)
	{
		// Récupère l'élément à déplacer
		$element = getElement($content, $path);

		// Récupère le parent de l'élément à déplacer
		$parent = getParent($content, $path);

		// Fait une cope de l'élément à déplacer
		$elementCopy = clone $element; 

		// Indique que l'original de l'élément à déplacé doit être supprimé
		$element->type = "removed";

		// Insère la copie de l'élément à déplacer à l'endroit indiqué
		$content = insertElement($content, $pathTo, $elementCopy);

		// Supprime l'original de l'élément à déplacer
		for ($i = 0; $i < count($parent->content); $i++)
		{
			if ($parent->content[$i]->type == "removed")
				array_splice( $parent->content, $i , 1 );
		}
	}
	
	return $content;
}

/* ----------------------
Supprimer
---------------------- */
function deleteElement($content, $path)
{

	// Récupère l'élément à supprimer
	$element = getElement($content, $path);

	// Récupère son parent
	$parent = getParent($content, $path);

	// Met l'élément dans le fichier des éléments supprimés
	file_put_contents ("server/deleted.json", json_encode( $element ), FILE_APPEND );
	
	// Supprime l'élément de son parent
	array_splice( $parent->content, $path[ count($path) -1 ] , 1 );
	
	// Renvoie l'objet principal modifié
	return $content;
}

?>
