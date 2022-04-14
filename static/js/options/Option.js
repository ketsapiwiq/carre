class Option{
    constructor(name, fnct){
        this.name = name;
        this.function = fnct;
    }

    action(){
        this.function();
    }

    getName(){
        return this.name;
    }
}