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

async function enviar_y_recibir_datos() {
    const h2_informacion = document.getElementById("resultado_ensamblaje")
    h2_informacion.innerText = ""
    const input_shorts = document.getElementById("cantidad_shorts")

    const respaldar_db = document.querySelector("input[name='opcion_respaldo_db']:checked")
    const reutilizar_memes = document.querySelector("input[name='opcion_reutilizar_memes']:checked")
    const cantidad_shorts = input_shorts.valueAsNumber
    
    if (!respaldar_db) {
        h2_informacion.innerText = "Falta aclarar si se tiene permitido respaldar la base de datos"
        return
    } else if (!reutilizar_memes) {
        h2_informacion.innerText = "Falta aclarar si se tiene permitido reutilizar memes"
        return
    } else if (!cantidad_shorts){
        h2_informacion.innerText = "Falta introducir la cantidad de shorts a crear"
        return
    } 
    
    input_shorts.disabled = true

    const datos = {
        "respaldar_db": respaldar_db.value,
        "reutilizar_memes": reutilizar_memes.value,
        "cantidad_shorts": cantidad_shorts
    }
    try{
        const respuesta = await fetch("http://localhost:8080/ensamblar-short", {
        method: "POST",
        headers: {
        "Content-Type": "application/json" 
        },
        body: JSON.stringify(datos)
        });
        const resultado = await respuesta.json()
        const informacion = resultado.respuesta
        h2_informacion.innerText = informacion
    } catch (error) {
        h2_informacion.innerText = "Hubo un error con el servidor. Vuelva a intentar la creacion del short."
    } finally {
        input_shorts.disabled = false
    }
}

function recibir() {
    fetch("http://localhost:8080/test")
    .then(paquete => paquete.json())
    .then(datos => {
        console.log(datos.respuesta)
        const test = document.getElementById("test_flask")
        test.innerText = datos.respuesta
    }) 
}