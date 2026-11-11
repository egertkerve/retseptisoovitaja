"""
PROJEKT: Nutikas Külmkapiraamat / Retseptisoovitaja
AUTORID: Martin Saar ja Egert Kerve
KIRJELDUS: Programm otsib kasutaja sisestatud koostisosade põhjal sobivaid
retsepte ja kuvab neid sobivusprotsendi järgi pingerivis. Vesi, sool ja pipar
loetakse alati olemasolevaks.

KÄIVITAMINE:
1. Pane fail retseptid.json samasse kausta selle failiga.
2. Käivita programm käsuga: python failinimi.py
3. Sisesta oma toiduained ainsuse nimetavas käändes ükshaaval (nt "tatar", "või"). Tühi rida lõpetab sisestuse.
4. Vali nimekirjast retsepti number, kirjuta "järgmine" või "lõpeta".
"""

import json

def loe_retseptid(failinimi):
    
    """Loeb JSON-failist retseptide andmebaasi ja tagastab selle järjendina."""
    
    with open(failinimi, "r", encoding="utf-8") as fail:
        retseptid = json.load(fail)
    return retseptid

def leia_protsent(retsept):

    """Tagastab retsepti sobivusprotsendi sorteerimiseks."""
    return retsept['protsent']

def toiduainete_sisestamine():
    """Küsib kasutajalt toiduained ja tagastab need järjendina."""
    toiduained = []

    while True:
        toiduaine = input('Sisesta toiduained ainsuses ükshaaval: ').strip().lower()
        if toiduaine == '':
            break
        else:
            toiduained.append(toiduaine)
        
    print(f'Sinu toiduained: {toiduained}')
    return toiduained

def sobivad_retseptid(retseptid, toiduained):
     
    """Leiab sobivad retseptid ja järjestab need sobivusprotsendi järgi."""

    alati_olemas = {'vesi', 'sool', 'pipar'}
    
    sobilikud_retseptid = []
    for retsept in retseptid:
        koostisosad = retsept.get('koostisosad')
        sobivad = 0
        kasutaja_sobivad = 0
        for koostisosa_rida in koostisosad:
            koostisosa = koostisosa_rida.split('–')[0].strip().lower()
            if koostisosa in toiduained:
                sobivad += 1
                kasutaja_sobivad += 1
            elif koostisosa in alati_olemas:
                sobivad += 1
    
        sobivusprotsent = round(sobivad / len(koostisosad) * 100, 1)
        if kasutaja_sobivad > 0:
            sobilikud_retseptid.append({
                'retsept': retsept,
                'protsent': sobivusprotsent
            })
        
    sobilikud_retseptid.sort(key=leia_protsent, reverse=True)
    return sobilikud_retseptid

def kuva_retsept(valitud_retsept):
    """Kuvab valitud retsepti koostisosad ja valmistusjuhendi."""
    print("\n" + "="*40)
    print(f" RETSEPT: {valitud_retsept['nimi'].upper()} ")
    print("="*40)
    print("\nKoostisosad:")
    for koostisosa in valitud_retsept['koostisosad']:
        print(f" - {koostisosa}")
        
    print("\nValmistusjuhend:")
    for samm_nr, samm in enumerate(valitud_retsept['juhend'], 1):
        print(f" {samm_nr}. {samm}")
    print("="*40 + "\n")



def main():
    """Programmi põhitöövoog: sisend, arvutus, sorteerimine ja kuvamine."""
    
    retseptid = loe_retseptid("retseptid.json")
    toiduained = toiduainete_sisestamine()


    sobilikud_retseptid = sobivad_retseptid(retseptid, toiduained)

    kuvatud_indeks = 0
    vastete_arv = 15 

    while True:
        if len(sobilikud_retseptid) == 0:
            print("\nÜhtegi sobivat retsepti Sinu toiduainetega ei leitud.")
            break
            
        if kuvatud_indeks >= len(sobilikud_retseptid):
            print("\nRohkem sobivaid retsepte andmebaasis ei ole.")
            break

        print(f"\n--- Sobivad retseptid (Kuvatakse {kuvatud_indeks + 1} kuni {min(kuvatud_indeks + vastete_arv, len(sobilikud_retseptid))}) ---")
        
        praegune_valik = {}
        for i in range(kuvatud_indeks, min(kuvatud_indeks + vastete_arv, len(sobilikud_retseptid))):
            jarjekorranumber = i + 1
            üksus = sobilikud_retseptid[i]
            nimi = üksus['retsept']['nimi']
            protsent = üksus['protsent']
            
            print(f"[{jarjekorranumber}] {nimi} — sobivus: {protsent}%")
            praegune_valik[jarjekorranumber] = üksus['retsept']

        valik = input("\nSisesta retsepti NUMBER, 'järgmine' uute kuvamiseks või 'lõpeta': ").strip().lower()

        if valik == 'järgmine':
            kuvatud_indeks += vastete_arv
            continue
        elif valik == 'lõpeta':
            break
        
        try:
            valitud_number = int(valik)
            if valitud_number in praegune_valik:
                valitud_retsept = praegune_valik[valitud_number]
                kuva_retsept(valitud_retsept)
                uuesti = input("Kas soovid vaadata teisi retsepte? (jah/ei): ").strip().lower()
                if uuesti != 'jah':
                    print("Head kokkamist!")
                    break
            else:
                print("Seda numbrit pole praeguses valikus. Proovi uuesti.")
        except ValueError:
            print("Vigane sisend. Sisesta number, 'järgmine' või 'lõpeta'.")

if __name__ == "__main__":
    main()
