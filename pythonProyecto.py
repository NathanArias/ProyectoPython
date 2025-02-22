

# Proyecto: creación del codigo en python para la simulación de un parqueo.
# AUTOR: NATHANAEL ARIAS SALAS

# Definir el nombre de la empresa
nombre_empresa = "Parqueo LA PROGRA."

print(f"Bienvenido a {nombre_empresa}")

# Crear usuario y contraseña
usuario_creado = input("Crée su nombre de usuario: ")

contrasena_creada = ""
while len(contrasena_creada) < 4:
    contrasena_creada = input("Ingrese la contraseña (mínimo debe tener 4 caracteres): ")
    if len(contrasena_creada) < 4:
        print("La contraseña debe tener al menos 4 caracteres.")

# Mostrar los detalles de la cuenta creada
print(f"\nCuenta creada con éxito. Los detalles son:")
print(f"Usuario: {usuario_creado}")
print(f"Contraseña: {contrasena_creada}")

# Solicitar usuario y contraseña para entrar al sistema
print("\nPor favor, inicie sesión para continuar.")
usuario_ingreso = input("Usuario: ")
contrasena_ingreso = input("Contraseña: ")

# Validar las credenciales
while usuario_ingreso != usuario_creado or contrasena_ingreso != contrasena_creada:
    print("Usuario o contraseña incorrectos. Intente nuevamente.")
    usuario_ingreso = input("Usuario: ")
    contrasena_ingreso = input("Contraseña: ")

print("\nInicio de sesión exitoso.")

# Configuración inicial
n = int(input("Ingrese la capacidad máxima del parqueo: "))
tarifa_por_hora = float(input("Ingrese la tarifa por hora del parqueo: "))
tiempo_max_espera = int(input("Ingrese el tiempo máximo de espera permitido (en minutos): "))

tiempo_simulacion = int(input("Ingrese la duración de la simulación en horas: "))

# Variables del sistema
espacios_disponibles = n
fila_espera = 0
carros_atendidos = 0
tiempo_total_espera = 0
tiempo_total_permanencia = 0
carros_no_atendidos = 0
ingresos_totales = 0
tiempo_actual = 0

# Variables para rastrear tiempos de permanencia
vehiculos_estacionados = [0] * n  # Cada espacio representa un vehículo con su tiempo restante

# Lista para almacenar información de los vehículos
detalles_vehiculos = []

def generar_tiempo_permanencia():
    return 15 + (120 - 15) * tiempo_actual % 107  # Genera tiempo entre 15 y 120 minutos

def llegada_vehiculo():
    global espacios_disponibles, fila_espera, carros_no_atendidos, carros_atendidos
    if espacios_disponibles > 0:
        for i in range(n):
            if vehiculos_estacionados[i] == 0:
                vehiculos_estacionados[i] = generar_tiempo_permanencia()
                espacios_disponibles -= 1
                carros_atendidos += 1
                placa = input("Ingrese la placa del vehículo que acaba de llegar: ")
                detalles_vehiculos.append({"placa": placa, "horas": 0})
                break
    elif fila_espera < 10:
        fila_espera += 1
    else:
        carros_no_atendidos += 1

def procesar_fila_espera():
    global fila_espera, espacios_disponibles, tiempo_total_espera, carros_no_atendidos, carros_atendidos
    if fila_espera > 0 and espacios_disponibles > 0:
        fila_espera -= 1
        if fila_espera * tiempo_actual % 50 <= tiempo_max_espera:
            for i in range(n):
                if vehiculos_estacionados[i] == 0:
                    vehiculos_estacionados[i] = generar_tiempo_permanencia()
                    espacios_disponibles -= 1
                    carros_atendidos += 1
                    placa = input("Ingrese la placa del vehículo que pasó de la fila de espera al parqueo: ")
                    detalles_vehiculos.append({"placa": placa, "horas": 0})
                    tiempo_total_espera += fila_espera * tiempo_actual % 50
                    break
        else:
            carros_no_atendidos += 1

def salida_vehiculos():
    global espacios_disponibles, tiempo_total_permanencia, ingresos_totales
    for i in range(n):
        if vehiculos_estacionados[i] > 0:
            vehiculos_estacionados[i] -= 1
            if vehiculos_estacionados[i] == 0:
                espacios_disponibles += 1
                tiempo_permanencia = generar_tiempo_permanencia()
                tiempo_total_permanencia += tiempo_permanencia
                horas_estacionadas = int(input("Ingrese las horas de uso del parqueo para este vehículo: "))
                subtotal = tarifa_por_hora * horas_estacionadas
                iva = subtotal * 0.13
                total = subtotal + iva
                ingresos_totales += total

                # Actualizar detalles del vehículo
                for vehiculo in detalles_vehiculos:
                    if vehiculo["placa"] == input("Confirme la placa del vehículo que está saliendo: "):
                        vehiculo["horas"] = horas_estacionadas

                print(f"\nDetalles del cobro:")
                print(f"Subtotal: {subtotal:.2f} unidades monetarias")
                print(f"IVA (13%): {iva:.2f} unidades monetarias")
                print(f"Total a pagar: {total:.2f} unidades monetarias\n")

print("\nIniciando simulación...")

while tiempo_actual < tiempo_simulacion * 60:
    if espacios_disponibles == 0 and fila_espera == 0:
        print("El parqueo está lleno y no hay más vehículos en espera. Finalizando simulación anticipadamente.")
        break
    if tiempo_actual % 15 == 0:  # Llega un vehículo cada 15 minutos
        llegada_vehiculo()
    procesar_fila_espera()
    salida_vehiculos()

    tiempo_actual += 1

# Cálculo de métricas finales
ocupacion_promedio = (carros_atendidos / (n * (tiempo_simulacion * 60))) * 100
promedio_espera = tiempo_total_espera / carros_atendidos if carros_atendidos > 0 else 0
promedio_permanencia = tiempo_total_permanencia / carros_atendidos if carros_atendidos > 0 else 0

# Reporte final
print("\nReporte del día:")
print(f"Capacidad del parqueo: {n} espacios")
print(f"Carros atendidos: {carros_atendidos}")
print(f"Carros que no pudieron estacionarse: {carros_no_atendidos}")
print(f"Ingresos totales: {ingresos_totales:.2f} unidades monetarias")
print(f"Tiempo promedio de espera: {promedio_espera:.2f} minutos")
print(f"Tiempo promedio de permanencia: {promedio_permanencia:.2f} minutos")
print(f"Porcentaje promedio de ocupación: {ocupacion_promedio:.2f}%")
