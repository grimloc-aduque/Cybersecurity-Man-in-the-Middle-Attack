
import tkinter as tk
from tkinter import *
from connection import Connection
from threading import Thread
from configuration import config

class ChatGUI:
    
    def __init__(self):
        self.connection = Connection()
        self.root = Tk()
        self.build_root()
        self.root.mainloop()

    def build_root(self):
        self.root.title(f"Chat Asincrono")
        self.root.resizable = False

        # Margen de la ventana
        rootFrame = Frame(self.root, border=3, relief=tk.GROOVE)
        rootFrame.grid()

        # Mensajes

        msgFrame = Frame(rootFrame, border=1, relief=tk.GROOVE)
        msgFrame.grid(row=0, rowspan=20, column=0, columnspan=2, padx=15, pady=10)

        msgLabel = Label(msgFrame, text="Chat")
        msgLabel.pack(side=TOP, fill=BOTH)
        self.msgLabel = msgLabel

        msgScrollbar = Scrollbar(msgFrame)
        msgScrollbar.pack(side=RIGHT, fill=BOTH)

        msgListbox = Listbox(msgFrame)
        msgListbox.pack(side=LEFT, fill=BOTH)
        msgListbox.config(yscrollcommand=msgScrollbar.set, width=40, height=20)
        self.msgListbox = msgListbox

        inputMsg = Entry(rootFrame)
        inputMsg.grid(row=20, column=0, sticky=E + W, padx=15, pady=10)
        self.inputMsg = inputMsg

        btnSend = Button(rootFrame, text="Send", command=self.on_click_send_msg)
        btnSend.grid(row=20, column=1, sticky=E + W, padx=15, pady=10)
        self.btnSend = btnSend
        self.disable_btn(self.btnSend)

        # Esperar Conexion

        btnWaitConnection = Button(rootFrame, text='Wait Connection', command=self.on_click_wait_connection)
        btnWaitConnection.grid(row=0, column=2, columnspan=2, sticky=E + W, padx=15)
        self.btnWaitConnection = btnWaitConnection

        # Conectarse

        # IP
        varDomain = StringVar()
        varDomain.set("Domain:")
        labelDomain = Label(rootFrame, textvariable=varDomain)
        labelDomain.grid(row=2, column=2, sticky=W, padx=15)

        inputDomain = Entry(rootFrame, width=18)
        inputDomain.grid(row=2, column=3, sticky=E, padx=15)
        self.inputDomain = inputDomain

        btnConnect = Button(rootFrame, text='Connect', command=self.on_click_connect)
        btnConnect.grid(row=3, column=2, columnspan=2, sticky=E + W, padx=15)
        self.btnConnect = btnConnect

        # Close Connection

        btnDisconnect = Button(rootFrame, text='Disconnect', command=self.on_click_disconnect)
        btnDisconnect.grid(row=4, column=2, columnspan=2, sticky=E + W, padx=15)
        self.btnDisconnect = btnDisconnect
        self.disable_btn(self.btnDisconnect)

        self.root.protocol("WM_DELETE_WINDOW", self.on_click_exit)

    def on_click_wait_connection(self):
        self.set_waiting_state()
        PORT = config["PORT"]
        wait_connection_thread = Thread(target=self.accept_connection, args=[PORT])
        wait_connection_thread.start()

    def accept_connection(self, port):
        self.connection.wait_connection_on_port(port)
        self.connection.accept_diffie_hellman()
        self.set_connected_state()
        self.listen_incoming_msgs()

    def on_click_connect(self):
        self.set_connected_state()
        domain = self.inputDomain.get()
        IP = Connection.resolve_domain(domain)
        PORT = config["PORT"]
        self.connection.connect_to(IP, PORT)
        self.connection.start_diffie_hellman()
        listening_thread = Thread(target=self.listen_incoming_msgs)
        listening_thread.start()

    def listen_incoming_msgs(self):
        while True:
            msg = self.connection.read_encrypted_msg()
            self.msgListbox.insert(tk.END, msg)
            if msg == 'DISCONNECT':
                self.connection.write_encrypted_msg('DO DISCONNECT')
                break
            elif msg == 'DO DISCONNECT':
                break
        self.connection.close_socket()
        self.set_initial_state()
            
    def on_click_send_msg(self):
        msg = self.inputMsg.get()
        self.connection.write_encrypted_msg(msg)
        self.msgListbox.insert(tk.END, msg)

    def on_click_disconnect(self):
        self.connection.write_encrypted_msg('DISCONNECT')

    def on_click_exit(self):
        self.root.destroy()

    # Button states
    
    def set_initial_state(self):
        self.enable_btn(self.btnWaitConnection)
        self.enable_btn(self.btnConnect)
        self.disable_btn(self.btnDisconnect)
        self.disable_btn(self.btnSend)

    def set_waiting_state(self):
        self.disable_btn(self.btnWaitConnection)
        self.disable_btn(self.btnConnect)
        self.disable_btn(self.btnDisconnect)
        self.disable_btn(self.btnSend)

    def set_connected_state(self):
        self.disable_btn(self.btnWaitConnection)
        self.disable_btn(self.btnConnect)
        self.enable_btn(self.btnDisconnect)
        self.enable_btn(self.btnSend)

    def disable_btn(self, btn:Button):
        btn['state'] = 'disabled'

    def enable_btn(self, btn:Button):
        btn['state'] = 'active'



if __name__ == '__main__':
    gui = ChatGUI()
    
