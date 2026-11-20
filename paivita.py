#!/usr/bin/env python3
"""Päivittää sivun tiedot Google Drive -taulukosta "Legopaketit".

Käyttö:
    python3 paivita.py taulukko.json

taulukko.json on Google Sheetsin values-vastaus (tai pelkkä rivilista), jossa
ensimmäinen rivi on otsikko: Settinumero | Nimi | Teema | Ostohinta (€) | Kpl

Skripti
  1. kirjoittaa paketit.js-tiedoston, jota index.html lukee
  2. lataa puuttuvat tuotekuvat kuvat/-kansioon Rebrickablesta settinumerolla
  3. tulostaa yhteenvedon (pakettien määrä, yhteishinta, puuttuvat hinnat/kuvat)
"""
import io
import json
import os
import sys
import urllib.request

JUURI = os.path.dirname(os.path.abspath(__file__))
KUVAT = os.path.join(JUURI, "kuvat")


def luku(arvo):
    s = str(arvo).replace("€", "").replace(" ", "").replace(" ", "").replace(",", ".").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def lue_rivit(polku):
    with open(polku, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("values") or data.get("content", {}).get("values") or []
    return data


def paketit(rivit):
    tulos = []
    for r in rivit[1:]:
        r = list(r) + [""] * (5 - len(r))
        nro = str(r[0]).strip()
        if nro.endswith(".0"):
            nro = nro[:-2]
        if not nro:
            continue
        kpl = luku(r[4])
        p = {"nro": nro, "nimi": str(r[1]).strip() or f"Setti {nro}",
             "teema": str(r[2]).strip() or "Muu", "hinta": luku(r[3])}
        if kpl and int(kpl) > 1:
            p["kpl"] = int(kpl)
        tulos.append(p)
    return tulos


def kirjoita_js(lista):
    rivit = ",\n".join("  " + json.dumps(p, ensure_ascii=False) for p in lista)
    sisalto = ("/* Luotu automaattisesti Google Drive -taulukosta \"Legopaketit\" (paivita.py).\n"
               "   Älä muokkaa käsin: muutokset tehdään taulukkoon. */\n"
               f"const PAKETIT = [\n{rivit}\n];\n")
    polku = os.path.join(JUURI, "paketit.js")
    vanha = open(polku, encoding="utf-8").read() if os.path.exists(polku) else ""
    if vanha != sisalto:
        with open(polku, "w", encoding="utf-8") as f:
            f.write(sisalto)
    return vanha != sisalto


def lataa_kuva(nro):
    polku = os.path.join(KUVAT, f"{nro}.jpg")
    if os.path.exists(polku):
        return "olemassa"
    url = f"https://cdn.rebrickable.com/media/sets/{nro}-1.jpg"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
            raaka = r.read()
    except Exception as e:  # noqa: BLE001
        return f"epäonnistui ({e})"
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raaka))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            tausta = Image.new("RGB", im.size, (255, 255, 255))
            tausta.paste(im, mask=im.split()[3])
            im = tausta
        else:
            im = im.convert("RGB")
        im.thumbnail((800, 800))
        im.save(polku, "JPEG", quality=85, optimize=True)
    except ImportError:
        with open(polku, "wb") as f:
            f.write(raaka)
    return "ladattu"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    lista = paketit(lue_rivit(sys.argv[1]))
    if not lista:
        sys.exit("Taulukosta ei löytynyt yhtään pakettia, paketit.js jätettiin ennalleen.")
    muuttui = kirjoita_js(lista)
    os.makedirs(KUVAT, exist_ok=True)
    kuvat = {p["nro"]: lataa_kuva(p["nro"]) for p in lista}
    yht = sum((p["hinta"] or 0) * p.get("kpl", 1) for p in lista)
    print(f"paketit.js {'päivitetty' if muuttui else 'ei muutoksia'}")
    print(f"Paketteja: {sum(p.get('kpl', 1) for p in lista)}, yhteishinta: {yht:.2f} €".replace(".", ","))
    puuttuvat = [p["nro"] for p in lista if p["hinta"] is None]
    if puuttuvat:
        print("Hinta puuttuu:", ", ".join(puuttuvat))
    for nro, tila in kuvat.items():
        if tila != "olemassa":
            print(f"Kuva {nro}: {tila}")


if __name__ == "__main__":
    main()
