# Legokokoelma

Pojan legopaketit yhdellä sivulla (`index.html`). Sivun yläosassa näkyy pakettien yhteishinta.

## Tietojen päivittäminen

Pakettien tiedot ovat Google Drive -taulukossa **Legopaketit**
(https://docs.google.com/spreadsheets/d/1TeuiNlC6BCXnQ6bJzcLlY6HB33mq6ZA07wng4CZpeyA/edit).

Sarakkeet: Settinumero | Nimi | Teema | Ostohinta (€) | Kpl. Jätä hinta tyhjäksi, jos se ei ole tiedossa.

Ajastettu tehtävä lukee taulukon kerran kuukaudessa (kuun 1. päivä klo 00.00 Suomen aikaa),
ajaa `python3 paivita.py <taulukko.json>` ja pushaa muutokset. Skripti kirjoittaa `paketit.js`-tiedoston
ja lataa uusien settien kuvat `kuvat/`-kansioon settinumeron perusteella. `paketit.js`-tiedostoa ei muokata käsin.

## Julkaisu

GitHubissa: Settings → Pages → Deploy from a branch → valitse tämä haara ja `/ (root)`.
