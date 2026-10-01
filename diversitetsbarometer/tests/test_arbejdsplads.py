"""
Tests til klassen Arbejdsplads. De er skrevet på forhånd — jeres opgave er at
få dem til at sige ok.

    python3 tests/test_arbejdsplads.py

Kør fra roden af repositoriet. Ret ét TODO ad gangen, og kør igen.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.barometer import Arbejdsplads, UgyldigArbejdsplads

fejl = 0


def tjek(paastand, tekst):
    global fejl
    print(("  ok    " if paastand else "  FEJL  ") + tekst)
    fejl += not paastand


def afvises(**kw):
    """Rejser Arbejdsplads en UgyldigArbejdsplads for de her tal?"""
    try:
        Arbejdsplads(**kw)
        return False
    except UgyldigArbejdsplads:
        return True


normal = dict(ansatte=120, antal={"kvinder": 50, "seniorer": 20, "indvandrere": 8},
              branche="Handel", sektor="Privat", region="Hovedstaden")

print("TODO 1 · attributterne")
a = Arbejdsplads(**normal)
tjek(getattr(a, "ansatte", None) == 120, "arbejdspladsen husker antallet af ansatte")
tjek(getattr(a, "branche", None) == "Handel", "arbejdspladsen husker sin branche")
tjek(getattr(a, "antal", {}).get("kvinder") == 50, "arbejdspladsen husker antallet i hver gruppe")

print("\nTODO 2 · for små arbejdspladser afvises")
tjek(afvises(**{**normal, "ansatte": 49}), "49 ansatte afvises")
tjek(not afvises(**{**normal, "ansatte": 50}), "præcis 50 ansatte er med")

print("\nTODO 3 og 4 · tal, der ikke giver mening")
tjek(afvises(**{**normal, "antal": {"kvinder": -1, "seniorer": 20, "indvandrere": 8}}),
     "et negativt antal afvises")
tjek(afvises(**{**normal, "antal": {"kvinder": 200, "seniorer": 20, "indvandrere": 8}}),
     "flere kvinder end ansatte afvises")

print("\nTODO 5 · andelen")
tjek(abs(a.andel("kvinder") - 50 / 120) < 1e-9, "andel('kvinder') er 50 ud af 120")
tjek(abs(a.andel("seniorer") - 20 / 120) < 1e-9, "andel('seniorer') er 20 ud af 120")

print("\nTODO 6 · størrelsesgruppen")
for ansatte, forventet in [(60, "50-99"), (120, "100-249"), (300, "250-499"), (900, "500+")]:
    plads = Arbejdsplads(**{**normal, "ansatte": ansatte})
    tjek(plads.stoerrelsesgruppe == forventet, f"{ansatte} ansatte hører til {forventet}")

print("\nTODO 7 · en linje, et menneske kan læse")
tekst = str(a)
tjek("120" in tekst, "teksten nævner antallet af ansatte")
tjek("Handel" in tekst, "teksten nævner branchen")
tjek(tekst != "en arbejdsplads", "teksten er skrevet om")

print(f"\n{fejl} ting mangler endnu." if fejl else "\nAlt virker. Commit det.")
sys.exit(1 if fejl else 0)
