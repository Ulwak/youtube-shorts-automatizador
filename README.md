# Youtube-Shorts-Automatizador
La explicacion se encuentra tanto en version en español como version en ingles.
The explanation is available in both Spanish and English versions.

# Indice:

1. ¿Qué es un Automatizador de Shorts?
2. ¿Cual es la estructura del proyecto y qué hace cada modulo de codigo?
3. ¿Cómo funciona el Automatizador de Shorts?
4. ¿Cómo lo bajo a mi Visual Studio Code?
5. ¿Qué necesito para hacerlo funcionar?
6. ¿Cómo lo hago funcionar?
7. ¿Qué cosas se pueden cambiar a gusto del usuario?
8. ¿Cómo configuro un entorno ".venv" para evitar que las librerias se instalen globalmente en mi dispositivo?

1. Un automatizador de shorts es un programa encargado de seleccionar imagenes, fondos, musica y textos para ensamblarlos y publicarlos en un canal de Youtube, Tik-Tok, o Instagram (En este caso unicamente abarca Youtube) en formato de Short o Reel de manera Automatizada para que el usuario no necesite realizar la edicion y publicacion manualmente. (Ejemplo del automatizador puesto en practica en un canal: "https://www.youtube.com/@Ulwak-0")

2. Estructura de carpetas:

youtube-shorts-automatizador/
├── .gitignore #Encargado de evitar la subida de archivos especificos a github por seguridad.
├── LICENSE #La licencia del repositorio.
├── README.md #La explicacion sobre el proyecto y su funcionamiento.
├── requirements.txt #Requisitos para utilizar el proyecto en otra PC
│── .env.example #Archivo .env de ejemplo.
│
├── comentarios/    #Carpeta donde se deben colocar imagenes para generar comentarios.
│   
│   
│
├── database/  #Carpeta encargada de almacenar la Base de Datos y el archivo .sql que se encarga de la estructuracion de la misma.
│   └── registro.sql
│
├── fondos/ #Carpeta encargada de almacenar los fondos para los shorts en formato de imagen.
│   
│   
│
├── fuentes/ #La fuente para el texto del short.
│   └── Anton/ #Carpeta del tipo de fuente.
│       ├── Anton-Regular.ttf #Archivos de la fuente para el texto.
│       └── OFL.txt
│
├── likes/  #Carpeta que almacena las imagenes que piden likes a la persona que vea el short.
│   
│   
│
├── memes/ #Carpeta que almacena los memes para los shorts.
│  
│  
│
├── metadata/ #Carpeta encargada de almacenar a "metadata.json" el cual es un diccionario con los titulos para cada short, descripciones y hashtags.
│   └── metadata.json #Archivo encargado de proporcionar los metadatos para la subida del short a youtube.
│
├── musica/ #Carpeta que almacena la musica de fondo de los shorts.
│   
│   
│
├── output/ #Carpeta donde se generara el short al momento de finalizar el programa.
│   └── .gitkeep
│
└── src/ #Carpeta que almacena el codigo del programa.
    ├── armador.py #Script central encargado de gestionar el programa y organizar al resto de scripts para que realizen sus tareas correctamente.
    │
    ├── Base/ #Carpeta que incluye el codigo "Base" o principal del programa para el ensamblaje de videos.
    │   ├── ensamblador.py #Encargado de ensamblar el short con las imagenes/fondos/memes/musica/comentarios/like seleccionados por seleccionador.py
    │   ├── selector.py #Encargado de seleccionar los archivos para que ensamblador.py pueda realizar el ensamblaje del short.
    │   └── subidor.py #Encargado de subir el short a tu cuenta de youtube programado para que se publiquen con intervalos de 6 horas entre ellos.
    │
    └── api_memes_google/ #Codigo encargado de la conexion con la api de memes (Creada por D3vd) para descargar memes y con la api de google para realizarle consultas a Gemini.
        ├── descargador_y_verificador_memes.py #Encargado de traer memes de la api y verificar si ya han sido descargados alguna vez. En caso de que no seran enviados a Gemini para su evaluacion
        ├── verificador_categoria_google.py #Encargado de verificar a que categoria de las carpetas que tiene el usuario en "memes" corresponde el meme o si debe ser descartado (+18)
        └── verificadores_creador_sql.py #Encargado de almacenar todas las funciones para la busqueda en la base de datos y los registros en la misma.

