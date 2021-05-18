import os
import shutil
import re
cwd = os.getcwd()
outDir = os.path.join(f"{cwd}/nytest")

os.makedirs("outDir", exist_ok=True)



personnummer = re.compile(r'(\d{8})-(\d{4}|\w{2}\d{2}).*')
lista = []
for text in open("lista.txt"):
    for match in re.finditer(personnummer, text):
        elev = (f"{match.group(1)}{match.group(2)}")
        lista.append(elev)
print(f'Här kommer listan över elever: {lista}')

nytuple = tuple(lista)
print(f'Här är den fina tuplen: {nytuple}')
elevlista = []
with os.scandir(cwd) as it:
    for entry in it:
        if entry.name.startswith(nytuple):
            print(f"{cwd}\{entry.name}")
            elevgrej = f'{entry.name [0:8]}-{entry.name[8:12]}'
            shutil.copytree(f"{cwd}\{entry.name}", f"{outDir}/{entry.name}")
            if entry.name.startswith(nytuple) and elevgrej not in elevlista:
                elevlista.append(elevgrej)
            else:
                continue
        else:
            print(f"INTE {entry.name}")

with open('elevlistaoutput.txt', 'w') as outputfile:
    outputfile.write('\n'.join(elevlista))

