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
            updateMenu(data);

        })
        .fail(function(){
            throw new Error("Récupération du menu impossible");
        })
}

function updateMenu(data){
    $("#liste").children().slice().remove();
    menu = JSON.parse(data);
    var menuHtml = $("#liste");
    menuHtml.append("<li>");
    for (var i in menu){
        menuHtml.append("<ul class='parent'><h2>" + menu[i]["parent"] + "</h2></ul>");
        for(var j in menu[i]["pads"]){
            menuHtml.append("<ul class='child'>" + menu[i]["pads"][j]["Nom"] + "</ul>");
        }
    }
    menuHtml.append("</li>");

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
        deleteDialog("#options");
    });
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
    var op3 = new Option("Renommer le dossier", renameDirectory, parent.text());
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
* Supprime les boîtes de dialogues et les menus
*/
function deleteDialog(element){
    $(element).children().slice().remove();
    $(element).removeAttr("style");
    optionDisplay = false;
}

/**
* Création d'un nouveau pad
* @param parent : le parent du nouveau pad
*/
function addPad(parent){

    let d = $("#dialog");
    // Possible de factoriser les lignes liées au style
    d.css("position", "absolute");
    d.css("margin-left", "50%");
    d.css("margin-top", "10%");
    d.css("width", "40%");
    d.css("height", "15%");

    d.append("<h2>Entrez le nom du nouveau pad : </h2>");

    //'formAddPad(this," + parent + ")'
    d.append("<form method='GET' onsubmit='return formAddPad(this,\"" + parent + "\")'><input type='text' name='padName'><button type='submit'>OK</button><button type='button' id='cancel'> Annuler </button></form>");

    $("#cancel").click(function(){
        deleteDialog("#dialog");
    });

    // -- REGEX -- //
    // [^&+<+>+\?+!+]
    // ^[a-z0-9]+$/i
    // \d+|[A-Z]+|[a-z]+)+/g"



    // @nono : une meilleur validation des noms des pads serait chouette ;
    // on boucle tant qu'on n'a pas un nom valable, ou une action d'annulation ?
    // Faire attention si le nom du pad permet l'introduction d'une faille XSS !

    // Voir les API REST et leurs implémentations en JS.

    //Requête AJAX
}

// Faire en sorte que la fenêtre de dialogue se ré-ouvre si le nom du pad est invalide

function formAddPad(form, parent){
    namePad = form.padName.value;
    // Regex qui ne fonctionne pas
    /*let regex = "[><?;!&\/=]+";
    let matching = regex.match(namePad);
    if(matching != null){
        alert("Pas Valide");
        // Si le pad n'est pas valide, on relance la fonction addPad (Pour ça, il faudrait que la regex marche :c )
    }else{
        alert("Valide");
    }*/
    $.ajax({
      url: "/api/add/pad",
      method: "POST",
      data: {name: namePad, parent: parent}
    })
    .done(function(response){
      updateMenu(response);
      return true;
    })
    .fail(function(){
      throw "Ajout du pad impossible";
      addPad(parent);
      return false;
  })
}


// A faire plus tard : fonctions pour les options
function deleteDirectory(){
    alert("Fonctionnalité non développée, c'est pour bientôt ;)");
}

function renameDirectory(elementName){
    let d = $("#dialog");

    d.css("position", "absolute");
    d.css("margin-left", "50%");
    d.css("margin-top", "10%");
    d.css("width", "25%");
    d.css("height", "15%");

    d.append("<h2>Nouveau nom du dossier : </h2>");

    d.append("<form method='GET' onsubmit='return formRenameDirectory(this,\"" + elementName + "\")'><input type='text' name='directoryName'><button type='submit'>OK</button><button type='button' id='cancel'> Annuler </button></form>");
    $("form").css("margin-left","25%");

    $("#cancel").click(function(){
        deleteDialog("#dialog");
    });
}

function formRenameDirectory(form, oldName){
    newName = form.directoryName.value;
    $.ajax({
      url: "/api/rename/dir",
      method: "POST",
      data: {oldName: oldName, newName: newName}
    })
    .done(function(response){
      updateMenu(response);
      return true;
    })
    .fail(function(){
      throw "Renommage du dossier impossible";
      addPad(parent);
      return false;
  })
}

function addDirectory(){
    alert("Fonctionnalité non développée, c'est pour bientôt ;)");
}


function displayPadMenu(event, pad){
    event.preventDefault();
    var op1 = new Option("Renommer", renamePad);
    var op2 = new Option("Supprimer", deletePad, pad.text());
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    var menuOp = new menuOptions(tabOp)
    let posX = event.clientX + window.pageXOffset;
    let posY = event.clientY + window.pageYOffset;
    menuOp.afficherMenu(posX, posY, tabOp);
    optionDisplay = true;
}

function deletePad(namePad){
    $.ajax({
      url: "/api/remove/pad",
      method: "POST",
      data: {name: namePad}
    })
    .done(function(response){
      updateMenu(response);
      optionDisplay = false;
      return true;
    })
    .fail(function(){
      throw "Impossible de supprimer ce pad";
      return false;
  })
}

function renamePad(){

}
