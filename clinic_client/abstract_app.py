import abc
import tkinter.ttk as ttk
import tkinter as tk
from typing import Tuple

import requests


class AbstractApp(abc.ABC):
    title: str
    columns: Tuple[str, ...]
    titles: Tuple[str, ...]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self._init_main_gui()
        self._init_table_gui()
        self._init_control_gui()
        self._init_edit_gui()

    def _init_main_gui(self):
        self.root.title(self.title)
        self.root.config(padx=20, pady=20)

    def _init_table_gui(self):
        self.get_button = tk.Button(self.root, width=50, height=1, text='Получить данные', command=self._update_data)
        self.get_button.grid(column=0, row=0, columnspan=3)
        self.root.grid_rowconfigure(0, pad=20)

        self.tree = ttk.Treeview(self.root, show='headings', columns=self.columns)
        for item in zip(self.columns, self.titles):
            self.tree.heading(item[0], text=item[1])

        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=3, sticky="ns")

        self.tree.grid(column=0, row=1, columnspan=3)
        self.tree.bind('<ButtonRelease-1>', self._check_focus)

    def _init_control_gui(self):
        self.add_button = tk.Button(self.root, width=10, height=1, text='Добавить', command=self._add)
        self.add_button.grid(column=0, row=2)

        self.update_button = tk.Button(self.root, width=10, height=1, text='Обновить', command=self._update)
        self.update_button.grid(column=1, row=2)

        self.delete_button = tk.Button(self.root, width=10, height=1, text='Удалить', command=self._delete)
        self.delete_button.grid(column=2, row=2)

        self.root.grid_rowconfigure(2, pad=20)

    @abc.abstractmethod
    def _check_focus(self, event):
        ...

    @abc.abstractmethod
    def _init_edit_gui(self):
        ...

    @abc.abstractmethod
    def _update_data(self):
        ...

    @abc.abstractmethod
    def _add(self):
        ...

    @abc.abstractmethod
    def _update(self):
        ...

    @abc.abstractmethod
    def _delete(self):
        ...

    @staticmethod
    def _fetch(url: str) -> list[dict]:
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _clear_entries(entries: list[tk.Entry]):
        for entry in entries:
            entry.delete(0, tk.END)

    def _insert_entries(self, entries: list[tk.Entry], values: list[str]):
        if len(entries) != len(values):
            raise RuntimeError('Entries and Values list lengths not equal')
        self._clear_entries(entries)
        for i in range(len(entries)):
            entries[i].insert(0, values[i])
