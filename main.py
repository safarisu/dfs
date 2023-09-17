import random
import tkinter as tk
from collections import defaultdict
from tkinter import font as tkfont
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
#from tkinter.ttk import Label, Button, Frame


class GraphIsCyclic(Exception):
    pass

class NoPath(Exception):
    pass

class WrongInput(Exception):
    pass


def parse_input(text:str):
    try:
        lines = text.split("\n")
        vertices, edges = lines[0].split(" ")
        vertices_list = []

        if lines[-1] == "":
            lines = lines[:-1]

        g = Graph(vertices)
        if int(edges) != len(lines[1:]):
            raise WrongInput

        for line in lines[1:]:
            vertex1, vertex2 = line.split(" ")
            g.addEdge(vertex1, vertex2)
            vertices_list.append(vertex1)
            vertices_list.append(vertex2)

        if len(set(vertices_list)) != int(vertices):
            raise WrongInput

        return g

    except:
        raise WrongInput


class Graph:

    def __init__(self, vertices):

        self.graph = defaultdict(list)
        self.output = ""
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DFSUtil(self, v, visited, rec_stack):

        visited.add(v)
        rec_stack.add(v)
        self.output += v + " "

        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited, rec_stack)
            elif neighbour in rec_stack:
                raise GraphIsCyclic

        return self.output

    def DFS(self, v):

        visited = set()
        rec_stack = set()

        self.DFSUtil(v, visited, rec_stack)


class DFSApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Depth First Search")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, TextInputPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def show_choice(self, text, parent, controller):
        try:
            g = parse_input(text)
        except WrongInput:
            messagebox.showerror("Błąd!", "Nieprawidłowe dane wejściowe.")
            controller.show_frame("StartPage")
            return
        except NoPath:
            return

        frame = ChoiceFrame(parent, controller, g)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_output(self, g:Graph, key, parent, controller):
        try:
            for k in list(g.graph.keys()):
                g.DFS(k)
        except GraphIsCyclic:
            messagebox.showerror("Błąd!", "Graf zawiera cykl.")
            controller.show_frame("StartPage")
            return

        #output
        g.output = ""
        g.DFS(key)

        frame = OutputFrame(parent, controller, g)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def read_from_file(self, parent, controller):
        try:
            text = open_file()
            self.show_choice(text, parent, controller)
        except NoPath:
            pass


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Depth First Search", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Wczytaj tekst",
                            command=lambda: controller.show_frame("TextInputPage"))
        button2 = tk.Button(self, text="Wczytaj z pliku",
                            command=lambda: controller.read_from_file(parent, controller))
        button1.pack(padx=5, pady=5)
        button2.pack(padx=5, pady=5)

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        raise NoPath
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()

    return text


class TextInputPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Wprowadź tekst: ", font=tkfont.Font(family='Helvetica', size=12))
        label.pack(side="top", pady=5)
        text_edit = tk.Text(self)
        text_edit.pack(fill="both", expand=1)
        button = tk.Button(self, text="Zatwierdź",
                           command=lambda: controller.show_choice(text_edit.get("1.0", tk.END), parent, controller))
        button.pack(side="bottom", pady=5)


class ChoiceFrame(tk.Frame):

    def __init__(self, parent, controller, g:Graph):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Wybierz wierzchołek", font=tkfont.Font(family='Helvetica', size=12))
        label.pack(side="top", fill="x", pady=10)

        buttons = []

        for key in g.graph.keys():
            buttons.append(tk.Button(self, text=key, command=lambda key=key: controller.show_output(g, key, parent, controller)))

        for button in buttons:
            button.pack(fill="x", pady=5, side="top")


class OutputFrame(tk.Frame):

    def __init__(self, parent, controller, g:Graph):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Przechodzenie grafu:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        output = tk.Label(self, text=g.output, font=controller.title_font)
        output.pack(fill="x", pady=10)
        button = tk.Button(self, text="Wczytaj inny graf",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=5)


if __name__ == "__main__":
    app = DFSApp()
    app.mainloop()
