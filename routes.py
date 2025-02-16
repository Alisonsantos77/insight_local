import logging
import flet as ft
from pages.home_page import HomePage
from pages.formulario_page import FormularioPage
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
                    controls=[
                        ft.Text("Pesquisador"),
                        ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            )

        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            logging.info(f"Retornando para a rota anterior: {top_view.route}")
            page.go(top_view.route)
        else:
            logging.info("Sem mais views no histórico, retornando à home.")
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    if not page.route:
        logging.info("Nenhuma rota especificada, redirecionando para a home")
        page.go("/")
    else:
        route_change(page.route)
