/**
    Script appelé au 1er chargement de la page
    - Initialise tous les composants dont on a besoin :
        - Menu
        - Pad (Création d'un pad par défaut si besoin)
        - Options
 */

var menu;
var pad;

$(document).ready(function(){
    init();
});

/*
 * Récupérer et afficher le menu
 * Afficher le pad par défaut
 **/
function init(){
    //S'il y a un click droit --> Lancer la fenêtre modale
    // Initialisation du pad
    pad = $("#pad");
    pad.append("<iframe id='iPad' src='https://pad.lqdn.fr/p/9tlotestDev'> </iframe>")
    // Initialisation du menu
    // Doit récupérer le tableau contenant le menu et l'afficher sur la page
    $.get('initMenu')
        .done(function(data){
            // Traitement et affichage du menu
            menu = JSON.parse(data)
            var menuHtml = $("#menu");
            menuHtml.append("<li>");
            for (var i in menu){
                menuHtml.append("<ul class='parent'><h2>" + menu[i]["parent"] + "</h2></ul>");
                for(var j in menu[i]["pads"]){
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
            $("ul.parent").contextmenu(function(){
                displayDirectoryMenu();
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
    alert(adress);
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

function displayDirectoryMenu(){
    //Créer les options
    var op1 = new Option("Ajouter un pad");
    var tabOp = new Array();
    tabOp.push(op1);
    alert(op1.getName());
    var menuOp = new menuOptions(tabOp);
    menuOp.afficherMenu();
    return false;
}