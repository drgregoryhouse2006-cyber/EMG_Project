## Ficha 2. Requerimientos técnicos y especificaciones de diseño

### 2.1 Necesidad y Objetivo del Sistema
El sistema debe captar la señal diferencial proveniente de la superficie del músculo Gastrocnemio, rechazar el ruido de modo común intrínseco del cuerpo humano, amplificar la señal a un nivel manejable por instrumentación digital y filtrar las frecuencias fuera de la banda de interés electromiográfico, garantizando en todo momento la integridad física del sujeto de prueba.

### 2.2 Especificaciones Cuantitativas de Diseño
A partir de la fundamentación fisiológica (Ficha 1), se derivan los siguientes requerimientos ingenieriles:

| Parámetro | Especificación | Criterio de Diseño / Justificación |
| :--- | :--- | :--- |
| **Ganancia Total (Av)** | 1000 V/V a 2000 V/V | Elevar la señal biomédica de 1 mV - 5 mV a un rango de 1 V - 5 V para aprovechar el rango dinámico completo del ADC. |
| **CMRR** | > 90 dB | Crítico para atenuar la interferencia de 60 Hz de la red eléctrica acoplada capacitivamente al cuerpo. |
| **Impedancia de Entrada** | > 1 GΩ | Evitar el efecto de carga y pérdida de señal en la interfaz electrodo-piel (cuya impedancia es variable y alta). |
| **Frecuencia de Corte Inferior** | 20 Hz | Filtro pasa-altas para eliminar artefactos de movimiento y fluctuaciones lentas de la línea base. |
| **Frecuencia de Corte Superior** | ~450 Hz - 500 Hz | Filtro pasa-bajas para evitar *aliasing* en la digitalización y limitar el ruido térmico de alta frecuencia. |
| **Rango de Salida** | 0 a 5 V (con offset) | Acondicionamiento final para compatibilidad de nivel con el conversor Analógico-Digital unipolar del microcontrolador. |

### 2.3 Arquitectura de Filtrado, Frecuencias y Restricciones de Seguridad

Para garantizar la fidelidad de la señal biológica y la protección del paciente, la etapa de acondicionamiento analógico se rige por las siguientes especificaciones críticas:

* **Trazabilidad Fisiológica del Rango (20 Hz - 500 Hz):**
  La ventana espectral seleccionada no es arbitraria. El gastrocnemio, al estar compuesto por una mezcla de fibras de contracción rápida y lenta (Tipo I y II), concentra su mayor densidad de potencia espectral entre 50 Hz y 150 Hz.
  * *Filtro Pasa-Altas (20 Hz):* Suprime drásticamente la fluctuación de la línea base (offset DC) inducida por la respiración del paciente, los cambios electroquímicos en la interfaz piel-electrodo y los artefactos mecánicos. Mantiene la señal rigurosamente centrada.
  * *Filtro Pasa-Bajas (~450 Hz):* Este corte asegura la captura íntegra del reclutamiento de unidades motoras sin atenuación, actuando simultáneamente como filtro *anti-aliasing* para cumplir el Teorema de Nyquist-Shannon antes del ADC.

* **Selección de Respuesta Butterworth:**
  Se seleccionó la aproximación matemática de Butterworth debido a su característica de respuesta "máximamente plana" en la banda de paso. A diferencia de Chebyshev o Bessel, Butterworth garantiza que las amplitudes de los Potenciales de Acción de Unidad Motora (MUAP) no sufran atenuaciones asimétricas ni distorsiones morfológicas mientras transitan por la banda de paso.

* **Topología Sallen-Key con Filtros Activos:**
  La implementación física se realizará mediante filtros activos de segundo orden utilizando amplificadores operacionales con entrada JFET (TL084). La topología Sallen-Key permite un diseño modular en cascada sin efecto de carga, gracias a la altísima impedancia de entrada y baja impedancia de salida de los operacionales, facilitando la sintonización independiente del factor de calidad (Q = 0.707) y la frecuencia.

> **Consideraciones de Seguridad Eléctrica (Rigor Normativo):**
> El diseño se adhiere a los principios de la norma **IEC 60601-1**. El sistema analógico es alimentado exclusivamente por una fuente dual aislada galvánicamente (baterías de ±9V). Esta arquitectura clasifica la etapa de captación como una parte aplicada tipo **BF (Body Floating)**. Se prohíbe el uso de fuentes de alimentación conectadas a la red pública durante la captación real para evitar la creación de bucles de tierra (*ground loops*) que degradarían el CMRR y para eliminar el 100% del riesgo de macrochoques eléctricos por corrientes de fuga hacia el paciente.