import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=plt.cbook.mplDeprecation)
import pandas as pd

import openai
openai.api_key = "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"

# Limpiar la consola
print("\033c")

# Leer el archivo CSV
df = pd.read_csv('DATA.csv')

# Calcular la calidad del agua y redondear a 2 decimales
df['calidad_agua'] = round(98.03 - 36.45 * (df['pH'] - 7.0) - 0.48 * df['Turbiedad'] - 0.1 * df['Dureza total'] + 0.09 * df['Alcalinidad total'] + 0.07 * df['Conductividad'] + 0.01 * df['Fósforo total'], 2)

print("\n" + " Bienvenido a HydroIQ ".center(50, "-") + "\n")

# creado por
print("Creado por Carlos Veryan y Diego Partida\n")

print("Aquí puedes agregar nuevos datos para calcular la calidad del agua y obtener recomendaciones para mejorarla.\n")

# Preguntar al usuario si quiere agregar un nuevo dato
while True:
    print("¿Desea agregar un nuevo dato?")
    if input("\nY/N: ") == 'Y':
        # Agregar un nuevo dato
        df = df.append({'Fecha': input("Fecha: "), 'pH': float(input("pH: ")), 'Turbiedad': float(input("Turbiedad: ")), 'Dureza total': float(input("Dureza total: ")), 'Alcalinidad total': float(input("Alcalinidad total: ")), 'Conductividad': float(input("Conductividad: ")), 'Fósforo total': float(input("Fósforo total: "))}, ignore_index=True)
        # Calcular la calidad del agua y redondear a 2 decimales
        df['calidad_agua'] = round(98.03 - 36.45 * (df['pH'] - 7.0) - 0.48 * df['Turbiedad'] - 0.1 * df['Dureza total'] + 0.09 * df['Alcalinidad total'] + 0.07 * df['Conductividad'] + 0.01 * df['Fósforo total'], 2)

        # Guardar los datos en el archivo CSV
        df.to_csv('DATA.csv', index=False)

        # Preguntar a openai si el agua es potable
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt="""Teniendo en cuenta la fórumla para calcular la calidad del agua:

            Calidad del agua = 98.03 - 36.45 * (pH - 7.0) - 0.48 * Turbiedad - 0.1 * Dureza total + 0.09 * Alcalinidad total + 0.07 * Conductividad + 0.01 * Fósforo total

            Y teniendo en cuenta los siguientes datos:
            ph: """ + str(df['pH'][len(df) - 1]) + """
            Turbiedad: """ + str(df['Turbiedad'][len(df) - 1]) + """
            Dureza total: """ + str(df['Dureza total'][len(df) - 1]) + """
            Alcalinidad total: """ + str(df['Alcalinidad total'][len(df) - 1]) + """
            Conductividad: """ + str(df['Conductividad'][len(df) - 1]) + """
            Fósforo total: """ + str(df['Fósforo total'][len(df) - 1]) + """

            Obtenemos un resultado de """ + str(df['calidad_agua'][len(df) - 1]) + """.

            Explicame cómo afecta cada uno de estos datos a la calidad del agua y que ocurre en cada parte de la fórmula para llegar al resultado final, menciona la calidad actual del agua en escala buena-moderada-mala, y da recomendaciones para mejorar la calidad del agua.
            """,
            max_tokens=3000,
            temperature=0
        )
        print("\n" + " Resultado ".center(50, "-") + "\n")
        print(completion.choices[0].text)
        print("\n" + " ".center(50, "-") + "\n")
    else:
        break

# Imprimir el resultado y al lado su fecha
print("\n" + " Resultados ".center(50, "-") + "\n")
for i in range(len(df)):
    print(df['Fecha'][i], end=': ')
    print(df['calidad_agua'][i])

# Grafica de línea
plt.plot(df['Fecha'], df['calidad_agua'])
plt.title('Calidad del agua (linea)')
plt.xlabel('Fecha')
plt.ylabel('Calidad del agua')
plt.xticks(rotation=45)
plt.gcf().canvas.set_window_title('HydroIQ Gráfico de línea')
plt.show()

# Grafica de barras
plt.bar(df['Fecha'], df['calidad_agua'])
plt.title('Calidad del agua (barras)')
plt.xlabel('Fecha')
plt.ylabel('Calidad del agua')
plt.xticks(rotation=45)
plt.gcf().canvas.set_window_title('HydroIQ Gráfico de barras')
plt.show()

"""
Casos de prueba: 
ph: 8.42
Turbiedad: 12.1
Dureza total: 261.4
Alcalinidad total: 504
Conductividad: 1192
Fósforo total: 3.62

Casos de prueba: 
ph: 7.42
Turbiedad: 4.5
Dureza total: 261.4
Alcalinidad total: 549.9
Conductividad: 1536
Fósforo total: 5.27

Casos de prueba: 
pH: 7.05
Turbiedad: 17.3
Dureza total: 71.04
Alcalinidad total: 229.11
Conductividad: 528.0
Fósforo total: 0.81
"""