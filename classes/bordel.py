import tkinter
from functools import partial
def varToBordel(optionsO,playerO):
    global options,player
    options = optionsO
    player = playerO
def editor(ide,tk,tab):
    global id,editorActivated
    tk.destroy()
    tab[0] = ide
    editorActivated = True
def next(tk,page,tiles,id):
    """
    Passe à la page suivante dans l'éditeur (touche y)
    """
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
    """
    Passe à la page précédente dans l'éditeur (touche y)
    """
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
def globalToLocalCoord(x,y):
    """
    Convertisseur de coordonnées sur la carte à des coordonnées sur l'écran à partir du coin en haut à gauche
    """
    rx = (x+(options["fen"]["width"]/2)-player.x*32)
    ry = (y+(options["fen"]["height"]/2)-player.y*32)
    return rx,ry
def join(tk,game,map):
    """
    Rejoindre une nouvelle partie multijoueur
    """
    if(game == "newGame"):
        map.updates.append(("changeMap",game))
    elif(game.get() != ""):
        map.updates.append(("changeMap",game.get()))
