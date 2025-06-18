import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calcular_projeto():
    try:
        Vin = float(entry_vin.get())
        Vout = float(entry_vout.get())
        Po = float(entry_po.get())
        fs_kHz = float(entry_fs.get())
        fs = fs_kHz * 1e3
        T = 1 / fs

        D = 1 - (Vin / Vout)
        Io = Po / Vout
        Iin = Po / Vin
        delta_IL = 0.3 * Iin
        L = (Vin * D) / (fs * delta_IL)
        delta_Vo = 0.02 * Vout
        C = (Io * D) / (fs * delta_Vo)

        resultados["Vin"] = Vin
        resultados["Vout"] = Vout
        resultados["Po"] = Po
        resultados["fs_kHz"] = fs_kHz
        resultados["D"] = D
        resultados["Iin"] = Iin
        resultados["Io"] = Io
        resultados["delta_IL"] = delta_IL
        resultados["L"] = L
        resultados["C"] = C
        resultados["fs"] = fs
        resultados["T"] = T
        resultados["delta_Vo"] = delta_Vo

        lbl_resultados["D"].config(text=f"{D:.4f}")
        lbl_resultados["Iin"].config(text=f"{Iin:.2f} A")
        lbl_resultados["Io"].config(text=f"{Io:.2f} A")
        lbl_resultados["delta_IL"].config(text=f"{delta_IL:.2f} A")
        lbl_resultados["L"].config(text=f"{L * 1e6:.2f} µH")
        lbl_resultados["C"].config(text=f"{C * 1e6:.2f} µF")

    except ValueError:
        messagebox.showerror("Erro", "Verifique se todos os valores foram preenchidos corretamente.")

def mostrar_graficos():
    if not resultados:
        messagebox.showinfo("Aviso", "Calcule o projeto antes de gerar os gráficos.")
        return

    fs = resultados["fs"]
    T = resultados["T"]
    Iin = resultados["Iin"]
    delta_IL = resultados["delta_IL"]
    Vout = resultados["Vout"]
    D = resultados["D"]
    delta_Vo = resultados["delta_Vo"]

    t = np.linspace(0, 2*T, 1000)
    IL = Iin + (delta_IL/2) * np.sign(np.sin(2 * np.pi * fs * t))
    Vo = Vout + (delta_Vo/2) * np.sin(2 * np.pi * fs * t)
    Id = np.where(np.mod(t, T) > D*T, IL, 0)

    fig, axs = plt.subplots(3, 1, figsize=(7, 6))
    axs[0].plot(t*1e6, IL, color='blue')
    axs[0].set_title("Corrente no Indutor")
    axs[0].set_ylabel("Corrente (A)")
    axs[0].grid(True)

    axs[1].plot(t*1e6, Vo, color='green')
    axs[1].set_title("Tensão de Saída")
    axs[1].set_ylabel("Tensão (V)")
    axs[1].grid(True)

    axs[2].plot(t*1e6, Id, color='red')
    axs[2].set_title("Corrente no Diodo")
    axs[2].set_xlabel("Tempo (µs)")
    axs[2].set_ylabel("Corrente (A)")
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

def exportar_relatorio():
    if not resultados:
        messagebox.showinfo("Aviso", "Calcule o projeto antes de exportar.")
        return

    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Arquivo de Texto", "*.txt")],
                                        title="Salvar Relatório")
    if not file:
        return

    with open(file, "w") as f:
        f.write("RELATÓRIO TÉCNICO DO CONVERSOR BOOST CC-CC\n")
        f.write("="*50 + "\n\n")
        f.write(f"Tensão de Entrada (Vin): {resultados['Vin']} V\n")
        f.write(f"Tensão de Saída (Vout): {resultados['Vout']} V\n")
        f.write(f"Potência de Saída (Po): {resultados['Po']} W\n")
        f.write(f"Frequência de Comutação (fs): {resultados['fs_kHz']} kHz\n\n")
        f.write(f"Razão Cíclica (D): {resultados['D']:.4f}\n")
        f.write(f"Corrente de Entrada (Iin): {resultados['Iin']:.2f} A\n")
        f.write(f"Corrente de Saída (Io): {resultados['Io']:.2f} A\n")
        f.write(f"Ondulação de Corrente (ΔIL): {resultados['delta_IL']:.2f} A\n")
        f.write(f"Indutância Recomendada (L): {resultados['L']*1e6:.2f} µH\n")
        f.write(f"Capacitância Recomendada (C): {resultados['C']*1e6:.2f} µF\n")
        f.write(f"Ondulação de Tensão Estimada (ΔVo): {resultados['delta_Vo']:.2f} V\n\n")
        f.write("="*50 + "\n")
        f.write("Observações Técnicas:\n")
        f.write("- ΔIL considerado como 30% da corrente de entrada.\n")
        f.write("- ΔVo estimado como 2% da tensão de saída.\n")
        f.write("- Valores sugeridos para componentes práticos podem variar.\n")

    messagebox.showinfo("Sucesso", "Relatório salvo com sucesso!")

# Interface
root = tk.Tk()
root.title("Projeto de Conversor Boost CC-CC")
root.geometry("520x550")
root.configure(bg="#f0f0f5")

resultados = {}

frame_inputs = ttk.LabelFrame(root, text="Entradas", padding=10)
frame_inputs.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_inputs, text="Vin [V]").grid(row=0, column=0, sticky="w")
entry_vin = ttk.Entry(frame_inputs)
entry_vin.insert(0, "12")
entry_vin.grid(row=0, column=1)

ttk.Label(frame_inputs, text="Vout [V]").grid(row=1, column=0, sticky="w")
entry_vout = ttk.Entry(frame_inputs)
entry_vout.insert(0, "36")
entry_vout.grid(row=1, column=1)

ttk.Label(frame_inputs, text="Potência Po [W]").grid(row=2, column=0, sticky="w")
entry_po = ttk.Entry(frame_inputs)
entry_po.insert(0, "108")
entry_po.grid(row=2, column=1)

ttk.Label(frame_inputs, text="Frequência fs [kHz]").grid(row=3, column=0, sticky="w")
entry_fs = ttk.Entry(frame_inputs)
entry_fs.insert(0, "100")
entry_fs.grid(row=3, column=1)

ttk.Button(root, text="Calcular Projeto", command=calcular_projeto).pack(pady=10)
ttk.Button(root, text="Mostrar Gráficos", command=mostrar_graficos).pack(pady=5)
ttk.Button(root, text="Exportar Relatório", command=exportar_relatorio).pack(pady=5)

frame_results = ttk.LabelFrame(root, text="Resultados", padding=10)
frame_results.pack(fill="x", padx=10, pady=5)

lbl_resultados = {
    "D": ttk.Label(frame_results, text="---"),
    "Iin": ttk.Label(frame_results, text="---"),
    "Io": ttk.Label(frame_results, text="---"),
    "delta_IL": ttk.Label(frame_results, text="---"),
    "L": ttk.Label(frame_results, text="---"),
    "C": ttk.Label(frame_results, text="---"),
}

labels = ["Razão Cíclica (D)", "Corrente de Entrada", "Corrente de Saída", "Ondulação de Corrente", "Indutância", "Capacitância"]
for i, nome in enumerate(labels):
    ttk.Label(frame_results, text=nome).grid(row=i, column=0, sticky="w")
    lbl_resultados[list(lbl_resultados.keys())[i]].grid(row=i, column=1, sticky="e")

root.mainloop()
