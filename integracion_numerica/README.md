# Laboratorio de Cálculo Integral: Integración Numérica, Sucesiones y Series (Motor LaTeX)
**Facultad de Ingeniería · Asignatura: Cálculo Integral**

Plataforma interactiva para la simulación numérica, análisis de convergencia y visualización analítica de problemas de Cálculo Integral basada en los talleres de la asignatura, con renderizado matemático en tiempo real y exportación de reportes en **LaTeX**.

---

## 🚀 Módulos Implementados

### 📐 Módulo 1: Integración Numérica y Cálculo de Áreas
Comparación rigurosa de métodos de aproximación numérica frente a la solución analítica exacta:
- **Regla Compuesta del Trapecio**: Aproximación lineal por tramos con convergencia cuadrática:
  $$\int_a^b f(x)\,dx \approx \frac{h}{2} \left[ f(a) + 2\sum_{i=1}^{n-1} f(x_i) + f(b) \right], \quad E_T = \mathcal{O}(h^2)$$
- **Regla Compuesta de Simpson 1/3**: Interpolación parabólica por tramos con convergencia de cuarto orden:
  $$\int_a^b f(x)\,dx \approx \frac{h}{3} \left[ f(a) + 4\sum_{i=1,3,\dots}^{n-1} f(x_i) + 2\sum_{i=2,4,\dots}^{n-2} f(x_i) + f(b) \right], \quad E_S = \mathcal{O}(h^4)$$
- **Gráficas Integradas**:
  1. Interpretación geométrica del área real frente a los polígonos del trapecio con etiquetas y títulos matemáticos en LaTeX.
  2. Gráfico log-log de error absoluto vs número de subintervalos $n$, demostrando las pendientes teóricas $-2$ y $-4$.
- **Ejercicios del Taller Incorporados**:
  - Taller 2a: $\int_0^1 x \sin(2x)\,dx$
  - Taller 2c: $\int_0^2 x \sqrt{1 + x^2}\,dx$
  - Taller 2d: $\int_3^4 \frac{2x}{x^2 - 1}\,dx$
  - Taller 2f: $\int_0^2 \frac{1}{\sqrt{1 + e^x}}\,dx$
  - Taller 2g: $\int_0^1 \frac{2x+1}{3+2x}\,dx$
  - Taller 2h: $\int_1^3 \frac{\ln(x)}{\sqrt{x}}\,dx$
  - Taller 1a (Áreas): Región acotada por $y=x$ y $y=x^2$
  - Taller 1d (Áreas): Región acotada por $y=x^2+3$ y $y=4x^2$
  - Integral Gaussiana: $\int_0^1 e^{-x^2}\,dx$

---

### 🔢 Módulo 2: Sucesiones y Series (Límites y Sumas Parciales)
Análisis de sucesiones infinitas $\{a_n\}$ y comportamiento asintótico de series $\sum a_n$:
- **Cálculo del Término General**: Evaluación analítica y numérica de $a_n$ para $n = 1, 2, \dots, k$.
- **Diagnóstico Automático de Límites**:
  $$\lim_{n \to \infty} a_n = L$$
  Distingue sucesiones convergentes, divergentes a $\pm\infty$ y oscilantes (e.g. $\sin\frac{n\pi}{2}$).
- **Sumas Parciales de Series**:
  $$S_k = \sum_{n=1}^k a_n$$
- **Ejercicios del Taller Incorporados**:
  - Taller 1: $a_n = \frac{n}{2n+1} \implies \lim = \frac{1}{2}$
  - Taller 2: $a_n = \sin\left(\frac{n\pi}{2}\right) \implies \text{Oscilante}$
  - Taller 4a: $a_n = \frac{1}{5^n} \implies \lim = 0$
  - Taller 4b: $a_n = 4\sqrt{n} \implies \text{Diverge a } +\infty$
  - Taller 4c: $a_n = \frac{n^2 - 1}{n^2 + 1} \implies \lim = 1$
  - Taller 4d: $a_n = \frac{4n-3}{3n+4} \implies \lim = \frac{4}{3}$
  - Taller 4e: $a_n = \frac{n^4}{2^n} \implies \lim = 0$
  - Taller 4f: $a_n = n 2^{-n} \implies \lim = 0$
  - Taller 5a: $\sum_{n=1}^\infty \frac{(-2)^{n-1}}{4^n}$ (Serie Geométrica)
  - Taller 5c: $\sum_{n=1}^\infty \frac{1}{n(n+2)}$ (Serie Telescópica)

---

## 🧮 Integración con LaTeX

El proyecto cuenta con un sistema completo de visualización y exportación en LaTeX:
1. **Previsualización en tiempo real**: Mini-canvases Matplotlib (GUI) y KaTeX (Web) que muestran las fórmulas matemáticas con tipografía formal en tiempo real.
2. **Generador de Código LaTeX para Informes**: Botón interactivo **📋 Copiar LaTeX** que genera bloques listos para pegar en Overleaf o documentos `.tex`, incluyendo tablas de convergencia y ecuaciones.
3. **Tipografía Matemática en Gráficos**: Todos los ejes, leyendas y títulos utilizan el renderizador Mathtext de Matplotlib.

---

## 💻 Instrucciones de Ejecución

### Opción 1: Menú Interactivo (Recomendado)
Haz doble clic en:
```text
ejecutar.bat
```
Permite elegir entre la interfaz de escritorio, la interfaz web o el modo consola.

### Opción 2: Interfaz Gráfica Nativa (Tkinter + Matplotlib)
Haz doble clic en:
```text
abrir_interfaz_escritorio.bat
```
O desde la consola:
```bash
python app_gui.py
```

### Opción 3: Dashboard Web Interactivo
Haz doble clic en:
```text
abrir_interfaz_web.bat
```
O abre directamente en tu navegador web:
```text
web/index.html
```

### Opción 4: Modo Terminal / Consola
```bash
python main.py --cli --show
```

---

## 📁 Estructura del Repositorio
```
calculo_integral_project/
├── app_gui.py                 # Interfaz de escritorio Tkinter con previsualizador LaTeX
├── app_web.py                 # Servidor local para el Dashboard web
├── calculo_core.py            # Motor matemático (Trapecio, Simpson, Sucesiones, LaTeX)
├── main.py                    # Punto de entrada unificado (GUI, Web, CLI)
├── web/
│   └── index.html             # Dashboard web completo con KaTeX y Canvas
├── integracion_numerica/       # Réplica sincronizada del paquete
├── ejecutar.bat               # Lanzador principal con menú interactivo
├── abrir_interfaz_escritorio.bat
├── abrir_interfaz_web.bat
└── README.md                  # Documentación técnica completa
```
