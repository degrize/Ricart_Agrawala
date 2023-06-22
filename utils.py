import os
import re

file = "ip_address.txt"
counter_file = "counter.txt"


def insertHostIP(ip_address):
    # Vérifier si le fichier existe
    if os.path.exists(file):
        # Le fichier existe, l'ouvrir en mode ajout
        with open(file, "a") as fichier:
            fichier.write(ip_address + "\n")

    else:
        # Le fichier n'existe pas, le créer en mode écriture
        with open(file, "w") as fichier:
            fichier.write(ip_address + "\n")


def getIPAddresses():
    # Liste pour stocker les adresses IP
    addresses_ip = []

    # Vérifier si le fichier existe
    if os.path.exists(file):
        # Lire le fichier texte
        with open(file, "r") as f:
            # Parcourir chaque ligne du fichier
            for ligne in f:
                if validate_ip(ligne):
                    # Ajouter l'adresse IP à la liste
                    address_ip = ligne.replace("\n", "")
                    addresses_ip.append(address_ip)

    # Afficher la liste des adresses IP
    return addresses_ip


def validate_ip(ip):
    # IPv4
    ipv4_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|^localhost$'

    # IPv6
    ipv6_regex = r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'

    if re.match(ipv4_regex, ip) or re.match(ipv6_regex, ip):
        return True
    else:
        return None


def getThreadNumber():
    # Check if the file exists, create it if it doesn't
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as file_count:
            file_count.write('0')
    # Open the file for reading and writing
    with open(counter_file, 'r+') as file_count:
        # Read the current value from the file
        value = int(file_count.read())
        # Increment the value
        value += 1
        # Write the new value back to the file
        file_count.seek(0)
        file_count.write(str(value))
        file_count.truncate()
    # Print the new value
    return value -1


def init_utils():
    if os.path.exists(file):
        os.remove(file)
    if os.path.exists(counter_file):
        os.remove(counter_file)
    pass
