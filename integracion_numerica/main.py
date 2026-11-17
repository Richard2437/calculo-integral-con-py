import os
import sys
import tempfile
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib_cache")

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def regla_trapecio(f, a, b, n):
    """
    Regla del Trapecio compuesta:
    T = (h/2) * [ f(x_0) + 2*f(x_1) + ... + 2*f(x_{n-1}) + f(x_n) ]
    Error proporcional a h^2 (O(h^2))
    """
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return float((h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1]))

def regla_simpson(f, a, b, n):
    """
    Regla de Simpson 1/3 compuesta:
    S = (h/3) * [ f(x_0) + 4*f(x_1) + 2*f(x_2) + ... + 4*f(x_{n-1}) + f(x_n) ]
    Error proporcional a h^4 (O(h^4))
    Requiere n par.
    """
    if n % 2 != 0:
        raise ValueError(f"Para la regla de Simpson, n debe ser par (se recibió n={n}).")
    
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    suma_impares = np.sum(y[1:-1:2])
    suma_pares = np.sum(y[2:-1:2])
    return float((h / 3.0) * (y[0] + 4.0 * suma_impares + 2.0 * suma_pares + y[-1]))

def ejecutar_demo_consola(mostrar_grafica=True):
    print("=" * 65)
    print(" INGENIERÍA INFORMÁTICA · CÁLCULO INTEGRAL")
    print(" Integración Numérica Clásica: Regla del Trapecio y Simpson")
    print("=" * 65)

    # 1. Definir función y límites según la presentación
    # f(x) = exp(-x^2) en el intervalo [0, 1]
    f = lambda x: np.exp(-x**2)
    a, b = 0.0, 1.0

    # Valor de referencia exacto con alta precisión
    valor_exacto, _ = quad(f, a, b)
    
    print(f"\nFunción: f(x) = e^(-x^2)")
    print(f"Intervalo: [{a}, {b}]")
    print(f"Valor exacto de referencia: {valor_exacto:.10f}\n")

    # 2. Reproducción exacta de la tabla de la diapositiva 5
    subintervalos_n = [4, 8, 16, 32]
    errores_trapecio = []
    errores_simpson = []

    print(f"{'Subintervalos n':<16} | {'Error trapecio':<16} | {'Error Simpson':<16}")
    print("-" * 52)

    for n in subintervalos_n:
        val_trap = regla_trapecio(f, a, b, n)
        val_simp = regla_simpson(f, a, b, n)

        err_trap = abs(valor_exacto - val_trap)
        err_simp = abs(valor_exacto - val_simp)

        errores_trapecio.append(err_trap)
        errores_simpson.append(err_simp)

        print(f"{n:<16d} | {err_trap:<16.2e} | {err_simp:<16.2e}")

    print("-" * 52)
    print(f"Valor exacto: {valor_exacto:.10f}. Simpson converge mucho más rápido.\n")

    # 3. Generación de Gráficos (Demo en vivo)
    print("Generando visualizaciones...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Gráfico 1: Área sombreada y aproximación de trapecios
    n_muestra = 4
    x_curva = np.linspace(a, b, 200)
    y_curva = f(x_curva)
    x_nodos = np.linspace(a, b, n_muestra + 1)
    y_nodos = f(x_nodos)

    ax1.plot(x_curva, y_curva, 'navy', lw=2.5, label=r"$f(x) = e^{-x^2}$")
    ax1.fill_between(x_curva, y_curva, alpha=0.15, color='royalblue', label="Área real bajo la curva")
    ax1.plot(x_nodos, y_nodos, 'ro--', lw=1.5, label=f"Trapecios (n={n_muestra})")
    for xi, yi in zip(x_nodos, y_nodos):
        ax1.vlines(xi, 0, yi, colors='gray', linestyles=':')
    ax1.set_title("1. Interpretación Geométrica (Trapecios)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc='lower left')

    # Gráfico 2: Convergencia de error vs n (Escala Log-Log)
    ax2.loglog(subintervalos_n, errores_trapecio, 's-', color='#d95f02', lw=2, label=r"Trapecio $\mathcal{O}(h^2)$")
    ax2.loglog(subintervalos_n, errores_simpson, 'o-', color='#1b9e77', lw=2, label=r"Simpson $\mathcal{O}(h^4)$")
    ax2.set_title("2. Error vs n (Escala Logarítmica)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Número de subintervalos (n)")
    ax2.set_ylabel("Error absoluto")
    ax2.set_xticks(subintervalos_n)
    ax2.set_xticklabels(subintervalos_n)
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    
    # Guardar imagen para visualización asegurada
    ruta_grafico = "comparativa_integracion.png"
    plt.savefig(ruta_grafico, dpi=300)
    print(f"Gráfico guardado exitosamente como '{ruta_grafico}'.")
    
    if mostrar_grafica:
        print("Mostrando ventana de gráficos (ciérrala para terminar)...")
        plt.show()

def main():
    args = sys.argv[1:]
    
    if "--cli" in args or "--console" in args:
        mostrar = "--show" in args
        ejecutar_demo_consola(mostrar_grafica=mostrar)
        return
        
    if "--web" in args:
        import app_web
        app_web.iniciar_servidor_web()
        return

    # Por defecto: Iniciar la interfaz gráfica de usuario (GUI)
    try:
        import app_gui
        app_gui.main()
    except Exception as e:
        print(f"Nota: No se pudo abrir la interfaz de escritorio directamente ({e}).")
        print("Iniciando modo consola con generación de gráficos...")
        ejecutar_demo_consola(mostrar_grafica=False)

if __name__ == "__main__":
    main()
