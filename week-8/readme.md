data_fetcher.py -

UrbanStyle'i andmete hankimise moodul.

Vastutus:
    - .env konfiguratsiooni laadimine
    - Supabase ühenduse loomine
    - müügiandmete hankimine
    - kliendiandmete hankimine
    - tooteandmete hankimine

Kõik andmed tagastatakse pandas DataFrame kujul.

See moodul ei tegele:
    - andmete puhastamisega
    - KPI-de arvutamisega
    - andmete agregeerimisega
    - diagrammide loomisega
    - andmete eksportimisega

Need tegevused asuvad projekti teistes moodulites.

Moodulit saab kasutada:
    1. importides funktsioonid pipeline.py-sse
    2. käivitades fetch_data.py iseseisvalt,
       mille puhul tehakse ühenduse ja päringute test.



transform.py -

UrbanStyle'i müügiandmete transformatsioonimoodul.

Vastutus:
    - müügiandmete puhastamine
    - müügiandmete nädalane agregeerimine
    - müügi KPI-de arvutamine
    - müügi- ja kliendiandmete ühendamine

See moodul ei tegele:
    - Supabase'ist andmete hankimisega
    - diagrammide loomisega
    - andmete eksportimisega

Neid ülesandeid käsitlevad eraldi moodulid.

Moodulit saab kasutada:
    1. importides funktsioonid pipeline.py-sse
    2. käivitades transform.py iseseisvalt, mille puhul
       käivitatakse sisseehitatud kvaliteeditestid.