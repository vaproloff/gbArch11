import tkinter as tk
import requests

from .abstract_app import AbstractApp
from .const import (
    API_ROOT_URL,
    CLIENTS_GET_URL,
    CLIENTS_ADD_URL,
    CLIENTS_UPDATE_URL,
    CLIENTS_DELETE_URL,
)


class ClientsApp(AbstractApp):
    def __init__(self, root: tk.Tk) -> None:
        self.title = 'ClinicClient'
        self.columns = ('id', 'surname', 'first_name', 'patronymic', 'birthday', 'document')
        self.titles = ('ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Документ')
        super().__init__(root)

    def _init_edit_gui(self):
        self.id_label = tk.Label(self.root, text="ID:")
        self.id_label.grid(row=3, column=0, sticky=tk.W)
        self.id_entry = tk.Entry(self.root, state='readonly')
        self.id_entry.grid(row=4, column=0)

        self.surname_label = tk.Label(self.root, text="Фамилия:")
        self.surname_label.grid(row=3, column=1, sticky=tk.W)
        self.surname_entry = tk.Entry(self.root)
        self.surname_entry.grid(row=4, column=1)

        self.first_name_label = tk.Label(self.root, text="Имя:")
        self.first_name_label.grid(row=3, column=2, sticky=tk.W)
        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.grid(row=4, column=2)

        self.patronymic_label = tk.Label(self.root, text="Отчество:")
        self.patronymic_label.grid(row=5, column=0, sticky=tk.W)
        self.patronymic_entry = tk.Entry(self.root)
        self.patronymic_entry.grid(row=6, column=0)

        self.birthday_label = tk.Label(self.root, text="Дата рождения:")
        self.birthday_label.grid(row=5, column=1, sticky=tk.W)
        self.birthday_entry = tk.Entry(self.root)
        self.birthday_entry.grid(row=6, column=1)

        self.document_label = tk.Label(self.root, text="Документ:")
        self.document_label.grid(row=5, column=2, sticky=tk.W)
        self.document_entry = tk.Entry(self.root)
        self.document_entry.grid(row=6, column=2)

    def _check_focus(self, _):
        row = self.tree.selection()
        entries = [
            self.id_entry,
            self.surname_entry,
            self.first_name_entry,
            self.patronymic_entry,
            self.birthday_entry,
            self.document_entry,
        ]
        values = self.tree.item(row[0]).get('values') if len(row) else ["" for _ in entries]

        self.id_entry.config(state='normal')
        self._insert_entries(entries, values)
        self.id_entry.config(state='disabled')

    def _update_data(self) -> None:
        self.tree.destroy()
        self._init_table_gui()
        for client in self._fetch(f'{API_ROOT_URL}{CLIENTS_GET_URL}'):
            self.tree.insert("", tk.END, values=([client[key] for key in self.columns]))
        self._check_focus(None)

    def _add(self):
        surname = self.surname_entry.get()
        first_name = self.first_name_entry.get()
        patronymic = self.patronymic_entry.get()
        birthday = self.birthday_entry.get()
        document = self.document_entry.get()
        if None not in (first_name, surname, patronymic, birthday, document):
            data_dict = {
                'surname': surname,
                'first_name': first_name,
                'patronymic': patronymic,
                'birthday': birthday,
                'document': document,
            }
            response = requests.post(url=f'{API_ROOT_URL}{CLIENTS_ADD_URL}', json=data_dict)
            response.raise_for_status()
            self._update_data()

    def _update(self):
        client_id = self.id_entry.get()
        surname = self.surname_entry.get()
        first_name = self.first_name_entry.get()
        patronymic = self.patronymic_entry.get()
        birthday = self.birthday_entry.get()
        document = self.document_entry.get()
        if None not in (first_name, surname, patronymic, birthday, document):
            data_dict = {
                'surname': surname,
                'first_name': first_name,
                'patronymic': patronymic,
                'birthday': birthday,
                'document': document,
            }
            response = requests.put(url=f'{API_ROOT_URL}{CLIENTS_UPDATE_URL}/{client_id}', json=data_dict)
            response.raise_for_status()
            self._update_data()

    def _delete(self):
        client_id = self.id_entry.get()
        if client_id:
            response = requests.delete(url=f'{API_ROOT_URL}{CLIENTS_DELETE_URL}/{client_id}')
            response.raise_for_status()
            self._update_data()
