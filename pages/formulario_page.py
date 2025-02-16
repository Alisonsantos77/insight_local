import logging
import flet as ft
from utils.database import SessionLocal, Formulario


def FormularioPage(page: ft.Page):
    logging.info("Inicializando Formulário de Pesquisa")

    # ----- Função para atualizar o indicador de progresso e estado do botão -----
    def update_progress_and_button():
        # Campos obrigatórios: estabelecimento, responsável, segmento
        total = 3
        filled = sum([
            1 if campo_estabelecimento.value and campo_estabelecimento.value.strip() else 0,
            1 if campo_responsavel.value and campo_responsavel.value.strip() else 0,
            1 if dropdown_segmento.value and dropdown_segmento.value.strip() else 0,
        ])
        progress_bar.value = filled / total
        submit_button.disabled = (filled < total)
        progress_bar.update()
        submit_button.update()

    # ----- Função para atualizar a pré-visualização e também progresso/botão -----
    def update_preview():
        preview_lines = []
        preview_lines.append(
            f"Estabelecimento: {campo_estabelecimento.value or '[vazio]'}")
        preview_lines.append(
            f"Responsável: {campo_responsavel.value or '[vazio]'}")
        preview_lines.append(f"Telefone: {campo_telefone.value or '[vazio]'}")
        preview_lines.append(
            f"Segmento: {dropdown_segmento.value or '[vazio]'}")
        preview_lines.append(
            f"Atendimento Online: {campo_atendimento_online.value or '[vazio]'}")
        # Uso de bots com detalhamento dinâmico
        uso_bots_str = campo_uso_bots.value or "[vazio]"
        if campo_uso_bots.value == "sim":
            uso_bots_str += f" - {campo_experiencia_bots.value or '[sem descrição]'}"
        elif campo_uso_bots.value == "nao":
            uso_bots_str += f" - {campo_interesse_bots.value or '[sem interesse]'}"
        preview_lines.append(f"Uso de Bots: {uso_bots_str}")
        # Tarefas para automatizar
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
        preview_lines.append(
            f"Tarefas para automatizar: {', '.join(tarefas) or '[nenhuma]'}")
        # Delivery e gerenciamento
        preview_lines.append(f"Delivery: {campo_delivery.value or '[vazio]'}")
        if campo_delivery.value == "sim":
            preview_lines.append(
                f"Gerenciamento de Pedidos: {campo_gerenciamento_pedidos.value or '[vazio]'}")
        # Software de estoque
        software_val = campo_software_estoque.value or "[vazio]"
        if campo_software_estoque.value == "sim":
            software_val += f" - {campo_software_estoque_descricao.value or '[vazio]'}"
        preview_lines.append(f"Software de Estoque: {software_val}")
        # Dispositivos
        dispositivos_sel = []
        if chk_computadores.value:
            dispositivos_sel.append("Computadores")
        if chk_celulares.value:
            dispositivos_sel.append("Celulares")
        if chk_tablets.value:
            dispositivos_sel.append("Tablets")
        preview_lines.append(
            f"Dispositivos: {', '.join(dispositivos_sel) or '[nenhum]'}")
        preview_lines.append(
            f"Dificuldade Digital: {campo_dificuldade_digital.value or '[vazio]'}")
        preview_text.value = "\n".join(preview_lines)
        preview_text.update()
        update_progress_and_button()

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

    # =============================
    # Sessão 1: Identificação
    # =============================
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
            "Alimentação", "Varejo", "Serviços", "Manufatura", "Outro"]],
        on_change=lambda e: update_preview()
    )

    # =============================
    # Sessão 2: Atendimento Online e Automação
    # =============================
    campo_atendimento_online = ft.TextField(
        label="Como você atende seus clientes online?",
        hint_text="Ex: WhatsApp, Redes Sociais, Site",
        on_change=lambda e: update_preview()
    )
    # Uso de bots com interação dinâmica

    def on_bots_change(e):
        if campo_uso_bots.value == "sim":
            campo_experiencia_bots.visible = True
            campo_interesse_bots.visible = False
        else:
            campo_experiencia_bots.visible = False
            campo_interesse_bots.visible = True
        # Utilize AnimatedSwitcher para uma transição suave
        experiencia_switcher.content = campo_experiencia_bots if campo_experiencia_bots.visible else ft.Container()
        interesse_switcher.content = campo_interesse_bots if campo_interesse_bots.visible else ft.Container()
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
    campo_interesse_bots = ft.TextField(
        label="Você tem interesse em usar bots para atendimento?",
        visible=False,
        on_change=lambda e: update_preview()
    )
    # AnimatedSwitcher para os campos dinâmicos de bots
    experiencia_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container())
    interesse_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container())

    # Tarefas repetitivas a automatizar (Checkboxes com opção "Outro")
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

    # =============================
    # Sessão 3: Delivery e Gerenciamento de Pedidos
    # =============================
    def on_delivery_change(e):
        campo_gerenciamento_pedidos.visible = (campo_delivery.value == "sim")
        # Utilize AnimatedSwitcher para exibir com transição
        delivery_switcher.content = campo_gerenciamento_pedidos if campo_gerenciamento_pedidos.visible else ft.Container()
        delivery_switcher.update()
        update_preview()
    campo_delivery = ft.RadioGroup(
        content=ft.Column([
            ft.Text("Sua empresa possui serviço de delivery?"),
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não"),
        ]),
        on_change=on_delivery_change
    )
    campo_gerenciamento_pedidos = ft.TextField(
        label="Como você gerencia os pedidos e entregas?",
        hint_text="Ex: Software, Planilha, Manualmente",
        visible=False,
        on_change=lambda e: update_preview()
    )
    delivery_switcher = ft.AnimatedSwitcher(
        duration=300, content=ft.Container())

    # =============================
    # Sessão 4: Gestão de Estoque e Equipamentos
    # =============================
    def on_software_estoque_change(e):
        campo_software_estoque_descricao.visible = (
            campo_software_estoque.value == "sim")
        software_switcher.content = campo_software_estoque_descricao if campo_software_estoque_descricao.visible else ft.Container()
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
        duration=300, content=ft.Container())
    # Dispositivos disponíveis (Checkboxes)
    chk_computadores = ft.Checkbox(
        label="Computadores", on_change=lambda e: update_preview())
    chk_celulares = ft.Checkbox(
        label="Celulares", on_change=lambda e: update_preview())
    chk_tablets = ft.Checkbox(
        label="Tablets", on_change=lambda e: update_preview())

    # =============================
    # Sessão 5: Desafios Digitais
    # =============================
    campo_dificuldade_digital = ft.TextField(
        label="Qual a maior dificuldade ao gerenciar a parte digital do seu negócio?",
        on_change=lambda e: update_preview()
    )

    # ----- Indicador de Progresso -----
    progress_bar = ft.ProgressBar(value=0, width=300)

    # ----- Área de Pré-visualização das Respostas -----
    preview_text = ft.Text(value="Respostas serão exibidas aqui...", size=12)
    preview_container = ft.Container(
        content=preview_text,
        padding=10,
        border_radius=8,
    )

    # ----- Botão de Envio (inicialmente desabilitado) -----
    submit_button = ft.ElevatedButton(
        text="Enviar Formulário",
        icon=ft.icons.SEND,
        on_click=lambda e: validar_formulario(e),
        style=ft.ButtonStyle(
            padding=20,
            elevation={"pressed": 0, "": 3}
        ),
        disabled=True  # Desabilitado até preencher os campos obrigatórios
    )

    def validar_formulario(e):
        """Extrai, valida e persiste os dados do formulário usando SQLAlchemy."""
        logging.info("Iniciando validação e gravação dos dados.")

        estabelecimento = campo_estabelecimento.value.strip(
        ) if campo_estabelecimento.value else ""
        responsavel = campo_responsavel.value.strip() if campo_responsavel.value else ""
        telefone = campo_telefone.value.strip() if campo_telefone.value else None
        segmento = dropdown_segmento.value or ""
        atendimento_online = campo_atendimento_online.value.strip(
        ) if campo_atendimento_online.value else ""
        uso_bots = campo_uso_bots.value or ""
        if campo_uso_bots.value == "sim":
            uso_bots += f" - {campo_experiencia_bots.value.strip()}" if campo_experiencia_bots.value else ""
        elif campo_uso_bots.value == "nao":
            uso_bots += f" - {campo_interesse_bots.value.strip()}" if campo_interesse_bots.value else ""
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
        if campo_software_estoque.value == "sim":
            software_estoque += f" - {campo_software_estoque_descricao.value.strip()}" if campo_software_estoque_descricao.value else ""
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

        if not all([estabelecimento, responsavel, segmento]):
            logging.error(
                "Validação falhou: campos obrigatórios não preenchidos.")
            snackbar = ft.SnackBar(
                content=ft.Text("Preencha todos os campos obrigatórios."),
                bgcolor=ft.Colors.ERROR,
                action="OK",
            )
            snackbar.on_action = lambda e: None
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
            return

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

    # Montagem final da interface
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
                progress_bar,
                criar_secao_titulo("Identificação do Estabelecimento"),
                campo_estabelecimento,
                campo_responsavel,
                campo_telefone,
                dropdown_segmento,
                criar_secao_titulo("Atendimento Online e Automação"),
                campo_atendimento_online,
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
                criar_secao_titulo("Delivery e Gerenciamento de Pedidos"),
                campo_delivery,
                delivery_switcher,
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
                criar_secao_titulo("Desafios Digitais"),
                campo_dificuldade_digital,
                criar_secao_titulo("Pré-visualização das Respostas"),
                preview_container,
                submit_button,
            ]
        ),
        padding=ft.padding.all(20),
        expand=True
    )
