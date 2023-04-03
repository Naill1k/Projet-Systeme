#os.listdir, os.path.join, os.path.isfile,
#os.path.isdir, os.path.islink, os.path.basename, os.getcwd,
#et os.chdir pour construire une liste de “noms de fichiers”,
#et appellé os.stat pour récupérer toutes les informations
#utiles sur ces fichiers, qui font pleinement partie de la liste de fichiers.

arg="reptest"
import os

print(os.listdir(arg))
print(os.path.islink(arg))
print(os.path.basename(arg))
print(os.getcwd())
print(os.chdir(arg))
print(os.stat(os.getcwd()+"/fichier_normal"))
