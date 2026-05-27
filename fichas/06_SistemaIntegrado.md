## Ficha 6. Prueba de Funcionamiento del Sistema Integrado

### 6.1 Descripción del Sistema Integrado

La prueba de funcionamiento del sistema completo se realizó con todas las etapas operando de forma encadenada y continua, desde la captación de la señal biológica hasta su visualización procesada en pantalla. El sistema integrado comprende las siguientes etapas en cascada:

```
Electrodos Ag/AgCl → INA128 → Filtro HP (20 Hz) → Filtro LP (~450 Hz) → 
Offset LM741 → ADC Arduino UNO → Puerto Serial → MATLAB (Notch + RMS)
```

---

### 6.2 Condiciones de Adquisición

| Parámetro | Valor | Observación |
| :--- | :--- | :--- |
| **Músculo registrado** | Gastrocnemio (gemelar) | Electrodo activo sobre el vientre muscular, referencia sobre maléolo |
| **Tipo de electrodo** | Ag/AgCl superficial | Conexión mediante terminales de caimán |
| **Frecuencia de muestreo** | ~1000 Hz | Estimada; determinada por el ciclo de lectura del Arduino UNO |
| **Resolución ADC** | 10 bits | Rango 0–1023 unidades digitales, $V_{ref} = 5\text{ V}$ |
| **Baudrate serial** | 115200 bps | Comunicación Arduino → PC |
| **Alimentación analógica** | ±15 V DC | Fuente variable NI ELVIS III |
| **Alimentación digital** | 5 V USB | Arduino UNO alimentado desde PC |
| **Frecuencia notch digital** | 60 Hz | Filtro IIR Notch, factor de calidad Q = 30 |
| **Posición del sujeto** | Sentado, pierna en reposo | Músculo en estado relajado entre contracciones |
| **Tipo de contracción** | Voluntaria isométrica | Flexión plantar sin desplazamiento articular |

---

### 6.3 Procedimiento de Prueba del Sistema Completo

El procedimiento se ejecutó en el siguiente orden:

1. **Preparación de la piel:** limpieza superficial de la zona de colocación de electrodos con algodón para reducir la impedancia electrodo-piel.

2. **Colocación de electrodos:** electrodo activo (+) sobre el vientre del gastrocnemio medial, electrodo activo (−) a 2 cm de distancia sobre el mismo músculo, electrodo de referencia (tierra) sobre el maléolo lateral.

3. **Energización del circuito:** activación de la fuente dual ±15V del NI ELVIS III, verificación de tensiones con multímetro antes de conectar electrodos al sujeto.

4. **Verificación de reposo:** con el músculo relajado, se verificó que la señal en MATLAB presentara amplitud baja y estable, confirmando ausencia de saturación o ruido excesivo.

5. **Adquisición de contracciones:** se solicitó al sujeto realizar contracciones voluntarias del gastrocnemio (flexión plantar) separadas por períodos de reposo de 2 a 3 segundos.

6. **Registro continuo:** el script de MATLAB registró la señal en tiempo real, aplicando el filtro Notch de 60 Hz de forma continua y actualizando la gráfica con una ventana deslizante.

7. **Post-procesamiento RMS:** una vez finalizada la adquisición, se aplicó el algoritmo de envolvente RMS con remoción dinámica de offset para obtener la representación de activación muscular.

---

### 6.4 Registros Obtenidos

#### 6.4.1 Señal EMG filtrada — Contracción individual

![EMG filtrada - contracción única](/imagenes/emg_contraccion_unica.jpg)

*Fig. 1 — Señal EMG con filtro Notch 60 Hz activo durante una contracción muscular individual (~600 muestras). El burst de activación es claramente identificable alrededor de la muestra 200, con amplitud pico de aproximadamente 1000 unidades ADC. La relación señal-ruido es adecuada para la identificación del evento.*

#### 6.4.2 Señal EMG filtrada — Ventana media

![EMG filtrada - ventana media](/imagenes/emg_ventana_media.jpg)

*Fig. 2 — Señal EMG con filtro Notch activo en ventana de ~2500 muestras. Se aprecia un evento de contracción dominante alrededor de la muestra 1000 con amplitud máxima de ~80 unidades, y actividad muscular de menor intensidad en el resto del registro. La escala de amplitud en esta sesión refleja un nivel de esfuerzo muscular diferente respecto a la sesión de la Fig. 1.*

