# Legokokoelma

Pojan legopaketit yhdellä sivulla (`index.html`). Sivun yläosassa näkyy pakettien yhteishinta.

## Paketin lisääminen

Avaa `index.html` ja lisää rivi `PAKETIT`-listaan:

```js
{ nro: "60414", nimi: "Paloasema ja paloauto", teema: "City", hinta: 99.95 },
```

- `hinta: null`, jos hinta ei ole tiedossa
- `kpl: 2`, jos samaa settiä on useampi

Kuva haetaan ensin kansiosta `kuvat/<nro>.jpg` ja sen jälkeen netistä settinumeron perusteella.
Rakennusohjeen linkki muodostetaan settinumerosta LEGOn ohjesivulle.

## Julkaisu

GitHubissa: Settings → Pages → Deploy from a branch → valitse tämä haara ja `/ (root)`.
