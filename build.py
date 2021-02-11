from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Mmorpg",
    version = "0.1",
    description = "jeu de qualité",
    executables = [Executable("main.py")],
)
