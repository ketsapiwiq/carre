class menuOptions{

    //Options est un tableau d'options
    constructor(options){
        this.options = options;
    }

    afficherMenu(posx, posy, options) {
        let m = $("#options");
        // Possible de factoriser les lignes liées au style
        m.css("margin-left", posx);
        m.css("margin-top", posy);

        m.onmouseover = function () {
            this.style.cursor = 'pointer';
        }

        for (var i = 0; i < options.length; ++i) {
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
