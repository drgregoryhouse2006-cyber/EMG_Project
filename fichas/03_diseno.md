## Ficha 3. Diseño Detallado del Sistema

### 3.1 Diagrama de Bloques General

El sistema completo de adquisición sEMG se organiza en dos dominios de procesamiento encadenados:

**Dominio analógico (PCB):**

$$\text{Electrodos Ag/AgCl} \rightarrow \text{INA128} \rightarrow \text{HP Sallen-Key (20 Hz)} \rightarrow \text{LP Sallen-Key (450 Hz)} \rightarrow \text{Offset DC (LM741)} \rightarrow \text{ADC}$$

**Dominio digital (Arduino + MATLAB):**

$$\text{ADC Arduino UNO} \rightarrow \text{Notch IIR (60\text{ Hz})} \rightarrow \text{Envolvente RMS} \rightarrow \text{Visualización}$$

Cada bloque cumple una función específica dentro de la cadena de acondicionamiento. Los criterios de diseño de cada etapa se desarrollan en las secciones siguientes.

### 3.1.1 Esquemático de Simulación

El diagrama de bloques fue implementado y verificado en simulación 
antes del montaje físico. El esquemático completo del circuito 
analógico se muestra a continuación:

[🔍 Ver esquemático completo del sistema — Multisim](/imagenes/esquematico_simulacion.png)

*Fig. 0 — Esquemático de simulación del sistema completo. 
De izquierda a derecha: fuente de señal XFG1, amplificador 
de instrumentación AD620AN, filtro pasa-altas Sallen-Key (U2A — LM358AD), 
filtro pasa-bajas Sallen-Key (U2B — LM358AD), etapa de offset DC 
(U3 — 741), y osciloscopio XSC1 para verificación de la señal de salida.*
---

### 3.2 Etapa 1: Preamplificación Diferencial — INA128

#### Objetivo

Capturar la diferencia de potencial entre los dos electrodos activos (S1 y S2) colocados sobre el músculo gastrocnemio, rechazar el ruido de modo común (interferencia de red acoplada al cuerpo humano) y amplificar la señal biológica a un nivel útil para las etapas de filtrado.

#### Principio de operación

El INA128 es un amplificador de instrumentación de tres op-amps internos. Su ganancia se programa con una única resistencia externa $R_G$ conectada entre los pines 1 y 8:

$$G = 1 + \frac{49.4\text{ k}\Omega}{R_G}$$

La impedancia de entrada diferencial del INA128 es mayor a $10\text{ G}\Omega$, garantizando una interfaz no invasiva con la piel. El CMRR típico supera los 90 dB, asegurando rechazo efectivo de la interferencia de 60 Hz acoplada en modo común.

> **Nota de equivalencia:** El diseño original especificaba el AD620. Durante la implementación se sustituyó por el **INA128**, que comparte el mismo principio de operación, pinout compatible y constante de ganancia idéntica ($49.4\text{ k}\Omega$). El CMRR típico del INA128 (>90 dB) cumple la especificación de diseño.

#### Cálculo de ganancia

La señal EMG superficial del gastrocnemio tiene una amplitud típica de $1\text{ mV}$ a $5\text{ mV}$. Se requiere amplificarla a un nivel manejable para las etapas de filtrado sin saturar los op-amps alimentados a $\pm15\text{ V}$. Se establece una ganancia objetivo de $G = 50$:

$$R_G = \frac{49.4\text{ k}\Omega}{G - 1} = \frac{49.4\text{ k}\Omega}{50 - 1} = \frac{49.4\text{ k}\Omega}{49} \approx 1\text{ k}\Omega$$

Se implementó con un **potenciómetro de $1\text{ k}\Omega$**, permitiendo ajuste fino. La ganancia real obtenida es:

$$G_{real} = 1 + \frac{49.4\text{ k}\Omega}{1\text{ k}\Omega} = 1 + 49.4 = \mathbf{50.4 \text{ V/V}}$$

#### Verificación del rango de salida

$$V_{out,min} = 50.4 \times 1\text{ mV} = 50.4\text{ mV}$$
$$V_{out,max} = 50.4 \times 5\text{ mV} = 252\text{ mV}$$

