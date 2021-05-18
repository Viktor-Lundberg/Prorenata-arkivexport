import os
import re
import glob
import shutil

personnummer = re.compile(r'(\d{6})-(\d{4}|\w{2}\d{2}).*')
cwd = os.getcwd()
outDir = os.path.join(cwd, 'arkivpaket')
xmlDir = os.path.join(cwd, 'XML/XML_GY')
outDir2 = os.path.join(cwd, 'arkivpaket_hogstadie')
xmlDir2 = os.path.join(cwd, 'XML/XML_HOGSTADIE')
outDir3 = os.path.join(cwd, 'arkivpaket_pe')
xmlDir3 = os.path.join(cwd, 'XML/XML_PE')

# Tömmer outdir på alla filer om den finns
if os.path.exists(outDir):
    for r, d, f, in os.walk(outDir):
        for cur in f:
            os.remove(os.path.join(r, cur))

# Skapar katalogen output om den inte finns
os.makedirs(outDir, exist_ok=True)
os.makedirs(xmlDir, exist_ok=True)
os.makedirs(outDir2, exist_ok=True)
os.makedirs(xmlDir2, exist_ok=True)
os.makedirs(outDir3, exist_ok=True)
os.makedirs(xmlDir3, exist_ok=True)

# Skapar gallringslistan som ska ges till PRN
gallringslista = open("Gallringslista.txt", "w")
gallringslista.write("Elever som arkiveras från ProRenata:\n")

# Skapar lista över elever som finns med i elevregistret men som inte har exportmapp
eleverutanexportmapp = open("saknarmapp.txt", "w")
eleverutanexportmapp.write("Elever som inte har någon exportmapp från ProRenata: \n")

# Variabel för antal elever i exporten
i = 0
# Variabel för antal elever som finns på listan men som inte finns i exporten
i2 = 0
# Variabel för antalet mappar som finns med i exporten
antalmappar = 0

# Går igenom listan med personnummer och matchar dessa mot kataloger i cwd
for text in open("lista.txt"):
    for match in re.finditer(personnummer, text):
       forled = (match.group(1))
       efterled = (match.group(2))
       arkivelev = (f"{forled}{efterled}")
       #mappar = glob.glob1(cwd, "*" + arkivelev + "*")
       arkivmapp = ' '.join(glob.glob1(cwd, "*" + arkivelev + "*gymnasiet*"))
       arkivmapp_hogstadie = ' '.join(glob.glob1(cwd, "*" + arkivelev + "*skola*"))
       arkivmapp_pe = ' '.join(glob.glob1(cwd, "*" + arkivelev + "*" ", pe"))

        # Kollar om det finns gy-mapp och högstadiemapp
       if os.path.exists(f"{arkivmapp}") and os.path.exists(f"{arkivmapp_hogstadie}"):
           antalmappar += 2
           print(f"Flyttar {arkivmapp} till arkivpaket")
           shutil.copytree(arkivmapp, f"arkivpaket/{arkivmapp}")
           i += 1
           # shutil.move(arkivmapp, "arkivpaket") #Ändra till move när du kör skarpt!
           gallringslista.write(f"{forled}-{efterled}\n")
           print(f"Flyttar {arkivmapp_hogstadie} till arkivpaket_hogstadie")
           shutil.copytree(arkivmapp_hogstadie, f"arkivpaket_hogstadie/{arkivmapp_hogstadie}")

       # Kollar om det finns en PE-mapp och antingen en högstadiemapp eller gy-mapp
       elif os.path.exists(f"{arkivmapp_pe}") is True and (os.path.exists(f"{arkivmapp_hogstadie}") or os.path.exists(f"{arkivmapp}")) is True:
           antalmappar += 2
           # Kollar om det är en PE + högstadie
           if os.path.exists(f"{arkivmapp_pe}") and os.path.exists(f"{arkivmapp_hogstadie}"):
               print(f"Flyttar {arkivmapp_pe} till arkivpaket_pe")
               shutil.copytree(arkivmapp_pe, f"arkivpaket_pe/{arkivmapp_pe}")
               print(f"Flyttar {arkivmapp_hogstadie} till arkivpaket_hogstadie")
               shutil.copytree(arkivmapp_hogstadie, f"arkivpaket_hogstadie/{arkivmapp_hogstadie}")
               i += 1
               # shutil.move(arkivmapp, "arkivpaket") #Ändra till move när du kör skarpt!
               gallringslista.write(f"{forled}-{efterled}\n")
           # Annars flyttar den PE + GY mapp
           else:
               print(f"Flyttar {arkivmapp_pe} till arkivpaket_pe")
               shutil.copytree(arkivmapp_pe, f"arkivpaket_pe/{arkivmapp_pe}")
               print(f"Flyttar {arkivmapp} till arkivpaket")
               shutil.copytree(arkivmapp, f"arkivpaket/{arkivmapp}")
               i += 1
               gallringslista.write(f"{forled}-{efterled}\n")

        # Kollar om det bara finns en GY-mapp
       elif os.path.exists(f"{arkivmapp}"):
           print(f"Flyttar {arkivmapp} till arkivpaket")
           shutil.copytree(arkivmapp, f"arkivpaket/{arkivmapp}")
           antalmappar += 1
           i += 1
           #shutil.move(arkivmapp, "arkivpaket") #Ändra till move när du kör skarpt!
           gallringslista.write(f"{forled}-{efterled}\n")

        # Kollar om det bara finns en högstadiemapp
       elif os.path.exists(f"{arkivmapp_hogstadie}"):
           print(f"Flyttar {arkivmapp_hogstadie} till arkivpaket_hogstadie")
           shutil.copytree(arkivmapp_hogstadie, f"arkivpaket_hogstadie/{arkivmapp_hogstadie}")
           antalmappar += 1
           i += 1
           # shutil.move(arkivmapp, "arkivpaket") #Ändra till move när du kör skarpt!
           gallringslista.write(f"{forled}-{efterled}\n")

        # Kollar om det bara finns en PE-mapp
       elif os.path.exists(f"{arkivmapp_pe}"):
           print(f"Flyttar {arkivmapp_pe} till arkivpaket_pe")
           shutil.copytree(arkivmapp_pe, f"arkivpaket_pe/{arkivmapp_pe}")
           i +=1
           antalmappar += 1
           gallringslista.write(f"{forled}-{efterled}\n")
        # Skriver ut att eleven saknas i exporten i eleverutanexportmapp.txt om eleven inte matchar något av ovanstående
       else:
           print(f"Eleven {forled}-{efterled} ingår inte i exporten.")
           i2 +=1
           eleverutanexportmapp.write(f"{i2}. {forled}-{efterled}\n")

