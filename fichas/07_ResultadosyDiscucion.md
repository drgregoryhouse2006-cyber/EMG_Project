## Ficha 7. Resultados y Discusión

### 7.1 Síntesis de los Principales Resultados

El sistema de adquisición de señales EMG superficiales desarrollado durante las cuatro semanas de práctica cumplió el objetivo central planteado en la Ficha 2: capturar, acondicionar y visualizar la actividad eléctrica del músculo gastrocnemio de forma identificable y reproducible.

Los resultados concretos obtenidos se resumen a continuación:

| Resultado | Valor obtenido | Especificación original | Cumplimiento |
| :--- | :--- | :--- | :--- |
| Ganancia total del sistema analógico | ~19.3 V/V (INA128, $R_G = 2.7\text{ k}\Omega$) + ganancia de etapas de filtrado | 1000–2000 V/V | Parcial — ganancia distribuida entre etapas analógica y digital |
| Banda de paso analógica | 20 Hz – ~450 Hz | 20 Hz – 500 Hz | ✓ Cumplido |
| Supresión de interferencia 60 Hz | Efectiva mediante Notch IIR digital (Q=30) | CMRR > 90 dB (analógico) | Parcial — compensada digitalmente |
| Rango de salida ADC | 0 – 5 V (sin saturación observada) | 0 – 5 V | ✓ Cumplido |
| Identificación de contracciones musculares | 3 a 4 eventos claramente diferenciados en envolvente RMS | Señal fisiológicamente coherente | ✓ Cumplido |
| Resolución de adquisición | 10 bits (~4.88 mV/LSB) | No especificada formalmente | Aceptable para prototipo académico |

La señal EMG adquirida presentó los patrones morfológicos esperados para el músculo gastrocnemio: bursts de activación con envolvente irregular durante la contracción voluntaria y retorno al nivel basal durante el reposo, consistente con la naturaleza estocástica de los Potenciales de Acción de Unidad Motora (MUAP) descrita en la Ficha 1.

---

### 7.2 Análisis Crítico del Comportamiento del Sistema

#### 7.2.1 Etapa de amplificación diferencial

El INA128 demostró un desempeño adecuado como etapa de entrada. La ganancia programada de $A_v \approx 19.3\text{ V/V}$ resultó conservadora respecto al rango de 1000–2000 V/V especificado inicialmente, lo cual es una decisión de diseño válida para evitar saturación prematura ante fluctuaciones de la línea base y artefactos de movimiento. La ganancia total del sistema se completó mediante las etapas de filtrado activo y el procesamiento digital en MATLAB.

La alta impedancia de entrada diferencial del INA128 (típicamente >10 GΩ en modo diferencial) garantizó una interfaz no invasiva con la piel, preservando la integridad de la señal biológica en la frontera electrodo-tejido.

#### 7.2.2 Etapas de filtrado activo

Los filtros Sallen-Key de segundo orden implementados con LM358 operaron dentro de la banda de diseño. La frecuencia de corte del filtro pasa-altas (20 Hz) fue efectiva para eliminar la deriva lenta de la línea base entre contracciones. La frecuencia de corte del filtro pasa-bajas (~450 Hz) limitó correctamente el contenido espectral antes de la digitalización, actuando como filtro anti-aliasing para la frecuencia de muestreo de 1 kHz.

Se observó que la sustitución del TL084 (especificado en la Ficha 3) por el LM358 no degradó perceptiblemente la respuesta en la banda de interés, aunque el LM358 presenta limitaciones de slew rate y ancho de banda que podrían manifestarse en diseños con frecuencias de corte más elevadas.

#### 7.2.3 Cadena digital — Arduino UNO y MATLAB

La cadena de adquisición digital funcionó de forma continua y estable durante las sesiones de prueba. La comunicación serial a 115200 bps entre el Arduino y MATLAB no presentó pérdidas de datos perceptibles en las sesiones registradas.

El filtro Notch IIR implementado en MATLAB (Q=30, $f_0 = 60\text{ Hz}$) resultó indispensable para obtener una señal visualmente limpia. Este resultado revela que la atenuación de la interferencia de red en la etapa analógica fue insuficiente, consecuencia directa de la ausencia de aislamiento galvánico completo al utilizar el NI ELVIS III como fuente de alimentación.

El algoritmo de envolvente RMS con remoción dinámica de offset representó el resultado de mayor utilidad práctica: transformó una señal oscilatoria de difícil interpretación directa en una representación clara de los episodios de activación muscular, con contracciones individuales perfectamente delimitadas.

---

### 7.3 Discusión Técnica de las Fuentes de Error

#### 7.3.1 Interferencia de modo común (60 Hz)

La fuente principal de ruido en el sistema fue la interferencia de la red eléctrica a 60 Hz, acoplada capacitivamente al cuerpo del sujeto y conducida hacia el circuito a través de la tierra compartida entre el NI ELVIS III y el computador conectado por USB. Esta condición degradó el CMRR efectivo del sistema respecto al valor teórico del INA128, obligando a implementar supresión digital adicional.

**Cuantificación del impacto:** sin el filtro Notch digital, la componente de 60 Hz habría sido la componente dominante del espectro de la señal, enmascarando completamente la actividad muscular de interés concentrada entre 50 Hz y 150 Hz.