La señal amplificada queda en el rango $50\text{ mV}$ a $252\text{ mV}$, apropiado para ingresar a las etapas de filtrado sin saturación con alimentación $\pm15\text{ V}$.

#### Configuración de pines INA128

| Pin | Señal |
| :--- | :--- |
| 1, 8 | $R_G$ externa ($1\text{ k}\Omega$) |
| 2 | $V_{in}^-$ (electrodo S2) |
| 3 | $V_{in}^+$ (electrodo S1) |
| 4 | $V^-$ ($-15\text{ V}$) |
| 5 | REF (referencia, a GND) |
| 6 | $V_o$ (salida diferencial amplificada) |
| 7 | $V^+$ ($+15\text{ V}$) |

| Parámetro | Valor |
| :--- | :--- |
| $R_G$ | $1\text{ k}\Omega$ (potenciómetro) |
| Ganancia real $G$ | $50.4$ V/V |
| Señal de entrada | $1\text{ mV} - 5\text{ mV}$ |
| Señal de salida esperada | $50\text{ mV} - 252\text{ mV}$ |
| CMRR | $> 90\text{ dB}$ |
| Alimentación | $\pm15\text{ V}$ |

---

### 3.3 Etapa 2: Filtro Pasa-Altas Activo — 20 Hz (LM358)

#### Objetivo

Eliminar la componente de continua (offset DC), la deriva electroquímica de los electrodos y los artefactos de baja frecuencia (movimiento corporal, respiración) que se encuentran por debajo de 20 Hz, conservando intacta la banda de interés EMG (20–500 Hz).

#### Topología y función de transferencia

Se selecciona la topología **Sallen-Key de segundo orden con aproximación Butterworth** ($Q = 0.707$). La función de transferencia del filtro pasa-altas es:

$$H(s) = \frac{s^2/\omega_c^2}{s^2/\omega_c^2 + \dfrac{\sqrt{2}\,s}{\omega_c} + 1}$$

donde $\omega_c = 2\pi f_c$ y los coeficientes Butterworth de segundo orden son:

$$a_1 = \sqrt{2} = 1.4142, \qquad Q = \frac{1}{a_1} = \frac{1}{\sqrt{2}} \approx 0.707$$

#### Fórmula de frecuencia de corte

Para la topología Sallen-Key HP con capacitores iguales $C_1 = C_2 = C$:

$$f_c = \frac{1}{2\pi C \sqrt{R_1 R_2}}$$

#### Cálculo de componentes

Se fijan $C_1 = C_2 = 1\text{ }\mu\text{F}$ y se aplica la condición Butterworth $R_1 = 2R_2$ para obtener $Q = 0.707$.

$$f_c = \frac{1}{2\pi \cdot C \cdot \sqrt{2R_2 \cdot R_2}} = \frac{1}{2\pi \cdot C \cdot R_2\sqrt{2}}$$

Despejando $R_2$ para $f_c = 20\text{ Hz}$:


$$R_2 = \frac{1}{2\pi \cdot f_c \cdot C \cdot \sqrt{2}} = \frac{1}{2\pi \cdot 20 \cdot 1\times10^{-6} \cdot \sqrt{2}}$$

$$R_2 = \frac{1}{2\pi \cdot 20 \cdot 1.4142 \times 10^{-6}} = \frac{1}{1.7772\times10^{-4}} \approx 5{,}627\text{ }\Omega \approx 5.6\text{ k}\Omega$$

$$R_1 = 2 \times R_2 = 2 \times 5.6\text{ k}\Omega = 11.2\text{ k}\Omega \approx 11\text{ k}\Omega$$

#### Ganancia del op-amp interno

Para la topología Sallen-Key se fija ganancia $G = 2$ con $R_3 = R_4$:

$$G = 1 + \frac{R_4}{R_3} = 2 \implies R_3 = R_4 = 10\text{ k}\Omega$$

#### Valores comerciales seleccionados

| Componente | Valor calculado | Valor comercial | Tolerancia |
| :--- | :--- | :--- | :--- |
| $R_1$ | $11.26\text{ k}\Omega$ | $11\text{ k}\Omega$ | 1% |
| $R_2$ | $5.63\text{ k}\Omega$ | $5.6\text{ k}\Omega$ | 1% |
| $C_1 = C_2$ | $1\text{ }\mu\text{F}$ | $1\text{ }\mu\text{F}$ | 5% |
| $R_3 = R_4$ | — | $10\text{ k}\Omega$ c/u | 1% |

