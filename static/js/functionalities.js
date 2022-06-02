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

function deleteDirectory(nameDir){
    let data = {nameDir : nameDir};
    let url = '/api/remove/dir';
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
