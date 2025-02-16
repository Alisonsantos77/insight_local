import logging
import flet as ft
from pages.home_page import HomePage
from pages.formulario_page import FormularioPage
from pages.coletados import ColetadosPage
import logging

# Configurando o logging nativo
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("flet_core").setLevel(logging.INFO)


def setup_routes(page: ft.Page):
    logging.info("Configurando rotas")

    def route_change(route):
        logging.info(f"Rota alterada para: {route}")
        page.views.clear()

        page.title = "Insight local"
        page.views.append(
            ft.View(
                route="/",
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    HomePage(page),
                ],
            )
        )

        if page.route == "/formulario":
            page.title = "formulario - Insight local"
            page.views.append(
                ft.View(
                    route="/formulario",
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    appbar=ft.AppBar(
                        title=ft.Text("formulario - Insight local"),
                        bgcolor=ft.colors.SURFACE,
                    ),
                    controls=[
                        FormularioPage(page),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        elif page.route == "/pesquisador":
            page.title = "Pesquisador - Insight local"
            page.views.append(
                ft.View(
                    route="/pesquisador",
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    appbar=ft.AppBar(
                        title=ft.Text("Pesquisador - Insight local"),
                        bgcolor=ft.colors.SURFACE,
                    ),
                    controls=[
                        ColetadosPage(page),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        logging.info(f"Retornando para a rota anterior: {top_view.route}")
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
