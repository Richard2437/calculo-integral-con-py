import os
import io
import re
import base64
import tempfile
import numpy as np

# Configurar cache de matplotlib de forma segura en carpeta temporal existente
cache_dir = os.path.join(tempfile.gettempdir(), "matplotlib_cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = cache_dir

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import ScalarFormatter, NullLocator, FixedLocator
from scipy.integrate import quad

# =========================================================================
# 1. PREAJUSTES DE INTEGRALES (Incluye ejercicios del Taller)
# =========================================================================
PREAJUSTES = [
    {
        "id": "taller_2a",
        "nombre": "Taller 2a: f(x) = x · sin(2x)",
        "expr": "x * sin(2*x)",
        "a": "0.0",
        "b": "1.0",
        "n_default": 6,
        "descripcion": "Ejercicio 2a del taller. Integración por partes: valor exacto = (sin(2) - 2*cos(2))/4 ≈ 0.4354."
    },
    {
        "id": "taller_2c",
        "nombre": "Taller 2c: f(x) = x · √(1 + x²)",
        "expr": "x * sqrt(1 + x**2)",
        "a": "0.0",
        "b": "2.0",
        "n_default": 6,
        "descripcion": "Ejercicio 2c del taller. Sustitución simple u=1+x²: valor exacto = (5√5 - 1)/3 ≈ 3.3934."
    },
    {
        "id": "taller_2d",
        "nombre": "Taller 2d: f(x) = 2x / (x² - 1)",
        "expr": "2*x / (x**2 - 1)",
        "a": "3.0",
        "b": "4.0",
        "n_default": 4,
        "descripcion": "Ejercicio 2d del taller. Fracciones parciales / sustitución: valor exacto = ln(15/8) ≈ 0.6286."
    },
    {
        "id": "taller_2f",
        "nombre": "Taller 2f: f(x) = 1 / √(1 + eˣ)",
        "expr": "1 / sqrt(1 + exp(x))",
        "a": "0.0",
        "b": "2.0",
        "n_default": 6,
        "descripcion": "Ejercicio 2f del taller. Integral con función exponencial irracional."
    },
    {
        "id": "taller_2g",
        "nombre": "Taller 2g: f(x) = (2x + 1) / (3 + 2x)",
        "expr": "(2*x + 1) / (3 + 2*x)",
        "a": "0.0",
        "b": "1.0",
        "n_default": 4,
        "descripcion": "Ejercicio 2g del taller. División de polinomios: valor exacto = 1 - ln(5/3) ≈ 0.4892."
    },
    {
        "id": "taller_2h",
        "nombre": "Taller 2h: f(x) = ln(x) / √x",
        "expr": "log(x) / sqrt(x)",
        "a": "1.0",
        "b": "3.0",
        "n_default": 6,
        "descripcion": "Ejercicio 2h del taller. Integración por partes: valor exacto = 2√3·ln(3) - 4√3 + 4 ≈ 0.8778."
    },
    {
        "id": "taller_area_1a",
        "nombre": "Taller 1a (Área): y₁=x, y₂=x²  ->  f(x) = x - x²",
        "expr": "x - x**2",
        "a": "0.0",
        "b": "1.0",
        "n_default": 4,
        "descripcion": "Ejercicio 1a del taller. Área de la región encerrada entre la recta y=x y la parábola y=x² (Exacto = 1/6 ≈ 0.1667)."
    },
    {
        "id": "taller_area_1d",
        "nombre": "Taller 1d (Área): y₁=x²+3, y₂=4x²  ->  f(x) = 3 - 3x²",
        "expr": "3 - 3*x**2",
        "a": "-1.0",
        "b": "1.0",
        "n_default": 6,
        "descripcion": "Ejercicio 1d del taller. Área encerrada entre dos parábolas intersecadas en x=±1 (Exacto = 4.0)."
    },
    {
        "id": "exp_neg_x2",
        "nombre": "Clásica: f(x) = e^(-x²)",
        "expr": "exp(-x**2)",
        "a": "0.0",
        "b": "1.0",
        "n_default": 4,
        "descripcion": "Función Gaussiana sin primitiva elemental. Caso clásico de integración numérica."
    },
    {
        "id": "arctan",
        "nombre": "Clásica: f(x) = 1 / (1 + x²)",
        "expr": "1 / (1 + x**2)",
        "a": "0.0",
        "b": "1.0",
        "n_default": 4,
        "descripcion": "Integral analítica es arctan(1) = π/4 ≈ 0.785398."
    }
]

# =========================================================================
# 2. PREAJUSTES DE SUCESIONES Y SERIES (Ejercicios del Taller)
# =========================================================================
SUCESIONES_PREAJUSTES = [
    {
        "id": "suc_1",
        "nombre": "Taller 1: aₙ = n / (2n + 1)",
        "expr": "n / (2*n + 1)",
        "k_default": 8,
        "limite_esperado": 0.5,
        "estado_esperado": "CONVERGE a 1/2 (0.5)",
        "descripcion": "Ejercicio 1 del taller. Términos: 1/3, 2/5, 3/7, 4/9, 5/11, 6/13... Divide entre n: lim = 1/2."
    },
    {
        "id": "suc_2",
        "nombre": "Taller 2: aₙ = sin(n·π / 2)",
        "expr": "sin(n * pi / 2)",
        "k_default": 8,
        "limite_esperado": None,
        "estado_esperado": "DIVERGE (Oscila periódicamente: {1, 0, -1, 0...})",
        "descripcion": "Ejercicio 2 del taller. La sucesión oscila indefinidamente entre 1, 0, -1, 0. No tiene límite único."
    },
    {
        "id": "suc_4a",
        "nombre": "Taller 4a: aₙ = 1 / 5ⁿ",
        "expr": "1 / (5**n)",
        "k_default": 8,
        "limite_esperado": 0.0,
        "estado_esperado": "CONVERGE a 0",
        "descripcion": "Ejercicio 4a del taller. Sucesión exponencial decreciente. Como |1/5| < 1, su límite es 0."
    },
    {
        "id": "suc_4b",
        "nombre": "Taller 4b: aₙ = 4·√n",
        "expr": "4 * sqrt(n)",
        "k_default": 8,
        "limite_esperado": None,
        "estado_esperado": "DIVERGE a +∞",
        "descripcion": "Ejercicio 4b del taller. Conforme n crece, 4√n crece sin cota superior hacia el infinito."
    },
    {
        "id": "suc_4c",
        "nombre": "Taller 4c: aₙ = (n² - 1) / (n² + 1)",
        "expr": "(n**2 - 1) / (n**2 + 1)",
        "k_default": 8,
        "limite_esperado": 1.0,
        "estado_esperado": "CONVERGE a 1",
        "descripcion": "Ejercicio 4c del taller. Términos: 0, 3/5, 8/10, 15/17... Los grados mayor de n son iguales: lim = 1."
    },
    {
        "id": "suc_4d",
        "nombre": "Taller 4d: aₙ = (4n - 3) / (3n + 4)",
        "expr": "(4*n - 3) / (3*n + 4)",
        "k_default": 8,
        "limite_esperado": 4/3,
        "estado_esperado": "CONVERGE a 4/3 (≈ 1.3333)",
        "descripcion": "Ejercicio 4d del taller. Dividiendo numerador y denominador entre n: lim = 4/3."
    },
    {
        "id": "suc_4e",
        "nombre": "Taller 4e: aₙ = n⁴ / 2ⁿ",
        "expr": "(n**4) / (2**n)",
        "k_default": 10,
        "limite_esperado": 0.0,
        "estado_esperado": "CONVERGE a 0",
        "descripcion": "Ejercicio 4e del taller. Crecimiento exponencial vence al potencial (regla de L'Hôpital): lim = 0."
    },
    {
        "id": "suc_4f",
        "nombre": "Taller 4f: aₙ = n · 2⁻ⁿ",
        "expr": "n * (2**(-n))",
        "k_default": 8,
        "limite_esperado": 0.0,
        "estado_esperado": "CONVERGE a 0",
        "descripcion": "Ejercicio 4f del taller. Equivale a n / 2ⁿ. Por L'Hôpital: lim = 1 / (2ⁿ·ln 2) = 0."
    },
    {
        "id": "suc_5a",
        "nombre": "Taller 5a (Serie): aₙ = (-3)ⁿ⁻¹ / 4ⁿ",
        "expr": "((-3)**(n-1)) / (4**n)",
        "k_default": 8,
        "limite_esperado": 0.0,
        "estado_esperado": "CONVERGE (Serie Geométrica r = -3/4, Suma = 1/7)",
        "descripcion": "Ejercicio 5a del taller. Serie geométrica con razón |r| = |-3/4| < 1. Converge a a/(1-r) = (1/4)/(7/4) = 1/7."
    },
    {
        "id": "suc_5c",
        "nombre": "Taller 5c (Serie): aₙ = 1 / (n·(n + 2))",
        "expr": "1 / (n * (n + 2))",
        "k_default": 8,
        "limite_esperado": 0.0,
        "estado_esperado": "CONVERGE (Serie Telescópica, Suma = 3/4 = 0.75)",
        "descripcion": "Ejercicio 5c del taller. Serie telescópica por fracciones parciales 1/2 * [1/n - 1/(n+2)]. Suma = 3/4."
    }
]

def preprocesar_expresion(expr_str):
    expr = expr_str.strip()
    expr = re.sub(r'\bsen\b', 'sin', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\bln\b', 'log', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\btg\b', 'tan', expr, flags=re.IGNORECASE)
    expr = expr.replace('^', '**')
    
    expr = expr.replace('log10', '__LOG10__')
    expr = re.sub(r'(\d)\s*([xXeEnN]|pi|\()', r'\1*\2', expr)
    expr = re.sub(r'(\))\s*(\d|[xXeEnN]|pi|\()', r'\1*\2', expr)
    expr = expr.replace('__LOG10__', 'log10')
    
    return expr

def evaluar_limite(limite_val):
    if isinstance(limite_val, (int, float)):
        return float(limite_val)
    s = str(limite_val).strip().lower()
    s = s.replace(',', '.')
    if s == 'pi':
        return float(np.pi)
    if s == 'e':
        return float(np.e)
    scope = {'pi': np.pi, 'e': np.e, 'np': np}
    s_norm = preprocesar_expresion(s)
    return float(eval(s_norm, {'__builtins__': {}}, scope))

def obtener_funcion_segura(expr_str):
    expr_limpia = preprocesar_expresion(expr_str)
    
    allowed_names = {
        'x': 0, 'np': np,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'sen': np.sin, 'tg': np.tan,
        'exp': np.exp, 'log': np.log, 'ln': np.log, 'log10': np.log10,
        'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e,
        'abs': np.abs, 'arcsin': np.arcsin, 'arccos': np.arccos, 'arctan': np.arctan
    }
    
    code = compile(expr_limpia, '<string>', 'eval')
    for name in code.co_names:
        if name not in allowed_names:
            raise ValueError(f"Identificador o función no permitida: '{name}'")
            
    def f(val):
        x_arr = np.asarray(val, dtype=float)
        local_scope = {**allowed_names, 'x': x_arr}
        res = eval(code, {'__builtins__': {}}, local_scope)
        
        if np.isscalar(val):
            return float(np.asarray(res).item())
            
        res_arr = np.asarray(res, dtype=float)
        if res_arr.shape != x_arr.shape:
            res_arr = np.broadcast_to(res_arr, x_arr.shape).copy()
        return res_arr

    return f, expr_limpia

def regla_trapecio(f, a, b, n):
    if n <= 0:
        raise ValueError("El número de subintervalos n debe ser mayor a 0.")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return float((h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1]))

