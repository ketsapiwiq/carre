/**
    Script appelé au 1er chargement de la page
    - Initialise tous les composants dont on a besoin :
        - Menu
        - Pad (Création d'un pad par défaut si besoin)
        - Options
 */

var menu;
// Liste de tous les pads
var pads = [];

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

    var socket = io();

    socket.on('broadcast_response', function(data) {
        updateMenu(JSON.stringify(data));
    })

    socket.on('error', function(data){
        alert(data);
    })
}

function createMenu(indice){

    for(i = indice; i < menu.length - 1; ++i){
        if(menu[i]['isDirectory']){
            let liste = document.getElementById(menu[i]['parent']);
            let sousListe = document.createElement("ul");
            sousListe.setAttribute("class", "parent");
            sousListe.setAttribute("id", menu[i]['name']);
            let titre = document.createElement("h2");
            titre.innerText = menu[i]['name'];
            sousListe.appendChild(titre);
            liste.appendChild(sousListe);
            //console.log("Création de : " + menu[i]['name']);

            // Repère les pads
            for(j = i+1; j < menu.length; ++j){
                if(menu[i]['name'] == menu[j]['parent']){
                    //console.log(menu[j]['name'] + " a pour parent " + menu[i]['name']);
                    //console.log(j + " : " + menu[j]['name']);
                    if(!menu[j]['isDirectory']){
                        titre = document.createElement("li");
                        titre.innerText = menu[j]['name'];
                        sousListe.appendChild(titre);
                        liste.appendChild(sousListe);
                    }
                }
            }
            // Repère les dossiers
            for(k = i+1; k < menu.length; ++k){
                if(menu[i]['name'] == menu[k]['parent'] && menu[k]['isDirectory']){
                    createMenu(k);
                }
            }
        }
    }
}

