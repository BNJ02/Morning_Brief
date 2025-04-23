import subprocess

def connect_bluetooth_device(mac_address):
    # Lancer bluetoothctl
    process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Envoyer les commandes nécessaires
    commands = [
        'power on\n',               # Activer le Bluetooth (si ce n'est pas déjà fait)
        f'connect {mac_address}\n',  # Se connecter à l'appareil avec l'adresse MAC donnée
        'exit\n'                    # Quitter bluetoothctl
    ]
    
    for cmd in commands:
        process.stdin.write(cmd)
        process.stdin.flush()
    
    # Lire la sortie pour vérifier le succès
    process.communicate()

    # Afficher le résultat
    if process.returncode == 0:
        print(f'Connexion réussie avec {mac_address}')
    else:
        print(f'Échec de la connexion avec {mac_address}')

def disconnect_bluetooth_device(mac_address):
    # Lancer bluetoothctl
    process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Envoyer les commandes nécessaires
    commands = [
        'power on\n',                   # Activer le Bluetooth (si ce n'est pas déjà fait)
        f'disconnect {mac_address}\n',  # Se connecter à l'appareil avec l'adresse MAC donnée
        'exit\n'                        # Quitter bluetoothctl
    ]
    
    for cmd in commands:
        process.stdin.write(cmd)
        process.stdin.flush()
    
    # Lire la sortie pour vérifier le succès
    process.communicate()

    # Afficher le résultat
    if process.returncode == 0:
        print(f'Déconnexion réussie avec {mac_address}')
    else:
        print(f'Échec de la déconnexion avec {mac_address}')

# Exemple d'utilisation
mac_address = 'E4:BD:95:C7:92:A2'

# Se connecter à l'appareil
connect_bluetooth_device(mac_address)

# Attendre quelques secondes
input('Appuyez sur Entrée pour déconnecter l\'appareil')

# Se déconnecter de l'appareil
disconnect_bluetooth_device(mac_address)
