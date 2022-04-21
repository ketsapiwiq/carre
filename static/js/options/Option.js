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
}