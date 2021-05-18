# Prorenata-arkivexport
Skript för att göra kontroller och förbereda exporter ur journalsystemet Prorenata för e-arkivering.


## Beskrivning 
Skripten placeras i rotkatalogen i den aktuella exporten från Prorenata tillsammans med en lista i csv-format över de journaler som ska arkiveras.   
Skripten kontrollerar så att det inte kommit med några elever som har fingerade personuppgifter och kopierar ut de elevmappar som ska ingå i arkiveringen till mappen "arkivexport". Eventuella dublettmappar placeras i en särskild katalog "dubletter".           
Elevmapparna som ingår i arkiveringen får därefter nytt namn efter elevens personnummer och en kopia av elevernas xml-journalerna placeras i en särskild mapp "xml".
Eventuella fel skrivs ut i prompten och i en txt-fil. Exempel på sådana fel är att det saknas elevmapp eller att "sekretesselever" inte har riktiga personuppgifter. Även antalet mappar som ska ingå i arkiveringen enligt listan och hur många mappar som skriptet har hittat vid körningen skrivs ut i prompten för att kunna säkerställa att antalen matchar varandra.  
  
Om iipax-archive används som arkivsystem kan "prorenata.xsl"(finns i repository "iipaxskript") användas som preingestskript. Placera xml-filerna i aktuell-dropmapp och elevmapparna i aktuell documentLocation-mapp så läses materialet in i e-arkivet, under förutsättning att samma objektskonfiguration används.  


## Skript  
###### check_catalogs.py  - Används då csvfilen innehåller personnummer, namn och skola.
###### check_catalogs_no_school.py - Används när csv-filen bara innehåller personnummer.
###### rest_folders.py - Placeras i dublettmappen för att göra dubletterna klara för arkivering

### OLD
Mappen innehåller gamla skript från tidigare arkiveringar som inte längre används på grund av att exportlistan har förändrats. Skripten finns kvar i referenssyfte. Användning och funktion beskrivs i "läs mig.txt". preflight.py körs först, därefter körs "ProRenata_fleramappar_old.py"  