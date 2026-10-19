import json
import requests
from datetime import datetime
from pyproj import Transformer

# Aito havaintodata
nykyinen_vuosi = datetime.now().year
HAVAINTO_API = f"https://marjahavainnot.fi/api/v1/observations?year={nykyinen_vuosi}"

# Luodaan muuntaja: EPSG:3067 (Luken metrit) -> EPSG:4326 (WGS84 GPS-asteet)
# always_xy=True varmistaa, että järjestys on aina (pituusaste, leveysaste)
transformer = Transformer.from_crs("EPSG:3067", "EPSG:4326", always_xy=True)

# Suomen 19 maakuntaa karkeina laatikkoina
ALUEET = [
    {
        "nimi": "Ahvenanmaa",
        "min_lat": 59.7, "max_lat": 60.5, "min_lon": 19.3, "max_lon": 21.2,
        "min_x": 100000, "max_x": 180000, "min_y": 6630000, "max_y": 6720000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Varsinais-Suomi",
        "min_lat": 60.0, "max_lat": 61.0, "min_lon": 21.0, "max_lon": 24.0,
        "min_x": 180000, "max_x": 310000, "min_y": 6650000, "max_y": 6780000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Uusimaa",
        "min_lat": 59.8, "max_lat": 60.8, "min_lon": 23.0, "max_lon": 26.5,
        "min_x": 270000, "max_x": 450000, "min_y": 6630000, "max_y": 6750000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Satakunta",
        "min_lat": 60.9, "max_lat": 62.0, "min_lon": 21.3, "max_lon": 23.0,
        "min_x": 190000, "max_x": 260000, "min_y": 6760000, "max_y": 6890000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Kanta-Häme",
        "min_lat": 60.6, "max_lat": 61.3, "min_lon": 23.3, "max_lon": 25.0,
        "min_x": 300000, "max_x": 400000, "min_y": 6720000, "max_y": 6810000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Pirkanmaa",
        "min_lat": 61.1, "max_lat": 62.4, "min_lon": 22.6, "max_lon": 24.8,
        "min_x": 250000, "max_x": 370000, "min_y": 6770000, "max_y": 6930000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Päijät-Häme",
        "min_lat": 60.8, "max_lat": 61.7, "min_lon": 24.9, "max_lon": 26.3,
        "min_x": 390000, "max_x": 460000, "min_y": 6740000, "max_y": 6850000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Kymenlaakso",
        "min_lat": 60.3, "max_lat": 61.2, "min_lon": 26.0, "max_lon": 27.9,
        "min_x": 450000, "max_x": 540000, "min_y": 6690000, "max_y": 6790000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Etelä-Karjala",
        "min_lat": 60.7, "max_lat": 61.6, "min_lon": 27.2, "max_lon": 29.7,
        "min_x": 520000, "max_x": 630000, "min_y": 6730000, "max_y": 6840000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Etelä-Savo",
        "min_lat": 61.2, "max_lat": 62.5, "min_lon": 26.0, "max_lon": 29.6,
        "min_x": 450000, "max_x": 610000, "min_y": 6780000, "max_y": 6940000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Pohjois-Savo",
        "min_lat": 62.2, "max_lat": 63.9, "min_lon": 25.8, "max_lon": 29.0,
        "min_x": 450000, "max_x": 580000, "min_y": 6900000, "max_y": 7090000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Pohjois-Karjala",
        "min_lat": 61.8, "max_lat": 63.8, "min_lon": 28.5, "max_lon": 31.6,
        "min_x": 570000, "max_x": 730000, "min_y": 6850000, "max_y": 7090000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Keski-Suomi",
        "min_lat": 61.6, "max_lat": 63.4, "min_lon": 24.0, "max_lon": 26.6,
        "min_x": 360000, "max_x": 470000, "min_y": 6830000, "max_y": 7040000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Etelä-Pohjanmaa",
        "min_lat": 62.1, "max_lat": 63.4, "min_lon": 21.2, "max_lon": 24.4,
        "min_x": 200000, "max_x": 340000, "min_y": 6890000, "max_y": 7040000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Pohjanmaa",
        "min_lat": 62.0, "max_lat": 64.0, "min_lon": 20.9, "max_lon": 23.4,
        "min_x": 200000, "max_x": 290000, "min_y": 6890000, "max_y": 7110000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Keski-Pohjanmaa",
        "min_lat": 63.3, "max_lat": 64.1, "min_lon": 23.3, "max_lon": 24.8,
        "min_x": 310000, "max_x": 380000, "min_y": 7030000, "max_y": 7120000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Pohjois-Pohjanmaa",
        "min_lat": 63.6, "max_lat": 66.3, "min_lon": 23.5, "max_lon": 30.0,
        "min_x": 320000, "max_x": 620000, "min_y": 7060000, "max_y": 7360000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Kainuu",
        "min_lat": 63.7, "max_lat": 65.5, "min_lon": 27.5, "max_lon": 30.3,
        "min_x": 500000, "max_x": 640000, "min_y": 7060000, "max_y": 7280000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    },
    {
        "nimi": "Lappi",
        "min_lat": 65.5, "max_lat": 70.1, "min_lon": 20.5, "max_lon": 30.2,
        "min_x": 230000, "max_x": 600000, "min_y": 7260000, "max_y": 7780000,
        "mustikka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "puolukka": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}, "karpalo": {"tila": "tuntematon", "kuvaus": "Ei havaintoja"}
    }
]

