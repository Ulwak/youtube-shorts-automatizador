CREATE TABLE IF NOT EXISTS memes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Categoria TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Phash TEXT NOT NULL,
    Ruta TEXT NOT NULL,
    Fecha TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado INTEGER NOT NULL DEFAULT 0 CHECK (Estado IN (0,1))
);

CREATE TABLE IF NOT EXISTS musica (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado INTEGER NOT NULL DEFAULT 0 CHECK (Estado IN (0, 1)),
    Ruta TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS fondos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado INTEGER NOT NULL DEFAULT 0 CHECK (Estado IN (0, 1)),
    Ruta TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS likes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado INTEGER NOT NULL DEFAULT 0 CHECK (Estado IN (0, 1)),
    Ruta TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comentarios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado INTEGER NOT NULL DEFAULT 0 CHECK (Estado IN (0, 1)),
    Ruta TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS revisiones (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL UNIQUE,
    Fecha_modificacion TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS nombres_memes ON memes(Nombre);
CREATE INDEX IF NOT EXISTS Phash_memes ON memes (Phash);
CREATE INDEX IF NOT EXISTS Ruta_memes On memes (Ruta);
CREATE INDEX IF NOT EXISTS Estado_memes ON memes (Estado);

CREATE INDEX IF NOT EXISTS Nombres_Musica ON musica (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Musica ON musica (Estado);
CREATE INDEX IF NOT EXISTS Rutas_Musica ON musica (Ruta);

CREATE INDEX IF NOT EXISTS Nombres_Fondos ON fondos (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Fondos ON fondos (Estado);
CREATE INDEX IF NOT EXISTS Rutas_Fondos ON fondos (Ruta);

CREATE INDEX IF NOT EXISTS Nombres_Comentarios ON comentarios (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Comentarios ON comentarios (Estado);
CREATE INDEX IF NOT EXISTS Rutas_Comentarios ON comentarios (Ruta);

CREATE INDEX IF NOT EXISTS Nombres_Likes ON likes (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Likes ON likes (Estado);
CREATE INDEX IF NOT EXISTS Rutas_Likes ON likes (Ruta);

CREATE INDEX IF NOT EXISTS Nombres_Revision ON revisiones (Nombre);
CREATE INDEX IF NOT EXISTS Fechas_Revision ON revisiones (Fecha_modificacion);