-- init_db.sql

CREATE TABLE IF NOT EXISTS TypesVoix (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    language_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Themes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Jours (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    heure TEXT NOT NULL,
    type_voix_id INTEGER NOT NULL,
    themes TEXT NOT NULL,
    son INTEGER NOT NULL CHECK(son BETWEEN 1 AND 100),
    FOREIGN KEY (type_voix_id) REFERENCES TypesVoix(ID)
);

CREATE TABLE IF NOT EXISTS HistoriqueJours (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    jour_id INTEGER NOT NULL,
    date_passage DATE NOT NULL DEFAULT CURRENT_DATE,
    son INTEGER NOT NULL,
    type_voix TEXT NOT NULL,
    lien_son TEXT,
    themes TEXT NOT NULL,
    FOREIGN KEY (jour_id) REFERENCES Jours(ID)
);

INSERT INTO TypesVoix (name, language_code) VALUES
('fr-FR-Neural2-A', 'fr-FR'),
('fr-FR-Neural2-B', 'fr-FR'),
('fr-FR-Neural2-C', 'fr-FR'),
('fr-FR-Neural2-D', 'fr-FR'),
('fr-FR-Neural2-E', 'fr-FR'),
('fr-FR-Standard-A', 'fr-FR'),
('fr-FR-Standard-B', 'fr-FR'),
('fr-FR-Standard-C', 'fr-FR'),
('fr-FR-Standard-D', 'fr-FR'),
('fr-FR-Standard-E', 'fr-FR'),
('fr-FR-Standard-F', 'fr-FR'),
('fr-FR-Standard-G', 'fr-FR'),
('fr-FR-Wavenet-A', 'fr-FR'),
('fr-FR-Wavenet-B', 'fr-FR'),
('fr-FR-Wavenet-C', 'fr-FR'),
('fr-FR-Wavenet-D', 'fr-FR'),
('fr-FR-Wavenet-E', 'fr-FR'),
('fr-FR-Wavenet-F', 'fr-FR'),
('fr-FR-Wavenet-G', 'fr-FR'),
('fr-CA-Neural2-A', 'fr-CA'),
('fr-CA-Neural2-B', 'fr-CA'),
('fr-CA-Neural2-C', 'fr-CA'),
('fr-CA-Neural2-D', 'fr-CA'),
('fr-CA-Wavenet-A', 'fr-CA'),
('fr-CA-Wavenet-B', 'fr-CA'),
('fr-CA-Wavenet-C', 'fr-CA'),
('fr-CA-Wavenet-D', 'fr-CA'),
('fr-CA-Standard-A', 'fr-CA'),
('fr-CA-Standard-B', 'fr-CA'),
('fr-CA-Standard-C', 'fr-CA'),
('fr-CA-Standard-D', 'fr-CA');

INSERT INTO Themes (nom) VALUES
('France'),
('International'),
('Sciences et technologies'),
('Divertissement'),
('Sports'),
('Santé'),
('Environnement'),
('Politique');

INSERT INTO Jours (nom, heure, type_voix_id, themes, Son) VALUES
('Lundi', '08:00', 1, '[]', 50),
('Mardi', '08:00', 2, '[]', 50),
('Mercredi', '08:00', 3, '[]', 50),
('Jeudi', '08:00', 4, '[]', 50),
('Vendredi', '08:00', 5, '[]', 50),
('Samedi', '08:00', 6, '[]', 50),
('Dimanche', '08:00', 7, '[]', 50);