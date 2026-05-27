## Ficha 5. Implementación y pruebas por etapas

### 5.1 Descripción General del Proceso de Implementación

La implementación del sistema se desarrolló en tres fases progresivas: prototipado en protoboard para validación funcional por bloques, fabricación de PCB perforada para integración permanente del circuito analógico, y validación digital mediante adquisición y procesamiento en MATLAB. Este enfoque incremental permitió identificar y corregir problemas en cada etapa antes de avanzar a la siguiente.

---

### 5.2 Fase 1 — Prototipo en Protoboard

#### 5.2.1 Evidencia de montaje

![Prototipo inicial en protoboard](/imagenes/protoboard_prototipo.jpg)

*Fig. 1 — Prototipo inicial sobre protoboard. Se observan los ICs de la etapa de filtrado, el Arduino UNO para adquisición digital y la fuente de laboratorio para alimentación dual.*

#### 5.2.2 Objetivo de esta fase

Verificar el funcionamiento individual de cada bloque (amplificación, filtrado pasa-altas, filtrado pasa-bajas, offset) antes de comprometer el diseño en una PCB permanente. Esta fase permite realizar ajustes de componentes sin costo adicional.

#### 5.2.3 Procedimiento de prueba

1. Se montaron las etapas de filtrado activo (LM358) en protoboard.
2. Se verificó la alimentación dual con multímetro antes de energizar el circuito.
3. Se aplicó una señal de prueba desde el generador de funciones del NI ELVIS III para verificar la respuesta en frecuencia de cada filtro por separado.
4. Se conectó el Arduino UNO al pin de salida y se verificó la recepción de datos por el monitor serial.

#### 5.2.4 Resultados y observaciones

- La etapa de filtrado respondió correctamente a señales de prueba en el rango de 20 Hz a 500 Hz.
- Se identificó la necesidad de un filtro Notch digital adicional para suprimir la interferencia residual de 60 Hz, no contemplada inicialmente como etapa analógica separada.
- El prototipo confirmó la viabilidad del diseño antes de proceder a la PCB.

---

### 5.3 Fase 2 — Implementación en PCB Perforada

#### 5.3.1 Evidencia de montaje

![PCB implementada - vista frontal](/imagenes/pcb_frontal.jpg)

*Fig. 2 — PCB perforada con el circuito analógico completo. De izquierda a derecha: terminales de entrada S1/S2 y alimentación V+/GND/V−, amplificador de instrumentación INA128, etapas de filtrado con LM358, etapa de offset con LM741, terminal de salida Vo/GND.*

![Sistema completo en NI ELVIS III](/imagenes/sistema_elvis.jpg)

*Fig. 3 — Sistema integrado sobre plataforma NI ELVIS III. La PCB se alimenta desde la fuente variable del ELVIS III. El Arduino UNO recibe la señal acondicionada y la transmite al computador via USB para procesamiento en MATLAB.*

#### 5.3.2 Ajustes introducidos respecto al diseño original

| Parámetro | Diseño (Ficha 3) | Implementación real | Justificación del cambio |
| :--- | :--- | :--- | :--- |
| Amplificador de instrumentación | AD620 | **INA128** | Mayor disponibilidad en laboratorio. Pinout compatible, CMRR típico equivalente (>90 dB). |
| Op-Amp etapas de filtrado | TL084 (JFET) | **LM358** | Disponibilidad comercial. Opera correctamente con la señal acondicionada en el rango de trabajo. |
| Etapa de offset | No especificada | **LM741** | Se añadió para ajuste fino del nivel DC de salida hacia el ADC del Arduino. |
| Alimentación | ±9V baterías | **±15V NI ELVIS III** | Mayor margen de operación para los op-amps. Implicaciones de seguridad documentadas en Ficha 4. |
| Filtro Notch 60 Hz | No contemplado | **Implementado en MATLAB** | La interferencia de red residual, visible en la señal digital, se suprimió mediante filtro IIR Notch digital (Q=30) en software. |

---

### 5.4 Fase 3 — Pruebas de Adquisición y Procesamiento Digital

Las pruebas de adquisición se realizaron conectando los electrodos Ag/AgCl al músculo gastrocnemio del sujeto de prueba. La señal acondicionada se digitalizó mediante el ADC del Arduino UNO (resolución de 10 bits, $V_{ref} = 5V$) a una frecuencia de muestreo estimada de **1 kHz** y se transmitió por puerto serial (baudrate: 115200) a MATLAB para procesamiento en tiempo real.

#### 5.4.1 Prueba 1 — Adquisición de contracción muscular individual

Se solicitó al sujeto realizar una contracción voluntaria del gastrocnemio y relajar el músculo. El objetivo fue verificar que el sistema captura un evento discreto de activación muscular.

