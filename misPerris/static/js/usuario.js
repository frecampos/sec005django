class usuario{
    //propiedades
    rut;
    nombre;
    fecha;
    //mutadores
    setRut(rut){ this.rut = rut;}
    setNombre(nombre){ this.nombre= nombre;}
    setFecha(fecha){ this.fecha=fecha;}
    //accesadores
    getRut(){ return this.rut;}
    getNombre(){ return this.nombre;}
    getFecha(){ return this.fecha;}
    // tostring
    imprimir(){
        return 'Nombre:'+this.nombre+' Rut:'+this.rut+' Fecha:'+this.fecha;
    }
}