function esperar(milisegundos) {
    return new Promise(function(resolve) {
        setTimeout(resolve, milisegundos);    
    });
}

async function procesar(){
    let contador = 1
    const h2_puntitos = document.getElementById("encabezado_puntitos")
    while (true) {
        h2_puntitos.innerText = `Procesando${".".repeat(contador)}`
        await esperar(1000)
        contador = contador + 1
        if (contador == 7) {
            contador = 1
        }
    }
}

function test() {
    fetch("http://localhost:8080/test")
    .then(paquete => paquete.json())
    .then(datos => {
        console.log(datos.respuesta)
        const test = document.getElementById("test_flask")
        test.innerText = datos.respuesta
    }) 
}