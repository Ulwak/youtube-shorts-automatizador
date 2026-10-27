let empezar_puntitos
const h2_puntitos = document.getElementById("encabezado_puntitos")

function iniciar_puntitos(){
    let contador = 0
    empezar_puntitos = setInterval(() => {
        contador = (contador + 1) % 5
        h2_puntitos.innerText = "Procesando" + ".".repeat(contador)}, 1000)
}

function detener_puntitos() {
    clearInterval(empezar_puntitos)
    h2_puntitos.innerText = ""
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
    } else if (cantidad_shorts <= 0) {
        h2_informacion.innerText = "La cantidad de shorts debe ser igual o mayor a 1."
        return
    } else if (!cantidad_shorts) {
        h2_informacion.innerText = "Falta introducir la cantidad de shorts a crear"
        return
    }

    iniciar_puntitos()
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
        detener_puntitos()
    }
}