def regla_simpson(f, a, b, n):
    if n <= 0:
        raise ValueError("El número de subintervalos n debe ser mayor a 0.")
    if n % 2 != 0:
        raise ValueError(f"Para la regla de Simpson 1/3, n debe ser un número par (se recibió n={n}).")
    
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    suma_impares = np.sum(y[1:-1:2])
    suma_pares = np.sum(y[2:-1:2])
    return float((h / 3.0) * (y[0] + 4.0 * suma_impares + 2.0 * suma_pares + y[-1]))

def calcular_analisis_completo(expr_str, a_raw, b_raw, n_actual=4, subintervalos_tabla=None):
    if subintervalos_tabla is None:
        subintervalos_tabla = [2, 4, 8, 16, 32, 64]
        
    a = evaluar_limite(a_raw)
    b = evaluar_limite(b_raw)
    
    if b <= a:
        raise ValueError("El límite superior (b) debe ser mayor que el límite inferior (a).")
        
    f, expr_limpia = obtener_funcion_segura(expr_str)
    
    n_act = int(n_actual)
    if n_act % 2 != 0:
        n_act += 1
        
    try:
        valor_exacto, precision_estimada = quad(f, a, b)
    except Exception:
        valor_exacto = regla_simpson(f, a, b, 4000)
        precision_estimada = 1e-10
    
    h_actual = (b - a) / n_act
    val_trapecio = regla_trapecio(f, a, b, n_act)
    err_trapecio = abs(valor_exacto - val_trapecio)
    err_rel_trapecio = (err_trapecio / abs(valor_exacto) * 100) if abs(valor_exacto) > 1e-15 else 0.0
    
    val_simpson = regla_simpson(f, a, b, n_act)
    err_simpson = abs(valor_exacto - val_simpson)
    err_rel_simpson = (err_simpson / abs(valor_exacto) * 100) if abs(valor_exacto) > 1e-15 else 0.0
    
    ratio_precision = (err_trapecio / err_simpson) if err_simpson > 1e-15 else 1e9
    
    lista_ns = sorted(list(set(subintervalos_tabla + [n_act])))
    filas_tabla = []
    errores_trap_lista = []
    errores_simp_lista = []
    
    for n in lista_ns:
        n_eval = n if (n % 2 == 0) else (n + 1)
        h_i = (b - a) / n_eval
        vt = regla_trapecio(f, a, b, n_eval)
        vs = regla_simpson(f, a, b, n_eval)
        et = abs(valor_exacto - vt)
        es = abs(valor_exacto - vs)
        
        errores_trap_lista.append(et)
        errores_simp_lista.append(es)
        
        filas_tabla.append({
            "n": n_eval,
            "h": h_i,
            "val_trapecio": vt,
            "error_trapecio": et,
            "error_rel_trapecio": (et / abs(valor_exacto) * 100) if abs(valor_exacto) > 1e-15 else 0.0,
            "val_simpson": vs,
            "error_simpson": es,
            "error_rel_simpson": (es / abs(valor_exacto) * 100) if abs(valor_exacto) > 1e-15 else 0.0,
        })
        
    return {
        "expr": expr_limpia,
        "a": a,
        "b": b,
        "valor_exacto": valor_exacto,
        "precision_quad": precision_estimada,
        "n_actual": n_act,
        "h_actual": h_actual,
        "val_trapecio": val_trapecio,
        "err_trapecio": err_trapecio,
        "err_rel_trapecio": err_rel_trapecio,
        "n_simpson": n_act,
        "val_simpson": val_simpson,
        "err_simpson": err_simpson,
        "err_rel_simpson": err_rel_simpson,
        "ratio_precision": ratio_precision,
        "tabla": filas_tabla,
        "lista_ns": [f["n"] for f in filas_tabla],
        "errores_trap_lista": errores_trap_lista,
        "errores_simp_lista": errores_simp_lista
    }

