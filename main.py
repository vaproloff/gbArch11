import tkinter as tk
from clinic_client.clients_app import ClientsApp

if __name__ == '__main__':
    clients_app = ClientsApp(tk.Tk())
    clients_app.root.mainloop()
