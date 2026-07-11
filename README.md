# Youtube-Shorts-Automatizador
La explicacion se encuentra tanto en version en español como version en ingles.
The explanation is available in both Spanish and English versions.

Indice:

1. ¿Qué es un Automatizador de Shorts?
2. ¿Cual es la estructura del proyecto y qué hace cada modulo de codigo?
3. ¿Cómo funciona el Automatizador de Shorts?
4. ¿Qué necesito para hacerlo funcionar?
5. ¿Cómo lo hago funcionar?
6. ¿Qué cosas se pueden cambiar a gusto del usuario?

1. Un automatizador de shorts es un programa encargado de seleccionar imagenes, fondos, musica y textos para ensamblarlos y publicarlos en un canal de Youtube, Tik-Tok, o Instagram en formato de Short o Reel de manera Automatizada para que el usuario no necesite realizar la edicion y publicacion manualmente.

2. Estructura de carpetas:
youtube-shorts-automatizador/
├── .gitignore #Encargado de evitar la subida de archivos especificos a github por seguridad.
├── LICENSE #La licencia del repositorio.
├── README.md #La explicacion sobre el proyecto y su funcionamiento.
├── requirements.txt #Requisitos para utilizar el proyecto en otra PC
│
├── comentarios/    #Carpeta donde se deben colocar imagenes para generar comentarios.
│   ├── disponibles/ #Carpeta que almacena las imagenes que generan comentarios que aun no fueron usadas.
│   └── usados/ #Carpeta que almacena las imagenes que generan comentarios que ya fueron utilizadas.
│
├── database/  #Carpeta encargada de almacenar la Base de Datos y el archivo .sql que se encarga de la estructuracion de la misma.
│   └── registro.sql
│
├── fondos/ #Carpeta encargada de almacenar los fondos para los shorts en formato de imagen.
│   ├── disponibles/ #Carpeta encargada de almacenar los fondos que aun no se utilizaron
│   └── usados/ #Carpeta encargada de almacenar los fondos ya utilizados.
│
├── fuentes/ #La fuente para el texto del short.
│   └── Anton/ #Carpeta del tipo de fuente.
│       ├── Anton-Regular.ttf #Archivos de la fuente para el texto.
│       └── OFL.txt
│
├── likes/  #Carpeta que almacena las imagenes que piden likes a la persona que vea el short.
│   ├── disponibles/ #Carpeta que almacena las imagenes para pedir likes que aun no fueron utilizadas
│   └── usados/ #Carpeta que almacena las imagenes para pedir likes ya utilizadas
│
├── memes/ #Carpeta que almacena los memes para los shorts.
│   ├── disponibles/ #Carpeta que almacena los memes no utilizados aun
│   └── usados/ #Carpeta que almacena los memes ya utilizados.
│
├── metadata/ #Carpeta encargada de almacenar a "Metadata.json" el cual es un diccionario con los titulos para cada short, descripciones y hashtags.
│   └── metadata.json #Archivo encargado de proporcionar los metadatos para la subida del short a youtube.
│
├── musica/ #Carpeta que almacena la musica de fondo de los shorts.
│   ├── disponibles/ #Carpeta que almacena la musica de fondo de los shorts sin utilizar
│   └── usados/  #Carpeta que almacena la musica de fondo de los shorts ya utilizados
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
    │   └── subidor.py #Encargado de subir el short a tu cuenta de youtube en modo privado para que solo tengas que ajustar la hora de publicacion.
    │
    └── api_memes_google/ #Codigo encargado de la conexion con la api de memes (Creada por D3vd) para descargar memes y con la api de google para realizarle consultas a Gemini.
        ├── descargador_y_verificador_memes.py #Encargado de traer memes de la api y verificar si ya han sido descargados alguna vez. En caso de que no seran enviados a Gemini para su evaluacion
        ├── verificador_categoria_google.py #Encargado de verificar a que categoria de las carpetas que tiene el usuario en memes / disponibles corresponde el meme o si debe ser descartado (+18)
        └── verificadores_creador_sql.py #Encargado de almacenar todas las funciones para la busqueda en la base de datos y los registros en la misma.

3. El automatizador de shorts funciona extrayendo memes desde una API publica llamada Meme-API creada por D3vd. De esta manera el programa obtiene los memes y posteriormente los somete a un filtro simple para evitar repetidos. El filtro consiste en tres etapas:

