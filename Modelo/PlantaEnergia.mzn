% Ejecutar con solver COIN-BC:

% Lectura de entradas:
array[1..3, 1..2] of int: plantaEnergetica;
int: dias;
int: clientes;
array[1..clientes, 1..dias] of int: demanda;
int: diasRegimen;
float: porcentaje;

% Variables:

% Producción de cada planta para cada día:
array[1..3, 1..dias] of var int: produccion;

% Restricciones:

% Validación de producciones y capacidades:
constraint forall(i in 1..3, j in 1..dias)(produccion[i,j] >= 0 /\ produccion[i,j] <= plantaEnergetica[i,1]);

% Validación de satisfacción de demanda:
constraint forall(i in 1..dias)(sum(produccion[1..3,i]) >= sum(demanda[1..clientes,i]));

% Validación de régimen alto:
constraint not exists(i in 1..dias, j in 1..dias where j-i+1 == diasRegimen)(forall(k in i..j)(produccion[2,k] > plantaEnergetica[2,1]*porcentaje));

% Función objetivo:
var float: costoTotal;
constraint costoTotal = sum(i in 1..3, j in 1..dias)(produccion[i,j] * plantaEnergetica[i,2]);
solve minimize costoTotal;

% Salida:
output ["\nProducción de cada planta para cada día:\n\n\(produccion[1, 1..dias])\n\(produccion[2, 1..dias])\n\(produccion[3, 1..dias])\n\nCosto Total: \(costoTotal)"];