#### Verificación con valores comerciales

$$f_c = \frac{1}{2\pi \cdot 1\times10^{-6} \cdot \sqrt{11\times10^3 \cdot 5.6\times10^3}}$$

$$= \frac{1}{2\pi \cdot 1\times10^{-6} \cdot \sqrt{61.6\times10^6}}$$

$$= \frac{1}{2\pi \cdot 1\times10^{-6} \cdot 7{,}848}$$

$$\boxed{f_c = \frac{1}{0.04933} \approx 20.3\text{ Hz} \checkmark}$$

#### Análisis de sensibilidad por tolerancia (±5% en capacitores)

Peor caso — ambos capacitores 5% por encima del nominal:

$$f_{c,min} = \frac{f_c}{\sqrt{1.05 \times 1.05}} = \frac{20.3}{1.05} \approx 19.3\text{ Hz}$$

Peor caso — ambos capacitores 5% por debajo del nominal:

$$f_{c,max} = \frac{f_c}{\sqrt{0.95 \times 0.95}} = \frac{20.3}{0.95} \approx 21.4\text{ Hz}$$

El rango de variación $[19.3\text{ Hz},\, 21.4\text{ Hz}]$ es aceptable y no compromete la banda de señal EMG. ✓

---

### 3.4 Etapa 3: Filtro Pasa-Bajas Activo — 450 Hz (LM358)

#### Objetivo

Limitar el contenido espectral de la señal a la banda de interés EMG (hasta ~500 Hz), evitar el aliasing durante la conversión analógico-digital y atenuar el ruido térmico y electromagnético de alta frecuencia fuera de la banda útil.

#### Topología y función de transferencia

Misma topología **Sallen-Key de segundo orden con aproximación Butterworth**. La función de transferencia del filtro pasa-bajas es:

$$H(s) = \frac{G}{1 + \dfrac{\sqrt{2}\,s}{\omega_c} + \dfrac{s^2}{\omega_c^2}}$$

con $\omega_c = 2\pi f_c$, $a_1 = \sqrt{2}$, $Q = 0.707$.

#### Fórmula de frecuencia de corte

$$f_c = \frac{1}{2\pi\sqrt{R_1 R_2 C_1 C_2}}$$

#### Cálculo de componentes

Se adopta diseño con capacitores asimétricos para obtener resistencias en valores comerciales estándar. Se fijan $C_1 = 10\text{ nF}$ y $C_2 = 22\text{ nF}$:

Para $f_c = 450\text{ Hz}$:

$$f_c = \frac{1}{2\pi\sqrt{R_1 R_2 \cdot 10\times10^{-9} \cdot 22\times10^{-9}}}$$

$$450 = \frac{1}{2\pi\sqrt{R_1 R_2 \cdot 2.2\times10^{-16}}}$$

$$\sqrt{R_1 R_2} = \frac{1}{2\pi \cdot 450 \cdot \sqrt{2.2\times10^{-16}}} = \frac{1}{2\pi \cdot 450 \cdot 1.483\times10^{-8}}$$

$$\sqrt{R_1 R_2} = \frac{1}{4.192\times10^{-5}} = 23{,}854\text{ }\Omega$$

$$R_1 R_2 = (23{,}854)^2 = 5.69\times10^8\ \Omega^2$$

Eligiendo $R_1 = 33\text{ k}\Omega$:

$$R_2 = \frac{5.69\times10^8}{33\times10^3} = 17{,}242\text{ }\Omega \approx 18\text{ k}\Omega$$

#### Ganancia del op-amp interno

Para Butterworth LP con $Q = 0.707$:

$$G = 1 + \frac{R_4}{R_3} = 1.5 \implies R_4 = 0.5 \cdot R_3$$

Con $R_3 = 20\text{ k}\Omega$ y $R_4 = 10\text{ k}\Omega$.

#### Valores comerciales seleccionados

