/**
    Script appelé au 1er chargement de la page
    - Initialise tous les composants dont on a besoin :
        - Menu
        - Pad (Création d'un pad par défaut si besoin)
        - Options
 */

var menu;
var pad;
var adrServ;
var optionDisplay = false;

$(document).ready(function(){
    init();
});

/*
 * Récupérer et afficher le menu
 * Afficher le pad par défaut
 **/
function init(){
    $.get('/api/init/var')
      .done(function(data){
        adrServ = data["adrserv"];
        // Initialisation du pad
        pad = $("#pad");
        pad.append("<iframe id='iPad' src='" + adrServ + "p/9tlotestDev'> </iframe>");
      })
      .fail(function(){
        throw new Error("Variables de config non initialisées");
      })

    // Initialisation du menu
    $.get('/api/init/menu')
        .done(function(data){
            // Traitement et affichage du menu
            menu = JSON.parse(data);
            var menuHtml = $("#menu");
            menuHtml.append("<li>");
            for (var i in menu){
                menuHtml.append("<ul class='parent'><h2>" + menu[i]["parent"] + "</h2></ul>");
                for(var j in menu[i]["pads"]){
                    menuHtml.append("<ul class='child'>" + menu[i]["pads"][j]["Nom"] + "</ul>");
                }
            }
            menuHtml.append("</li>")

            //------Ajout des EventListener--------//
            //Click sur le nom d'un pad
            $("ul.child").click(function(){
                updateIFrame($(this));
            });

            //Click droit sur le nom d'un pad
            $("ul.child").contextmenu(function(event){
              if(!optionDisplay){
                displayPadMenu(event, $(this));
              }
            });

            //Passage de la souris sur le nom d'un pad
            $("ul.child").hover(function(){
                $(this).css('cursor','pointer');
            });

            //Click droit sur le nom d'un dossier
            $("ul.parent").contextmenu(function(event){
                if(!optionDisplay){
                    displayDirectoryMenu(event, $(this));
                }
            });

            //La souris n'est plus sur le menu d'options
            $("#options").mouseleave(function(){
                deleteOptions();
            });

        })
        .fail(function(){
            throw new Error("Récupération du menu impossible");
        })
}

/**
* Changement de pad
* @param e : élément du menu cliqué
*/
function updateIFrame(e){
    document.getElementById("iPad").remove();
    let text = e.html();
    $("ul").css('background-color','white');
    e.css('background-color','red');
    let adress = findAdress(text);
    // @nono: Attention à l'adresse du serveur de pad : il doit pouvoir être changé dans la
    // configuration du serveur sans éditer le source code.
    pad.append("<iframe id='iPad' src='" + adrServ + adress + "'> </iframe>")
}


/**
* Renvoie l'adresse d'un pad
* @param text : Le nom du pad pour lequel on veut récupérer l'adresse
*/
// @nono : Y'a sûrement une meilleur manière de faire, ici c'est une compléxité
// n*m, ça va devenir très lent quand y'aura bcp de pads.
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


/**
* Création du menu d'options pour les dossiers
* @param event :
* @param parent : élément cliqué
*/
function displayDirectoryMenu(event, parent){
    event.preventDefault();
    var op1 = new Option("Ajouter un pad", addPad, parent.text());
    var op2 = new Option("Supprimer le dossier", deleteDirectory);
    var op3 = new Option("Renommer le dossier", renameDirectory);
    var op4 = new Option("Ajouter un dossier", addDirectory);
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    tabOp.push(op3);
    tabOp.push(op4);
    var menuOp = new menuOptions(tabOp);
    let posX = event.clientX + window.pageXOffset;
    let posY = event.clientY + window.pageYOffset;
    menuOp.afficherMenu(posX, posY, tabOp);
    optionDisplay = true;
}

/**
* Supprime le menu d'options
*/
function deleteOptions(){
    $("#options").children().slice().remove();
    optionDisplay = false;
}

/**
* Création d'un nouveau pad
* @param parent : le parent du nouveau pad
*/
function addPad(parent){
    let namePad = prompt("Entrez le nom du nouveau pad : ", "");
    if (namePad == null || namePad == "") {
        return 1;
    }
    // @nono : une meilleur validation des noms des pads serait chouette ;
    // on boucle tant qu'on n'a pas un nom valable, ou une action d'annulation ?
    // Faire attention si le nom du pad permet l'introduction d'une faille XSS !


    // @nono : À la place d'un formulaire caché, on devrait plutôt faire une
    // requête AJAX directement vers le serveur sans éditer l'HTML.
    // Voir les API REST et leurs implémentations en JS.

    // Création du formulaire caché
    let form = document.createElement("form");
    form.setAttribute("method","POST");
    form.setAttribute("action", "/api/add/pad");

    let inputName = document.createElement("input");
    inputName.setAttribute("type","hidden");
    inputName.setAttribute("name","name");
    inputName.setAttribute("value",namePad);

    let inputParent = document.createElement("input");
    inputParent.setAttribute("type","hidden");
    inputParent.setAttribute("name","parent");
    inputParent.setAttribute("value",parent);

    form.appendChild(inputName);
    form.appendChild(inputParent);
    document.body.append(form)
    form.submit();
}


// A faire plus tard : fonctions pour les options
function deleteDirectory(){
    alert("Fonctionnalité non développée, c'est pour bientôt ;)");
}

function renameDirectory(){
    alert("Fonctionnalité non développée, c'est pour bientôt ;)");
}

function addDirectory(){
    alert("Fonctionnalité non développée, c'est pour bientôt ;)");
}


function displayPadMenu(event, pad){
    event.preventDefault();
    var op1 = new Option("Renommer", renamePad);
    var op2 = new Option("Supprimer", deletePad);
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    var menuOp = new menuOptions(tabOp)
    let posX = event.clientX + window.pageXOffset;
    let posY = event.clientY + window.pageYOffset;
    menuOp.afficherMenu(posX, posY, tabOp);
    optionDisplay = true;
}

function renamePad(){

}

function deletePad(){

}
