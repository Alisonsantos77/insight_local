import logging
import flet as ft
from models.database import SessionLocal, Formulario


def FormularioPage(page: ft.Page):
    logging.info("Inicializando Formulário de Pesquisa")

    # ----- Função para atualizar a pré-visualização e também o estado do botão -----
    def update_preview():
        preview_lines = []

        # Seção Identificação
        preview_lines.append("=== Identificação do Estabelecimento ===")
        preview_lines.append(
            f"Estabelecimento: {campo_estabelecimento.value or '[vazio]'}")
        preview_lines.append(
            f"Responsável: {campo_responsavel.value or '[vazio]'}")
        preview_lines.append(f"Telefone: {campo_telefone.value or '[vazio]'}")
        segmento_val = dropdown_segmento.value or "[vazio]"
        if dropdown_segmento.value == "Outro":
            segmento_val += f" - {campo_segmento_outro.value or '[vazio]'}"
        preview_lines.append(f"Segmento: {segmento_val}")
        preview_lines.append("")

        # Seção Atendimento Online e Bots
        preview_lines.append("=== Atendimento Online e Bots ===")
        atendimento_val = campo_atendimento_online.value or "[vazio]"
        if campo_atendimento_online.value == "Outro":
            atendimento_val += f" - {campo_atendimento_online_outro.value or '[vazio]'}"
        preview_lines.append(f"Atendimento Online: {atendimento_val}")
        uso_bots_str = campo_uso_bots.value or "[vazio]"
        if campo_uso_bots.value == "sim":
            uso_bots_str += f" - {campo_experiencia_bots.value or '[sem descrição]'}"
        elif campo_uso_bots.value == "nao":
            uso_bots_str += f" - {campo_interesse_bots.value or '[sem interesse]'}"
        preview_lines.append(f"Uso de Bots: {uso_bots_str}")
        preview_lines.append("")

        # Seção Automação
        preview_lines.append("=== Tarefas para Automatizar ===")
        tarefas = []
        if chk_estoque.value:
            tarefas.append("Controle de estoque")
        if chk_pedidos.value:
            tarefas.append("Processamento de pedidos")
        if chk_envio.value:
            tarefas.append("Envio de mensagens automáticas")
        if chk_automacao_outro.value:
            tarefas.append(
                f"Outro: {campo_automacao_outro.value or '[vazio]'}")
        preview_lines.append(f"Tarefas: {', '.join(tarefas) or '[nenhuma]'}")
        preview_lines.append("")

        # Seção Delivery
        preview_lines.append("=== Delivery e Gerenciamento de Pedidos ===")
        preview_lines.append(f"Delivery: {campo_delivery.value or '[vazio]'}")
        if campo_delivery.value == "sim":
            gerenc = campo_gerenciamento_pedidos.value or "[vazio]"
            if campo_gerenciamento_pedidos.value == "software":
                gerenc += f" - {campo_gerenciamento_software.value or '[vazio]'}"
            preview_lines.append(f"Gerenciamento de Pedidos: {gerenc}")
        preview_lines.append("")

        # Seção Estoque e Equipamentos
        preview_lines.append("=== Gestão de Estoque e Equipamentos ===")
        software_val = campo_software_estoque.value or "[vazio]"
        if campo_software_estoque.value == "sim":
            software_val += f" - {campo_software_estoque_descricao.value or '[vazio]'}"
        preview_lines.append(f"Software de Estoque: {software_val}")
        dispositivos_sel = []
        if chk_computadores.value:
            dispositivos_sel.append("Computadores")
        if chk_celulares.value:
            dispositivos_sel.append("Celulares")
        if chk_tablets.value:
            dispositivos_sel.append("Tablets")
        preview_lines.append(
            f"Dispositivos: {', '.join(dispositivos_sel) or '[nenhum]'}")
        preview_lines.append("")

        # Seção Desafios Digitais
        preview_lines.append("=== Desafios Digitais ===")
        preview_lines.append(
            f"Dificuldade Digital: {campo_dificuldade_digital.value or '[vazio]'}")

        preview_text.value = "\n".join(preview_lines)
        preview_text.update()
        update_submit_button()

    def numChange(e):
        """Formata o telefone para o padrão (XX) XXXXX-XXXX, permitindo apenas números."""
        logging.debug("numChange chamado com valor: %s", e.control.value)
        num = ''.join(filter(str.isdigit, e.control.value))
        if len(num) > 11:
            num = num[:11]
        if len(num) <= 2:
            formatted = f"({num}"
        elif len(num) <= 6:
            formatted = f"({num[:2]}) {num[2:]}"
        else:
            formatted = f"({num[:2]}) {num[2:7]}"
            if len(num) > 7:
                formatted += f"-{num[7:]}"
        e.control.value = formatted
        e.control.update()
        logging.debug("numChange atualizou valor para: %s", formatted)
        update_preview()

    def criar_secao_titulo(titulo: str):
        return ft.Container(
            content=ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(top=20, bottom=10)
        )

    # --------------------
    # Sessão 1: Identificação
    # --------------------
    campo_estabelecimento = ft.TextField(
        label="Nome oficial do estabelecimento",
        hint_text="Ex: Padaria Central",
        on_change=lambda e: update_preview()
    )
    campo_responsavel = ft.TextField(
        label="Nome do responsável",
        hint_text="Ex: João da Silva",
        on_change=lambda e: update_preview()
    )
    campo_telefone = ft.TextField(
        label="Telefone para contato",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="(DDD) XXXXX-XXXX",
        on_change=numChange
    )
    dropdown_segmento = ft.Dropdown(
        label="Segmento principal",
        options=[ft.dropdown.Option(s) for s in [
            "Alimentação", "Varejo", "Serviços", "Manufatura", "Outro"
        ]],
        on_change=lambda e: handle_segmento_change(e)
    )
    # Campo extra para "Outro" no dropdown
    campo_segmento_outro = ft.TextField(
        label="Especifique o segmento",
        visible=False,
        on_change=lambda e: update_preview()
    )
    segmento_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )

    def handle_segmento_change(e):
        if e.control.value == "Outro":
            campo_segmento_outro.visible = True
            segmento_switcher.content = campo_segmento_outro
        else:
            campo_segmento_outro.visible = False
            segmento_switcher.content = ft.Container(visible=True)
        segmento_switcher.update()
        update_preview()

    # --------------------
    # Sessão 2: Atendimento Online e Automação
    # --------------------
    def handle_atendimento_online_change(e):
        if e.control.value == "Outro":
            campo_atendimento_online_outro.visible = True
            atendimento_online_switcher.content = campo_atendimento_online_outro
        else:
            campo_atendimento_online_outro.visible = False
            atendimento_online_switcher.content = ft.Container(visible=True)
        atendimento_online_switcher.update()
        update_preview()

    campo_atendimento_online_outro = ft.TextField(
        label="Especifique o tipo de atendimento online",
        visible=False,
        on_change=lambda e: update_preview()
    )
    campo_atendimento_online = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Como você atende seus clientes online?"),
            ft.Radio(value="WhatsApp", label="WhatsApp"),
            ft.Radio(value="Redes Sociais", label="Redes Sociais"),
            ft.Radio(value="Site", label="Site"),
            ft.Radio(value="Outro", label="Outro"),
        ]),
        on_change=handle_atendimento_online_change
    )
    atendimento_online_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )

    # Uso de bots com interação dinâmica
    def on_bots_change(e):
        if campo_uso_bots.value == "sim":
            campo_experiencia_bots.visible = True
            campo_interesse_bots.visible = False
        else:
            campo_experiencia_bots.visible = False
            campo_interesse_bots.visible = True
        experiencia_switcher.content = campo_experiencia_bots if campo_experiencia_bots.visible else ft.Container(
            visible=True)
        interesse_switcher.content = campo_interesse_bots if campo_interesse_bots.visible else ft.Container(
            visible=True)
        experiencia_switcher.update()
        interesse_switcher.update()
        update_preview()

    campo_uso_bots = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Você já utiliza ou já utilizou bots para atendimento online?"),
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não"),
        ]),
        on_change=on_bots_change
    )
    campo_experiencia_bots = ft.TextField(
        label="Descreva sua experiência com bots",
        visible=False,
        on_change=lambda e: update_preview()
    )
    campo_interesse_bots = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Você tem interesse em usar bots para atendimento?"),
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não"),
        ]),
        visible=False,
        on_change=lambda e: update_preview()
    )
    experiencia_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )
    interesse_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )

    # Tarefas para automatizar (Checkboxes com opção "Outro")
    chk_estoque = ft.Checkbox(
        label="Controle de estoque", on_change=lambda e: update_preview())
    chk_pedidos = ft.Checkbox(
        label="Processamento de pedidos", on_change=lambda e: update_preview())
    chk_envio = ft.Checkbox(
        label="Envio de mensagens automáticas", on_change=lambda e: update_preview())

    def on_automacao_outro_change(e):
        campo_automacao_outro.visible = chk_automacao_outro.value
        campo_automacao_outro.update()
        update_preview()

    chk_automacao_outro = ft.Checkbox(
        label="Outro",
        on_change=on_automacao_outro_change
    )
    campo_automacao_outro = ft.TextField(
        label="Especifique outra tarefa",
        visible=False,
        on_change=lambda e: update_preview()
    )

    # --------------------
    # Sessão 3: Delivery e Gerenciamento de Pedidos
    # --------------------
    def on_delivery_change(e):
        campo_gerenciamento_pedidos.visible = (campo_delivery.value == "sim")
        delivery_switcher.content = campo_gerenciamento_pedidos if campo_gerenciamento_pedidos.visible else ft.Container(
            visible=True)
        delivery_switcher.update()
        update_preview()

    delivery_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )

    campo_delivery = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Sua empresa possui serviço de delivery?"),
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não"),
        ]),
        on_change=on_delivery_change
    )
    # Campo para Gerenciamento de Pedidos

    def handle_gerenciamento_pedidos_change(e):
        if e.control.value == "software":
            gerenciamento_software_switcher.content = campo_gerenciamento_software
        else:
            gerenciamento_software_switcher.content = ft.Container()  # Apenas um container vazio

        gerenciamento_software_switcher.update()
        update_preview()

    campo_gerenciamento_pedidos = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Como você gerencia os pedidos e entregas?"),
            ft.Radio(value="software", label="Software"),
            ft.Radio(value="planilha", label="Planilha"),
            ft.Radio(value="manual", label="Manualmente"),
        ]),
        on_change=handle_gerenciamento_pedidos_change
    )
    campo_gerenciamento_software = ft.TextField(
        label="Especifique o software de gerenciamento",
        visible=False,
        on_change=lambda e: update_preview()
    )
    gerenciamento_software_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )

    # --------------------
    # Sessão 4: Gestão de Estoque e Equipamentos
    # --------------------
    def on_software_estoque_change(e):
        campo_software_estoque_descricao.visible = (
            campo_software_estoque.value == "sim")
        software_switcher.content = campo_software_estoque_descricao if campo_software_estoque_descricao.visible else ft.Container(
            visible=True)
        software_switcher.update()
        update_preview()

    campo_software_estoque = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Utiliza software para gerenciar o estoque?"),
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não"),
        ]),
        on_change=on_software_estoque_change
    )
    campo_software_estoque_descricao = ft.TextField(
        label="Qual software?",
        visible=False,
        on_change=lambda e: update_preview()
    )
    software_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container(visible=True)
    )
    # Dispositivos disponíveis (Checkboxes)
    chk_computadores = ft.Checkbox(
        label="Computadores", on_change=lambda e: update_preview())
    chk_celulares = ft.Checkbox(
        label="Celulares", on_change=lambda e: update_preview())
    chk_tablets = ft.Checkbox(
        label="Tablets", on_change=lambda e: update_preview())

    # --------------------
    # Sessão 5: Desafios Digitais
    # --------------------
    campo_dificuldade_digital = ft.TextField(
        label="Descreva aqui",
        on_change=lambda e: update_preview()
    )

    # ----- Área de Pré-visualização das Respostas -----
    preview_text = ft.Text(
        value="Respostas serão exibidas aqui...", size=12, font_family="monospace")
    preview_container = ft.Container(
        content=preview_text,
        padding=10,
        border_radius=8,
        border=ft.border.all(1, ft.Colors.OUTLINE)
    )

    # ----- Feedback de validação -----
    error_text = ft.Text(
        value="", color=ft.Colors.RED, visible=False
    )

    # ----- Botão de Envio (inicialmente desabilitado) -----
    submit_button = ft.ElevatedButton(
        text="Enviar Formulário",
        icon=ft.icons.SEND,
        on_click=lambda e: validar_formulario(e),
        style=ft.ButtonStyle(
            padding=ft.padding.all(10),
            bgcolor={
                ft.ControlState.HOVERED: ft.colors.GREEN_100,
                ft.ControlState.FOCUSED: ft.colors.GREEN_100,
                ft.ControlState.DEFAULT: ft.colors.GREEN,
            },
            color={
                ft.ControlState.DEFAULT: ft.colors.WHITE,
                ft.ControlState.HOVERED: ft.colors.WHITE,
            },
            elevation={"pressed": 0, "": 1},
            animation_duration=500,
            shape=ft.RoundedRectangleBorder(radius=6),
        ),
        disabled=True,
        width=200,
    )

    def check_validations():
        errors = []
        if not campo_estabelecimento.value.strip():
            errors.append("Preencha o nome do estabelecimento.")
        if not campo_responsavel.value.strip():
            errors.append("Preencha o nome do responsável.")
        if not dropdown_segmento.value:
            errors.append("Selecione o segmento principal.")
        if dropdown_segmento.value == "Outro" and not campo_segmento_outro.value.strip():
            errors.append("Especifique o segmento.")
        if not campo_atendimento_online.value:
            errors.append("Responda como atende os clientes online.")
        if campo_atendimento_online.value == "Outro" and not campo_atendimento_online_outro.value.strip():
            errors.append("Especifique o atendimento online.")
        if not campo_delivery.value:
            errors.append("Responda se possui serviço de delivery.")
        if campo_delivery.value == "sim":
            if not campo_gerenciamento_pedidos.value:
                errors.append("Responda como gerencia os pedidos e entregas.")
            if campo_gerenciamento_pedidos.value == "software" and not campo_gerenciamento_software.value.strip():
                errors.append(
                    "Especifique o software de gerenciamento dos pedidos.")
        if not campo_software_estoque.value:
            errors.append(
                "Responda se utiliza software para gerenciar o estoque.")
        if campo_software_estoque.value == "sim" and not campo_software_estoque_descricao.value.strip():
            errors.append("Especifique o software de estoque utilizado.")
        return errors

    def update_submit_button():
        errors = check_validations()
        if errors:
            submit_button.disabled = True
            error_text.value = "\n".join(errors)
            error_text.visible = True
        else:
            submit_button.disabled = False
            error_text.visible = False
            # Exemplo de animação: altera o estilo do botão para verde
            submit_button.style = ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                padding=20,
                elevation={"pressed": 0, "": 3}
            )
        submit_button.update()
        error_text.update()

    def validar_formulario(e):
        logging.info("Iniciando validação e gravação dos dados.")
        errors = check_validations()
        if errors:
            logging.error("Validação falhou: %s", errors)
            snackbar = ft.SnackBar(
                content=ft.Text("\n".join(errors)),
                bgcolor=ft.Colors.ERROR,
                action="OK",
            )
            snackbar.on_action = lambda e: None
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
            return

        estabelecimento = campo_estabelecimento.value.strip(
        ) if campo_estabelecimento.value else ""
        responsavel = campo_responsavel.value.strip() if campo_responsavel.value else ""
        telefone = campo_telefone.value.strip() if campo_telefone.value else None
        segmento = dropdown_segmento.value or ""
        if dropdown_segmento.value == "Outro" and campo_segmento_outro.value:
            segmento += f" - {campo_segmento_outro.value.strip()}"
        atendimento_online = campo_atendimento_online.value.strip(
        ) if campo_atendimento_online.value else ""
        if campo_atendimento_online.value == "Outro" and campo_atendimento_online_outro.value:
            atendimento_online += f" - {campo_atendimento_online_outro.value.strip()}"
        uso_bots = campo_uso_bots.value or ""
        if campo_uso_bots.value == "sim" and campo_experiencia_bots.value:
            uso_bots += f" - {campo_experiencia_bots.value.strip()}"
        elif campo_uso_bots.value == "nao" and campo_interesse_bots.value:
            uso_bots += f" - {campo_interesse_bots.value.strip()}"

        tarefas = []
        if chk_estoque.value:
            tarefas.append("Controle de estoque")
        if chk_pedidos.value:
            tarefas.append("Processamento de pedidos")
        if chk_envio.value:
            tarefas.append("Envio de mensagens automáticas")
        if chk_automacao_outro.value and campo_automacao_outro.value:
            tarefas.append(f"Outro: {campo_automacao_outro.value.strip()}")
        automacao = ", ".join(tarefas)

        delivery = campo_delivery.value or ""
        gerenciamento_pedidos = campo_gerenciamento_pedidos.value.strip() if (
            campo_delivery.value == "sim" and campo_gerenciamento_pedidos.value) else ""
        software_estoque = campo_software_estoque.value or ""
        if campo_software_estoque.value == "sim" and campo_software_estoque_descricao.value:
            software_estoque += f" - {campo_software_estoque_descricao.value.strip()}"
        dispositivos_sel = []
        if chk_computadores.value:
            dispositivos_sel.append("Computadores")
        if chk_celulares.value:
            dispositivos_sel.append("Celulares")
        if chk_tablets.value:
            dispositivos_sel.append("Tablets")
        dispositivos = ", ".join(dispositivos_sel)
        dificuldade_digital = campo_dificuldade_digital.value.strip(
        ) if campo_dificuldade_digital.value else ""

        try:
            with SessionLocal() as session:
                novo_formulario = Formulario(
                    estabelecimento=estabelecimento,
                    responsavel=responsavel,
                    telefone=telefone,
                    segmento=segmento,
                    atendimento_online=atendimento_online,
                    uso_bots=uso_bots,
                    automacao=automacao,
                    delivery=delivery,
                    gerenciamento_pedidos=gerenciamento_pedidos,
                    software_estoque=software_estoque,
                    dispositivos=dispositivos,
                    dificuldade_digital=dificuldade_digital
                )
                session.add(novo_formulario)
                session.commit()
                session.refresh(novo_formulario)
                logging.info("Formulário salvo com sucesso: ID %s",
                             novo_formulario.id)
                snackbar = ft.SnackBar(
                    content=ft.Text("Formulário enviado com sucesso!"),
                    bgcolor=ft.Colors.GREEN,
                    action="OK",
                )
                snackbar.on_action = lambda e: None
                page.overlay.append(snackbar)
                snackbar.open = True
                page.update()
        except Exception as ex:
            logging.exception("Erro ao salvar o formulário: %s", ex)
            snackbar = ft.SnackBar(
                content=ft.Text("Erro ao enviar formulário. Tente novamente."),
                bgcolor=ft.Colors.ERROR,
                action="OK",
            )
            snackbar.on_action = lambda e: None
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

    # Montagem final da interface com Dividers entre sessões
    return ft.Container(
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Text("Formulário de Pesquisa",
                                    size=20, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    padding=20
                ),
                criar_secao_titulo("Identificação do Estabelecimento"),
                campo_estabelecimento,
                campo_responsavel,
                campo_telefone,
                dropdown_segmento,
                segmento_switcher,
                ft.Divider(),
                criar_secao_titulo("Atendimento Online e Automação"),
                campo_atendimento_online,
                atendimento_online_switcher,
                campo_uso_bots,
                experiencia_switcher,
                interesse_switcher,
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Quais tarefas repetitivas você gostaria de automatizar?"),
                        chk_estoque,
                        chk_pedidos,
                        chk_envio,
                        chk_automacao_outro,
                        campo_automacao_outro,
                    ])
                ),
                ft.Divider(),
                criar_secao_titulo("Delivery e Gerenciamento de Pedidos"),
                delivery_switcher,
                campo_delivery,
                campo_gerenciamento_pedidos,
                gerenciamento_software_switcher,
                ft.Divider(),
                criar_secao_titulo("Gestão de Estoque e Equipamentos"),
                campo_software_estoque,
                software_switcher,
                ft.Container(
                    content=ft.Column([
                        ft.Text("Dispositivos utilizados nas operações:"),
                        chk_computadores,
                        chk_celulares,
                        chk_tablets,
                    ])
                ),
                ft.Divider(),
                criar_secao_titulo("Desafios Digitais"),
                ft.Text(
                    "Qual a maior dificuldade ao gerenciar a parte digital do seu negócio?", size=12),
                campo_dificuldade_digital,
                ft.Divider(),
                criar_secao_titulo("Pré-visualização das Respostas"),
                preview_container,
                error_text,
                ft.Row([
                    submit_button,
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]
        ),
        padding=ft.padding.all(20),
        expand=True
    )