| Componente | Valor calculado | Valor comercial | Tolerancia |
| :--- | :--- | :--- | :--- |
| $R_1$ | $33\text{ k}\Omega$ | $33\text{ k}\Omega$ | 1% |
| $R_2$ | $17.2\text{ k}\Omega$ | $18\text{ k}\Omega$ | 1% |
| $C_1$ | $10\text{ nF}$ | $10\text{ nF}$ | 10% |
| $C_2$ | $22\text{ nF}$ | $22\text{ nF}$ | 10% |
| $R_3$ | — | $20\text{ k}\Omega$ | 1% |
| $R_4$ | — | $10\text{ k}\Omega$ | 1% |

#### Verificación con valores comerciales

$$f_c = \frac{1}{2\pi\sqrt{33\times10^3 \cdot 18\times10^3 \cdot 10\times10^{-9} \cdot 22\times10^{-9}}}$$

Calculando paso a paso:

$$R_1 \cdot R_2 = 33{,}000 \times 18{,}000 = 5.94\times10^8\ \Omega^2$$

$$C_1 \cdot C_2 = 10\times10^{-9} \times 22\times10^{-9} = 2.2\times10^{-16}\ \text{F}^2$$

$$R_1 R_2 C_1 C_2 = 5.94\times10^8 \times 2.2\times10^{-16} = 1.307\times10^{-7}$$

$$\sqrt{1.307\times10^{-7}} = 3.615\times10^{-4}$$

$$\boxed{f_c = \frac{1}{2\pi \cdot 3.615\times10^{-4}} \approx 440\text{ Hz} \checkmark}$$

El valor de 440 Hz está dentro del rango especificado (450 ± 10%). ✓

#### Análisis de sensibilidad por tolerancia (±10% en capacitores)

Peor caso — ambos capacitores 10% por encima:

$$f_{c,min} = \frac{440}{1.1} \approx 400\text{ Hz}$$

Peor caso — ambos capacitores 10% por debajo:

$$f_{c,max} = \frac{440}{0.9} \approx 489\text{ Hz}$$

El rango $[400\text{ Hz},\, 489\text{ Hz}]$ permanece por debajo de los 500 Hz especificados como límite de Nyquist para $f_s = 1\text{ kHz}$, confirmando robustez del diseño. ✓

---

### 3.5 Etapa 4: Acondicionamiento DC — LM741

#### Objetivo

Desplazar el nivel de continua de la señal filtrada para centrarla dentro del rango unipolar $0-5\text{ V}$ requerido por el ADC del Arduino UNO, que no admite tensiones negativas en su pin analógico.

#### Principio de operación

El LM741 se configura como **sumador no inversor** que añade un offset de referencia $V_{ref} \approx +2.5\text{ V}$ a la señal procesada, centrando la señal de salida en el punto medio del rango del ADC. Esto maximiza el aprovechamiento de los 10 bits de resolución disponibles:

$$V_{out} = V_{señal} + V_{ref} = V_{señal} + 2.5\text{ V}$$

$$\text{Rango resultante: } 0\text{ V} \leq V_{out} \leq 5\text{ V}$$

#### Configuración de pines LM741

| Pin | Señal |
| :--- | :--- |
| 1, 5 | Offset Null (compensación de offset interno) |
| 2 | $V_{in}^-$ (entrada inversora) |
| 3 | $V_{in}^+$ (entrada no inversora) |
| 4 | $V^-$ ($-15\text{ V}$) |
| 6 | $V_o$ (salida hacia ADC) |
| 7 | $V^+$ ($+15\text{ V}$) |

---

### 3.6 Etapa 5: Conversión Analógico-Digital — Arduino UNO

| Parámetro | Valor |
| :--- | :--- |
| Resolución | 10 bits (0–1023 pasos) |
| Tensión de referencia | $V_{ref} = 5\text{ V}$ |
| Resolución por paso | $\dfrac{5\text{ V}}{1024} \approx 4.88\text{ mV/LSB}$ |
| Frecuencia de muestreo estimada | $f_s \approx 1\text{ kHz}$ |
| Protocolo de transmisión | Serial UART, 115200 bps |

#### Verificación del Teorema de Nyquist-Shannon

La frecuencia de muestreo de 1 kHz debe ser al menos el doble de la frecuencia máxima de la señal:

