"""
Diversitetsbarometer appen.

Kør den lokalt:
    shiny run --reload app/app.py

Appen regner ikke selv noget ud. Den læser felterne, laver en Arbejdsplads, og
beder barometeret om et svar. Al logikken ligger i barometer/.
"""

from shiny import App, reactive, render, ui

from barometer import Arbejdsplads, Referencetal, UgyldigArbejdsplads, vurder

referencetal = Referencetal()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("branche", "Branche", referencetal.muligheder("branche")),
        ui.input_radio_buttons("sektor", "Sektor", ["Offentlig", "Privat"], inline=True),
        ui.input_select("region", "Region", referencetal.muligheder("region")),
        ui.input_numeric("ansatte", "Antal ansatte", 120, min=0),
        ui.input_numeric("kvinder", "Heraf kvinder", 84, min=0),
        ui.input_numeric("seniorer", "Heraf 55 år eller derover", 26, min=0),
        ui.input_numeric("indvandrere", "Heraf med indvandrerbaggrund", 9, min=0),
        width=330,
    ),
    ui.div("Tallene er syntetiske. Barometeret siger endnu intet om virkelige arbejdspladser.",
           class_="alert alert-secondary"),
    ui.output_ui("svar"),
    title="Diversitetsbarometeret",
)


def server(input, output, session):

    @reactive.calc
    def arbejdsplads():
        return Arbejdsplads(
            ansatte=int(input.ansatte() or 0),
            antal={"kvinder": int(input.kvinder() or 0),
                   "seniorer": int(input.seniorer() or 0),
                   "indvandrere": int(input.indvandrere() or 0)},
            branche=input.branche(),
            sektor=input.sektor(),
            region=input.region(),
        )

    @render.ui
    def svar():
        try:
            linjer = vurder(arbejdsplads(), referencetal)
        except UgyldigArbejdsplads as fejl:
            return ui.div(str(fejl), class_="alert alert-warning")
        return ui.div(*[ui.p(linje) for linje in linjer])


app = App(app_ui, server)
