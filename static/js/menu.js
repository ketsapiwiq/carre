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
    eventsManager();
}

function eventsManager(){
    //------Ajout des EventListener--------//

    $("body").contextmenu(function(){
        if(!clickMenu && !optionDisplay){
        defaultMenu(event);
        }
    })
    //Click sur le nom d'un pad
    $("ul>li").click(function(){
        deleteDialog("#options");
        updateIFrame($(this));
    });

    //Click droit sur le nom d'un pad
    $("ul>li").contextmenu(function(event){
        deleteDialog("#options");
        if(!optionDisplay){
            deleteDialog("#options");
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
        deleteDialog("#options");
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
function findAdress(text){
    for (var i = 0; i < pads.length; i++){
        if(text == pads[i]['name']){
            return pads[i]['adresse'];
        }
    }
}