$$f_s \geq 2 \cdot f_{max} \implies 1\text{ kHz} \geq 2 \times 500\text{ Hz} = 1\text{ kHz} \checkmark$$

La condición se cumple en el límite. El filtro LP a 450 Hz garantiza que no existan componentes espectrales por encima de 500 Hz que puedan causar aliasing. ✓

---

### 3.7 Etapa 6: Procesamiento Digital en MATLAB

#### 3.7.1 Filtro Notch IIR a 60 Hz

Durante las pruebas se identificó interferencia residual de la red eléctrica a 60 Hz no suprimida completamente por la etapa analógica, debido a la ausencia de aislamiento galvánico completo entre la fuente NI ELVIS III y la red AC. Se implementó un **filtro Notch IIR** en MATLAB para su supresión digital.

**Cálculo de la frecuencia normalizada:**

$$\omega_0 = \frac{f_0}{f_s/2} = \frac{60\text{ Hz}}{1000\text{ Hz}/2} = \frac{60}{500} = 0.12$$

**Cálculo del ancho de banda:**

$$BW = \frac{\omega_0}{Q} = \frac{0.12}{30} = 0.004$$

Los coeficientes del filtro se obtienen en MATLAB con:

```matlab
[b, a] = iirnotch(0.12, 0.004);
```

El factor de calidad $Q = 30$ garantiza una banda de rechazo estrecha centrada en 60 Hz que no afecta las componentes espectrales adyacentes de la señal EMG (en particular las componentes a 40 Hz y 80 Hz permanecen intactas).

**Respuesta en frecuencia esperada:** atenuación mayor a 40 dB en $f_0 = 60\text{ Hz}$ con ancho de banda de rechazo de $BW = Q/f_0 = 2\text{ Hz}$.

#### 3.7.2 Envolvente RMS con remoción dinámica de offset

La envolvente RMS se calcula sobre una ventana deslizante de $N$ muestras, precedida de remoción dinámica del offset DC para compensar la deriva de línea base:

$$V_{RMS}[n] = \sqrt{\frac{1}{N}\sum_{k=n-N+1}^{n}\bigl(x[k] - \bar{x}\bigr)^2}$$

donde $\bar{x}$ es el valor medio local calculado dinámicamente. Este procesamiento convierte la señal oscilatoria de alta frecuencia en una representación suave de la energía instantánea del músculo, directamente proporcional al nivel de activación muscular.

---

### 3.8 Resumen de Componentes Implementados

| Etapa | Componente diseño original | Componente implementado | Justificación |
| :--- | :--- | :--- | :--- |
| Amplificador de instrumentación | AD620 | **INA128** | Disponibilidad en laboratorio; especificaciones equivalentes; mismo pinout |
| Filtros activos (HP y LP) | TL084 (JFET) | **LM358** | Accesibilidad comercial; opera correctamente en la banda de trabajo |
| Acondicionamiento offset | No especificado | **LM741** | Necesidad identificada durante implementación para compatibilidad con ADC |
| Alimentación | ±9 V baterías | **±15 V NI ELVIS III** | Mayor margen de operación; implicaciones de seguridad en Ficha 4 |
| Supresión 60 Hz | No contemplada | **Notch IIR digital (MATLAB)** | Interferencia residual por ausencia de aislamiento galvánico completo |

---

### 3.9 Criterios de Integración entre Bloques

La cadena de acondicionamiento se diseñó bajo el principio de **impedancias en cascada**: la impedancia de salida de cada bloque debe ser significativamente menor que la impedancia de entrada del bloque siguiente, garantizando que no exista efecto de carga que degrade la señal en la interfaz entre etapas.

Los amplificadores operacionales en configuración Sallen-Key presentan alta impedancia de entrada y baja impedancia de salida de forma inherente. La impedancia de entrada diferencial del INA128 ($> 10\text{ G}\Omega$) asegura una interfaz no invasiva con la piel del sujeto.

La banda de paso resultante del sistema analógico completo queda definida entre **20 Hz** (filtro HP) y **440 Hz** (filtro LP), cubriendo la banda de interés EMG superficial del gastrocnemio con margen adecuado en ambos extremos.