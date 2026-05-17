from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from pathlib import Path

ANCHO_DE_VIDEO = 1080
ALTO_DE_VIDEO = 1920
DURACION_DEL_SHORT = 8
TAMAÑO_MEME_SUPERIOR_INFERIOR = (int(ANCHO_DE_VIDEO * 0.85), int(ALTO_DE_VIDEO * 0.30))
TAMAÑO_MEMES_CENTRALES = (int(ANCHO_DE_VIDEO * 0.42), int(ALTO_DE_VIDEO * 0.18))
MARGEN_ALTURA = int(ALTO_DE_VIDEO * 0.03)

def size_de_imagenes(memes, fondo, like, musica, comentarios):
    imagen_fondo = ImageClip(str(fondo)).with_duration(DURACION_DEL_SHORT)

    imagen_memes = [ImageClip(str(i)).with_duration(DURACION_DEL_SHORT) for i in memes]

    datos = [like, comentarios]
    imagenes = [ImageClip(str(n)).with_duration(DURACION_DEL_SHORT) for n in datos]
    
    imagen_fondo = imagen_fondo.resized((ANCHO_DE_VIDEO, ALTO_DE_VIDEO))

    imagen_memes = [k.resized(TAMAÑO_MEME_SUPERIOR_INFERIOR) for k in imagen_memes]

    imagenes = [l.resized(TAMAÑO_MEMES_CENTRALES) for l in imagenes]

    return imagenes, imagen_fondo, imagen_memes

def textos_short_creacion_ubicacion():
    texto1 = TextClip(
        text="MEMES PARA TODOS/AS",
        font_size=57,
        font= str(Path(__file__).parent.parent / "fuentes" / "Anton" / "Anton-Regular.ttf"),
        color="#ff66cc",
        stroke_color="#ff00aa",
        stroke_width=3
    )

    texto2 = TextClip(
        text="LIKE Y SUSCRIBETE",
        font_size=57,
        font= str(Path(__file__).parent.parent / "fuentes" / "Anton" / "Anton-Regular.ttf"),
        color="#ff66cc",
        stroke_color="#ff00aa",
        stroke_width=3
    )

    return texto1, texto2

def ubicacion_de_imagenes(imagenes, imagen_memes, texto1, texto2):
    altura_meme_1_2 = imagen_memes[0].h
    y_meme1 = MARGEN_ALTURA 
    x_meme1_2 = int((ANCHO_DE_VIDEO - imagen_memes[0].w) / 2)

    texto1_y = int(MARGEN_ALTURA + altura_meme_1_2)
    texto1_x = int((ANCHO_DE_VIDEO - texto1.w) / 2)

    altura_centrales = imagenes[0].h
    y_central = MARGEN_ALTURA + altura_meme_1_2 + texto1.h
    x_central1 = int((ANCHO_DE_VIDEO - (imagenes[0].w * 2)) / 2)
    x_central2 = int(x_central1 + imagenes[0].w)

    texto2_y = int(MARGEN_ALTURA + altura_meme_1_2 + texto1.h + altura_centrales)
    texto2_x = int((ANCHO_DE_VIDEO - texto2.w) / 2)

    y_meme2 = int(MARGEN_ALTURA + altura_meme_1_2 + texto1.h + altura_centrales + texto2.h)
       
    imagen_memes[0] = imagen_memes[0].with_position((x_meme1_2, y_meme1))
    imagen_memes[1] = imagen_memes[1].with_position((x_meme1_2, y_meme2))

    texto1 = texto1.with_position((texto1_x, texto1_y))
    texto2 = texto2.with_position((texto2_x, texto2_y))

    imagenes[0] = imagenes[0].with_position((x_central1, y_central))
    imagenes[1] = imagenes[1].with_position((x_central2, y_central))

    return imagenes, imagen_memes, texto1, texto2

def ensamblar_short(imagenes, imagen_fondo, imagen_memes, texto1, texto2, musica):

    musica = AudioFileClip(str(musica)).with_duration(DURACION_DEL_SHORT)

    ubicacion_shorts = Path(__file__).parent.parent / "output"
    contador = len(list([n for n in ubicacion_shorts.iterdir() if n.is_file() and not n.name.startswith('.')]))
    nombre = f"short_{contador + 1:03d}.mp4"

    short = CompositeVideoClip([imagen_fondo, imagen_memes[0], texto1, imagenes[0], imagenes[1], texto2, imagen_memes[1]]).with_audio(musica)

    short.write_videofile(str(ubicacion_shorts / nombre))