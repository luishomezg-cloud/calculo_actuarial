# Simulador de Cálculo Actuarial según decreto 1833 de 2026 modificado por decreto 1296 de 2022

## Descargo de responsabilidades

> El contenido y los algoritmos desarrollados en este repositorio (calculadora_actuarial) han sido creados exclusivamente con fines educativos y académicos y no pretende ser un sustituto de las herramientas oficiales dispuestas por las entidades Colombianas autorizadas tales como [Soy Actuario](https://www.soyactuario.com.co/home), y las Administradoras de Fondos de Pensiones.
> 
> El autor **no posee ni representa a ninguna entidad, institución financiera o autoridad regulatoria oficial**. Los cálculos, proyecciones y resultados obtenidos a través de esta herramienta son de carácter puramente ilustrativo y educativo.
> 
> En consecuencia, el autor **no se hace responsable** por el uso de este software en entornos de producción, ni por decisiones financieras, legales, comerciales o de cualquier otra índole tomadas con base en dichos resultados. El uso de esta herramienta corre bajo el total y propio riesgo del usuario.

Este repositorio se desarrolla con el fin de lograr una mayor comprensión de la forma en que se realizan los cálculos actuariales en Colombia según las normas establecidas por las instituciones responsables.

A continuación una breve descripción de las formulas tenidas en cuenta para su desarrollo, según las normas citadas en el título de este documento:


## Formula General de Cálculo actuarial.

$$\boxed{VRA = \left[\left(PR \times FAC_{1}\right) + \left(AR \times FAC_{2}\right)\right] \times FAC_{3}}$$

### Pensión de referencia $PR$

$$PR = SR \times TR$$
### Salario de referencia $SR$.
$$SR = SB \times \dfrac{SMN_{FR}}{SMN_{FC}}$$

* $SB$ : Salario base (El último salario a la fecha final de la omisión actualizado con el IPC mensual reportado por el DANE, bien sea a la fecha de referencia o a la fecha de corte).
* $SMN_{FR}$ : Salario Medio Nacional a la fecha de referencia, conforme registra en la tabla referida por el decreto 1833 de 2016 modificado por el decreto 1296 de 2022.
* $SMN_{FC}$ : Salario Medio Nacional a la fecha de causación, es decir, la fecha final del periodo omiso.

#### Interpolación de índices SMN cuan la edad no corresponde a un número entero:

Este paso es necesario para el cálculo del Salario de Referencia $SR$, con la mayor exactitud posible de acuerdo a la norma.

$$V_{0} = \dfrac{d_{1} \cdot V_{2} + d_{2} \cdot V_{1}}{d_{1} + d_{2}}$$

* $V_{0}$: El SMN que se desea interpolar correspondiente a una fecha intermedia.
* $V_{1}$: El SMN a la edad en años completos;
* $V_{2}$: El SMN a la edad posterior;
* $d_{1}$: Número de días trascurridos desde la fecha del último cumpleaños hasta la fecha intermedia;
* $d_{2}$: Número de días faltantes desde la fecha intermedia hasta la fecha del siguiente cumpleaños.

### Tasa de referencia $TR$.

* *Según Decreto 1833 de 2016: "La tasa de remplazo se determina adoptando las reglas establecidas en el artículo 34 de la Ley 100 de 1993, modificado por el artículo 10 de la Ley 797 de 2003, así:"*

$$TR = \left[0.655 - 0.005 \cdot \min\left[\left(\dfrac{SR}{SMMLV_{FC}}\right) , 21\right]\right] + \min \left[0.015 \cdot \left(\dfrac{(n + t) \cdot 52.18 - SemMin}{50}\right) , 0.15\right]$$

* t = *Años y fracción cotizados al sistema*
* n = *Años faltantes hasta la fecha de pensión*

*Nota: Estos valores son calculados con corte a la fecha de referencia en caso de ser anterior a la fecha de pago, o en caso contrario con corte a la fecha de pago.

### Factor actuarial uno $FAC_{1}$ ***(valor presente de una renta vitalicia)***

*Aunque existen discusiones técnicas sobre su actualización debido al incremento en la expectativa de vida, la [Resolución 1555 de 2010](https://www.fasecolda.com/wp-content/uploads/res-1555-2010.pdf) sigue siendo el estándar legal vigente para los cálculos actuariales de administradoras de pensiones y aseguradoras de vida*

$$FAC_{1} = \displaystyle\sum^{\omega - x}_{t=0}\dfrac{1}{(1 + i)^t}\cdot { }_{t}p_{x}$$

* x = *Edad de pensión*
* t = *Es el año futuro que estamos calculando (después de la pensión)*
* $\omega$ = *Es el tiempo máximo que podría vivir una persona (110 o 115 años en Colombia)*
* i = *Es la tasa de interés técnico 4% o 3% según fecha de afiliación*
* ${ }_{t}p_{x}$ = *Probabilidad de supervivencia*

### Auxilio Funerario de referencia $AR$

*Según Decreto 1833 de 2016 Artículo 2.2.4.4.2: "Definido como un valor igual a PR sin que sea inferior a cinco (5) salarios mínimos legales mensuales vigentes ni superior a diez (10) salarios mínimos legales mensuales vigentes a la fecha de corte".


### Factor actuarial dos $FAC_{2}$ ***(Auxilio Funerario)***

$$FAC_{2} = \displaystyle\sum_{t = 0}^{\omega - x} \dfrac{1}{(1 + i)^{t + 1}} \cdot {}_{t}|q_{x}$$

* ${}_{t}|q_{x}$ = *Probabilidad de fallecer en el año inmediatamente siguiente*

### Factor actuarial tres $FAC_{3}$ ***(Interés real acumulado como factor de descuento cuando FC es menor que FR)***

$$FAC_{3} = \left(1 + i\right)^\frac{FC-FR}{365,25}$$
### DTF Pensional (Actualización de la Reserva Actuarial, Protege el valor de la reserva frente a la inflación).

$$DTF Pensional_{i} = 1,03 \times\left(1 + INF_{i}\right)$$
* $TIRR$ = *Tasa Real de Rendimiento equivalente a 0,03 o 0.04 (ver norma)*
* $INF_{i}$ = *"Variación anual del Índice de Precios al Consumidor (IPC) calculado por el DANE del año calendario inmediatamente anterior"*

