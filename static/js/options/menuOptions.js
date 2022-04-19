class menuOptions{

    //Options est un tableau d'options
    constructor(options){
        this.options = options;
    }

    // A voir plus tard
    afficherMenu(posx, posy, options) {
        let m = $("#options");
        // Possible de factoriser les lignes liées au style
        m.css("margin-left", posx);
        m.css("margin-top", posy);

        m.onmouseover = function () {
            this.style.cursor = 'pointer';
        }
        //console.log(options[0].getName());
        for (var i = 0; i < options.length; ++i) {
            //mettre un event listener sur les p et récupérer le texte et lancer la fonction associée
            //m.append("<p onclick='" + options[i].action() + "'>" + options[i].getName() + "</p>");
            m.append("<p>" + options[i].getName() + "</p>");
        }
        // Pas optimisé
        $("#options p").click(function() {
            let optionName = $(this).html();
            for(let i = 0; i < options.length;++i){
                if(optionName == options[i].getName()){
                    options[i].action();
                }
            }
        });

    }



}