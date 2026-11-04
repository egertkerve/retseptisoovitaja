import json

def loe_retseptid(failinimi):
    with open(failinimi, "r", encoding="utf-8") as fail:
        retseptid = json.load(fail)
    return retseptid

retseptid = loe_retseptid("retseptid.json")


toiduained = []

while True:
    toiduaine = input('Sisesta toiduained ükshaaval: ').strip().lower()
    if toiduaine == '':
        break
    else:
        toiduained.append(toiduaine)

print(f'Sinu toiduained: {toiduained}')


for retsept in retseptid:
    koostisosad1 = retsept.get('koostisosad')
    sobivad = 0
    for toiduaine in toiduained:
        if toiduaine in koostisosad1:
            sobivad += 1

    sobviusprotsent = round(sobivad / len(koostisosad1) * 100, 1)
    print(f'{retsept["nimi"]} sobib {sobviusprotsent}%')