#### 7.3.2 Deriva de la línea base (offset dinámico)

Se observó un desplazamiento lento y progresivo del nivel DC de la señal a lo largo de las sesiones de adquisición. Este fenómeno tiene dos orígenes identificables:

- **Electroquímico:** cambios en el potencial de media celda de los electrodos Ag/AgCl durante la adquisición, causados por variaciones en la concentración iónica en la interfaz electrodo-gel-piel.
- **Mecánico:** micro-desplazamientos de los cables de caimán que modifican la geometría de contacto y por tanto la impedancia de la interfaz.

La remoción dinámica de offset implementada en MATLAB mitigó este efecto de forma efectiva, aunque introduce una latencia en la respuesta ante cambios rápidos del nivel basal.

#### 7.3.3 Artefactos de movimiento

El evento de alta amplitud (~1100 unidades ADC) registrado al final de la sesión extendida se identifica como un artefacto de movimiento por desplazamiento físico del electrodo. Morfológicamente se distingue de la actividad muscular real por su forma impulsional y amplitud desproporcionada respecto a las contracciones voluntarias. Este tipo de artefacto es intrínseco al uso de electrodos con conexión por caimán sin adhesivo.

#### 7.3.4 Incertidumbre en la frecuencia de muestreo

La frecuencia de muestreo de 1 kHz declarada en el script de MATLAB es una estimación basada en el tiempo de ciclo nominal del Arduino UNO. En la práctica, el bucle de adquisición del Arduino no es determinista: está sujeto a interrupciones internas del microcontrolador y a la latencia variable del puerto serial. Esta incertidumbre temporal implica que el eje de muestras de las gráficas no es estrictamente equivalente a un eje temporal calibrado, lo que limitaría cualquier análisis cuantitativo de frecuencia basado en la FFT de la señal adquirida.

---

### 7.4 Limitaciones del Diseño Implementado

1. **Sin aislamiento galvánico real:** la alimentación desde el NI ELVIS III, conectado a la red eléctrica, impide clasificar el sistema como Tipo BF según IEC 60601-1 en sentido estricto. Esta es la limitación más significativa para una eventual aplicación clínica.

2. **Ganancia total distribuida de forma no óptima:** la ganancia analógica fue conservadora (~19 V/V), lo que trasladó la carga de amplificación al dominio digital. Aunque funcional, un diseño con mayor ganancia analógica aprovecharía mejor el rango dinámico del ADC antes de la digitalización, mejorando la relación señal-cuantización.

3. **ADC de 10 bits:** la resolución de ~4.88 mV/LSB es suficiente para visualización, pero insuficiente para análisis cuantitativo de MUAPs individuales, cuya amplitud puede estar en el rango de décimas de milivoltio.

4. **Electrodo de referencia no optimizado:** la ubicación del electrodo de referencia sobre el maléolo lateral es una solución práctica, pero no es el sitio de menor potencia eléctrica del cuerpo. Una ubicación sobre prominencia ósea sin actividad muscular subyacente (cresta tibial, por ejemplo) mejoraría el rechazo de modo común.

5. **Sin calibración del sistema:** no se realizó una calibración formal de la ganancia total con señal de referencia conocida, por lo que las amplitudes en unidades ADC no pueden convertirse a milivoltios con trazabilidad metrológica.

---

### 7.5 Posibles Mejoras y Desarrollos Futuros

| Mejora | Impacto esperado | Complejidad |
| :--- | :--- | :--- |
| Alimentación con baterías ±9V aisladas | Elimina la interferencia de 60 Hz en origen; aislamiento galvánico real | Baja |
| Resistencias de protección en entradas (10–47 kΩ) | Protección ante transitorios eléctricos en la interfaz con el sujeto | Baja |
| Filtro Notch analógico a 60 Hz (Twin-T) | Elimina dependencia del software para supresión de interferencia de red | Media |
| ADC externo de 12–16 bits (ADS1115, MCP3204) | Mejora la resolución de cuantización y permite análisis cuantitativo | Media |
| Electrodos adhesivos Ag/AgCl con gel conductor | Elimina artefactos de movimiento por desplazamiento de caimanes | Baja |
| Frecuencia de muestreo calibrada con timer de hardware | Eje temporal preciso; habilita análisis espectral cuantitativo (FFT) | Media |
| Implementación de FFT en tiempo real en MATLAB | Visualización del espectro de potencia EMG para análisis de fatiga muscular | Alta |
| Clasificación de patrones gestuales (ML) | Aplicación en interfaces hombre-máquina y control de prótesis | Alta |

### 7.6 Conclusión General

El proyecto demostró que es posible diseñar e implementar un sistema funcional de adquisición de biopotenciales EMG con componentes de bajo costo y herramientas de laboratorio académico estándar. El proceso evidenció la importancia del diseño por etapas, la documentación sistemática de las decisiones de ingeniería y la capacidad de adaptar el diseño original ante las restricciones reales del entorno de implementación.

Las discrepancias entre el diseño teórico y la implementación final — sustitución de componentes, cambio de fuente de alimentación, adición del filtro Notch digital — no constituyen errores del proceso sino evidencia del ciclo de ingeniería real: diseñar, implementar, observar y ajustar. La bitácora técnica registra ese proceso con precisión, cumpliendo el propósito central de la práctica.