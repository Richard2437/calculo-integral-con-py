# Simulador Interactivo de Integración Numérica (Trapecio vs Simpson)
**Ingeniería Informática · Cálculo Integral**

Este proyecto implementa y compara los dos métodos numéricos clásicos para aproximación de áreas bajo la curva:
- **Regla del Trapecio compuesta** ($\mathcal{O}(h^2)$)
- **Regla de Simpson 1/3 compuesta** ($\mathcal{O}(h^4)$)

---

## 🚀 Cómo Iniciar el Frontend (Fácil y Rápido)

Tienes **3 opciones sencillas** para mostrar el trabajo a tu profesor:

### Opción 1: Menú interactivo (Recomendado)
Haz doble clic en:
👉 `ejecutar.bat`

Te permitirá elegir entre la interfaz de escritorio, la interfaz web o el modo consola.

---

### Opción 2: Interfaz Gráfica de Escritorio (Ventana Nativa)
Haz doble clic en:
👉 `abrir_interfaz_escritorio.bat`

O desde la terminal:
```bash
python app_gui.py
```
**Características:**
- Ventana nativa rápida y ligera (Tkinter + Matplotlib).
- Botones de ejemplos predefinidos de las diapositivas de clase (ej. $f(x) = e^{-x^2}$).
- Control deslizante interactivo para variar $n$ (subintervalos).
- Barra de herramientas con zoom, desplazamiento y guardado de imágenes.
- Tabla comparativa de error vs $n$ en tiempo real.

---

### Opción 3: Interfaz Web en el Navegador (Dashboard Visual)
Haz doble clic en:
👉 `abrir_interfaz_web.bat`

O simplemente abre el archivo directamente en tu navegador (Chrome, Edge, etc.):
👉 `web/index.html`

O desde la terminal con el servidor local:
```bash
python app_web.py
```
**Características:**
- Dashboard moderno con gráficos interactivos dinámicos en Canvas.
- Tarjetas de métricas con valor exacto (SciPy Quad), Trapecio y Simpson.
- Resumen pedagógico listo para explicar y defender ante el profesor.
- Funciona 100% sin internet.

---

### Opción 4: Modo Consola Original
```bash
python main.py --cli --show
```
Muestra la tabla en la terminal y genera el archivo `comparativa_integracion.png`.

---

## 📂 Estructura de Archivos del Proyecto
- `app_gui.py`: Frontend de escritorio (interfaz Tkinter interactiva).
- `app_web.py`: Servidor web local para el dashboard en el navegador.
- `web/index.html`: Frontend web moderno y autónomo.
- `calculo_core.py`: Motor matemático y de integración (Trapecio, Simpson, SciPy Quad, generación de gráficos).
- `main.py`: Punto de entrada universal con soporte para GUI, Web y Consola.
- `ejecutar.bat`: Lanzador con menú selector.
- `abrir_interfaz_escritorio.bat`: Acceso directo a la interfaz de escritorio.
- `abrir_interfaz_web.bat`: Acceso directo a la interfaz web.
- `comparativa_integracion.png`: Gráficos generados de alta resolución.
