import tkinter
from functools import partial
try:
    options = json.loads(open("config.json",'r').read()) # On importe le fichier json sous forme d'un objet
except:
    print("Erreur dans le chargement du fichier de configuration (existe-t-il ?)")
def editor(ide,tk,tab):
    global id,editorActivated
    tk.destroy()
    tab[0] = ide
    editorActivated = True
def next(tk,page,tiles,id):
    page+=1
    tk.destroy()
    tk = tkinter.Tk()
    for j in tiles[page*10:((page+1)*10)]:
        bouton = tkinter.Button(tk,text=j.name,command=partial(editor,j.id,tk,id))
        bouton.pack()
    tkinter.Button(tk,text="Page suivante",command=partial(next,tk,page,tiles,id)).pack()
    tkinter.Button(tk,text="Page précédente",command=partial(past,tk,page,tiles,id)).pack()
    tk.mainloop()
def past(tk,page,tiles,id):
    if(page != 0):
        page-=1
        tk.destroy()
        tk = tkinter.Tk()
        for j in tiles[page*10:((page+1)*10)]:
            bouton = tkinter.Button(tk,text=j.name,command=partial(editor,j.id,tk,id))
            bouton.pack()
        tkinter.Button(tk,text="Page suivante",command=partial(next,tk,page,tiles,id)).pack()
        tkinter.Button(tk,text="Page précédente",command=partial(past,tk,page,tiles,id)).pack()
        tk.mainloop()
def globalToLocalCoord(x,y,playerx,playery):
    rx = (x-(options["fen"]["width"]/2)+playerx*32)
    rx = (y-(options["fen"]["height"]/2)+playery*32)
    return rx,ry
