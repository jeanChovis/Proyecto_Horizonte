
CONSIGNA

Implemente en Python el algoritmo para calcular el sueldo a pagar a un trabajador
de la empresa "Horizonte”; aplicando el desarrollo guiado por pruebas y control de
versiones.
El trabajador percibe las siguientes bonificaciones:
1. Por cada hora extra se le paga 50% más que una hora normal.
2. Bonificación por movilidad igual a 1000.
3. Bonificación suplementaria igual al 3% del sueldo básico (sueldo).
4. La bonificación total es la suma de todas las bonificaciones que percibe.
Asimismo, el trabajador está sujeto a los siguientes descuentos:
1. Las tardanzas y faltas se descuentan con respecto a remuneración
computable. La remuneración computable es igual al sueldo básico más la
suma de todas las bonificaciones excepto la bonificación por horas extras.
2. El total de descuentos se obtiene sumando todos los descuentos.

ALGORITMO GENERAL

1. Ingreso de datos
2. Cálculo el sueldo a pagar
3. Imprime boleta de pago.

PRIMER REFINAMIENTO

1. Ingreso de datos.
1.1. Ingreso del nombre del trabajador (nombreTrabajador) y sueldo
básico (sueldoBasico).
1.2. Ingreso de días de faltas (diasFalta) y minutos de tardanzas
(minutosTardanza).
1.3. Ingreso de horas extras (horasExtras).
2. Cálculo el sueldo a pagar.
2.1. Cálculo de bonificaciones (bonifaciones).
Instrucciones:
• Desarrolle las actividades solicitadas.
• Recuerde que sólo se calificarán los aportes que se realicen antes de la fecha
de vencimiento de la entrega.

Construcción de software

2.2. Cálculo de descuentos (descuentos).
2.3. sueldoNeto=sueldoBasico+bonificaciones+descuentos.
3. Imprimir boleta de pago.

SEGUNDO REFINAMIENTO

2.1. Cálculo de bonificaciones.
2.1.1. Pago por horas extras (pagoHorasExtras)= 1.50 * horasExtras

* sueldoBasico / 30 / 8.
Para incrementar 50% a X, es suficiente multiplicar a la cantidad
por 1.50 porque 100% de X + 25% de X es 150% de X que a su vez
es igual a 1.50*X.
El pago por una hora normal es igual al resultado de
sueldoBasico/30/8. El sueldo básico corresponde al mes y está
dividido entre 30 días que tiene el mes y este resultado es dividido
entre 8 que es la cantidad de horas que se trabaja durante un
día.

2.1.2. movilidad=1000.
2.1.3. bonificacionSuplementaria=0.03*sueldoBasico.
2.1.4. bonificaciones=movilidad + bonificacionSuplementaria

+ pagoHorasExtras.

2.1.5. remuneracionComputable= sueldoBasico + movilidad

+ bonificacionSuplementaria.

2.2. Cálculo de descuentos
2.2.1. remuneracionMinima=sueldoBasico+bonificacion.
2.2.2. DescuentoFaltas = remuneracionComputable / 30 * diasFalta.
Para obtener el descuento por falta: la remuneración
computable se divide entre la cantidad de días que tiene el mes,
el mes comercial tiene 30 días.

2.2.3. descuentoTardanzas= remuneracionComputable / 30 / 8 / 60

* minutosTardanza.
Para obtener el descuento por la tardanza: la remuneración
computable se divide secuencialmente entre la cantidad de
días que tiene el mes, entre la cantidad de horas trabajadas por
día y entre la cantidad de minutos que tiene una hora.
2.2.4. descuentos= DescuentoFaltas + descuentoTardanzas.