![EMG filtrada - contracción única](/imagenes/emg_contraccion_unica.jpg)

*Fig. 4 — Señal EMG filtrada (sin 60 Hz) durante una contracción muscular individual. Se observa claramente el burst de activación alrededor de la muestra 200, con amplitud pico de ~1000 unidades ADC, seguido del retorno al estado de reposo.*

**Observación:** La señal presenta el patrón morfológico esperado para una contracción voluntaria: incremento rápido de amplitud durante la activación, seguido de decremento al cesar el esfuerzo. La oscilación residual post-contracción es consistente con el ruido de fondo del sistema.

#### 5.4.2 Prueba 2 — Sesión de adquisición extendida (múltiples contracciones)

Se registraron múltiples ciclos de contracción-relajación durante una sesión continua de aproximadamente 18 segundos (18000 muestras a 1 kHz).

![EMG filtrada - sesión completa](/imagenes/emg_sesion_completa.jpg)

*Fig. 5 — Señal EMG filtrada (sin 60 Hz) durante la sesión completa de adquisición. Se aprecian múltiples eventos de activación muscular a lo largo de la sesión, con un evento de mayor amplitud (~1100 unidades ADC) hacia el final del registro.*

**Observación:** La variabilidad en amplitud entre contracciones es fisiológicamente coherente y refleja diferencias en el nivel de esfuerzo muscular realizado por el sujeto.

#### 5.4.2 Prueba 1b — Ventana media con contracción dominante

![EMG filtrada - ventana media](/imagenes/emg_ventana_media.jpg)

*Fig. 5 — Señal EMG filtrada (sin 60 Hz) en ventana de ~2500 muestras. 
Se aprecia un evento de contracción dominante (~80 unidades) alrededor 
de la muestra 1000, con actividad muscular de menor intensidad dispersa 
en el resto del registro. La diferencia de escala respecto a la Fig. 4 
refleja una variación en el nivel de esfuerzo muscular entre sesiones.*

#### 5.4.3 Prueba 3 — Procesamiento RMS y detección de activación

Se implementó un algoritmo de procesamiento adicional en MATLAB para extraer la envolvente RMS de la señal, con remoción dinámica de offset y umbralización para detección de activación muscular.

![EMG procesada - envolvente RMS](/imagenes/emg_rms.jpg)

*Fig. 6 — Envolvente RMS de la señal EMG procesada. Se identifican claramente 3 a 4 eventos de contracción con amplitudes entre 20 y 42 unidades normalizadas. La remoción dinámica de offset elimina la deriva de la línea base entre contracciones.*

**Observación:** La envolvente RMS proporciona una representación limpia de la actividad muscular, adecuada para aplicaciones de detección de gestos o control de prótesis. Los picos son claramente distinguibles del nivel basal.

---

### 5.5 Síntesis de Resultados por Etapa

| Etapa | Prueba realizada | Resultado | Estado |
| :--- | :--- | :--- | :--- |
| Protoboard | Verificación funcional por bloque con señal de prueba | Respuesta en frecuencia correcta en banda 20–500 Hz | ✓ Superada |
| PCB | Adquisición de señal EMG real con electrodos superficiales | Señal capturada y transmitida correctamente al PC | ✓ Superada |
| Notch digital 60 Hz | Supresión de interferencia de red residual | Reducción efectiva de la componente de 60 Hz | ✓ Superada |
| Contracción individual | Captura de un evento discreto de activación | Burst claramente identificable, morfología coherente | ✓ Superada |
| Sesión extendida | Registro continuo de múltiples contracciones | Múltiples eventos registrados, amplitud variable | ✓ Superada |
| Envolvente RMS | Procesamiento y detección de activación muscular | Envolvente limpia, contracciones bien diferenciadas | ✓ Superada |

---

### 5.6 Discrepancias y Ajustes Registrados

1. **Interferencia de 60 Hz:** La etapa analógica no suprimió completamente la interferencia de red por la ausencia de aislamiento galvánico total (NI ELVIS III en lugar de baterías). Se compensó con filtro Notch digital en MATLAB.

2. **Deriva de línea base:** Se observó desplazamiento lento del nivel DC de la señal entre contracciones, atribuible a cambios en la impedancia electrodo-piel y al movimiento de los cables. Se corrigió mediante remoción dinámica de offset en el algoritmo MATLAB.

3. **Pico de alta amplitud en sesión extendida:** El evento de amplitud ~1100 unidades ADC registrado hacia el final de la sesión (Fig. 5) se atribuye a un artefacto de movimiento por desplazamiento del electrodo, no a actividad muscular real. Este tipo de artefacto es esperado en sistemas sin fijación rígida de electrodos.
