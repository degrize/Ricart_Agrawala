from socket_and_comm import *
from time import sleep
from threading import Thread

INITIAL_PORT = 10000
DATA_BIT = 1024
UTF8 = "utf8"


class RicartAgrawala:
    def __init__(self):
        # les configs de base
        self.num_site = None
        self.list_sites = []
        self.ip_addresses_sites = None
        self.nb_total_site = 0
        self.mon_nbre_seq = 0
        self.sup_nbre_seq = 0
        self.reponse_diff = []
        self.n_accord = 0
        self.candidat = False
        self.requete = "0"
        self.accord = "1"

    def obtention_accord(self, conn):
        msg = self.recevoir(conn)
        if len(msg) > 1:
            type_msg = msg[0]
            hote_source = msg[1]
            print("accord obtenu ",msg, " de ", hote_source)
            if type_msg == self.accord:
                self.n_accord += 1

    def echange_communication(self, moi_meme, mon_socket):
        message = self.recevoir(mon_socket)
        if message[0] == self.requete:
            heure = int(message[1])
            num = int(message[2])
            print("requete recu de ", num, " est ", message)
            self.sup_nbre_seq = max(self.sup_nbre_seq, heure) + 1
            prioritaire = self.candidat and (self.mon_nbre_seq < heure) or (
                        (self.mon_nbre_seq == heure) and (moi_meme < num))
            if prioritaire:
                self.reponse_diff.append(mon_socket)
                print("accord de ", num, "différé, puisque moi_meme ", moi_meme, " je suis prioritaire")
                print("heure de la de demande ", heure, " mon_nbre_seq", self.mon_nbre_seq)
            else:
                # je ne suis pas prioritaire j'envoie donc mon accord
                mon_accord = self.accord + str(moi_meme) + self.accord

                msg = mon_accord.encode(UTF8)  # on encode le msg
                mon_socket.sendall(msg)  # on envoi le msg

                print("accord transmis par ", moi_meme, " à ", num, " est ", mon_accord)
                if not self.candidat:
                    print("moi_meme processus ", moi_meme, " je ne suis pas encore candidat")
                else:
                    print("heure de la de demande ", heure, " mon_nbre_seq {self.mon_nbre_seq}")

    # Requête Reception d'une demande d'entrer en section critique
    def recevoir_req(self, moi_meme):
        port = INITIAL_PORT + moi_meme
        socketserver = SocketClientServer("", port)
        socketserver.start_server()
        unsocket = socketserver.socket
        while True:
            unsocket.listen()  # on écoute un socket
            canal, address = unsocket.accept()
            self.traiter(canal, self.echange_communication(moi_meme, canal, ))

    # Requête d'une demande d'entrer en section critique
    def section_crit_demande(self, moi_meme, reseau):
        self.candidat = True
        self.mon_nbre_seq = self.sup_nbre_seq + 1
        mon_message = self.requete + str(self.mon_nbre_seq) + str(moi_meme)
        print("Moi Processus ", moi_meme, " demande à entrer en section critique")

        # On diffuse le msg
        for site in reseau:
            msg = mon_message.encode(UTF8)  # on encode le msg
            site.sendall(msg)  # on envoi le msg

        for canal in reseau:
            self.traiter(canal, self.obtention_accord(canal))

        while self.n_accord < (self.nb_total_site - 1):
            print(" ", self.n_accord, end=".")
        print("Moi processus ", moi_meme, " suis en section critique")
        sleep(10)  # temps mort
        print("Moi processus ", moi_meme, " suis sorti de la section critique")

        self.candidat = False
        mon_accord = str(self.accord) + str(moi_meme) + str(self.accord)
        # étant sorti de la section critique, envoie son accord à tous ceux pour qui il l'avait différé
        for site in self.reponse_diff:
            msg = mon_accord.encode(UTF8)  # on encode le msg
            site.sendall(msg)  # on envoi le msg

    def recevoir(self, conn):
        message = conn.recv(DATA_BIT)
        message = message.decode(UTF8)
        return message

    def traiter(self, conn, task=recevoir):
        t = Thread(target=task, args=(conn,))
        t.start()

    def launch(self):

        # Câblage du réseau 
        network = build_network(self.num_site, self.list_sites, self.ip_addresses_sites, INITIAL_PORT)
        demander_section = Thread(target=self.section_crit_demande, args=(self.num_site, network,))
        demander_section.start()
