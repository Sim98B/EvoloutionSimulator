# 🍄 Simulazione Evolutiva di Funghi (Mushroom Evolution)

Una simulazione basata su principi di evoluzione naturale, dove i funghi (Mushroom) si sviluppano, competono e si riproducono in un ambiente rappresentato da un "bosco" (Wood), che fornisce nutrienti in base alla loro distribuzione.

---

## 🎯 Obiettivo

Questo progetto implementa una **simulazione evolutiva di funghi** che si adattano all'ambiente (nutrienti, competizione, rischio) e si riproducono in base a un sistema di fitness. Ogni fungo ha:

- **Fenotipi**: cappello, stoma, micelio, spore
- **Geni**: parametri che influiscono sulle caratteristiche (es. crescita, dispersione, rischio)
- **Comportamenti**: competizione, riproduzione, mutazioni

Il sistema valuta la **fitness** di ogni fungo in base alla quantità di nutrienti locali, alla competizione con altri funghi e ai costi energetici.

---

## 📦 Componenti Principali

### 1. `Wood` – L'ambiente (il "bosco")

La classe `Wood` rappresenta il mondo in cui vivono i funghi. Include:

- **Mappe di nutrienti**: combinazione di umidità e sostanze organiche.
- **Generazione di cluster**: per simulare la distribuzione di nutrienti.
- **Metodi**:
  - `get_nutrients(x, y, radius, grid)`: restituisce la quantità di nutrienti intorno a una posizione.
  - `display(ax)`: visualizza il mondo e i funghi (cappelli, micelio, ecc.).

### 2. `Mush` – Il fungho (l'individuo)

La classe `Mush` rappresenta un singolo fungho con:

- **Fenotipi**:
  - `cap`: dimensione del cappello
  - `stem`: lunghezza dello stoma
  - `mycelium`: dimensione del micelio
  - `spore`: quantità di spore
- **Geni**:
  - Parametri che influiscono sulla crescita, dispersione, rischio e costi.
- **Metodi**:
  - `compute_fitness()`: calcola il valore di fitness basandosi su:
    - Nutrienti locali
    - Competizione con altri funghi
    - Costi energetici (energia, struttura, manutenzione)
  - `reproduce()`: genera nuovi funghi (figli) con mutazioni e dispersione.

---

## 🔍 Come funziona il sistema

1. **Inizializzazione**:
   - Si crea un ambiente (`Wood`) con una dimensione, risoluzione e distribuzione di nutrienti.
   - Si generano un numero di funghi (es. 300) in posizioni casuali.

2. **Generazioni**:
   - Ogni generazione:
     - Ogni fungho calcola il proprio **fitness** (valore di adattamento).
     - Solo i funghi con fitness > `survival_threshold` sopravvivono.
     - I più adattati si riproducono, generando figli con **mutazioni** (in geni e fenotipi).
     - I nuovi funghi si posizionano in posizioni casuali e si espandono.

3. **Visualizzazione**:
   - Ogni generazione, il mondo viene visualizzato con `matplotlib`.
   - Si tracciano i trend dei fenotipi (cap, stem, mycelium, spore) e della popolazione.

4. **Salvataggio**:
   - I dati delle generazioni (media, deviazione, popolazione) vengono salvati in un file CSV (`run.csv`).

---

## 📊 Grafici e Dati

I risultati vengono visualizzati in un grafico con:
- **Trend dei fenotipi** (cap, stem, mycelium, spore) per generazione (media ± deviazione).
- **Popolazione** nel tempo (numero di funghi vivi).

> Il file `run.csv` contiene tutti i dati delle generazioni, utile per analisi e ripetizioni.

---

## 🛠️ Come eseguire il codice

1. Assicurati di avere installati i requisiti:
   ```bash
   pip install numpy matplotlib pandas
   ```

2. Esegui il file `SME.py` (o il file principale del progetto).

3. Osserva la visualizzazione in tempo reale (grafico con `matplotlib`).

4. Al termine, il file `run.csv` conterrà i dati delle generazioni.

---

## 🚀 Possibili miglioramenti

- Aggiungere **adattamento al territorio** (es. aree con più nutrienti).
- Introdurre **interazione tra specie** (es. predazione, cooperazione).
- **Analisi più dettagliata** dei geni e delle mutazioni.
- **Riproduzione strategica** basata su fitness.

---

## 📚 Note

- Il sistema è un esempio di **evoluzione per selezione naturale**.
- I parametri di mutazione e fitness sono semplici ma efficaci per mostrare i principi fondamentali.
- Il codice è scritto in **Python**, con uso di `numpy` per operazioni vettoriali e `matplotlib` per la visualizzazione.

---

## 📄 Licenza

Questo progetto è a scopo educativo e di esempio.  
Tutti i diritti riservati.
