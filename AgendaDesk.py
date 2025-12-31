import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk
import json
import os

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_TAREFAS = os.path.join(BASE_DIR, "tarefas.json")
ICON_PATH = os.path.join(BASE_DIR, "assets", "logo.ico")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

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
            dados = json.load(f)

        if isinstance(dados, list):
            tarefas = []
            for t in dados:
                tarefas.append({
                    "descricao": t.get("descricao", ""),
                    "pauta": t.get("pauta", ""),
                    "data_hora": t.get("data_hora", ""),
                    "concluida": t.get("concluida", False),
                    "notificado": t.get("notificado", False)
                })
        else:
            tarefas = []

    except Exception as e:
        print("Erro ao carregar tarefas:", e)
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

# ================= UI =================
def atualizar_lista():
    lista.delete(*lista.get_children())

    for i, t in enumerate(tarefas):
        status = "Concluída" if t.get("concluida") else "Pendente"
        lista.insert(
            "", "end", iid=i,
            values=(t.get("descricao", ""), status, t.get("data_hora", "")),
            tags=("done" if t.get("concluida") else "pending",)
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
style.configure(
    "Treeview",
    background=CARD,
    foreground=TEXT,
    rowheight=34,
    fieldbackground=CARD,
    borderwidth=0,
    font=("Segoe UI", 10)
)
style.map("Treeview", background=[("selected", ACCENT)])

# ================= HEADER =================
header = tk.Frame(janela, bg=CARD, height=70)
header.pack(fill="x")

header_inner = tk.Frame(header, bg=CARD)
header_inner.pack(side="left", padx=20)

try:
    img = Image.open(ICON_PATH)
    img = img.resize((36, 36), Image.LANCZOS)
    logo = ImageTk.PhotoImage(img)

    lbl_logo = tk.Label(header_inner, image=logo, bg=CARD)
    lbl_logo.image = logo
    lbl_logo.pack(side="left", padx=(0, 10))
except Exception as e:
    print("Erro ao carregar ico:", e)


tk.Label(
    header_inner,
    text="AgendaDesk",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(side="left")


# ================= CONTEÚDO =================
conteudo = tk.Frame(janela, bg=BG)
conteudo.pack(fill="both", expand=True, padx=20, pady=20)

left = tk.Frame(conteudo, bg=BG)
left.pack(side="left", fill="y")

tk.Label(left, text="Título", bg=BG, fg=TEXT).pack(anchor="w")
entry_desc = tk.Entry(left, width=40, bg=CARD, fg=TEXT, insertbackground=TEXT)
entry_desc.pack(pady=6)

tk.Label(left, text="Pauta de Conteúdos", bg=BG, fg=TEXT).pack(anchor="w", pady=(10, 0))
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

# ================= LISTA =================
right = tk.Frame(conteudo, bg=BG)
right.pack(side="right", fill="both", expand=True)

lista = ttk.Treeview(right, columns=("desc", "status", "data"), show="headings")
lista.heading("desc", text="Título")
lista.heading("status", text="Status")
lista.heading("data", text="Data / Hora")

lista.column("desc", width=420)
lista.column("status", width=120, anchor="center")
lista.column("data", width=200)

lista.pack(fill="both", expand=True)
lista.bind("<Double-1>", marcar_concluida)

carregar_tarefas()
atualizar_lista()

janela.mainloop()