def arvioi_tila_ja_teksti(phase, havainto_pvm_str):
    try:
        havainto_pvm = datetime.strptime(havainto_pvm_str, "%Y-%m-%d")
        ika = (datetime.now() - havainto_pvm).days

        if phase == "ripe":
            if ika > 30: 
                return "ohi", f"Sato ohi (Viimeisin kypsä havainto: {havainto_pvm_str})"
            else: 
                return "kypsä", f"Kypsä (Todennettu: {havainto_pvm_str})"
                
        elif phase in ["flower", "unripe"]:
            if ika > 60: 
                return "ohi", f"Sato ohi (Viimeisin havainto: {havainto_pvm_str})"
            elif ika > 20: 
                return "kypsä", f"Arvioitu kypsäksi (Alkuperäinen havainto: raakile/kukka {havainto_pvm_str})"
            else: 
                tila_fi = "Kukkii" if phase == "flower" else "Raakile"
                return "raakile", f"{tila_fi} (Todennettu: {havainto_pvm_str})"
                
        elif phase == "overripe":
            return "ohi", f"Sato ohi (Todennettu: {havainto_pvm_str})"
            
    except (ValueError, TypeError):
        pass

    return "tuntematon", "Ei havaintoja"

def kaanna_marja(berry):
    if berry == "blueberry": return "mustikka"
    if berry == "lingonberry": return "puolukka"
    if berry == "cloudberry": return "karpalo"
    return None

def hae_ja_kasittele_data():
    print(f"Haetaan aitoa dataa: {HAVAINTO_API}")
    response = requests.get(HAVAINTO_API, timeout=10)
    response.raise_for_status()
    havainnot = response.json()
    
    # Järjestetään havainnot vanhimmasta uusimpaan.
    havainnot.sort(key=lambda k: k.get("observed", ""), reverse=False)
    
    loydetyt = 0
    
    for h in havainnot:
        x, y = h.get("x"), h.get("y")
        berry = kaanna_marja(h.get("berry"))
        pvm = h.get("observed")
        
        if not x or not y or not berry or not pvm: 
            continue

        for alue in ALUEET:
            if alue["min_x"] <= x <= alue["max_x"] and alue["min_y"] <= y <= alue["max_y"]:
                tila, kuvaus_teksti = arvioi_tila_ja_teksti(h.get("phase"), pvm)
                
                # MUUNNOS: X/Y-metrit -> Lon/Lat-asteiksi
                lon, lat = transformer.transform(x, y)
                
                alue[berry]["tila"] = tila
                alue[berry]["kuvaus"] = kuvaus_teksti
                alue[berry]["havainto_lat"] = lat
                alue[berry]["havainto_lon"] = lon
                loydetyt += 1

    # Siivotaan TM35FIN koordinaatit
    for alue in ALUEET:
        if "min_x" in alue:
            del alue["min_x"]
            del alue["max_x"]
            del alue["min_y"]
            del alue["max_y"]

    tulos = {
        "alueet": ALUEET
    }
    
    with open("satotilanne.json", 'w', encoding='utf-8') as f:
        json.dump(tulos, f, ensure_ascii=False, indent=4)
        
    print(f"Data prosessoitu onnistuneesti! Käsiteltiin ja päivitettiin {loydetyt} aluehavaintoa.")
    print("---> 'satotilanne.json' luotu.")

if __name__ == "__main__":
    hae_ja_kasittele_data()
