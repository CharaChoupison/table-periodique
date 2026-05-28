# API Python - Tableau periodique

Petite API Python sans dependance externe pour consulter les elements du tableau periodique.

## Lancer le serveur

```bash
python3 app.py
```

Par defaut, le serveur demarre sur :

```text
http://127.0.0.1:3000
```

Tu peux changer le port :

```bash
PORT=4000 python3 app.py
```

## Page web

Ouvre :

```text
http://127.0.0.1:3000
```

La page permet de tester les routes, chercher un element et filtrer par classe.

## Routes API

### Tout le tableau periodique

```http
GET /elements
```

### Element par numero atomique ou acronyme/symbole

```http
GET /elements/26
GET /elements/Fe
```

### Elements par classe

```http
GET /classes/metal-lourd
GET /classes/gaz-noble
GET /classes/halogene
```

Classes disponibles :

- `non-metal`
- `gaz-noble`
- `metal-alcalin`
- `metal-alcalino-terreux`
- `metalloide`
- `halogene`
- `metal-de-transition`
- `metal-lourd`
- `metal-pauvre`
- `lanthanide`
- `actinide`
- `inconnue`