Etapa 1:
    Se obtiene el nombre del archivo del meme y se comprueba si el nombre ya existe en una base de datos sqlite3 (esta base de datos se crea al ejecutar armador.py por primera vez). Si el nombre ya existe simplemente se descarta el meme y se prosigue a analizar el siguiente. En caso de que el nombre no exista se avanza a la etapa 2.

Etapa 2:
    Se procede a descargar a la memoria RAM la imagen del meme (de esta manera se evita descargarla a el disco duro) y posteriormente se le extrae su Phash (El pHash permite identificar imagenes aunque hayan sido comprimidas o redimensionadas permitiendo asi evitar repetidos aunque se le haya cambiado el nombre). Acto seguido se realiza una comprobacion rapida en la base de datos para examinar si el pHash correspondiente a esa imagen ya fue registrado. Si ya fue registrado es descartado en caso contrario se avanza a la etapa 3.

Etapa 3:
    Al comprobar que la imagen nunca antes fue utilizada, se le realiza una codificacion en base64 para obtener una cadena de texto la cual sera enviada junto a un prompt a gemini (la IA de google). En el prompt se le aclara a Gemini que debe responder con el nombre de una de las carpetas del usuario ubicadas en "memes / disponibles". Si la categoria del meme no corresponde a ningun nombre de las carpetas existentes se le pide que responda "varios" para poder almacenar el meme en una carpeta que junte a aquellos que no tengan una categoria especifica. Ademas se le pide especificamente que si el contenido posee contenido sexual o insinuante responda con "descartado". En este caso el automatizador era para un canal de memes en español asi que los subreddits desde donde se extraen los memes son de memes en español. Tambien debido a esto se le agrego un filtro extra en el prompt el cual es que si el meme esta en ingles responda con "descartado". Finalmente si Gemini responde con "varios" o alguno de los nombres de las carpetas del usuario se procede a realizar el registro en la base de datos con el nombre, el pHash y la categoria, si Gemini respondio "Descartado" el meme es ignorado y se repite el proceso en bucle.

Este filtro sucede dentro de un bucle el cual se rompera unicamente cuando el usuario tenga suficientes memes en cada carpeta para cubrir la cantidad de shorts que solicito (por cada short se utilizan 2 memes), puede llegar a pasar que el usuario ya tenga la cantidad de memes necesarios y simplemente el bucle sera ignorado. Esto debido a que en el peor de los escenarios puede llegar a pasar que una unica carpeta sea la seleccionada al azar todos los intentos siendo necesario por esto que todas las carpetas tengan para cumplir con la cantidad de shorts solicitada.

En caso de que el usuario no tenga conexion a internet se realizara un conteo rapido de los memes en sus carpetas y se le avisara de si tiene suficientes o si no le alcanzan para cubrir el peor de los escenarios (el cual seria de que se repita la misma carpeta siempre). Se le preguntara al usuario si quiere proseguir o si quiere detenerse a rellenar las carpetas. Esto sucede debido a que en caso de que el programa seleccione una carpeta vacia de memes ira a buscar a la carpeta de su misma categoria en la parte de "memes / usados" y copiara su contenido a la carpeta original para poder seguir con el funcionamiento del programa mediante el reciclaje de memes ya utilizados. En caso de que la carpeta de usados tampoco tenga memes se le solicitara al usuario rellenarla con minimo 2 memes para asegurar su funcionamiento. Lo mismo sucedera con la carpeta de musica, likes, fondos y comentarios aunque en el caso de estos sera necesario rellenarlos con minimo 1 archivo de su tipo.

Finalmente el programa seleccionara 2 memes de una de las carpetas que se encuentran en "memes / disponibles", una musica aleatoria , un fondo aleatorio, una imagen para generar comentarios aleatoria y una imagen para generar likes aleatoria. Posteriormente le pasara estos archivos a ensamblador.py el cual sera el encargado de ajustarlos y ensamblar el short para su posterior subida.

Cuando ensamblador.py termina de armar el short el mismo es subido a la cuenta de youtube del usuario mediante subidor.py el cual se encarga de leer el archivo "metadata.json" de la carpeta "metadata" y determinar el titulo, descripcion y hashtags que deberan acompañar al short.

Finalmente armador.py muestra en pantalla si el short se subio exitosamente y realiza el movimiento de los archivos utilizados a sus respectivas carpetas de usados.

4. Para utilizarlo