#### 6.4.3 Señal EMG filtrada — Sesión extendida

![EMG filtrada - sesión completa](/imagenes/emg_sesion_completa.jpg)

*Fig. 3 — Registro completo de sesión de adquisición (~18000 muestras, ~18 segundos). Se observan múltiples eventos de contracción con amplitud variable a lo largo de la sesión. El evento de mayor amplitud (~1100 unidades ADC) registrado hacia el final del registro se atribuye a un artefacto de movimiento por desplazamiento del electrodo.*

#### 6.4.4 Envolvente RMS — Representación de activación muscular

![EMG procesada - envolvente RMS](/imagenes/emg_rms.jpg)

*Fig. 4 — Envolvente RMS de la señal EMG con remoción dinámica de offset. Se identifican entre 3 y 4 eventos de contracción muscular con amplitudes entre 20 y 42 unidades normalizadas. La línea base entre contracciones permanece estable gracias al algoritmo de remoción de offset.*

---

### 6.5 Evaluación de la Calidad de la Señal

| Criterio | Evaluación | Detalle |
| :--- | :--- | :--- |
| **Identificación de contracciones** | ✓ Satisfactoria | Los eventos de activación muscular son claramente distinguibles del ruido de fondo en todas las pruebas. |
| **Relación señal-ruido (SNR)** | Aceptable | La amplitud del burst de activación supera significativamente el nivel de ruido en reposo. SNR estimado visualmente > 10:1. |
| **Supresión de 60 Hz** | ✓ Efectiva | El filtro Notch IIR (Q=30) eliminó la componente de interferencia de red de forma consistente. |
| **Estabilidad de la línea base** | Moderada | Se observa deriva lenta del nivel DC entre contracciones, corregida por remoción dinámica de offset en software. |
| **Ausencia de saturación** | ✓ Confirmada | La señal acondicionada se mantuvo dentro del rango 0–5V del ADC durante toda la prueba. |
| **Reproducibilidad** | ✓ Confirmada | El patrón de activación muscular fue reproducible en múltiples contracciones de la misma sesión. |

---

### 6.6 Limitaciones Observadas

**1. Deriva de la línea base (offset dinámico):** se observó un desplazamiento lento del nivel DC de la señal, atribuible a cambios progresivos en la impedancia electrodo-piel durante la adquisición. Fue necesario compensarlo algorítmicamente en MATLAB.

**2. Artefactos de movimiento:** el evento de alta amplitud registrado al final de la sesión extendida (~1100 unidades ADC) corresponde a un artefacto por desplazamiento físico del electrodo, no a actividad muscular real. Un sistema con electrodos adhesivos reduciría significativamente este tipo de artefacto.

**3. Frecuencia de muestreo no certificada:** la frecuencia de muestreo de 1 kHz es una estimación basada en el tiempo de ciclo del Arduino UNO. No se realizó una calibración formal del ADC, por lo que el eje temporal de las gráficas está expresado en muestras y no en segundos.

**4. Ausencia de aislamiento galvánico:** como se documentó en la Ficha 4, la alimentación desde el NI ELVIS III introduce una referencia de tierra compartida con el computador, lo que incrementa la susceptibilidad a interferencia de 60 Hz respecto al diseño original con baterías.

**5. Resolución ADC de 10 bits:** la resolución del ADC del Arduino UNO ($\frac{5\text{ V}}{1024} \approx 4.88\text{ mV/LSB}$) es suficiente para la visualización general de la señal EMG, pero limita la capacidad de detectar MUAPs de muy baja amplitud en registros de precisión clínica.

---

### 6.7 Análisis Preliminar del Desempeño Global

El sistema integrado demostró ser funcional para el propósito académico planteado: la adquisición, filtrado y visualización de señales EMG superficiales del músculo gastrocnemio.

La cadena analógica (INA128 → LPF → HPF → offset) acondicionó la señal dentro del rango operable del ADC sin saturación. La etapa digital (filtro Notch + envolvente RMS) complementó el acondicionamiento analógico y proveyó una representación clara de la actividad muscular.

Las limitaciones identificadas son coherentes con las restricciones propias de un prototipo de laboratorio académico y no comprometen la validez del proceso de aprendizaje. Un sistema de mayor fidelidad requeriría: aislamiento galvánico real, frecuencia de muestreo calibrada, ADC de mayor resolución (≥ 12 bits) y electrodos con fijación adhesiva.