# =========================================================================
# 3. MOTOR DE ANÁLISIS DE SUCESIONES Y SERIES
# =========================================================================
def analizar_sucesion(expr_an, k_terminos=10):
    """
    Evalúa la sucesión a_n para n = 1, 2, ..., k_terminos.
    Calcula sumas parciales S_k de la serie y determina la convergencia y límite.
    """
    expr_limpia = preprocesar_expresion(expr_an)
    
    allowed = {
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'sen': np.sin, 'tg': np.tan,
        'exp': np.exp, 'log': np.log, 'ln': np.log,
        'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e,
        'abs': np.abs
    }
    
    code = compile(expr_limpia, '<string>', 'eval')
    for name in code.co_names:
        if name not in allowed and name != 'n':
            raise ValueError(f"Identificador no permitido en término general a_n: '{name}'")
            
    ns = list(range(1, k_terminos + 1))
    terminos = []
    
    for n in ns:
        try:
            val = float(eval(code, {'__builtins__': {}}, {**allowed, 'n': float(n)}))
            terminos.append(val)
        except Exception:
            terminos.append(float('nan'))
            
    sumas_parciales = list(np.nancumsum(terminos))
    
    # Análisis de límite evaluando puntos asintóticos grandes
    muestras_grandes = [100, 200, 500, 1000, 1001, 1002]
    vals_asintoticos = []
    for m in muestras_grandes:
        try:
            v = float(eval(code, {'__builtins__': {}}, {**allowed, 'n': float(m)}))
            if not np.isnan(v) and not np.isinf(v):
                vals_asintoticos.append(v)
            else:
                vals_asintoticos.append(None)
        except Exception:
            vals_asintoticos.append(None)
            
    # Detección de límite y convergencia
    converge = False
    limite = None
    estado_str = "Indeterminado"
    
    # Comprobar oscilación con muestras consecutivas (1000, 1001, 1002)
    val_1000 = vals_asintoticos[-3] if len(vals_asintoticos) >= 3 else None
    val_1001 = vals_asintoticos[-2] if len(vals_asintoticos) >= 2 else None
    val_1002 = vals_asintoticos[-1] if len(vals_asintoticos) >= 1 else None
    
    if val_1000 is not None and val_1001 is not None and val_1002 is not None:
        diff_consec = abs(val_1001 - val_1000)
        
        if diff_consec > 0.05:
            converge = False
            estado_str = "DIVERGE (Sucesión Oscilante sin límite único)"
        elif abs(val_1002) < 1e-5:
            converge = True
            limite = 0.0
            estado_str = "CONVERGE a 0"
        elif diff_consec < 1e-4:
            converge = True
            limite = round(val_1002, 6)
            # Reconocer fracciones comunes
            for num in range(-10, 11):
                for den in range(1, 11):
                    if abs(limite - (num/den)) < 1e-3:
                        limite_frac = f"{num}/{den}" if den != 1 else str(num)
                        estado_str = f"CONVERGE a {limite_frac} (≈ {limite})"
                        break
                if "CONVERGE a " in estado_str:
                    break
            if not "CONVERGE a " in estado_str:
                estado_str = f"CONVERGE a {limite}"
        elif val_1002 > 1e4:
            converge = False
            estado_str = "DIVERGE a +∞"
        elif val_1002 < -1e4:
            converge = False
            estado_str = "DIVERGE a -∞"
        else:
            converge = False
            estado_str = "DIVERGE"
    else:
        # Si dio overflow (como 4*sqrt(n) o exponenciales crecientes)
        if terminos[-1] > terminos[0] * 5:
            converge = False
            estado_str = "DIVERGE a +∞"
        else:
            converge = False
            estado_str = "DIVERGE"

    return {
        "expr": expr_limpia,
        "k_terminos": k_terminos,
        "ns": ns,
        "terminos": terminos,
        "sumas_parciales": sumas_parciales,
        "converge": converge,
        "limite": limite,
        "estado": estado_str
    }