3. El automatizador de shorts funciona descargando memes mediante varios workers desde una API publica llamada Meme-API creada por D3vd. De esta manera el programa obtiene los memes y posteriormente los somete a un filtro simple para evitar repetidos. El filtro consiste en tres etapas:

Etapa 1:
    Se obtiene el nombre del archivo del meme y se comprueba si el nombre ya existe en una base de datos sqlite3 (esta base de datos se crea al ejecutar armador.py por primera vez). Si el nombre ya existe simplemente se descarta el meme y se prosigue a analizar el siguiente. En caso de que el nombre no exista se avanza a la etapa 2.

Etapa 2:
    Se procede a descargar a la memoria RAM la imagen del meme (de esta manera se evita descargarla a el disco duro) y posteriormente se le extrae su Phash (El pHash permite identificar imagenes aunque hayan sido comprimidas o redimensionadas permitiendo asi evitar repetidos aunque se le haya cambiado el nombre). Acto seguido se realiza una comprobacion rapida en la base de datos para examinar si el pHash correspondiente a esa imagen ya fue registrado. Si ya fue registrado es descartado en caso contrario se avanza a la etapa 3.

Etapa 3:
    Al comprobar que la imagen nunca antes fue utilizada, se le realiza una codificacion en base64 para obtener una cadena de texto la cual sera enviada junto a un prompt a gemini (la IA de google). En el prompt se le aclara a Gemini que debe responder con el nombre de una de las carpetas del usuario ubicadas en "...memes/". Si la categoria del meme no corresponde a ningun nombre de las carpetas existentes se le pide que responda "varios" para poder almacenar el meme en una carpeta que junte a aquellos que no tengan una categoria especifica. Ademas se le pide especificamente que si el contenido posee contenido sexual o insinuante responda con "descartado". En este caso el automatizador era para un canal de memes en español asi que los subreddits desde donde se extraen los memes son de memes en español. Tambien debido a esto se le agrego un filtro extra en el prompt el cual es que si el meme esta en ingles responda con "descartado". Finalmente si Gemini responde con "varios" o alguno de los nombres de las carpetas del usuario se procede a realizar el registro en la base de datos con el nombre, el pHash, la categoria y posteriormente el guardado de la imagen en la carpeta correspondiente en el disco duro. Si Gemini respondio "Descartado" el meme es ignorado y se repite el proceso en bucle.

Este filtro sucede dentro de un bucle el cual se rompera unicamente cuando el usuario tenga suficientes memes en cada carpeta para cubrir la cantidad de shorts que solicito (por cada short se utilizan 2 memes), puede llegar a pasar que el usuario ya tenga la cantidad de memes necesarios y simplemente el bucle sea ignorado. Esto debido a que en el peor de los escenarios puede llegar a pasar que una unica carpeta sea la seleccionada al azar en todos los intentos siendo necesario por esto que todas las carpetas tengan para cumplir con la cantidad minima para los shorts solicitados.

En caso de que el usuario no tenga conexion a internet se realizara un conteo rapido de los memes en sus carpetas y se le avisara de si tiene suficientes o si no le alcanzan para cubrir el peor de los escenarios (el cual seria de que se repita la misma carpeta siempre). Se le preguntara al usuario si quiere proseguir o si quiere detenerse a rellenar las carpetas. Esto sucede debido a que en caso de que el programa seleccione una carpeta vacia de memes el mismo enviara una consulta SQL para colocar el estado de todos los memes en "no usados" en la base de datos (convirtiendo su estado de 1 a 0 en la base de datos) para poder seguir con el funcionamiento del programa mediante el reciclaje de memes ya utilizados. En caso de que luego de esto los memes no sean suficientes se le solicitara al usuario rellenarla con minimo 2 memes para asegurar su funcionamiento. Lo mismo sucedera con la carpeta de musica, likes, fondos y comentarios aunque en el caso de estos sera necesario rellenarlos con minimo 1 archivo de su tipo manualmente (En un futuro se incluira un autorrellenado para evitar trabajo manual).

