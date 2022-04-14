/**
    Script appelé au 1er chargement de la page
    - Initialise tous les composants dont on a besoin :
        - Menu
        - Pad (Création d'un pad par défaut si besoin)
        - Options
 */
var menu;

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
                    //menuHtml.append("<ul><a href=''>" + menu[i]["pads"][j]["Nom"] + "</a></ul>");
                    menuHtml.append("<ul class='child'>" + menu[i]["pads"][j]["Nom"] + "</ul>");
                }
            }
            menuHtml.append("</li>")
            //Ajout des EventListener
            $("ul.child").click(function(){
                updateIFrame($(this));

            });
            $("ul.child").hover(function(){
                $(this).css('cursor','pointer');
            });
        })
        .fail(function(){
            alert("le callback s'est mal passé");
        })
}

function updateIFrame(e){
    document.getElementById("iPad").remove();
    let text = e.html();
    $("ul").css('background-color','white');
    e.css('background-color','red');
    let adress = findAdress(text);
    pad.append("<iframe id='iPad' src='https://pad.lqdn.fr/" + adress + "'> </iframe>")
}

function findAdress(text){
    // Possibilité d'améliorer la boucle avec un foreach ?
    for (var i = 0; i < menu.length; i++){
        for(var j = 0; j < menu[i]["pads"].length; ++j){
            if(text == menu[i]["pads"][j]["Nom"]){
                return menu[i]["pads"][j]["Adresse"];
            }
        }
    }
}