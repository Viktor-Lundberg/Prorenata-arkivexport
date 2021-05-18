import os
import csv
import shutil

cwd = os.getcwd()
out_dir = os.path.join(f'{cwd}/arkivpaket')
xml_dir = os.path.join(f'{cwd}/xml')
dublett_dir = os.path.join(f'{cwd}/dubletter')
os.makedirs(xml_dir, exist_ok=True)

# Exportlistan från ProRenata
file = open('elevlista.csv')
csvfile = csv.reader(file, dialect='excel', delimiter=';')
rows = []
fellista = []

# Tar bort rubrikrad
for row in csvfile:
    rows.append(row)
del rows[0]

# Räknar ut antalet mappar i exporten
antalexportmappar = len(rows)
# Variabel för att räkna mappar
antalmappar = 0

# loopar igenom listan från exporten och kör mot elevmapparna i exporten
for row in rows:
    dirs = os.listdir(cwd)
    personnummer = row[0]
    matchcount = 0
    # Kontrollvariabel för att endast en mapp per rad ska kopieras
    loopstopper = False

    # Kollar så att det inte finns sekretesselever
    if row[1].startswith('xx') or row[1].startswith('XX'):
        fellista.append(f'SEKRETESS: {personnummer}')
        continue

    # Kollar om mapp startar med det aktuella personnumret och flyttar den till mappen arkivpaket
    for dir in dirs:
        if (dir.startswith(personnummer)) and (loopstopper is False):
            shutil.move(dir, f'{out_dir}/{dir}')
            matchcount += 1
            antalmappar += 1
            print(f'{dir} counting {matchcount}')
            loopstopper = True
        else:
            continue
    # Om eleven saknar mapp i exporten genereras ett felmeddelande i fellistan
    if matchcount == 0:
        fellista.append(f'SAKNAR MAPP: {personnummer}')

# Döper om mapparna i arkivpaket till elevens personnummer. Om personnumret redan finns läggs mappen i "dublettmappar"
for folder in os.listdir(out_dir):
    try:
        os.rename(f"{out_dir}/{folder}", f"{out_dir}/{folder[0:12]}")
    except:
        shutil.move(f'{out_dir}/{folder}',f'{dublett_dir}/{folder}')
        fellista.append(f'DUBLETTMAPP: {folder}')

# Kopierar ut alla xml-filer till en xml-katalog
for path, subdirs, files in os.walk(out_dir):
    for filename in files:
        if filename.endswith('.xml'):
            shutil.copy2(f"{path}/{filename}", xml_dir)
        else:
            continue
# Printar resultatet
print(f'antal mappar som ska arkiveras: {antalexportmappar}, antal mappar som flyttats {antalmappar}')

# Ev fel printas och hamnar i filen FEL.txt
if len(fellista) > 0:
    print(fellista)
    errorfil = open('FEL.txt', 'w')
    errorfil.write('\n'.join(fellista))