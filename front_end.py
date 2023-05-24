from tkinter import *
from PIL import ImageTk, Image
from backend import *
from tkinter.font import Font
from tkinter import messagebox
import customtkinter
import re

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("CustomTkinter simple_example.py")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=35, padx=10, fill="both", expand=True)
titulo = tk.Label(frame_1, text="Bienvenido a mi App", bg="black", fg="white", width=10, height=10, font=("Arial", 20))
titulo.pack(fill='both', expand=False)
frame_1.pack_propagate(False)  
titulo = tk.Label(frame_1, text="Podrás realizar balance de ecuaciones químicas y realizar cálculos termodinámicos", bg="black", fg="white", width=5, height=5, font=("Arial", 14))
titulo.pack(fill='both', expand=False, pady=15)
frame_1.pack_propagate(False)  
frame_2 = Frame(app)
frame_2.pack()

img = ImageTk.PhotoImage(Image.open("technology-physics-and-chemistry-chemistry-hd-wallpaper-preview.jpg"))
imagen = Label(frame_2, image=img)
imagen.grid(row=3, column=0, columnspan=1)
texto = Label(frame_2, text="al lado")
imagen.grid(row=3, column=2, columnspan=4)
#función que carga todas las especies y luego será llamada en el frame
especies = especies()



def frame_especies():
    global especies
    # Eliminar todos los widgets del marco principal
    for widget in app.winfo_children():
        widget.destroy()

    # Crear un nuevo marco
    frame_reac = tk.Frame(app)
    frame_reac.pack()

    # Agregar elementos al nuevo marco
    
    frame_sustancias = tk.Frame(app)
    frame_sustancias.pack(pady=10, padx=150)

    texto_reaccion = StringVar()
    texto_reaccion.set("Franco Alberti")
    etiqueta = tk.Label(frame_reac, textvariable=texto_reaccion, width=140, height=10, bg="#B2FFFF", font=("Arial", 10))
    etiqueta.pack()

    fila = 0
    columna = 0
    for especie in especies:
        btn_especie = Button(frame_sustancias, text=especie, bg="black", fg="white", font=("Arial", 15), command=lambda especie_text=especie: frame_sustancia(especie_text))
        btn_especie.grid(row=fila, column=columna, pady=25)
        if columna == 5:
            columna = 0
            fila +=1
        else:
            columna+=1
#presentar frame con sustancias según elementos
def frame_sustancia(specie):
    global frame_r
    for widget in app.winfo_children():
        widget.destroy()
    frame_sustancias = tk.Frame(app)
    frame_sustancias.grid(column=0)

    frame_r = tk.Frame(app)
    frame_r.grid(column=1, row=0)
    #ubicando las sustancias con mismo algoritmo de especies
    fila = 0
    columna = 0
    lista_sust = sustancias_especies(specie)
    for sustancia in lista_sust:
        btn_especie = Button(frame_sustancias, text=sustancia, bg="black", fg="white", font=("Arial", 20), command=lambda sustancia=sustancia: label_reac(sustancia))
        btn_especie.grid(row=fila, column=columna, pady=25)
        if columna == 2:
            columna = 0
            fila +=1
        else:
            columna+=1
    #volver a especies
    Button(frame_sustancias, text="Volver a especies", bg="red", fg="white", font=("Arial", 20), command=frame_especies).grid()
    Button(frame_sustancias, text="→", bg="red", fg="white", font=("Arial", 20), command= lambda: label_reac("→")).grid(column=3, row=0)
    Button(frame_sustancias, text="+", bg="red", fg="white", font=("Arial", 20), command= lambda: label_reac("+")).grid(column=4, row=0)
    Button(frame_sustancias, text="borrar", bg="red", fg="white", font=("Arial", 20), command= lambda: label_reac("borrar")).grid(column=5, row=0)
    Button(frame_sustancias, text="Ingresar Reacción", bg="red", fg="white", font=("Arial", 20), command= balancear).grid(column=6, row=0)
    
sustancia_str = StringVar()
def balancear():
    reaccion = sustancia_str.get()
    lista_reaccion = reaccion.split('→')
    lista_reaccion_total = []
    lista_reactante = []
    for i in lista_reaccion:
        lista_reaccion_total.append(i.split('+'))
    for i in lista_reaccion_total:
        for j in range(len(i)):
            i[j] = Sustancia(i[j])
    for i in lista_reaccion_total:
        lista_reactante.append(Reactante(*i))
    reaccion = Reacciones(*lista_reactante)
    reaccion_balanceada = (reaccion.balancear())
    Label(frame_r, text=reaccion_balanceada, bg="green", fg="white", font=("Arial", 15)).grid(column=2, row=10)

def label_reac(sustancia):
    global frame_r
    global etiqueta_react
    global sustancia_str
    if sustancia == "borrar":
        sustancia_str.set("")
    else:
        sustancia_str.set(sustancia_str.get() + sustancia)


    for widget in frame_r.winfo_children():
        widget.destroy()
    
    etiqueta_react = Label(frame_r, text=sustancia_str.get(), bg="red", fg="white", font=("Arial", 15)).grid(column=2)



btn_action = Button(app, text="Iniciar", bg="black", fg="white", font=("Arial", 20), command=frame_especies)
btn_action.pack(padx=1, pady=25)

app.mainloop()

