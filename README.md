# python_code_Demographic_history
En este repositorio se presentan una serie de codigos en python utilizados para graficar historia demografica y divergencia.
Se aplica en python un subprocess para correr el programa smc++ (historia demografica) a través de los 19 cromosomas y asi evitar correr uno por uno.
Se crean diccionarios para los cromosomas como para las longitudes de cada uno
Se aplica un try-except en el codigo de prueba_divergencia... para saltar los cromosomas que no pueden correrse por falta de informacion.
Se exportan las salidas de las historias demograficas y divergencias se exportan en .json 
Los archivos json se unen en el script analisis_split y genera un archivo excel con las historias demograficas y divergencias.
En el script analisis split se usan 3 codigos el primero unifica los json y calcula una mediana de historia demografica y divergencia y se grafica. El segundo grafica las divergencias de cada individuo vs su poblacion. Finalmente el tercer script unifica las medianas de la historia demografica y divergencia obtenidas en el segundo script y las grafica

