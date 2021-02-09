def editor(ide,tk,tab):
    global id,editorActivated
    tk.destroy()
    tab[0] = ide
    editorActivated = True
