# Imports
import dash
from dash import dcc, html, dash_table, Output, Input, State
import dash_bootstrap_components as dbc
import sqlite3
import ast
import os

from GoogleNews import GoogleNews
import google.generativeai as genai
from google.cloud import texttospeech
import json

from pydub import AudioSegment
import sounddevice as sd
import numpy as np

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Fonction pour la synthèse vocale
def text_to_speech(text, output_file):
    # Instanciez le client Text to Speech
    client = texttospeech.TextToSpeechClient()

    # AU, GB, US, IN pour l'anglais : en
    # FR, CA pour le français : fr

    # Définissez les paramètres de la voix
    voice = texttospeech.VoiceSelectionParams(
        name='fr-FR-Wavenet-C',
        language_code="fr-FR"
        # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Définissez les paramètres de l'audio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.15
    )

    # Créez la requête de synthèse vocale
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Créez la requête de synthèse vocale
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Enregistrez l'audio dans un fichier
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sqlite.db')

# Fonctions globales pour SQLite
def connect_sql():
    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def close_sql(cursor):
    cursor.close()
    return


def fetch_all(requete):
    _, cursor = connect_sql()
    cursor.execute(requete)
    result = cursor.fetchall()
    cursor.close()
    return result

# Constantes des listes
jours_list = [row[0] for row in fetch_all("SELECT nom FROM Jours")]
themes_list = [row[0] for row in fetch_all("SELECT nom FROM Themes")]
voices_list = [row[0] for row in fetch_all("SELECT name FROM TypesVoix")]


# Recuperation des infos par jours
def get_status_by_jour(nom_jour):
    _, cursor = connect_sql()
    cursor.execute("SELECT active FROM Jours WHERE nom = ?", (nom_jour,))
    active_status = cursor.fetchone()
    close_sql(cursor)

    return True if active_status else False

def get_themes_by_jour(nom_jour):
    _, cursor = connect_sql()
    cursor.execute("SELECT themes FROM Jours WHERE nom = ?", (nom_jour,))
    themes = cursor.fetchone()
    themes = ast.literal_eval(themes[0])

    result = []
    for theme in themes:
        cursor.execute("SELECT nom FROM Themes WHERE id = ?", (theme,))
        result.append(cursor.fetchone()[0])

    close_sql(cursor)

    return result

def get_voice_by_jour(nom_jour):
    _, cursor = connect_sql()
    cursor.execute("SELECT type_voix_id FROM Jours WHERE nom = ?", (nom_jour,))
    type_voix_id = cursor.fetchone()[0]

    cursor.execute("SELECT name FROM TypesVoix WHERE id = ?", (type_voix_id,))
    result = cursor.fetchone()[0]

    close_sql(cursor)

    return result

def get_sound_volume_by_jour(nom_jour):
    _, cursor = connect_sql()
    cursor.execute("SELECT son FROM Jours WHERE nom = ?", (nom_jour,))
    son = cursor.fetchone()[0]

    close_sql(cursor)

    return son

def get_hour_by_jour(nom_jour):
    _, cursor = connect_sql()
    cursor.execute("SELECT heure FROM Jours WHERE nom = ?", (nom_jour,))
    heure = cursor.fetchone()[0]

    heures, minutes = map(int, heure.split(':'))

    close_sql(cursor)

    return heures, minutes



# Layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                html.H1('Configuration du réveil', className='text-center my-4'),
                width=12
            )
        ),
        dcc.Tabs(
            id='tabs',
            value=jours_list[0],
            children=[
                # Label par default : le jour, il est ensuite modifie dans le callback avec un icone
                dcc.Tab(label=jour, value=jour, id=f'tab-{jour.lower()}', className='tab-inactive', children=[
                    dcc.Checklist(
                        options=[{'label': 'Actif', 'value': True}],
                        value=[get_status_by_jour(jour)],
                        id=f'checkbox-{jour.lower()}',
                        className='my-2'
                    ),
                    html.Label('Heure :'),
                    dcc.Input(
                        id=f'input-heure-{jour.lower()}',
                        className='my-2 input-hours',
                        type="number",
                        placeholder="Heure",
                        min=0, max=23, step=1,
                        value=get_hour_by_jour(jour)[0],
                        style={'marginLeft':'10px'}
                    ),
                    dcc.Input(
                        id=f'input-minute-{jour.lower()}',
                        className='my-2 input-minutes',
                        type="number",
                        placeholder="Minutes",
                        min=0, max=59, step=1,
                        value=get_hour_by_jour(jour)[1]
                    ),
                    html.Br(),
                    html.Label('Thèmes :'),
                    dcc.Dropdown(
                        id=f'dropdown-theme-{jour.lower()}',
                        options=[{'label': theme, 'value': theme} for theme in themes_list],
                        value=get_themes_by_jour(jour),
                        multi=True,
                        className='my-2'
                    ),
                    html.Label('Voix :'),
                    dcc.Dropdown(
                        id=f'dropdown-voice-{jour.lower()}',
                        options=[{'label': theme, 'value': theme} for theme in voices_list],
                        value=get_voice_by_jour(jour),
                        className='my-2'
                    ),
                    html.Label("Volume:"),
                    dcc.Slider(
	                        id=f"volume-slider-{jour.lower()}",
                        min=0,
                        max=100,
                        step=5,
                        value=get_sound_volume_by_jour(jour),
                        marks={0: "0%", 50: "50%", 100: "100%"},
                    ),
                ]) for jour in jours_list
            ]
        ),
        html.Button("Run a Morning Brief", id="play-button", n_clicks=0, style={"marginTop": "20px"}),
        html.Div('Coucou', id="output-div"),
        html.H2('Tableau d\'Historique', style={"marginTop": "50px"}),
        dash_table.DataTable(
            id='historique-table',
            columns=[
                {'name': 'Date', 'id': 'Date'},
                {'name': 'Jour', 'id': 'Jour'},
                {'name': 'Thèmes', 'id': 'Themes'},
                {'name': 'Description', 'id': 'Description'}
            ],
            # data=data.to_dict('records'),
        ),
    ],
    className='p-4'
)

# Callback pour run un Morning Brief
@app.callback(
    Output("output-div", "children"),
    Input("play-button", "n_clicks"),
    prevent_initial_call=True
)
def update_output(n_clicks):

    #################### NEWS PART ####################
    googlenews = GoogleNews()

    googlenews.set_lang('fr')
    googlenews.set_period('1d')
    googlenews.set_encode('utf-8')
    # googlenews.set_time_range('08/11/2024','08/11/2024')

    # Theme du brief
    googlenews.get_news('Sciences et Technologies')

    result = googlenews.results()
    print("Total news : ",len(result))

    # Liste de tous les titres
    titles = [x['title'] for x in result]
    print("Titles:", titles)

    # Écriture des données météo dans un fichier texte
    with open("theme_brief_w_AI.json", "w") as file:
        file.write(json.dumps(result))

    googlenews.clear()

    #################### AI PART ####################
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    my_prompt = """
    Tu es présentateur des actualités.
    Fais une synthèse des sujets les plus récurrents dans les actualités du jour.
    Evoque au maximum 5 sujets différents.
    Réalise qu'un seul paragraphe mais avec une introduction et un mot d'au revoir.
    """ + "\n".join(titles)

    ### Count Tokens
    # Call `count_tokens` to get the input token count (`total_tokens`).
    print("count_tokens: ", model.count_tokens(my_prompt))
    response = model.generate_content(my_prompt)
    print(response.usage_metadata)

    ### Génération de texte
    response = model.generate_content(my_prompt)
    print(response.text)

    ### Text to Speech
    output_file = "SportBrief.mp3"
    text_to_speech(response.text, output_file)

    #################### PLAY PART ####################

    # Charger le fichier MP3
    filename = "SportBrief.mp3"
    audio = AudioSegment.from_mp3(filename)

    # Convertir les données audio en tableau NumPy
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)

    # Convertir les données audio en format stéréo si nécessaire
    if audio.channels == 2:
        audio_data = audio_data.reshape((-1, 2))

    # Normaliser les données audio
    audio_data_normalized = audio_data / np.max(np.abs(audio_data))

    # Sélectionner la sortie audio
    print(sd.query_devices())
    # sd.default.device = 1  # Remplacez par l'index de votre périphérique audio
    # print(sd.query_devices())

    # Jouer les données audio
    sd.play(audio_data_normalized, audio.frame_rate)
    sd.wait()  # Attend la fin de la lecture

    return f"Le bouton a été cliqué {n_clicks} fois."