gallringslista.write(f"\n\n Totalt antal elever som arkiveras {i}")
gallringslista.write(f"\nTotalt antal mappar som arkiveras {antalmappar}")
gallringslista.close()
eleverutanexportmapp.write(f"\n\n Antal elever som saknar exportmapp: {i2}")
eleverutanexportmapp.close()

# Ger mapparna som flyttats till arkivpaket nytt namn efter elevens personnummer
for folder in os.listdir(outDir):
    os.rename(f"{outDir}/{folder}", f"{outDir}/{folder[0:12]}")

# Loopar igenom katalogerna i arkivpaket och söker upp alla xml-filer och kopierar dessa till mappen XML/XML_GY
for path, subdirs, files in os.walk(outDir):
    for f in files:
        if f.endswith('.xml'):
            print(f"Kopierar {path}/{f} till XML/XML_GY")
            shutil.copy2(f"{path}/{f}", xmlDir)
        else:
            continue

# Ger mapparna som flyttats till arkivpaket_hogstadie nytt namn efter elevens personnummer
for folder in os.listdir(outDir2):
    os.rename(f"{outDir2}/{folder}", f"{outDir2}/{folder[0:12]}")

# Loopar igenom katalogerna i arkivpaket och söker upp alla xml-filer och kopierar dessa till mappen XML/XML_HOGSTADIE
for path, subdirs, files in os.walk(outDir2):
    for f in files:
        if f.endswith('.xml'):
            print(f"Kopierar {path}/{f} till XML/XML_HOGSTADIE")
            shutil.copy2(f"{path}/{f}", xmlDir2)
        else:
            continue

# Ger mapparna som flyttats till arkivpaket_pe nytt namn efter elevens personnummer
for folder in os.listdir(outDir3):
    os.rename(f"{outDir3}/{folder}", f"{outDir3}/{folder[0:12]}")

# Loopar igenom katalogerna i arkivpaket och söker upp alla xml-filer och kopierar dessa till mappen XML/XML_PE
for path, subdirs, files in os.walk(outDir3):
    for f in files:
        if f.endswith('.xml'):
            print(f"Kopierar {path}/{f} till XML/XML_PE")
            shutil.copy2(f"{path}/{f}", xmlDir3)
        else:
            continue

# Printar reslutatet i prompten
print(f"Totalt antal mappar som arkiveras {antalmappar}")
print(f"Totalt antal elever som arkiveras {i}")
print(f"Antal elever som saknar exportmapp {i2}")
