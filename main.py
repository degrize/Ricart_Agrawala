from threading import Thread
from time import sleep

import utils
from Ricart_Agrawala import RicartAgrawala

utils.init_utils()
ip_address = ""
num_process = 0
while not utils.validate_ip(ip_address):
    if len(ip_address) > 0:
        print("ERROR invalid IP address")
    ip_address = str(input('Enter this site IP Address: \n>> '))

utils.insertHostIP(ip_address)
my_thread_number = utils.getThreadNumber()

ricart_agrawala = RicartAgrawala()

recevoir_requete = Thread(target=ricart_agrawala.recevoir_req, args=(my_thread_number,))
recevoir_requete.start()

print("veuillez patienter ne quittez pas...")

# on patiente que toutes les machines sont connectées
sleep(15)

ip_addresses = utils.getIPAddresses()
ricart_agrawala.ip_addresses_sites = ip_addresses
ricart_agrawala.num_site = my_thread_number
ricart_agrawala.nb_total_site = len(ip_addresses)

for i in range(len(ip_addresses)):
    ricart_agrawala.list_sites.append(i)

ricart_agrawala.launch()