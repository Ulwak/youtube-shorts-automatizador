from moviepy import ImageClip, AudioFileClip, CompositeVideoClip

ANCHO_DE_VIDEO = 1080
ALTO_DE_VIDEO = 1920
DURACION_DEL_SHORT = 8

def size_de_imagenes(memes, fondo, like, musica, comentarios):
    imagen_fondo = ImageClip(str(fondo)).with_duration(DURACION_DEL_SHORT)

    meme = [memes[0], memes[1]]
    imagen_memes = [ImageClip(str(i)).with_duration(DURACION_DEL_SHORT) for i in meme]

    datos = [like, comentarios]
    imagenes = [ImageClip(str(n)).with_duration(DURACION_DEL_SHORT) for n in datos]
    
    imagen_fondo = imagen_fondo.resized((ANCHO_DE_VIDEO, ALTO_DE_VIDEO))

    imagen_memes = [k.resized(width=int(ANCHO_DE_VIDEO * 0.85)) for k in imagen_memes]

    imagenes = [l.resized(width=int(ANCHO_DE_VIDEO * 0.42)) for l in imagenes]

    return imagenes, imagen_fondo, imagen_memes

def ubicacion_de_imagenes(imagenes, imagen_fondo, imagen_memes):

    

