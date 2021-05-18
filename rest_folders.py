import os
import shutil

cwd = os.getcwd()
xml_dir = os.path.join(f'{cwd}/xml')
os.makedirs(xml_dir, exist_ok=True)


for folder in os.listdir(cwd):
    for folder in os.listdir(cwd):
        try:
            os.rename(f"{cwd}/{folder}", f"{cwd}/{folder[0:12]}")
        except:
            continue


for path, subdirs, files in os.walk(cwd):
    for filename in files:
        if filename.endswith('.xml'):
            shutil.copy2(f"{path}/{filename}", xml_dir)
        else:
            continue

