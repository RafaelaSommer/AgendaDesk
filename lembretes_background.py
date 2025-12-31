import json
import os
from datetime import datetime, timedelta
import tkinter as tk

# ================= CONFIG =================
MINUTOS_ANTES = 5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_TAREFAS = os.path.join(BASE_DIR, "tarefas.json")
ICON_PATH = os.path.join(BASE_DIR, "assets", "logo.ico")

BG = "#252a31"
TEXT = "#ffffff"
ACCENT = "#6264A7"

# ================= ROOT OCULTO =================
root = tk.Tk()
root.withdraw()  # não mostra janela principal

# ================= POPUP =================
def popup_lembrete(titulo, pauta=""):
    popup = tk.Toplevel(root)
    popup.title("AgendaDesk • Lembrete")
    popup.configure(bg=BG)
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
    popup.focus_force()

    tk.Label(
        popup,
        text="⏰ Lembrete de Tarefa",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(20, 10))

    tk.Label(
        popup,
        text=titulo,
        bg=BG,
        fg=TEXT,
        wraplength=380,
        font=("Segoe UI", 11, "bold")
    ).pack(pady=5)

    if pauta:
        tk.Label(
            popup,
            text=pauta,
            bg=BG,
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
    try:
        if not os.path.exists(ARQUIVO_TAREFAS):
            root.after(15000, verificar_lembretes)
            return

        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            tarefas = json.load(f)

        agora = datetime.now()
        alterado = False

        for tarefa in tarefas:
            if tarefa.get("concluida"):
                continue

            if tarefa.get("notificado"):
                continue

            try:
                data_str, hora_str = tarefa["data_hora"].rsplit(" ", 1)
                data_hora = datetime.strptime(
                    f"{data_str} {hora_str}", "%d/%m/%Y %H:%M"
                )
            except:
                continue

            alerta = data_hora - timedelta(minutes=MINUTOS_ANTES)

            # janela de 2 minutos para garantir o disparo
            if alerta <= agora <= alerta + timedelta(minutes=2):
                popup_lembrete(
                    tarefa.get("descricao", "Tarefa"),
                    tarefa.get("pauta", "")
                )
                tarefa["notificado"] = True
                alterado = True

        if alterado:
            with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
                json.dump(tarefas, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("Erro no lembrete:", e)

    # verifica novamente a cada 15 segundos
    root.after(15000, verificar_lembretes)

# ================= START =================
print("AgendaDesk • Lembretes ativos")
verificar_lembretes()
root.mainloop()
