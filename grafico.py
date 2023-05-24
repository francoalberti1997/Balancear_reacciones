from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog

root = Tk()
root.title("La Calculadora")
vertical = Scale(root, from_=0, to=300)
vertical.pack()
root.geometry("400x400")
MODES = [("Anchoas","Anchoas"), ("Atún","Atún"),("Ajo","Ajo"), ("Jamón","Jamón"), ("apio","apio")]
pizza = StringVar()
pizza.set("Ajo")
etiqueta = Label(root, text=pizza.get())
etiqueta.pack()

for sabor, valor in MODES:
    Radiobutton(root, text=sabor, variable = pizza, value=valor).pack()

def open():
    global img
    top = Toplevel()
    Button(top, text="cerrar ventana", command=top.destroy).pack()
    img = ImageTk.PhotoImage(Image.open("chica_pool_2.jpg"))
    label = Label(top, text="new window").pack()
    label_img = Label(top, image=img).pack()
def show_img():
    global img_filename
    global opcion

    root_filename = filedialog.askopenfilename(initialdir='', title="seleccionar tps", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    img_filename = ImageTk.PhotoImage(Image.open(root_filename))
    opcion = IntVar()
    radiobutton = Radiobutton(root, text="mostrar img", variable=opcion, value=1, command=mostrar_imagen)
    radiobutton.pack()
def mostrar_imagen():
    if opcion.get() == 1:
        Label(root, image=img_filename).pack()
    else:
        Label(root, text="no se muestra por que se eligió que no").pack()

boton_abrir = Button(root,text="open new window", command=open).pack()
boton_abrir = Button(root,text="load file", command=show_img).pack()

var = StringVar()
def check_func(var):
    global label_check
    label_check = Label(root, text=str(var.get())).pack()


check_box = Checkbutton(root, text="te invito a que presiones aquí", variable=var, command=lambda: check_func(var), onvalue="Pizza")
check_box.deselect()
check_box.pack()
def clicked():
    etiqueta.config(text=pizza.get())
def pop_up():
    response = messagebox.askyesno("alerta", "boton presionado")
    if response == 1:
        Label(root, text="pusiste aceptar").pack()
    else:
        Label(root, text="pusiste no aceptar").pack()

click = Button(root, text="click me", command=clicked).pack()
aviso = Button(root, text="info", command=pop_up).pack()

root.mainloop()