Finalmente, el programa envia una consulta SQL para extraer la ruta de dos memes de una categoria al azar que no hayan sido utilizados, una musica aleatoria , un fondo aleatorio, una imagen para generar comentarios aleatoria y una imagen para generar likes aleatoria. Posteriormente le pasara estos archivos a ensamblador.py el cual sera el encargado de ajustarlos y ensamblar el short para su posterior subida.

Cuando ensamblador.py termina de armar el short el mismo es pasado a subidor.py el cual se encarga de consultar a la base de datos sobre el horario de subida del ultimo short para determinar a que hora debera programar el short siguiente (tienen 6 horas de diferencias entre ellos). En caso de que en la base de datos no se obtenga ningun registro, obtendra la hora y fecha del dispositivo para posteriormente tomar la decision. Luego de ese proceso se preparan los metadatos que requiere la API de Youtube para la subida del short y finalmente el short es subido al canal del usuario programado para alguno de los siguientes horarios: 05:45, 11:45, 17:45 y 23:45. Luego muestra un mensaje en pantalla de que la carga fue exitosa y registra en la base de datos el ID del short, el titulo con el que fue subido, su fecha de creacion y la fecha en la que se hara publico.

Finalmente armador.py se encarga de actualizar el estado de los memes, imagen para causar comentarios, imagen para pedir likes, la musica y el fondo a usados en la base de datos (Esto alterando la columna estado: 1 = Usado, 0 = Sin usar).

4. Para traer la estructura del proyecto y preparar el entorno usted debera abrir su Visual Studio Code en una carpeta de su preferencia, abrir una terminal y ejecutar "git clone https://github.com/Ulwak/youtube-shorts-automatizador.git". Se le bajara la estructura de carpetas, (En el proximo paso se le explicara que debe rellenar y que cosas debera agregar). Luego debera renombrar el archivo ".env.example" a ".env" (esto para que el programa pueda identificarlo correctamente). Luego puede crear carpetas de categorias de memes aunque si lo hace asegurese de agregar la categoria a los metadatos en "metadata.json" (ubicado en "metadata". Vease el paso 7.) siguiendo la estructura ya establecida (dentro de memes crear las subcarpetas como esta "varios" y en metadata.json crear el diccionario como esta el diccionario de "varios"). Finalmente debera realizar "pip install -r requirements.txt" para instalar las librerias necesarias para poder utilizar el proyecto sin que se produzcan errores (se recomienda configurar un entorno .venv de python para evitar instalarlas de manera global en su sistema operativo. Vease el paso 8).

