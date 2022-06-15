class menuOptions{

    //Options est un tableau d'options
    constructor(options){
        this.options = options;
    }

    afficherMenu(posx, posy, options) {
        let m = $("#options");
        m.css("margin-left", posx);
        //m.css("margin-top", posy);

        m.onmouseover = function () {
            this.style.cursor = 'pointer';
        }
        m.append("<ul class='dropdown-menu'>");
        for (var i = 0; i < options.length; ++i) {
            m.append("<p class='dropdown-item'>" + options[i].getName() + "</p>");
        }
        m.append("</ul>");

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
