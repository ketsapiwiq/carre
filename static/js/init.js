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
var dialogDisplay = false;
var clickMenu = false;

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

    $("body").contextmenu(function(){
        if(!clickMenu && !optionDisplay){
            displayDefaultMenu(event);
        }
    })
    //Click sur le nom d'un pad
    $("ul.child").click(function(){
        updateIFrame($(this));
    });

    //Click droit sur le nom d'un pad
    $("ul.child").contextmenu(function(event){
        if(!optionDisplay){
            clickMenu = true;
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
            clickMenu = true;
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
* Crée le menu contextuel d'options
* @param tabOptions : tableau contenant toutes les options que le menu doit contenir
**/
function displayMenu(tabOptions){
    var menuOp = new menuOptions(tabOptions);
    let posX = event.clientX + window.pageXOffset;
    let posY = event.clientY + window.pageYOffset;
    menuOp.afficherMenu(posX, posY, tabOptions);
    optionDisplay = true;
}

function displayDefaultMenu(event){
    event.preventDefault();
    let paramCreaDirectory = ["Nom du nouveau dossier : ", null, "addDirectory"];
    var op1 = new Option("Créer un dossier", createDialog, paramCreaDirectory);
    var tabOp = new Array();
    tabOp.push(op1);
    displayMenu(tabOp);
}


/**
* Création du menu d'options pour les dossiers
* @param event :
* @param parent : élément cliqué
*/
function displayDirectoryMenu(event, parent){
    event.preventDefault();

    let paramAjoutPad = ["Entrez le nom du nouveau pad : ", parent.text(), "syncAddPad"];
    let paramRenameDirectory = ["Nouveau nom du dossier :", parent.text(), "renameDirectory"];

    var op1 = new Option("Ajouter un pad", createDialog, paramAjoutPad);
    var op2 = new Option("Supprimer le dossier", deleteDirectory, parent.text());
    var op3 = new Option("Renommer le dossier", createDialog, paramRenameDirectory);
    var op4 = new Option("Ajouter un dossier", addDirectory);
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    tabOp.push(op3);
    tabOp.push(op4);
    displayMenu(tabOp);
}

/**
* Suppression des boîtes de dialogues et les menus
* @param element : la classe ou l'id dans le DOM pour lequel il faut supprimer les enfants
*/
function deleteDialog(element){
    $(element).children().slice().remove();
    $(element).removeAttr("style");
    optionDisplay = false;
    clickMenu = false;
    dialogDisplay = false;
}

/**
* Crée une boîte de dialogue avec un seul champ de contextmenu
* @param param : tableau de 3 paramètres
*         param[0] : titre de la boîte de dialogue --> résume l'action
*         param[1] : paramètre pour la bonne exécution de "param[2]"
*         param[2] : nom de la fonction à exécuter à la soumission du formulaire
**/
function createDialog(param){
    if(!dialogDisplay){
        dialogDisplay = true;
        let d = $("#dialog");
        d.css("position", "absolute");
        d.css("margin-left", "50%");
        d.css("margin-top", "10%");
        d.css("width", "40%");
        d.css("height", "15%");

        d.append("<h2>"+param[0]+"</h2>");

        d.append("<form onsubmit='return " + param[2] + "(this,\"" + param[1] + "\")'><input type='text'name='name'><button type='submit'>OK</button><button type='button' id='cancel'> Annuler </button></form>");

        $("#cancel").click(function(){
            deleteDialog("#dialog");
        });
    }

}

async function syncAddPad(form, parent){
    let data = {name : form.name.value, parent : parent};
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/api/add/pad');
    xhr.responseType = 'json';
    xhr.send(JSON.stringify(data));

    xhr.onload = function(){
        alert("la requête AJAX fonctionne");
    }

    xhr.onerror = function(){
        alert("Erreur : requête AJAX");
    }
}

/**
* Création d'un nouveau pad
* @param form : le formulaire d'ajout du pad
* @param parent : le parent du nouveau pad
*/
function addPad(form, parent){
    namePad = form.name.value;
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
    })
    .fail(function(){
      throw "Ajout du pad impossible";
      addPad(parent);
  })
  deleteDialog("#dialog");
  return false;


    // -- REGEX -- //
    // [^&+<+>+\?+!+]
    // ^[a-z0-9]+$/i
    // \d+|[A-Z]+|[a-z]+)+/g"

    // @nono : une meilleur validation des noms des pads serait chouette ;
    // on boucle tant qu'on n'a pas un nom valable, ou une action d'annulation ?
    // Faire attention si le nom du pad permet l'introduction d'une faille XSS !

    // Voir les API REST et leurs implémentations en JS.


}

// Faire en sorte que la fenêtre de dialogue se ré-ouvre si le nom du pad est invalide



// A faire plus tard : fonctions pour les options
function deleteDirectory(nameDir){
    $.ajax({
        url: 'api/remove/dir',
        method: 'POST',
        data: {nameDir : nameDir}
    })
    .done(function(response){
        updateMenu(response);
    })
    .fail(function(){
        throw "Suppression du dossier impossible";
    })
}

function renameDirectory(form, oldName){
    newName = form.name.value;
    $.ajax({
      url: "/api/rename/dir",
      method: "POST",
      data: {oldName: oldName, newName: newName}
    })
    .done(function(response){
      updateMenu(response);
    })
    .fail(function(){
      throw "Renommage du dossier impossible";
      return false;
  })
  deleteDialog("#dialog");
  return false;
}


function addDirectory(form){
    name = form.name.value;
    $.ajax({
        url:"/api/add/dir",
        method: "POST",
        data : {name: name}
    })
    .done(function(reponse){
        updateMenu(response);
        optionDisplay = false;
    })
    .fail(function(){
        throw "Ajout du dossier impossible"
        return false;
    })
    deleteDialog("#dialog");
    return false;
}


function displayPadMenu(event, pad){
    event.preventDefault();

    let paramRenamePad = ["Nouveau nom du pad :", pad.text(), "renamePad"];

    var op1 = new Option("Renommer", createDialog, paramRenamePad);
    var op2 = new Option("Supprimer", deletePad, pad.text());
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    displayMenu(tabOp);
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

function renamePad(form, oldName){
    newName = form.name.value;
    $.ajax({
      url: "/api/rename/pad",
      method: "POST",
      data: {oldName: oldName, newName: newName}
    })
    .done(function(response){
      updateMenu(response);
    })
    .fail(function(){
      throw "Renommage du pad impossible";
      return false;
  })
  deleteDialog("#dialog");
  return false;
}