5. Para utilizarlo debera ingresar como minimo 1 imagen en comentarios, likes, fondos y una musica en la carpeta musica. Luego debera ingresar a "https://aistudio.google.com/welcome" (Servicio de google desde el cual se deben crear las API KEY necesarias para utilizar Gemini), presionar el boton central que dice "Get started" y luego iniciar sesion. Luego debera dirigirse al apartado que dice "Proyectos" y presionar el boton de "Crear nuevo proyecto". Debera completar con un nombre (puede colocarle "Automatizador-Shorts" por ejemplo) y luego debera colocar un nombre para la clave que google le dara. Luego vera en el panel su proyecto con una seccion que dice "Claves", al presionar alli entrara a otro panel en el cual podra ver en la primer columna una serie de letras y numeros aleatorios NO DEBE COMPARTIRLOS CON NADIE O CON INTERNET BAJO NINGUN CONCEPTO SI QUIERE MANTER SU SEGURIDAD (esto debido a que las API KEY permiten que usted se identifique ante google para utilizar por ejemplo, un servicio de IA). Luego debera copiar todas esa letras dentro del archivo ".env" en el campo de "GEMINI" dentro de las "". Finalmente debera ir a "console.cloud.google.com/cloud-hub" crear un proyecto y en la seccion de IAM Administracion --> IAM --> otorgar acceso y ahi debera rellenar los campos: En entidad colocara el correo electronico del canal donde usted quiera subir los shorts, en rol colocara propietario. Luego debera abrir Visual Studio code y debera ejecutar el programa desde la carpeta src (...youtube-shorts-automatizador/src python actualizador_db.py) la cual actualizara los datos de la DB (Por favor no lo ejecutes 2 veces o podrias repetir datos) y luego cuando finalize deberas ejecutar "python armador.py" e ingresar la cantidad de shorts que usted necesita. Se recomienda producir tandas de 5 a 10 shorts por dia y para tandas de mas grandes (50 por ejemplo) se recomienda reutilizar los memes que fue almacenando con el tiempo. Finalmente cuando llegue el momento de la subida el programa le solicitara iniciar sesion en una pestaña de su navegador mediante los servicios de google, le advertiran de que la aplicacion no esta verificada aunque esto es a raiz de que cada persona que quiera usar el codigo debera crear un proyecto nuevo. No hay razon de preocupacion pues las unicas conexiones que realiza el programa con el exterior son para descargar los memes, verificar los memes con gemini y subir el short a youtube. Luego de que inicie sesion sus tokens (No debe compartirlos tampoco) se guardaran en ...Youtube-Shorts-Automatizador/src/Base/token.json y siempre y cuando se pueda el programa los renovara automaticamente. Finalmente puede esperar a que se realize la carga del short y utilizar o modificar el programa si lo requiere o prefiere.

6. Primero luego de ingresar todos los archivos en comentarios, musica, fondos y likes debera ejecutar una UNICA VEZ (esto debido a que aun esta en proceso y estamos mejorandolo ejecutarlo dos veces duplicaria las entradas en la base de datos) "actualizador_db.py" para que la base de datos detecte esos archivos que usted ya relleno. Finalmente debera ejecutar "python armador.py" desde su terminal estando en la carpeta src/ del su proyecto (...youtube-shorts-automatizador/src), luego indicar la cantidad de shorts y en caso de que sea necesario volver a iniciar sesion con la cuenta en la que se subiran los videos. El resto del proceso es automatico.

7. Usted puede modificar las categorias por las que quiere que Gemini clasifique aunque esto puede volver la clasificacion mucho mas tardada. Se recomienda encarecidamente no borrar carpetas que ya contengan memes clasificados en su interior para evitar fallas con el programa (se esta trabajando en ello). Siempre que añada una carpeta a "memes" debera añadir en metadata.json los datos correspondientes a los memes de esa carpeta como ya esta colocado con "varios". Se debera seguir la misma estructura. Si modifica el programa y consigue una mejora puede colaborar y ayudar a mejorarlo entre todos.

8. Para configurar un entorno ".venv" y evitar que las librerias se instalen de manera global en su dispositivo (lo cual no suele ser recomendable a largo plazo) usted debera abrir la carpeta raiz del proyecto en Visual Studio Code mediante "Open Folder" o "Abrir Carpeta" y luego abrir una terminal en la cual insertara el siguiente comando: "python -m venv .venv" y finalmente para activar el entorno ejecutara ".venv\Scripts\activate.bat" en su terminal. Luego de esto puede utilizar "pip install -r requirements.txt" para instalar las librerias que necesita el proyecto.

# Modificaciones objetivo en un futuro:

1. Lector automatico de archivos en likes, comentarios, y musica para que sean integrados a la DB sin necesidad de un script que deba ser ejecutado aparte.
2. Migrar de Moviepy a FFMPEG para mayor velocidad y eficiencia en los recursos del dispositivo al ensamblar un short.
3. Mayor manejo de errores.
4. Mayor sistema de logs.
5. Refactorizar para mantener el codigo mas legible.
6. Mas cafe.