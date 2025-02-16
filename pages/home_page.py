import flet as ft
from dotenv import load_dotenv
import os
load_dotenv()

ANIMATION_URL = os.getenv("ANIMATION_URL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def HomePage(page: ft.Page):
    page.title = "Home"

    def verificar_senha(e, dialog):
        senha_digitada = campo_senha.value
        # Senha padrão caso não esteja no .env
        senha_correta = os.getenv("ADMIN_PASSWORD")

        if senha_digitada == senha_correta:
            dialog.open = False
            page.go("/pesquisador")
            page.update()
        else:
            campo_senha.error_text = "Senha incorreta"
            page.update()

    def handle_close(e):
        page.close(dialog_senha)
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    campo_senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True
    )

    dialog_senha = ft.AlertDialog(
        modal=True,
        title=ft.Text("Área Restrita"),
        content=ft.Column([
            ft.Text("Digite a senha de acesso:"),
            campo_senha
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=handle_close),
            ft.TextButton(
                "Entrar", on_click=lambda e: verificar_senha(e, dialog_senha))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    return ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text(value="Bem-vindo ao Insight Local.",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                # imagem ilustrativa
                ft.Lottie(
                    src=os.getenv("ANIMATION_URL"),
                    reverse=False,
                    animate=True,
                    repeat=True,
                    background_loading=True,
                    filter_quality=ft.FilterQuality.HIGH,
                    fit=ft.ImageFit.CONTAIN,
                    width=300,
                    height=300
                ),
                ft.ElevatedButton(
                    text="Iniciar pesquisa",
                    style=ft.ButtonStyle(
                         padding=ft.padding.all(10),
                         bgcolor={
                             ft.ControlState.HOVERED: ft.colors.BLUE_400,
                             ft.ControlState.FOCUSED: ft.colors.BLUE,
                             ft.ControlState.DEFAULT: ft.colors.BLUE_800,
                         },
                        color={
                             ft.ControlState.DEFAULT: ft.colors.WHITE,
                             ft.ControlState.HOVERED: ft.colors.WHITE,
                         },
                        elevation={"pressed": 0, "": 1},
                        animation_duration=500,
                        shape=ft.RoundedRectangleBorder(radius=6),
                    ),
                    width=200,
                    on_click=lambda _: page.go("/formulario"),
                ),
                ft.ElevatedButton(
                    text="Área do pesquisador",
                    style=ft.ButtonStyle(
                         color={
                             ft.ControlState.HOVERED: ft.colors.BLUE_400,
                             ft.ControlState.FOCUSED: ft.colors.BLUE,
                             ft.ControlState.DEFAULT: ft.colors.BLUE_800,
                         },
                        bgcolor={
                             ft.ControlState.FOCUSED: ft.colors.TRANSPARENT, "": ft.colors.BACKGROUND},
                        overlay_color=ft.colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 1},
                        animation_duration=500,
                        side={
                             ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                             ft.ControlState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                         },
                        shape=ft.RoundedRectangleBorder(radius=6),
                    ),
                    width=200,
                    on_click=lambda e: page.open(dialog_senha),
                )
            ]
        )
    )
