import os
import sys
import tempfile
import numpy as np

# Configurar cache de matplotlib de forma segura en carpeta temporal existente
cache_dir = os.path.join(tempfile.gettempdir(), "matplotlib_cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = cache_dir

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import ScalarFormatter, NullLocator, FixedLocator

import calculo_core

class CalculoIntegralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taller Cálculo Integral · Integración Numérica y Sucesiones")
        self.root.geometry("1300x800")
        self.root.minsize(1050, 700)
        
        self.configurar_estilos()
        self.crear_layout_principal()
        
        # Cargar preajustes iniciales
        self.cargar_preajuste_integral(0)
        self.cargar_preajuste_sucesion(0)

    def configurar_estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
            
        style.configure(".", font=("Segoe UI", 9))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), foreground="#0f172a")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#64748b")
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), background="#2563eb", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=24, font=("Consolas", 9))

    def crear_layout_principal(self):
        # Header superior
        header_frame = ttk.Frame(self.root, padding="12 8 12 8")
        header_frame.pack(fill=tk.X)
        
        titulo = ttk.Label(header_frame, text="⚡ Taller de Cálculo Integral · Laboratorio Interactivo", style="Header.TLabel")
        titulo.pack(anchor="w")
        subtitulo = ttk.Label(header_frame, text="Módulos interactivos: Integración Numérica (Trapecio vs Simpson) · Sucesiones y Series (Límites y Convergencia)", style="SubHeader.TLabel")
        subtitulo.pack(anchor="w")

        # Pestañas principales de los dos módulos
        self.notebook_modulos = ttk.Notebook(self.root)
        self.notebook_modulos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # =====================================================
        # PESTAÑA MÓDULO 1: INTEGRACIÓN NUMÉRICA Y ÁREAS
        # =====================================================
        self.frame_modulo_integrales = ttk.Frame(self.notebook_modulos)
        self.notebook_modulos.add(self.frame_modulo_integrales, text=" 📐 Módulo 1: Integración Numérica y Áreas ")
        self.crear_modulo_integrales(self.frame_modulo_integrales)

        # =====================================================
        # PESTAÑA MÓDULO 2: SUCESIONES Y SERIES
        # =====================================================
        self.frame_modulo_sucesiones = ttk.Frame(self.notebook_modulos)
        self.notebook_modulos.add(self.frame_modulo_sucesiones, text=" 🔢 Módulo 2: Sucesiones y Series (Taller) ")
        self.crear_modulo_sucesiones(self.frame_modulo_sucesiones)

    # -----------------------------------------------------------------
    # CONSTRUCCIÓN DEL MÓDULO 1: INTEGRALES
    # -----------------------------------------------------------------
    def crear_modulo_integrales(self, parent):
        paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        # Panel izquierdo
        left = ttk.Frame(paned, width=410, padding="8")
        paned.add(left, weight=1)
        
        # Presets
        grp_pre = ttk.LabelFrame(left, text=" 📚 Ejercicios de Integrales del Taller ", padding="8")
        grp_pre.pack(fill=tk.X, pady=(0, 8))
        
        self.combo_integ = ttk.Combobox(grp_pre, state="readonly", values=[p["nombre"] for p in calculo_core.PREAJUSTES])
        self.combo_integ.pack(fill=tk.X, pady=(0, 4))
        self.combo_integ.bind("<<ComboboxSelected>>", self.on_preset_integral_selected)
        
        self.lbl_integ_desc = ttk.Label(grp_pre, text="", wraplength=360, font=("Segoe UI", 8, "italic"), foreground="#475569")
        self.lbl_integ_desc.pack(fill=tk.X)
        
        # Parámetros
        grp_par = ttk.LabelFrame(left, text=" ⚙️ Parámetros de la Integral ", padding="8")
        grp_par.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(grp_par, text="Función f(x):").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_expr = ttk.Entry(grp_par, font=("Consolas", 10))
        self.entry_expr.grid(row=0, column=1, columnspan=2, sticky="ew", pady=3)
        
        ttk.Label(grp_par, text="Límite inf. (a):").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_a = ttk.Entry(grp_par, width=12, font=("Consolas", 10))
        self.entry_a.grid(row=1, column=1, sticky="w", pady=3)
        
        ttk.Label(grp_par, text="Límite sup. (b):").grid(row=2, column=0, sticky="w", pady=3)
        self.entry_b = ttk.Entry(grp_par, width=12, font=("Consolas", 10))
        self.entry_b.grid(row=2, column=1, sticky="w", pady=3)
        
        ttk.Label(grp_par, text="Subintervalos (n):").grid(row=3, column=0, sticky="w", pady=3)
        s_frame = ttk.Frame(grp_par)
        s_frame.grid(row=3, column=1, columnspan=2, sticky="ew", pady=3)
        
        self.var_n = tk.IntVar(value=4)
        self.slider_n = ttk.Scale(s_frame, from_=2, to=64, variable=self.var_n, command=self.on_slider_n_change)
        self.slider_n.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.slider_n.bind("<ButtonRelease-1>", lambda e: self.calcular_integral())
        
        self.lbl_n_val = ttk.Label(s_frame, text="n = 4", width=7, font=("Segoe UI", 9, "bold"))
        self.lbl_n_val.pack(side=tk.LEFT, padx=4)
        grp_par.columnconfigure(1, weight=1)
        
        btn_c = ttk.Button(left, text="🚀 Calcular y Actualizar Gráficos", style="Accent.TButton", command=self.calcular_integral)
        btn_c.pack(fill=tk.X, pady=(0, 8), ipady=4)
        
        # Resumen
        grp_res = ttk.LabelFrame(left, text=" 📊 Resumen Numérico ", padding="6")
        grp_res.pack(fill=tk.BOTH, expand=True)
        
        f_txt = ttk.Frame(grp_res)
        f_txt.pack(fill=tk.BOTH, expand=True)
        self.txt_resumen = tk.Text(f_txt, wrap=tk.WORD, font=("Consolas", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        sc = ttk.Scrollbar(f_txt, orient=tk.VERTICAL, command=self.txt_resumen.yview)
        self.txt_resumen.configure(yscrollcommand=sc.set)
        self.txt_resumen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel derecho
        right = ttk.Frame(paned, padding="4")
        paned.add(right, weight=3)
        
        self.nb_integ = ttk.Notebook(right)
        self.nb_integ.pack(fill=tk.BOTH, expand=True)
        
        tab_g = ttk.Frame(self.nb_integ)
        self.nb_integ.add(tab_g, text=" 📈 Gráficos (Geometría + Error Log-Log) ")
        
        tab_t = ttk.Frame(self.nb_integ)
        self.nb_integ.add(tab_t, text=" 📋 Tabla de Convergencia ")
        
        # Figura Matplotlib
        self.fig_int = Figure(figsize=(9.2, 4.8), dpi=100)
        self.fig_int.subplots_adjust(wspace=0.28, left=0.08, right=0.96, top=0.90, bottom=0.14)
        self.ax1 = self.fig_int.add_subplot(1, 2, 1)
        self.ax2 = self.fig_int.add_subplot(1, 2, 2)
        
        self.canvas_int = FigureCanvasTkAgg(self.fig_int, master=tab_g)
        self.canvas_int.draw()
        
        tb_frame = ttk.Frame(tab_g)
        tb_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar_int = NavigationToolbar2Tk(self.canvas_int, tb_frame)
        self.toolbar_int.update()
        self.canvas_int.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.crear_tabla_integrales(tab_t)

    def crear_tabla_integrales(self, parent):
        cols = ("n", "h", "val_trap", "err_trap", "val_simp", "err_simp", "mejora")
        self.tree_int = ttk.Treeview(parent, columns=cols, show="headings", height=10)
        
        self.tree_int.heading("n", text="Subintervalos (n)")
        self.tree_int.heading("h", text="Paso (h)")
        self.tree_int.heading("val_trap", text="Aprox. Trapecio")
        self.tree_int.heading("err_trap", text="Error Trapecio")
        self.tree_int.heading("val_simp", text="Aprox. Simpson")
        self.tree_int.heading("err_simp", text="Error Simpson")
        self.tree_int.heading("mejora", text="Ventaja de Simpson")
        
        for c in cols:
            self.tree_int.column(c, anchor="center")
            
        sc = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree_int.yview)
        self.tree_int.configure(yscroll=sc.set)
        self.tree_int.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
        sc.pack(side=tk.RIGHT, fill=tk.Y, pady=6)

    def on_slider_n_change(self, val):
        n = int(round(float(val)))
        if n % 2 != 0:
            n += 1
        self.var_n.set(n)
        self.lbl_n_val.config(text=f"n = {n}")

    def on_preset_integral_selected(self, event=None):
        idx = self.combo_integ.current()
        if idx >= 0:
            self.cargar_preajuste_integral(idx)

    def cargar_preajuste_integral(self, idx):
        preset = calculo_core.PREAJUSTES[idx]
        self.combo_integ.current(idx)
        self.lbl_integ_desc.config(text=preset["descripcion"])
        self.entry_expr.delete(0, tk.END)
        self.entry_expr.insert(0, preset["expr"])
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, str(preset["a"]))
        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(preset["b"]))
        self.var_n.set(preset["n_default"])
        self.lbl_n_val.config(text=f"n = {preset['n_default']}")
        self.calcular_integral()

    def calcular_integral(self):
        expr_str = self.entry_expr.get().strip()
        try:
            a_val = calculo_core.evaluar_limite(self.entry_a.get())
            b_val = calculo_core.evaluar_limite(self.entry_b.get())
            n = int(self.var_n.get())
            if n % 2 != 0:
                n += 1
                self.var_n.set(n)
                self.lbl_n_val.config(text=f"n = {n}")
        except Exception as e:
            messagebox.showerror("Error en Límites", f"Revisa los límites a, b y n:\n{e}")
            return
            
        if b_val <= a_val:
            messagebox.showerror("Límites Inválidos", "El límite superior (b) debe ser mayor que el inferior (a).")
            return

        try:
            datos = calculo_core.calcular_analisis_completo(expr_str, a_val, b_val, n, [2, 4, 8, 16, 32, 64])
        except Exception as err:
            messagebox.showerror("Error de Cálculo", f"No se pudo procesar la función:\n{err}")
            return

        # Resumen
        self.txt_resumen.delete("1.0", tk.END)
        txt = [
            "========================================\n",
            f" Función: f(x) = {datos['expr']}\n",
            f" Intervalo: [{datos['a']:.4f}, {datos['b']:.4f}] | Paso h = {datos['h_actual']:.6f}\n",
            "========================================\n",
            f"• Valor Exacto (scipy.quad):\n  {datos['valor_exacto']:.10f}\n\n",
            f"• Regla del Trapecio (n = {datos['n_actual']}):\n",
            f"  Aprox : {datos['val_trapecio']:.8f}\n",
            f"  Error Abs : {datos['err_trapecio']:.2e}\n",
            f"  Error Rel : {datos['err_rel_trapecio']:.4f}%\n\n",
            f"• Regla de Simpson 1/3 (n = {datos['n_simpson']}):\n",
            f"  Aprox : {datos['val_simpson']:.8f}\n",
            f"  Error Abs : {datos['err_simpson']:.2e}\n",
            f"  Error Rel : {datos['err_rel_simpson']:.4f}%\n\n"
        ]
        if datos['err_simpson'] > 1e-15:
            r = datos['err_trapecio'] / datos['err_simpson']
            txt.append(f"⭐ Rendimiento Relativo:\n  Simpson es ~{r:.1f}x más preciso que Trapecio.\n")
        else:
            txt.append("⭐ Rendimiento Relativo:\n  Simpson es EXACTO (Error = 0.0).\n")
        self.txt_resumen.insert(tk.END, "".join(txt))

        # Gráficos
        self.ax1.clear()
        self.ax2.clear()
        
        f, _ = calculo_core.obtener_funcion_segura(datos["expr"])
        a, b, n_act = datos["a"], datos["b"], datos["n_actual"]
        
        x_c = np.linspace(a, b, 250)
        y_c = f(x_c)
        x_n = np.linspace(a, b, n_act + 1)
        y_n = f(x_n)
        
        self.ax1.plot(x_c, y_c, color='#1d4ed8', lw=2.2, label="f(x) real")
        self.ax1.fill_between(x_c, y_c, alpha=0.15, color='#3b82f6', label="Área exacta")
        
        for i in range(n_act):
            xs = [x_n[i], x_n[i], x_n[i+1], x_n[i+1]]
            ys = [0, y_n[i], y_n[i+1], 0]
            self.ax1.fill(xs, ys, color='#f97316', alpha=0.20, edgecolor='#c2410c', linestyle='--')
            
        self.ax1.plot(x_n, y_n, 'o--', color='#ea580c', lw=1.6, markersize=4, label=f"Trapecios (n={n_act})")
        if n_act <= 32:
            for xi, yi in zip(x_n, y_n):
                self.ax1.vlines(xi, 0, yi, colors='#94a3b8', linestyles=':')
                
        self.ax1.set_title(f"1. Interpretación Geométrica (n={n_act})", fontsize=11, fontweight='bold')
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("f(x)")
        self.ax1.grid(True, linestyle="--", alpha=0.5)
        self.ax1.legend(loc='best', fontsize=8)
        
        ns = datos["lista_ns"]
        errs_t = [max(float(e), 1e-16) for e in datos["errores_trap_lista"]]
        errs_s = [max(float(e), 1e-16) for e in datos["errores_simp_lista"]]
        
        self.ax2.loglog(ns, errs_t, 's-', color='#d97706', lw=2.0, markersize=5, label=r"Trapecio $\mathcal{O}(h^2)$")
        self.ax2.loglog(ns, errs_s, 'o-', color='#059669', lw=2.0, markersize=5, label=r"Simpson $\mathcal{O}(h^4)$")
        self.ax2.set_title("2. Error vs n (Escala Log-Log)", fontsize=11, fontweight='bold')
        self.ax2.set_xlabel("Subintervalos n")
        self.ax2.set_ylabel("Error Absoluto")
        
        self.ax2.xaxis.set_minor_locator(NullLocator())
        self.ax2.xaxis.set_major_locator(FixedLocator(ns))
        self.ax2.xaxis.set_major_formatter(ScalarFormatter())
        self.ax2.set_xticks(ns)
        self.ax2.set_xticklabels([str(x) for x in ns])
        self.ax2.grid(True, which="both", linestyle="--", alpha=0.5)
        self.ax2.legend(loc='best', fontsize=8)
        
        self.canvas_int.draw()

        # Tabla
        for it in self.tree_int.get_children():
            self.tree_int.delete(it)
        for row in datos["tabla"]:
            m = f"{row['error_trapecio']/row['error_simpson']:.1f}x veces" if row['error_simpson'] > 1e-15 else "Exacto"
            self.tree_int.insert("", tk.END, values=(
                row["n"], f"{row['h']:.4f}", f"{row['val_trapecio']:.8f}",
                f"{row['error_trapecio']:.2e}", f"{row['val_simpson']:.8f}",
                f"{row['error_simpson']:.2e}", m
            ))

    # -----------------------------------------------------------------
    # CONSTRUCCIÓN DEL MÓDULO 2: SUCESIONES Y SERIES
    # -----------------------------------------------------------------
    def crear_modulo_sucesiones(self, parent):
        paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        # Panel izquierdo
        left = ttk.Frame(paned, width=410, padding="8")
        paned.add(left, weight=1)
        
        grp_pre = ttk.LabelFrame(left, text=" 📚 Ejercicios de Sucesiones del Taller ", padding="8")
        grp_pre.pack(fill=tk.X, pady=(0, 8))
        
        self.combo_suc = ttk.Combobox(grp_pre, state="readonly", values=[p["nombre"] for p in calculo_core.SUCESIONES_PREAJUSTES])
        self.combo_suc.pack(fill=tk.X, pady=(0, 4))
        self.combo_suc.bind("<<ComboboxSelected>>", self.on_preset_sucesion_selected)
        
        self.lbl_suc_desc = ttk.Label(grp_pre, text="", wraplength=360, font=("Segoe UI", 8, "italic"), foreground="#475569")
        self.lbl_suc_desc.pack(fill=tk.X)
        
        grp_par = ttk.LabelFrame(left, text=" ⚙️ Término General aₙ ", padding="8")
        grp_par.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(grp_par, text="Fórmula aₙ:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_an = ttk.Entry(grp_par, font=("Consolas", 10))
        self.entry_an.grid(row=0, column=1, sticky="ew", pady=3)
        
        ttk.Label(grp_par, text="Cantidad de términos (k):").grid(row=1, column=0, sticky="w", pady=3)
        self.spin_k = ttk.Spinbox(grp_par, from_=4, to=50, width=6, font=("Consolas", 10))
        self.spin_k.set(8)
        self.spin_k.grid(row=1, column=1, sticky="w", pady=3)
        grp_par.columnconfigure(1, weight=1)
        
        btn_cs = ttk.Button(left, text="🚀 Analizar Sucesión y Límite", style="Accent.TButton", command=self.calcular_sucesion)
        btn_cs.pack(fill=tk.X, pady=(0, 8), ipady=4)
        
        grp_diag = ttk.LabelFrame(left, text=" 📋 Diagnóstico y Lista de Términos ", padding="6")
        grp_diag.pack(fill=tk.BOTH, expand=True)
        
        f_diag = ttk.Frame(grp_diag)
        f_diag.pack(fill=tk.BOTH, expand=True)
        self.txt_suc = tk.Text(f_diag, wrap=tk.WORD, font=("Consolas", 9), bg="#f8fafc", relief=tk.SOLID, bd=1)
        sc_s = ttk.Scrollbar(f_diag, orient=tk.VERTICAL, command=self.txt_suc.yview)
        self.txt_suc.configure(yscrollcommand=sc_s.set)
        self.txt_suc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc_s.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel derecho
        right = ttk.Frame(paned, padding="4")
        paned.add(right, weight=3)
        
        # Gráficos de sucesiones
        self.fig_suc = Figure(figsize=(9.2, 4.8), dpi=100)
        self.fig_suc.subplots_adjust(wspace=0.28, left=0.08, right=0.96, top=0.90, bottom=0.14)
        self.ax_suc1 = self.fig_suc.add_subplot(1, 2, 1)
        self.ax_suc2 = self.fig_suc.add_subplot(1, 2, 2)
        
        self.canvas_suc = FigureCanvasTkAgg(self.fig_suc, master=right)
        self.canvas_suc.draw()
        
        tb_frame_s = ttk.Frame(right)
        tb_frame_s.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar_suc = NavigationToolbar2Tk(self.canvas_suc, tb_frame_s)
        self.toolbar_suc.update()
        self.canvas_suc.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_preset_sucesion_selected(self, event=None):
        idx = self.combo_suc.current()
        if idx >= 0:
            self.cargar_preajuste_sucesion(idx)

    def cargar_preajuste_sucesion(self, idx):
        preset = calculo_core.SUCESIONES_PREAJUSTES[idx]
        self.combo_suc.current(idx)
        self.lbl_suc_desc.config(text=preset["descripcion"])
        self.entry_an.delete(0, tk.END)
        self.entry_an.insert(0, preset["expr"])
        self.spin_k.set(preset["k_default"])
        self.calcular_sucesion()

    def calcular_sucesion(self):
        expr_str = self.entry_an.get().strip()
        try:
            k = int(self.spin_k.get())
            if k < 2 or k > 100:
                k = 8
        except Exception:
            k = 8
            
        try:
            res = calculo_core.analizar_sucesion(expr_str, k)
        except Exception as err:
            messagebox.showerror("Error en Sucesión", f"No se pudo evaluar la sucesión a_n:\n{err}")
            return

        # Diagnóstico texto
        self.txt_suc.delete("1.0", tk.END)
        txt = [
            "========================================\n",
            f" Término general: aₙ = {res['expr']}\n",
            "========================================\n",
            f"• Dictamen de Convergencia:\n  👉 {res['estado']}\n\n",
            f"• Primeros {res['k_terminos']} términos:\n"
        ]
        
        for i, val in enumerate(res['terminos']):
            txt.append(f"  a_{i+1} = {val:.6f}\n")
            
        txt.append("\n• Sumas parciales acumuladas (Serie Sₖ):\n")
        for i, s_val in enumerate(res['sumas_parciales']):
            txt.append(f"  S_{i+1} = {s_val:.6f}\n")
            
        self.txt_suc.insert(tk.END, "".join(txt))

        # Dibujar Gráficos
        self.ax_suc1.clear()
        self.ax_suc2.clear()
        
        ns = res["ns"]
        terms = res["terminos"]
        sums = res["sumas_parciales"]
        lim = res["limite"]
        
        self.ax_suc1.plot(ns, terms, 'o--', color='#2563eb', lw=1.6, markersize=6, label=r"$a_n$")
        if lim is not None:
            self.ax_suc1.axhline(lim, color='#dc2626', linestyle=':', lw=2, label=f"Límite L = {lim}")
            
        self.ax_suc1.set_title("1. Términos de la Sucesión ($a_n$ vs $n$)", fontsize=11, fontweight='bold')
        self.ax_suc1.set_xlabel("Índice n")
        self.ax_suc1.set_ylabel("Valor aₙ")
        self.ax_suc1.set_xticks(ns)
        self.ax_suc1.grid(True, linestyle="--", alpha=0.5)
        self.ax1.legend(loc='best', fontsize=8)
        self.ax_suc1.legend(loc='best', fontsize=8)
        
        self.ax_suc2.plot(ns, sums, 's-', color='#059669', lw=2.0, markersize=6, label=r"$S_k = \sum a_n$")
        self.ax_suc2.set_title("2. Sumas Parciales de la Serie ($S_k$ vs $k$)", fontsize=11, fontweight='bold')
        self.ax_suc2.set_xlabel("Términos sumados (k)")
        self.ax_suc2.set_ylabel("Suma Acumulada Sₖ")
        self.ax_suc2.set_xticks(ns)
        self.ax_suc2.grid(True, linestyle="--", alpha=0.5)
        self.ax_suc2.legend(loc='best', fontsize=8)
        
        self.canvas_suc.draw()

def main():
    root = tk.Tk()
    app = CalculoIntegralApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
