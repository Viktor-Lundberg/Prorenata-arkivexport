import csv
import os
import shutil

cwd = os.getcwd()
out_dir = os.path.join(f'{cwd}/arkivpaket')
xml_dir = os.path.join(f'{cwd}/xml')
dublett_dir = os.path.join(f'{cwd}/dubletter')

os.makedirs(xml_dir, exist_ok=True)

file = open('elever.csv')
csvfile = csv.reader(file, dialect='excel', delimiter=';')
rowlist = list()

fellista = list()

for row in csvfile:
    rowlist.append(row)

# Ta bort rubrikrad
del rowlist[0]

antalelever = len(rowlist)
antalmappar = 0

# check sekretesselever
for row in rowlist:
    if row[2].startswith('Boråsskolan'):
        newrow = ','.join(row)
        fellista.append(f'SEKRETESS: {newrow}')
        rowlist.remove(row)

# check om det finns mappar för eleverna och kopierar
for row in rowlist:
    mapp = f"{row[1]} {row[0].lower().replace(' ', '-').replace('å','a').replace('ä','a').replace('ö','o')}, {row[2].lower().replace(' ', '-').replace('å','a').replace('ä','a').replace('ö','o')}"
    print(mapp)
    if os.path.exists(mapp):
        print('FINNS EXPORT')
        antalmappar += 1
        shutil.copytree(mapp,f'{out_dir}/{mapp}')
    else:
        print(f'{row} FINNS INTE I EXPORT')
        newrow = ','.join(row)
        fellista.append(f"SAKNAR MAPP: {newrow}")

# Namnger mapparna till personnummer och lägger dubbletter i särskild mapp
for folder in os.listdir(out_dir):
    print(folder)
    try:
        os.rename(f"{out_dir}/{folder}", f"{out_dir}/{folder[0:12]}")
    except:
        print('Eleven har redan mapp flyttar till dublettmapp')
        print(folder)
        shutil.move(f'{out_dir}/{folder}',f'{dublett_dir}/{folder}')
        fellista.append(f'DUBLETTMAPP: {folder}')

# Kopierar ut xml-filerna i arkivpaket och lägger i xml-katalog
for path, subdirs, files in os.walk(out_dir):
    for filename in files:
        if filename.endswith('.xml'):
            print(f"Kopierar {path}/{filename} till xml")
            shutil.copy2(f"{path}/{filename}", xml_dir)
        else:
            continue

print(f'antal elever: {antalelever}, antal mappar som flyttats {antalmappar}')


if len(fellista) > 0:
    print(f'{fellista}')
    errorfil = open('FEL.txt', 'w')
    errorfil.write('\n'.join(fellista))
