<?php

/* ----------------------
Mise à jour du client
---------------------- */ 

// L'emplacement du fichier contenant le menu
$file = "server/menu.json";

// Lorsque reçoit une demande de mise à jour du client
if (isset($_POST['updateClient']))
{
	// Récupère le contenu du fichier contenant le menu
	$content = file_get_contents($file);
	
	// Si le fichier n'existe pas encore ou contient une table vide
	if (!$content OR count( json_decode($content)->content ) == 0 )
	{
		// Crée l'objet principal
		$main = new stdClass;
		
		// Donne à l'objet principal un tableau qui contiendra ses éléments
		$main->content = array();
	
		// Créé un premier élément
		$newElement = createElement("Home", "newPage");
		
		// Met le nouvel élément dans le tableau de l'objet principal
		array_push($main->content, $newElement);
		
		// Convertit l'objet principal en JSON
		$content = json_encode($main);
		
		// Crée le fichier en y incluant le JSON
		file_put_contents ($file, $content);
	}
	
	// Envoie au client le contenu du tableau de l'objet principal
	echo json_encode(json_decode($content)->content);
}

?>