function updateMenu(data){
    $("#liste").children().slice().remove();
    menu = JSON.parse(data);
    let directory = [];
    var menuHtml = $("#liste");
    menuHtml.append("<ul>");
    console.log(menu);

    // Initialise le tableau des dossiers
    for (let i = 0; i < menu.length; ++i){
        if(menu[i]['isDirectory']){
            directory.push(menu[i]['name']);
        }
        else{
            pads.push({'name': menu[i]['name'], 'adresse': menu[i]['adresse']});
        }
    }
    let liste = document.querySelector("#liste>ul");
    let sousListe = document.createElement("ul");
    sousListe.setAttribute("class", "parent");
    sousListe.setAttribute("id", "Root");

    liste.appendChild(sousListe);

    // Afficher les pads de Root
    for(let x = 0; x < menu.length; ++x){
        if(menu[x]['parent'] == "Root" && !menu[x]['isDirectory']){
            let liste = document.getElementById("Root");
            titre = document.createElement("li");
            titre.innerText = menu[x]['name'];
            liste.appendChild(titre);
        }
    }
    createMenu(1);


    //------Ajout des EventListener--------//

    $("body").contextmenu(function(){
        if(!clickMenu && !optionDisplay){
        defaultMenu(event);
        }
    })
    //Click sur le nom d'un pad
    $("ul>li").click(function(){
        updateIFrame($(this));
    });

    //Click droit sur le nom d'un pad
    $("ul>li").contextmenu(function(event){
        if(!optionDisplay){
            clickMenu = true;
            // Récupérer le nom du parent
            //alert(this.parentNode.id);
            padMenu(event, $(this), this.parentNode.id);
        }
    });

    //Passage de la souris sur le nom d'un pad
    $("ul>li").hover(function(){
        $(this).css('cursor','pointer');
    });

    //Click droit sur le nom d'un dossier
    $("ul.parent>h2").contextmenu(function(event){
        if(!optionDisplay){
            clickMenu = true;
            directoryMenu(event, $(this));
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
    for (var i = 0; i < pads.length; i++){
        if(text == pads[i]['name']){
            return pads[i]['adresse'];
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

function defaultMenu(event){
    event.preventDefault();
    let paramCreaDirectory = ["Nom du nouveau dossier : ", "Root", "addDirectory"];
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
function directoryMenu(event, parent){
    event.preventDefault();
    let paramAjoutPad = ["Entrez le nom du nouveau pad : ", parent.text(), "addPad"];
    let paramRenameDirectory = ["Nouveau nom du dossier :", parent.text(), "renameDirectory"];
    let paramAddDirectory = ["Entrez le nom du nouveau dossier :", parent.text(), "addDirectory"];

    var op1 = new Option("Ajouter un pad", createDialog, paramAjoutPad);
    var op2 = new Option("Supprimer le dossier", deleteDirectory, parent.text());
    var op3 = new Option("Renommer le dossier", createDialog, paramRenameDirectory);
    // Dernière option : création d'un sous-dossier
    var op4 = new Option("Ajouter un dossier", createDialog, paramAddDirectory);
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
    tabOp.push(op3);
    tabOp.push(op4);
    displayMenu(tabOp);
}

function padMenu(event, pad, parent){
    event.preventDefault();

    let paramRenamePad = ["Nouveau nom du pad :", [pad.text(), parent], "renamePad"];
    let paramRemovePad = [pad.text(), parent];

    var op1 = new Option("Renommer", createDialog, paramRenamePad);
    var op2 = new Option("Supprimer", deletePad, paramRemovePad);
    var tabOp = new Array();
    tabOp.push(op1);
    tabOp.push(op2);
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

        d.append("<form method='POST' onsubmit='return " + param[2] + "(this,\"" + param[1] + "\")'><input type='text'name='name'><button type='submit'>OK</button><button type='button' id='cancel'> Annuler </button></form>");

        $("#cancel").click(function(){
            deleteDialog("#dialog");
        });
    }

}

function createAJAX(data, url){
    fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
      })
    })
    .then(function(){
        deleteDialog("#dialog");
        optionDisplay = false;
    })
    .catch(function(error) {
        console.error("Catch : " + error);
    })

}

/**
* Création d'un nouveau pad
* @param form : le formulaire d'ajout du pad
* @param parent : le parent du nouveau pad
*/
function addPad(form, parent){
    event.preventDefault();
    let data = {name : form.name.value, parent : parent};
    var url = "/api/add/pad";
    createAJAX(data, url);

}

    // -- REGEX -- //
    // [^&+<+>+\?+!+]
    // ^[a-z0-9]+$/i
    // \d+|[A-Z]+|[a-z]+)+/g"

    // @nono : une meilleur validation des noms des pads serait chouette ;
    // on boucle tant qu'on n'a pas un nom valable, ou une action d'annulation ?
    // Faire attention si le nom du pad permet l'introduction d'une faille XSS !

    // Voir les API REST et leurs implémentations en JS.



// Faire en sorte que la fenêtre de dialogue se ré-ouvre si le nom du pad est invalide


function deleteDirectory(nameDir){
    let data = {nameDir : nameDir};
    let url = 'api/remove/dir';
    createAJAX(data, url);
}

function renameDirectory(form, oldName){
    data = {oldName: oldName, newName: form.name.value};
    url = '/api/rename/dir';
    createAJAX(data, url);
    return false;
}


function addDirectory(form, parent){
    event.preventDefault();
    let data = {name : form.name.value, parent : parent};
    let url = "/api/add/dir";
    createAJAX(data, url);
    return false;
}


function deletePad(paramRemovePad){
  let data = {name : paramRemovePad[0], parent: paramRemovePad[1]};
  let url = "/api/remove/pad";
  createAJAX(data, url);
}

function renamePad(form, paramRename){
    paramRename = paramRename.split(",");
    let data = {oldName: paramRename[0], newName: form.name.value, parent: paramRename[1]};
    let url = "/api/rename/pad";
    createAJAX(data, url);
    return false;
}
