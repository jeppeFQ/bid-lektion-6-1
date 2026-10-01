# Køreplan

Planen samler, hvad vi kom frem til i lektion 5, og lægger ting fast.

Alt, der ikke står her, bestemmer I selv.

## Produktet

En hjemmeside med fire sider, bygget med Quarto og lagt på GitHub Pages:

| Side | Hvad den gør |
|---|---|
| **Forside** | Hvad barometeret er, hvem det er til, og hvad det ikke kan |
| **Barometer** | Brugeren taster sine egne tal ind og ser, hvor arbejdspladsen ligger |
| **Opslag** | Fordelingerne for brancher, størrelser og regioner, uden at taste noget ind |
| **Om** | Data, definitioner, begrænsninger, og hvad barometeret ikke må bruges til |

## Grænsefladen på barometersiden

**Brugeren taster ind:** branche, sektor, region, antal ansatte, og hvor mange af dem
der er kvinder, 55 år eller derover, og har indvandrerbaggrund.

**Brugeren får:**

- Tre placeringer, én pr. dimension.
- En figur med tre paneler: hvor den sammenlignelige gruppe ligger, hvor
  arbejdspladsen ligger i den og udvikling over tid
- En kort forklaring i ord
- Besked, hvis arbejdspladsen har under 50 ansatte

## Arkitekturen

Fire lag, som i lektion 4. Hvert lag taler kun med det nedenunder.

```
Siden        Quarto + appen          det brugeren ser
   │
Appen        app.py                  læser felter, viser svar
   │
Kernen       barometer/              alle klasserne. Ved intet om grænsefladen
   │
Data         referencetal.csv        aggregerede tal fra Danmarks Statistik
```

## Klasserne

Seks klasser. Navnene ligger fast, så vi har en fælles forståelse af dem. 

| Klasse | Ved | Kan |
|---|---|---|
| `Arbejdsplads` | ansatte, antal i hver gruppe, branche, sektor, region | `andel(dimension)`, `stoerrelsesgruppe` |
| `Referencetal` | alle referencetallene | `find(arbejdsplads, dimension)`, `muligheder(kolonne)` |
| `Referencegruppe` | beskrivelse, antal arbejdssteder, percentiler, om den er bredere end ønsket | `median()` |
| `Placering` | dimension, andel, referencegruppe | `interval()`, `saetning()` |
| `Barometer` | referencetallene | `vurder(arbejdsplads)` |
| `Resultat` | arbejdspladsen og de tre placeringer | `forklaring()`, `figur()` |

**Reglerne i klasserne**, hentet fra rapporten:

- Under 50 ansatte: `Arbejdsplads`: afvises
- Flere i en gruppe end der er ansatte, eller negative tal: afvises
- Mangler den præcise sammenligningsgruppe, falder `Referencetal.find` tilbage til en bredere og siger det

## Data

Referencetallene ligger i `data/` som **flere tabeller**, ligesom i en database: `brancher`, `regioner`, `sektorer`, `stoerrelser`, `dimensioner`, `grupper` og `fordelinger`. De sættes sammen med `merge` — det, der i en database hedder et join. `data/README.md` beskriver det hele.

Tallene er **syntetiske** indtil videre. Strukturen er den rigtige, så jeres kode virker videre, når de rigtige tal kommer.

To ting, I skal regne med:

- **Nogle grupper mangler.** 28 ud af 128 kombinationer er udeladt, fordi der ville være for få arbejdssteder i dem. `Referencetal.find` skal falde tilbage til en bredere gruppe og sige det.      
- **Der er ingen løn og ingen kommuner i dataene.**     

## Filerne

```
diversitetsbarometer/
│
├── README.md                     projektbeskrivelsen 
├── KOEREPLAN.md                  aftalen: produkt, lag, klasser, milepæle
├── DESIGN.md                     gruppens beslutninger, udfyldes undervejs
├── GRUPPE.md                     
├── .gitignore
├── .github/
│   └── pull_request_template.md  tjeklisten, der dukker op i hver pull request
│
├── oevelse-barometerets-kerne.ipynb    dagens øvelse
│
├── data/                         referencetallene som en lille database
│   ├── brancher.csv              9 rækker, id 0 = "Alle"
│   ├── regioner.csv              6
│   ├── sektorer.csv              3
│   ├── stoerrelser.csv           5, med min_ansatte og max_ansatte
│   ├── dimensioner.csv           3, kvinder, seniorer, indvandrere
│   ├── grupper.csv               224, én pr. sammenligningsgruppe
│   ├── fordelinger.csv           672, p10 til p90 pr. gruppe og dimension
│   ├── metadata.csv              oplysninger om datasættet selv
│   ├── lav_syntetiske_data.py    genererer tabellerne
│   ├── lav_fladt.py              samler dem til én fil
│   └── afledt/
│       └── referencetal.csv      den flade udgave, kan altid laves igen
│
├── app/                          alt, barometeret skal bruge i browseren
│   ├── README.md                 trin for trin: sådan kører I appen
│   ├── app.py                    Shiny-appen, tynd udgave
│   └── barometer/                kernen. Ved intet om grænsefladen
│       ├── __init__.py
│       ├── fejl.py               UgyldigArbejdsplads 
│       ├── arbejdsplads.py       
│       └── referencetal.py       
│
├── samarbejdspartnere/           fra lektion 3
│   ├── _skabelon.md
│   └── jeppefq.md
│
├── python/
│   ├── README.md
│   └── samarbejdspartnere.py     scriptet, du kører på projektoren
│
├── _quarto.yml                   hjemmesidens opsætning
```

## Det, I selv bestemmer

Alt det, der ikke står ovenfor.