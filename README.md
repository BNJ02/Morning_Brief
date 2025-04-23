# Morning Brief with AI on RaspberryPi

## Comment ajouter ses clefs API en tant que variables d'environnement

Exécuter :

`sudo nano /etc/environment`

Éditer avec votre clef API :

`MISTRAL_API_KEY="votre_clef_api"`

Enregistrer le fichier et fermer l'éditeur de texte

Redémarrer la RaspberryPi pour que les modifications prennent effet

Vous pouvez alors faire appel à cette variables dans votre script Python de cette manière :

```
import os

api_key = os.environ["MISTRAL_API_KEY"]
```
