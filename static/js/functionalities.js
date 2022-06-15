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
    if(form.name.value.trim() == ''){
        alert("Le nom du pad n'est pas valide");
        return false;
    }
    let data = {name : form.name.value, parent : parent, idCo: idConnexion};
    var url = "/api/add/pad";
    createAJAX(data, url);
}

function deleteDirectory(nameDir){
    let data = {nameDir : nameDir, idCo: idConnexion};
    let url = '/api/remove/dir';
    createAJAX(data, url);
}

function renameDirectory(form, oldName){
    if(form.name.value.trim() == ''){
        alert("Le nom du dossier n'est pas valide");
        return false;
    }
    data = {oldName: oldName, newName: form.name.value};
    url = '/api/rename/dir';
    createAJAX(data, url);
    return false;
}


function addDirectory(form, parent){
    event.preventDefault();
    if(form.name.value.trim() == ''){
        alert("Le nom du dossier n'est pas valide");
        return false;
    }
    let data = {name : form.name.value, parent : parent};
    let url = "/api/add/dir";
    createAJAX(data, url);
    return false;
}


function deletePad(paramRemovePad){
  let data = {name : paramRemovePad[0], parent: paramRemovePad[1], idCo: idConnexion};
  let url = "/api/remove/pad";
  createAJAX(data, url);
}

function renamePad(form, paramRename){
    paramRename = paramRename.split(",");
    if(form.name.value.trim() == ''){
        alert("Le nom du pad n'est pas valide");
        return false;
    }
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

        d.append("<form method='POST' onsubmit='return " + param[2] + "(this,\"" + param[1] + "\")'><input type='text'name='name' autofocus><button type='submit' type='button' class='btn btn-primary'>OK</button><button type='button' id='cancel' type='button' class='btn btn-danger'> Annuler </button></form>");

        //d.append("<div class='modal fade' id='inscription' data-bs-backdrop='static' data-bs-keyboard='false' tabindex='-1' aria-labelledby='staticBackdropLabel' aria-hidden='true'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'><h5 class='modal-title' id='staticBackdropLabel'>"+ param[0] +"</h5><button type='button' class='btn-close' data-bs-dismiss='modal' aria label='Close'></button> </div><form method='POST' onsubmit='return " + param[2] + "(this,\"" + param[1] + "\")'> <div class='modal-body'> <div class='mb-3'> <input type='text'name='name' autofocus></div><div class='mb-3'><label for='pseudo' class='col-form-label'>Pseudo: </label><input type='text' class='form-control' id='pseudo'></div></div><div class='modal-footer'><button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button><button type='submit' class='btn btn-primary' data-bs-dismiss='modal'>Understood</button></div></form></div></div></div>");

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

// GESTION DES COMPTES UTILISATEURS

function logInOrSignUp(title, url){
    event.preventDefault();
    window.stop();
    if(!dialogDisplay){
        dialogDisplay = true;
        let d = $("#dialog");
        /*d.css("position", "absolute");
        d.css("margin-left", "50%");
        d.css("margin-top", "10%");
        d.css("width", "40%");
        d.css("height", "15%");*/

        //d.append("<div class='modal-dialog'><div class='modal-content'><div class='modal-header'>")
        // onsubmit='return " + param[2] + "(this,\"" + param[1] + "\")'

        //onsubmit='return sendUserCredentials(this,\""+ url +"\")'
        // action='"+ url +"'

        //d.append("<h2 class='modal-title' id='staticBackdropLabel'>"+ title +"</h2></div></div>");

        d.append("<form method='POST' onsubmit='return sendUserCredentials(this,\""+ url +"\")'><input type='text' name='pseudo' autofocus> <input type='password' name='password'> <button type='submit'>OK</button><button type='button' id='cancel'> Annuler </button></form>");

        // d.append("<div class='mb-3'> <label for='pseudo' class='col-form-label'>Pseudo: </label><input type='text' class='form-control' id='pseudo'> </div>");
        //
        // d.append("<div class='mb-3'> <label for='password' class='col-form-label'>Mot de passe: </label><input type='password' class='form-control' id='password'> </div>");
        //
        // d.append("<div class='modal-footer'> <button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button> <button type='button' class='btn btn-primary'>Send message</button></div></div></div>");

        $("#cancel").click(function(){
            deleteDialog("#dialog");
        });

    }
    return false;
}



function sendUserCredentials(form, url){
    var data = {pseudo: form.pseudo.value, password: form.password.value};
    fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
      })
    })
    .then(response => response.json())
    .then(function(data){
        deleteDialog("#dialog");
        deleteDialog("#test");
        optionDisplay = false;
        // Si le serveur est OK --> renvoie l'id de connexion
        idConnexion = data['data'];
        updateForms();
    })
    .catch(function(error) {
        console.error("Catch : " + error);
    })
    return false;
}

