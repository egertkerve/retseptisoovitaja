import json

def loe_retseptid(failinimi):
    with open(failinimi, "r", encoding="utf-8") as fail:
        retseptid = json.load(fail)
    return retseptid

retseptid = loe_retseptid("retseptid.json")


toiduained = []

while True:
    toiduaine = input('Sisesta toiduaine: ').strip().lower()
    if toiduaine == '':
        break
    else:
        toiduained.append(toiduaine)

print(f'Sinu toiduained: {toiduained}')



