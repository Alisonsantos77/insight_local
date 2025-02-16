import flet as ft
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Formulario
import logging


def ColetadosPage(page: ft.Page):
    def carregar_formularios(pesquisa=None):
        try:
            engine = create_engine('sqlite:///formulario.db')
            Session = sessionmaker(bind=engine)
            session = Session()

            if pesquisa:
                return session.query(Formulario).filter(Formulario.estabelecimento.ilike(f'%{pesquisa}%')).all()
            return session.query(Formulario).all()
        except Exception as ex:
            logging.exception("Erro ao carregar formulários: %s", ex)
            return None

    def criar_card_formulario(form):
        return ft.Card(
            elevation=8,
            content=ft.Container(
                padding=15,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.BUSINESS,
                                            color=ft.colors.BLUE),
                            title=ft.Text(form.estabelecimento,
                                          weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(
                                f"Responsável: {form.responsavel}"),
                        ),
                        ft.Divider(),
                        ft.ExpansionTile(
                            title=ft.Text("Detalhes do Formulário"),
                            controls=[
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Campo")),
                                        ft.DataColumn(ft.Text("Valor")),
                                    ],
                                    rows=[
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Telefone")),
                                                ft.DataCell(
                                                    ft.Text(form.telefone or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Segmento")),
                                                ft.DataCell(
                                                    ft.Text(form.segmento or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Atendimento Online")),
                                                ft.DataCell(
                                                    ft.Text(form.atendimento_online or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Uso de Bots")),
                                                ft.DataCell(
                                                    ft.Text(form.uso_bots or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Automação")),
                                                ft.DataCell(
                                                    ft.Text(form.automacao or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Delivery")),
                                                ft.DataCell(
                                                    ft.Text(form.delivery or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Gerenciamento de Pedidos")),
                                                ft.DataCell(
                                                    ft.Text(form.gerenciamento_pedidos or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Software de Estoque")),
                                                ft.DataCell(
                                                    ft.Text(form.software_estoque or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Dispositivos")),
                                                ft.DataCell(
                                                    ft.Text(form.dispositivos or "N/A")),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                    ft.Text("Dificuldade Digital")),
                                                ft.DataCell(
                                                    ft.Text(form.dificuldade_digital or "N/A")),
                                            ]
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ),
        )

    def criar_view_sucesso(formularios):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[search_field],
                    ),
                    ft.ListView(
                        controls=[criar_card_formulario(
                            form) for form in formularios],
                        expand=True,
                        spacing=10,
                        padding=20,
                    ),
                ],
                expand=True,
            ),
        )

    def pesquisar_formularios(e):
        termo_pesquisa = e.control.value
        formularios = carregar_formularios(pesquisa=termo_pesquisa)
        if formularios is None:
            return criar_view_erro("Erro ao carregar formulários do banco de dados.")
        elif not formularios:
            return criar_view_erro("Nenhum formulário encontrado.")
        else:
            return criar_view_sucesso(formularios)

    search_field = ft.SearchBar(
        on_submit=pesquisar_formularios,
        view_elevation=4,
        divider_color=ft.colors.GREY_500,
        bar_hint_text="Pesquisar formulário",
        controls=[
            ft.Icon(ft.icons.SEARCH, color=ft.colors.GREY_500),
        ]
    )

    search_field.on_change = pesquisar_formularios

    def criar_view_erro(mensagem):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.ERROR_OUTLINE,
                            size=48, color=ft.colors.RED),
                    ft.Text(mensagem, size=20, color=ft.colors.RED),
                    ft.ElevatedButton(
                        "Voltar",
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: page.go("/"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )

    # Carregar formulários
    formularios = carregar_formularios()

    if formularios is None:
        return criar_view_erro("Erro ao carregar formulários do banco de dados.")
    elif not formularios:
        return criar_view_erro("Nenhum formulário encontrado.")
    else:
        return criar_view_sucesso(formularios)