def generar_figura_sucesion(datos_suc):
    """Genera la figura Matplotlib de la sucesión y sus sumas parciales."""
    ns = datos_suc["ns"]
    terminos = datos_suc["terminos"]
    sumas = datos_suc["sumas_parciales"]
    limite = datos_suc["limite"]
    
    fig = Figure(figsize=(10.5, 4.8), dpi=100)
    fig.subplots_adjust(wspace=0.28, left=0.08, right=0.96, top=0.90, bottom=0.14)
    
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    
    # 1. Gráfica de los Términos de la Sucesión a_n vs n
    ax1.plot(ns, terminos, 'o--', color='#2563eb', lw=1.5, markersize=6, label=r"$a_n$")
    if limite is not None:
        ax1.axhline(limite, color='#dc2626', linestyle=':', lw=2, label=f"Límite L = {limite}")
        
    ax1.set_title("1. Términos de la Sucesión ($a_n$ vs $n$)", fontsize=11, fontweight='bold', pad=10)
    ax1.set_xlabel("Índice n", fontsize=10)
    ax1.set_ylabel("Valor aₙ", fontsize=10)
    ax1.set_xticks(ns)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc='best', framealpha=0.9)
    
    # 2. Gráfica de las Sumas Parciales de la Serie S_k
    ax2.plot(ns, sumas, 's-', color='#059669', lw=2.0, markersize=6, label=r"$S_k = \sum a_n$")
    ax2.set_title("2. Sumas Parciales de la Serie ($S_k$ vs $k$)", fontsize=11, fontweight='bold', pad=10)
    ax2.set_xlabel("Número de términos sumados (k)", fontsize=10)
    ax2.set_ylabel("Suma Acumulada Sₖ", fontsize=10)
    ax2.set_xticks(ns)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc='best', framealpha=0.9)
    
    return fig
