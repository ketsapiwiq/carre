/**
    Script appelé au 1er chargement de la page
    - Initialise tous les composants dont on a besoin :
        - Menu
        - Pad (Création d'un pad par défaut si besoin)
        - Options
 */

$(document).ready(function(){
    init();
});

/*
 * Récupérer et afficher le menu
 * Afficher le pad par défaut
 **/
function init(){
    // Initialisation du pad
    pad = $("#pad");
    pad.append("<iframe src='https://pad.lqdn.fr/p/9tlotestDev'> </iframe>")
    // Initialisation du menu
    //$.getJSON('initMenu');
    // Doit récupérer le tableau contenant le menu et l'afficher sur la page
    $.get('initMenu')
        .done(function(data){
            // Traitement et affichage du menu
            //alert(data["parent"]);
            //alert(data[1]);
            console.log(data);
            menu = JSON.stringify(data);
            menu = JSON.parse(menu);
            console.log(menu[0]);
        })
        .fail(function(){
            alert("le callback s'est mal passé");
        })
}