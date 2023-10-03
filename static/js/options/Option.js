/**
* Lie une fonction d'action et un nom
*/

class Option{
    constructor(name, fnct, paramFnct){
        this.name = name;
        this.function = fnct;
        this.paramFnct = paramFnct;
    }

    action(){
        this.function(this.paramFnct);
    }

    getName(){
        return this.name;
    }

    afficherForm(){
        
    }
}
