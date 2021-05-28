
function valida() {
    /*var resp= validaRut();
    if (resp == false) {
        return false;
    }
    resp = validaFecha();
    if ( resp == false) {
        return false;
    }*/
    //alert('formulario validado');
    var resp= validaNombre();
    if (resp == false) {
        return false;
    }
    return true;
}
function validaNombre() {
    var nombre = document.getElementById("txtNombre").value;
    if (nombre.trim().length==0) {
        alert("nombre no trae nada");
        return false;
    }
    if (nombre.trim().length<3 || nombre.trim().length>25) {
        alert("largo del nombre incorrecto");
        return false;
    }
    return true;
}
function validaFecha() {
    var fechaControl = document.getElementById('txtFechaNaci').value;
    var fechaSistema = new Date();
    /////////////////// 
    var ano = fechaControl.slice(0,4);
    var mes = fechaControl.slice(5,7);
    var dia = fechaControl.slice(8,10);
    /*alert('Año:' + ano);
    alert('Mes:' + mes);
    alert('Dia:' + dia);*/
    var fechaDelControl = new Date(ano,(mes-1),dia);
    //alert(fechaDelControl);
    if ( fechaDelControl > fechaSistema ) {
        //alert('fecha de nacimiento incorrecta');
        //Swal.fire('fecha de nacimiento incorrecta');
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'fecha de nacimiento incorrecta'
          });
        return false;
    }
    //////////////////////
    // saber si tiene minimo 18 años
    var unDia = 24 * 60 * 60 * 1000; // transformar un dia en milisegundos
    var diferencia = Math.round(Math.abs((fechaSistema.getTime() - fechaDelControl.getTime()) / unDia));
    //alert('dias:' +diferencia);
    var anos = Math.round( diferencia / 365);
    //alert('Años:' + anos);
    if ( anos >= 18 ) {
        //alert('Puede adoptar un perrito, es mayor de edad '+anos);
        return true;
    }else{
        alert('No puede adoptar una mascota, usted tiene tan solo '+anos+' anos de edad');
        return false;
    }
}


function validaRut() {
    var rut = document.getElementById('txtRut').value;
    console.log(rut);
    //////////////// determinar largo del rut /////////////////
    if ( rut.length != 10 && rut.length !=9) {
        alert('largo del rut incorrecto, maximo largo 10 caracteres');
        return false;
    }
    if ( rut.length == 9) {
        rut = '0'+rut;
    }
    ///////////// recortar caracter tras caracter el rut ////////////
    var num = 3;
    var suma = 0;
    for (let index = 0; index < 8; index++) {
        var caracter = rut.slice(index,index+1); 
        //alert(caracter + ' x '+ num);
        suma = suma + (caracter * num);
        num = num - 1;
        if ( num == 1) {
            num = 7;
        }

    }
    //alert('Suma:' + suma);
    var resto = suma % 11; // resto de la division
    //alert('Resto:' + resto);
    var dv = 11 - resto;
    if ( dv > 9 ) {
        if ( dv == 10 ) {
            dv ='K';
        }else{
            dv = 0;
        }
    }
    //alert('DV:' + dv);
    var dv_usuario = rut.slice(-1).toUpperCase();
    if ( dv != dv_usuario ) {
        alert('rut incorrecto');
        return false;
    }else{
        //alert('rut correcto');
    }
    return true;
}