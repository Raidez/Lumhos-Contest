import shutil
import zipfile
from pathlib import Path
from cx_Freeze import setup, Executable

# suppression du dossier de build
print("clean build folder")
shutil.rmtree("build", ignore_errors=True)

# options des paquets/ressources à inclure
build_exe_options = {
    "packages": ["pygame"],
    "excludes": ["tkinter"],
    "include_files": ["res/"],
}

# options des exécutables
base = "Win32GUI"  # application graphique Windows
targets = [
    Executable("fireflies.py", base=base, target_name="Lucioles"),
]

# compilation du code
setup(options={"build_exe": build_exe_options}, executables=targets)

# archivage dans un zip pour chaque build
print("create build archive")
for build in Path().glob("build/*"):
    zipname = f"{build}.zip"
    with zipfile.ZipFile(zipname, "w") as fp:
        for subfile in build.rglob("**/*"):
            pathfile = str(subfile).replace(
                str(build) + "\\", ""
            )  # chemin du fichier dans la structure interne du zip
            fp.write(subfile, arcname=pathfile)
