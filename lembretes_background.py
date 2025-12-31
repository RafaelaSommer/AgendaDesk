import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import json
import os

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_TAREFAS = os.path.join(BASE_DIR, "tarefas.json")
ICON_PATH = os.path.join(BASE_DIR, "assets", "logo.ico")

MINUTOS_ANTES = 5
INTERVALO_VERIFICACAO = 15000  # 15s

# ================= CORES =================
BG = "#1b1f23"
CARD = "#252a31"
TEXT = "#e6e6e6"
ACCENT = "#6264A7"
DANGER = "#c4314b"
SUCCESS = "#4caf50"

tarefas = []
indice_edicao = None

# ================= ARQUIVO =================
def carregar_tarefas():
    global tarefas
    if not os.path.exists(ARQUIVO_TAREFAS):
        tarefas = []
        return

    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            tarefas = json.load(f)
    except:
        tarefas = []

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)

# ================= CRUD =================
def adicionar_tarefa():
    desc = entry_desc.get().strip()
    hora = entry_hora.get().strip()

    if not desc or not hora:
        messagebox.showwarning("Atenção", "Preencha o título e a hora")
        return

    data = calendario.get_date()
    data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

    tarefas.append({
        "descricao": desc,
        "pauta": text_pauta.get("1.0", tk.END).strip(),
        "data_hora": f"{data_br} {hora}",
        "concluida": False,
        "notificado": False
    })

    salvar_tarefas()
    atualizar_lista()
    limpar_campos()

def preparar_edicao():
    global indice_edicao
    sel = lista.selection()
    if not sel:
        return

    indice_edicao = int(sel[0])
    t = tarefas[indice_edicao]

    entry_desc.delete(0, tk.END)
    entry_desc.insert(0, t["descricao"])

    try:
        data_br, hora = t["data_hora"].rsplit(" ", 1)
        calendario.selection_set(
            datetime.strptime(data_br, "%d/%m/%Y").strftime("%Y-%m-%d")
        )
        entry_hora.delete(0, tk.END)
        entry_hora.insert(0, hora)
    except:
        pass

    text_pauta.delete("1.0", tk.END)
    text_pauta.insert("1.0", t.get("pauta", ""))

    btn_add.config(text="Salvar Alterações", command=salvar_edicao)

def salvar_edicao():
    global indice_edicao
    if indice_edicao is None:
        return

    data = calendario.get_date()
    data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

    tarefas[indice_edicao].update({
        "descricao": entry_desc.get().strip(),
        "pauta": text_pauta.get("1.0", tk.END).strip(),
        "data_hora": f"{data_br} {entry_hora.get().strip()}",
        "notificado": False
    })

    indice_edicao = None
    btn_add.config(text="Adicionar Tarefa", command=adicionar_tarefa)

    salvar_tarefas()
    atualizar_lista()
    limpar_campos()

def excluir_tarefa():
    sel = lista.selection()
    if sel:
        del tarefas[int(sel[0])]
        salvar_tarefas()
        atualizar_lista()

def marcar_concluida(event):
    sel = lista.selection()
    if sel:
        i = int(sel[0])
        tarefas[i]["concluida"] = not tarefas[i]["concluida"]
        salvar_tarefas()
        atualizar_lista()

# ================= LEMBRETES =================
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

def verificar_lembretes():
    agora = datetime.now()
    alterado = False

    for tarefa in tarefas:
        if tarefa.get("concluida") or tarefa.get("notificado"):
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

    janela.after(INTERVALO_VERIFICACAO, verificar_lembretes)

# ================= UI =================
def atualizar_lista():
    lista.delete(*lista.get_children())
    for i, t in enumerate(tarefas):
        status = "Concluída" if t.get("concluida") else "Pendente"
        lista.insert("", "end", iid=i,
            values=(t["descricao"], status, t["data_hora"]),
            tags=("done" if t["concluida"] else "pending",)
        )

    lista.tag_configure("done", foreground=SUCCESS)
    lista.tag_configure("pending", foreground=TEXT)

def limpar_campos():
    entry_desc.delete(0, tk.END)
    entry_hora.delete(0, tk.END)
    text_pauta.delete("1.0", tk.END)

# ================= JANELA =================
janela = tk.Tk()
janela.title("AgendaDesk")
janela.geometry("1050x600")
janela.configure(bg=BG)

try:
    janela.iconbitmap(ICON_PATH)
except:
    pass

# ================= ESTILO =================
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background=CARD,
    foreground=TEXT,
    rowheight=34,
    fieldbackground=CARD,
    borderwidth=0,
    font=("Segoe UI", 10)
)
style.map("Treeview", background=[("selected", ACCENT)])

# ================= CONTEÚDO =================
conteudo = tk.Frame(janela, bg=BG)
conteudo.pack(fill="both", expand=True, padx=20, pady=20)

left = tk.Frame(conteudo, bg=BG)
left.pack(side="left", fill="y")

tk.Label(left, text="Título", bg=BG, fg=TEXT).pack(anchor="w")
entry_desc = tk.Entry(left, width=40, bg=CARD, fg=TEXT, insertbackground=TEXT)
entry_desc.pack(pady=6)

tk.Label(left, text="Pauta", bg=BG, fg=TEXT).pack(anchor="w")
text_pauta = tk.Text(left, width=40, height=6, bg=CARD, fg=TEXT, insertbackground=TEXT)
text_pauta.pack(pady=6)

calendario = Calendar(left, date_pattern="yyyy-mm-dd")
calendario.pack(pady=6)

entry_hora = tk.Entry(left, width=12, bg=CARD, fg=TEXT, insertbackground=TEXT)
entry_hora.pack(pady=6)
entry_hora.insert(0, "09:00")

btn_add = tk.Button(left, text="Adicionar Tarefa", bg=ACCENT, fg="white", command=adicionar_tarefa)
btn_add.pack(fill="x", pady=10)

tk.Button(left, text="Editar", bg="#3b3f45", fg=TEXT, command=preparar_edicao).pack(fill="x", pady=4)
tk.Button(left, text="Excluir", bg=DANGER, fg="white", command=excluir_tarefa).pack(fill="x")

right = tk.Frame(conteudo, bg=BG)
right.pack(side="right", fill="both", expand=True)

lista = ttk.Treeview(right, columns=("desc", "status", "data"), show="headings")
lista.heading("desc", text="Título")
lista.heading("status", text="Status")
lista.heading("data", text="Data / Hora")
lista.pack(fill="both", expand=True)
lista.bind("<Double-1>", marcar_concluida)

# ================= START =================
carregar_tarefas()
atualizar_lista()
verificar_lembretes()
janela.mainloop()
