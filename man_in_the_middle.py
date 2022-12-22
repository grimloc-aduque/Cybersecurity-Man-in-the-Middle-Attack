from connection import Connection
from threading import Thread
import tkinter as tk
from tkinter import *
from configuration import config


class Repetidor:
    conn_origen:Connection
    conn_destino:Connection
    frame:Frame
    listboxLog:Listbox
    colaMsgs:list

    def __init__(self, origen, destino, frame, listboxLog):
        self.origen = origen
        self.destino = destino
        self.frame = frame
        self.listboxLog = listboxLog
        self.colaMsgs = []

    def build_frame(self):
        Label(self.frame, text=f"Cola de Mensajes {self.origen} -> {self.destino}").pack(fill=tk.X)

        self.listboxMsgs = Listbox(self.frame)
        self.listboxMsgs.pack(fill=tk.X, pady=6)
        self.listboxMsgs.config(width=25, height=12)

        Label(self.frame, text=f"Mensaje {self.origen} -> {self.destino}").pack(fill=tk.X)

        self.mensajeEntry = Entry(self.frame)
        self.mensajeEntry.pack(fill=tk.X, pady=6)

        self.btnReenviar = Button(self.frame, text="Reenviar Mensaje", command=self.reenviar_msg)
        self.btnReenviar.pack(fill=tk.X)

    def set_connections(self, conn_origen, conn_destino):
        self.conn_origen = conn_origen
        self.conn_destino = conn_destino

    def log(self, msg):
        self.listboxLog.insert(tk.END, msg)
        
    def editando_msg(self):
        return len(self.mensajeEntry.get()) != 0

    def refrescar_listbox(self):
        self.listboxMsgs.delete(0, END)
        for i in range(len(self.colaMsgs)):
            msg = self.colaMsgs[i]
            self.listboxMsgs.insert(i, msg)

    def escuchar_origen(self):
        while True:
            msg = self.conn_origen.read_encrypted_msg()
            self.log(f"A -> MIM: {msg}")
            if self.editando_msg():
                self.colaMsgs.append(msg)
                self.refrescar_listbox()
            else:
                self.mensajeEntry.insert(0, msg)
            
    def reenviar_msg(self):
        msg = self.mensajeEntry.get()
        self.mensajeEntry.delete(0, 'end')
        self.log(f"MIM -> B: {msg}")
        self.conn_destino.write_encrypted_msg(msg)
        if len(self.colaMsgs) != 0:
            self.mensajeEntry.insert(0, self.colaMsgs.pop(0))
            self.refrescar_listbox()


class ManInTheMiddle:
    connectionA:Connection = Connection()
    connectionB:Connection = Connection()
    repetidorAB:Repetidor
    repetidorBA:Repetidor

    def __init__(self):
        self.root = Tk()
        self.build_root()
        Thread(target=self.start_attack).start()
        self.root.mainloop()

    def build_root(self):
        self.root.title(f"Man in the Middle")
        self.root.resizable = False
        rootFrame = Frame(self.root)
        rootFrame.grid(padx=15, pady=10)

        # Log de Mensajes Recibidos/Enviados

        frameLog = Frame(rootFrame, border=5)
        frameLog.grid(row=0, column=0)

        Label(frameLog, text="Log Mensajes").pack(fill=tk.X)

        scrollbarLog = Scrollbar(frameLog)
        scrollbarLog.pack(side=RIGHT, fill=BOTH)

        listboxLog = Listbox(frameLog)
        listboxLog.pack(side=LEFT, fill=BOTH)
        listboxLog.config(yscrollcommand = scrollbarLog.set, width=35, height=18)
        scrollbarLog.config(command = listboxLog.yview)

        # Mensajes A -> B
        frameAB = Frame(rootFrame, border=5)
        frameAB.grid(row=0, column=1)
        self.repetidorAB = Repetidor("A", "B", frameAB, listboxLog)
        self.repetidorAB.build_frame()

        # Mensajes B -> A
        frameBA = Frame(rootFrame, border=4)
        frameBA.grid(row=0, column=2)
        self.repetidorBA = Repetidor("B", "A", frameBA, listboxLog)
        self.repetidorBA.build_frame()


    def start_attack(self):
        PORT = config["PORT"]
        IPSERVER = config["IPSERVER"]

        self.connectionA.wait_connection_on_port(PORT)
        self.connectionA.accept_diffie_hellman()

        self.connectionB.connect_to(IPSERVER, PORT)
        self.connectionB.start_diffie_hellman()

        print(f"Key A: {self.connectionA.key}")
        print(f"Key B: {self.connectionB.key}")

        self.repetidorAB.set_connections(self.connectionA, self.connectionB)
        self.repetidorBA.set_connections(self.connectionB, self.connectionA)
        Thread(target=self.repetidorAB.escuchar_origen).start()
        Thread(target=self.repetidorBA.escuchar_origen).start()



if __name__ == '__main__':
    manInTheMiddle = ManInTheMiddle()