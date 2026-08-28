CREATE TABLE IF NOT EXISTS Memes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Categoria TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Phash TEXT NOT NULL,
    Fecha TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado BOOLEAN DEFAULT 0 CHECK (Estado IN (0,1))
);

CREATE TABLE IF NOT EXISTS Musica (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado BOOLEAN DEFAULT 0 CHECK (Estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Fondos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado BOOLEAN DEFAULT 0 CHECK (Estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Likes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado BOOLEAN DEFAULT 0 CHECK (Estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Comentarios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Fecha_uso TEXT,
    Estado BOOLEAN DEFAULT 0 CHECK (Estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Revisiones (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL UNIQUE,
    Fecha_modificacion TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS nombres_memes ON Memes(Nombre);
CREATE INDEX IF NOT EXISTS Phash_memes ON Memes (Phash);
CREATE INDEX IF NOT EXISTS disponibilidad ON Memes (Estado);

CREATE INDEX IF NOT EXISTS Nombres_musica ON Musica (Nombre);
CREATE INDEX IF NOT EXISTS Estado_musica ON Musica (Estado);

CREATE INDEX IF NOT EXISTS Nombres_Fondos ON Fondos (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Fondos ON Fondos (Estado);

CREATE INDEX IF NOT EXISTS Nombres_Comentarios ON Comentarios (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Comentarios ON Comentarios (Estado);

CREATE INDEX IF NOT EXISTS Nombres_Likes ON Likes (Nombre);
CREATE INDEX IF NOT EXISTS Estado_Likes ON Likes (Estado);

CREATE INDEX IF NOT EXISTS Nombres_Revision ON Revisiones (Nombre);
CREATE INDEX IF NOT EXISTS Fechas_Revision ON Revisiones (Fecha_modificacion);