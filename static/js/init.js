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
    pad.append("<iframe id='iPad' src='https://pad.lqdn.fr/p/9tlotestDev'> </iframe>")
    // Initialisation du menu
    // Doit récupérer le tableau contenant le menu et l'afficher sur la page
    $.get('initMenu')
        .done(function(data){
            // Traitement et affichage du menu
            menu = JSON.parse(data)
            menuHtml = $("#menu");
            menuHtml.append("<li>");
            for (var i in menu){
                menuHtml.append("<ul><h2>" + menu[i]["parent"] + "</h2></ul>");
                for(var j in menu[i]["pads"]){
                    //Renvoie vers une autre page avec le pad
                    //menuHtml.append("<ul><a href='https://pad.lqdn.fr/" + menu[i]["pads"][j]["Adresse"] + "'>" + menu[i]["pads"][j]["Nom"] + "</a></ul>");
                    menuHtml.append("<ul><a href=''>" + menu[i]["pads"][j]["Nom"] + "</a></ul>");
                }
            }
            menuHtml.append("</li>")
        })
        .fail(function(){
            alert("le callback s'est mal passé");
        })
    //Ajout des EventListener
    try{
        $("ul").click(function(){
            $(this).css('background-color', 'red');
        });
        /*$("h1").click(function(event)
        {
            console.log(event.target.id); //Affiche enfantDeMaDiv
            console.log($(this)); //Affiche maDiv
        });*/

       // const collection = document.getElementsByTagName("ul");

        /*for (let item of collection) {
            alert("Boucle collections");
            console.log(item.id);
        }*/
    } catch(err){
        console.error(err);
    }
}

function updateIFrame(){
    // Supprime l'iFrame
    document.getElementById("iPad").remove();
    let text = $(this).innerText;
    console.log($(this));
    console.log("Changement d'IFrame");
    console.log(text);
    // Le remet
    //pad.append("<iframe src='https://pad.lqdn.fr/" + this.Adresse + "'> </iframe>")
}