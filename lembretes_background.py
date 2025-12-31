import json
import os
from datetime import datetime, timedelta
import tkinter as tk

# ================= CONFIG =================
MINUTOS_ANTES = 5
INTERVALO_VERIFICACAO = 15000  # 15 segundos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_TAREFAS = os.path.join(BASE_DIR, "tarefas.json")
ICON_PATH = os.path.join(BASE_DIR, "assets", "logo.ico")

BG = "#252a31"
TEXT = "#ffffff"
ACCENT = "#6264A7"

# ================= ROOT OCULTO =================
root = tk.Tk()
root.withdraw()

# ================= POPUP =================
def popup_lembrete(titulo, pauta=""):
    popup = tk.Toplevel(janela)
    popup.title("AgendaDesk • Lembrete")
    popup.configure(bg=CARD)
    popup.resizable(False, False)

    largura, altura = 420, 260
    x = (popup.winfo_screenwidth() // 2) - (largura // 2)
    y = (popup.winfo_screenheight() // 2) - (altura // 2)
    popup.geometry(f"{largura}x{altura}+{x}+{y}")

    try:
        popup.iconbitmap(ICON_PATH)
    except:
        pass

    popup.attributes("-topmost", True)
    popup.lift()
    popup.focus_force()

    tk.Label(
        popup,
        text="⏰ Lembrete de Tarefa",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(20, 10))

    tk.Label(
        popup,
        text=titulo,
        bg=CARD,
        fg=TEXT,
        wraplength=380,
        font=("Segoe UI", 11, "bold")
    ).pack(pady=5)

    if pauta:
        tk.Label(
            popup,
            text=pauta,
            bg=CARD,
            fg="#d0d0d0",
            wraplength=380,
            justify="left",
            font=("Segoe UI", 10)
        ).pack(pady=10)

    tk.Button(
        popup,
        text="OK",
        bg=ACCENT,
        fg="white",
        width=14,
        command=popup.destroy
    ).pack(pady=20)

# ================= VERIFICAÇÃO =================
def verificar_lembretes():
    agora = datetime.now()
    alterado = False

    for tarefa in tarefas:
        if tarefa.get("concluida"):
            continue

        if tarefa.get("notificado"):
            continue

        try:
            data_hora = datetime.strptime(
                tarefa["data_hora"], "%d/%m/%Y %H:%M"
            )
        except:
            continue

        alerta = data_hora - timedelta(minutes=MINUTOS_ANTES)

        if alerta <= agora <= data_hora:
            popup_lembrete(
                tarefa.get("descricao", "Tarefa"),
                tarefa.get("pauta", "")
            )
            tarefa["notificado"] = True
            alterado = True

    if alterado:
        salvar_tarefas()

    janela.after(15000, verificar_lembretes)

# ================= START =================
print("AgendaDesk • Lembretes ativos")
verificar_lembretes()
root.mainloop()
