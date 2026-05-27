## Ficha 4. Consideraciones normativas, éticas y de seguridad

### 4.1 Marco Normativo Aplicable

El diseño e implementación de sistemas de adquisición de biopotenciales está regulado por normas internacionales que establecen los requisitos mínimos de seguridad eléctrica para equipos en contacto con el cuerpo humano. Las referencias normativas relevantes para este sistema son:

| Norma | Alcance |
| :--- | :--- |
| **IEC 60601-1** | Requisitos generales de seguridad básica y prestaciones esenciales para equipos electromédicos. |
| **IEC 60601-1-2** | Compatibilidad electromagnética (CEM) de equipos electromédicos. |
| **ANSI/AAMI ES60601-1** | Versión adoptada en América del estándar IEC 60601-1. |
| **IEC 60601-2-25** *(referencia)* | Requisitos particulares para electrocardiógrafos; aplicable por analogía a sistemas de adquisición superficial de biopotenciales. |

> **Nota de alcance:** Este sistema es un prototipo de laboratorio académico con fines de aprendizaje. No está certificado como dispositivo médico ni cumple la totalidad de los requisitos de la IEC 60601-1 en su versión formal. Las consideraciones normativas aquí descritas sirven como marco de referencia técnica y no como declaración de conformidad.

---

### 4.2 Clasificación del Sistema según IEC 60601-1

Según los criterios de la norma IEC 60601-1, el sistema puede clasificarse de la siguiente manera:

| Criterio | Clasificación | Justificación |
| :--- | :--- | :--- |
| **Tipo de parte aplicada** | Tipo **BF** *(Body Floating)* | Los electrodos superficiales Ag/AgCl hacen contacto con la piel intacta del sujeto. No existe contacto cardíaco directo. |
| **Grado de protección** | Clase II *(diseño)* | El diseño original contemplaba aislamiento galvánico total mediante baterías de ±9V. |
| **Modo de operación** | Continuo | La señal se adquiere de forma ininterrumpida durante el período de prueba. |

---

### 4.3 Análisis de Riesgos: Diseño vs. Implementación Real

Durante la fase de implementación se introdujo una modificación respecto al diseño original que tiene implicaciones directas en la seguridad eléctrica del sistema. Esta discrepancia se documenta de forma transparente:

**Diseño original (Ficha 2):** alimentación mediante dos baterías de 9V en configuración dual (±9V), completamente aisladas de la red eléctrica. Esta arquitectura garantizaba aislamiento galvánico total y clasificación tipo BF sin riesgo de corrientes de fuga.

**Implementación real:** la fuente de alimentación dual fue provista por la plataforma **NI ELVIS III**, cuya fuente variable interna está alimentada desde la red eléctrica de 120V AC a través de un transformador interno. Aunque el NI ELVIS III proporciona salidas DC reguladas, introduce una referencia de tierra compartida con el computador conectado por USB al Arduino UNO.

#### Tabla de análisis de riesgos identificados

| Riesgo | Origen | Nivel | Medida de mitigación aplicada |
| :--- | :--- | :--- | :--- |
| Corriente de fuga hacia el sujeto | Tierra compartida NI ELVIS III – USB – Arduino | **Medio** | Prueba realizada con compañero del equipo, consciente del procedimiento. Corrientes de fuga del NI ELVIS III dentro de límites de diseño del fabricante. |
| Bucle de tierra *(ground loop)* | Referencia común entre fuente y PC | **Medio** | Se verificó ausencia de sensación eléctrica por parte del sujeto durante toda la prueba. |
| Degradación del CMRR | Ruido de modo común de la red eléctrica (60 Hz) | **Bajo** | Se implementó filtro Notch digital a 60 Hz en MATLAB como compensación activa. |
| Macrochoques eléctricos | Ausencia de aislamiento galvánico total | **Bajo** | Voltajes de operación limitados a ±15V DC. El sujeto no presentó ninguna reacción adversa. |
| Artefactos mecánicos | Cables de caimán sin fijación rígida | **Bajo** | Sujeto en reposo durante la adquisición. |

> **Conclusión del análisis:** El nivel de riesgo real de la implementación se considera bajo en el contexto de laboratorio académico supervisado, dado que los voltajes de operación son bajos, el sujeto es un miembro del equipo con pleno conocimiento del procedimiento, y no se registró ninguna reacción adversa. Sin embargo, para una implementación clínica o con sujetos externos, esta arquitectura **requeriría** retornar al diseño original con baterías aisladas.

---

### 4.4 Consideraciones de Seguridad Eléctrica en la Interfaz con el Sujeto

#### Protección en las entradas del amplificador de instrumentación

En la implementación realizada, los electrodos superficiales Ag/AgCl se conectaron directamente a las entradas diferenciales del INA128 mediante cables con terminales de caimán, **sin resistencias de protección en serie**. Esta decisión implica lo siguiente:

- **Riesgo:** ante una falla del IC o un pico transitorio, no existe limitación de corriente entre el punto de medición y el sujeto.
- **Mitigación por contexto:** el INA128 opera con voltajes de alimentación de ±15V y su rango de entrada diferencial está protegido internamente. En condiciones normales de operación, la corriente que puede fluir a través de la piel es del orden de microamperios, muy por debajo del umbral de percepción (~1 mA) y del umbral de fibrilación ventricular (~100 mA para corriente DC, >>10 mA para AC).
- **Recomendación para mejora:** incorporar resistencias de 10 kΩ a 47 kΩ en serie con cada entrada del InAmp y diodos de protección hacia las rieles de alimentación, como práctica estándar en diseño de equipos electromédicos.

---

### 4.5 Aspectos Éticos

#### Consentimiento del sujeto de prueba

La prueba de adquisición fue realizada sobre un integrante voluntario del propio equipo de trabajo. Si bien no se formalizó un documento de consentimiento informado escrito, el procedimiento cumplió con los principios éticos mínimos aplicables en el contexto académico:

- El sujeto fue informado verbalmente del procedimiento completo antes de iniciar.
- El sujeto tenía pleno conocimiento de los componentes del circuito y sus niveles de operación.
- La participación fue completamente voluntaria y el sujeto tenía libertad de interrumpir la prueba en cualquier momento.
- No se registraron datos personales sensibles ni se almacenaron imágenes del sujeto con fines de identificación.

#### Uso de los datos adquiridos

Las señales EMG registradas son utilizadas exclusivamente con fines académicos dentro del marco de la asignatura. No serán publicadas, compartidas con terceros ni utilizadas fuera del contexto de este proyecto.

#### Reflexión ética sobre adquisición de biopotenciales

La adquisición de señales eléctricas del cuerpo humano, aunque superficial y no invasiva en este caso, involucra principios éticos fundamentales de la bioingeniería: **autonomía** del sujeto, **beneficencia** (el procedimiento no debe causar daño), **no maleficencia** y **justicia**. En proyectos futuros con sujetos externos al equipo, se recomienda implementar un protocolo formal de consentimiento informado alineado con la **Declaración de Helsinki** y los lineamientos del comité de ética institucional.