function deleteAccount(){
    let data = {idConnexion: idConnexion};
    fetch('/api/deleteAccount',{
        method: "POST",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
    })
    .then(function(){
        idConnexion = -1;
        updateForms();
    })
    return false;
}

function deconnect(){
    idConnexion = -1;
    updateForms();
    return false;
}

function updateForms(){
    let t = $("#test");
    //t.children().slice().remove();
    if(idConnexion == -1){
        // Formulaire de connexion
        //t.append("<form method='POST' onsubmit='return logInOrSignUp(\""+'Inscription'+"\",\""+ '/api/signup' +"\")'><button type='submit'>Inscription</button></form>");

        urlInscription = '/api/signup'
        urlConnexion = '/api/login'
        t.append("<button type='button' class='btn btn-primary' data-bs-toggle='modal' data-bs-target='#inscription'>Inscription </button>");
        t.append("<div class='modal fade' id='inscription' data-bs-backdrop='static' data-bs-keyboard='false' tabindex='-1' aria-labelledby='staticBackdropLabel' aria-hidden='true'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'><h5 class='modal-title' id='staticBackdropLabel'>Inscription</h5><button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button></div><form method='POST' onsubmit='return sendUserCredentials(this,\""+ urlInscription +"\")'><div class='modal-body'><div class='mb-3'><label for='pseudo' class='col-form-label'>Pseudo: </label><input type='text' class='form-control' id='pseudo'></div><div class='mb-3'><label for='password' class='col-form-label'>Mot de passe: </label><input type='password' class='form-control' id='password'></div></div><div class='modal-footer'><button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button><button type='submit' class='btn btn-primary'data-bs-dismiss='modal'>Understood</button></div></div></form></div></div>");
        // Formulaire d'Inscription
        //t.append('<form method="POST" action="" onSubmit="return logInOrSignUp(' + "Inscription" + ", '//api//signup')" + '><button> InscriptionJS </button></form>');
        //t.append("<form method='POST' onsubmit='return logInOrSignUp(\""+'Connexion'+"\",\""+ '/api/login' +"\")'><button type='submit'>Connexion</button></form>");
        t.append("<button type='button' class='btn btn-primary' data-bs-toggle='modal' data-bs-target='#connexion'>Connexion </button>");
        t.append("<div class='modal fade' id='connexion' data-bs-backdrop='static' data-bs-keyboard='false' tabindex='-1' aria-labelledby='staticBackdropLabel' aria-hidden='true'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'><h5 class='modal-title' id='staticBackdropLabel'>Connexion</h5><button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button></div><form method='POST' onsubmit='return sendUserCredentials(this,\""+ urlConnexion +"\")'><div class='modal-body'><div class='mb-3'><label for='pseudo' class='col-form-label'>Pseudo: </label><input type='text' class='form-control' id='pseudo'></div><div class='mb-3'><label for='password' class='col-form-label'>Mot de passe: </label><input type='password' class='form-control' id='password'></div></div><div class='modal-footer'><button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button><button type='submit' class='btn btn-primary'data-bs-dismiss='modal'>Understood</button></div></div></form></div></div>");

    }else{
        // Formulaire de déconnexion
        //t.append("<h3> Connected as " + idConnexion + "</h3>");
        t.append("<form method='POST' onsubmit='return deconnect()'> <button> Déconnexion </button></form>");
        // Formulaire de suppression du compte
        t.append("<form method='POST' onsubmit='return deleteAccount()'> <button> Supprimer mon compte </button> </form>");
    }
}