for jour in jours_list:
    # Changement de logo par jour & Update BDD
    @app.callback(
        Output(f'tab-{jour.lower()}', 'className'),
        State(f'tab-{jour.lower()}', 'value'),
        Input(f'checkbox-{jour.lower()}', 'value')
    )
    def update_day_state(jour_label, selected_values):
        conn, cursor = connect_sql()

        boolean = 1 if True in selected_values else 0
        cursor.execute("UPDATE Jours SET active = ? WHERE nom = ?", (boolean, jour_label))
        conn.commit()
        close_sql(cursor)

        className = "tab-active" if True in selected_values else "tab-inactive"

        return className
    
    # Update BDD themes
    @app.callback(
        Output(f'dropdown-theme-{jour.lower()}', 'value'),
        State(f'tab-{jour.lower()}', 'value'),
        Input(f'dropdown-theme-{jour.lower()}', 'value')
    )
    def update_themes(jour_label, value):
        conn, cursor = connect_sql()

        result = []
        for theme in value:
            cursor.execute("SELECT id FROM Themes WHERE nom = ?", (theme,))
            result.append(cursor.fetchone()[0])
        
        cursor.execute("UPDATE Jours SET themes = ? WHERE nom = ?", (str(result), jour_label))
        conn.commit()
        close_sql(cursor)
        return value	
    
    # Update BDD voix
    @app.callback(
        Output(f'dropdown-voice-{jour.lower()}', 'value'),
        State(f'tab-{jour.lower()}', 'value'),
        Input(f'dropdown-voice-{jour.lower()}', 'value')
    )
    def update_voices(jour_label, value):
        conn, cursor = connect_sql()

        # On recupere l'id du type de voix
        cursor.execute("SELECT id FROM TypesVoix WHERE name = ?", (value,))
        # On met a jour l'id dans la table Jours
        cursor.execute("UPDATE Jours SET type_voix_id = ? WHERE nom = ?", (cursor.fetchone()[0], jour_label))
        conn.commit()

        close_sql(cursor)
        return value
    
    # Update BDD volume
    @app.callback(
        Output(f'volume-slider-{jour.lower()}', 'value'),
        State(f'tab-{jour.lower()}', 'value'),
        Input(f'volume-slider-{jour.lower()}', 'value')
    )
    def update_volume(jour_label, value):
        conn, cursor = connect_sql()

        # On met a jour le volume dans la table Jours
        cursor.execute("UPDATE Jours SET son = ? WHERE nom = ?", (value, jour_label))
        conn.commit()

        close_sql(cursor)
        return value
    
    # Update BDD time
    @app.callback(	
        Output(f'input-heure-{jour.lower()}', 'value'),
        State(f'tab-{jour.lower()}', 'value'),
        Input(f'input-heure-{jour.lower()}', 'value'),
        Input(f'input-minute-{jour.lower()}', 'value')
    )
    def update_time(jour_label, heure, minute):
        conn, cursor = connect_sql()

        time = str(heure) + ":" + str(minute).zfill(2)

        # On met a jour l'heure dans la table Jours
        cursor.execute("UPDATE Jours SET heure = ? WHERE nom = ?", (time, jour_label))
        conn.commit()

        close_sql(cursor)
        return heure
    

# Main
if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
