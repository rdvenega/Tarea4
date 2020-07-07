# Tarea 4 Modelos Probabilisticos de Señales y Sistemas
# Grupo 2
# Estudiante: Rubén Venegas Zúñiga - Carné: B78278
# Profesor: Fabián Abarca Calderón

import csv, operator #Operador que permite usar archivos .csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import integrate
from scipy import signal

###### Obtencion de datos csv ##############
datos =[]
with open('bits10k.csv') as csvarchivo: #Se abre el archivo lote.csv
    entrada = csv.reader(csvarchivo) #Se guarda en entrada los datos de csv
    for inp in entrada: #Se recorre cada linea de entrada
        datos.append(int(inp[0]))
bits = np.array(datos)

### PARTE 1 ################################

# Número de bits
N =  len(bits)

# Frecuencia de operación
f = 5000 # Hz

# Duración del período de cada símbolo (onda)
T = 1/f 

# Número de puntos de muestreo por período
p = 50

# Puntos de muestreo para cada período
tp = np.linspace(0, T, p)

# Creación de la forma de onda de la portadora
sinus = np.sin(2*np.pi * f * tp)

# Frecuencia de muestreo
fs = p/T 

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*p)

# Inicialización de el vector de la señal modulada Tx
senal = np.zeros(t.shape)

# Creación de la señal modulada BPSK
for k, b in enumerate(bits):
    if (b == 1):
        senal[k*p:(k+1)*p] = sinus
    else:
        senal[k*p:(k+1)*p] = -sinus

# Visualización de los primeros bits modulados
pb = 5
print(bits[0:pb])
plt.figure()
plt.title('Señal modulada')
plt.plot(senal[0:pb*p])
plt.show()

### PARTE 2 ################################

# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)
BER_array = []
print('Potencia promedio de la señal: ', Ps, ' W')

SNR = -2
for n in range(0,6):
    ### PARTE 3 ################################
    # Relación señal-a-ruido deseada
    print('SNR: ', SNR)

    # Potencia del ruido para SNR y potencia de la señal dadas
    Pn = Ps / (10**(SNR / 10))

    # Desviación estándar del ruido
    sigma = np.sqrt(Pn)

    # Creacion de ruido (Pn = sigma^2)
    ruido = np.random.normal(0, sigma, senal.shape)

    # Simulacion de "el canal": señal recibida
    Rx = senal + ruido

    # Visualización de los primeros bits recibidos

    pb = 5
    plt.figure()
    title = 'SNR = ' + str(SNR) +  '. Canal ruidoso' 
    plt.title(title)
    plt.plot(Rx[0:pb*p])
    plt.show()

    ### PARTE 4 ################################

    # Antes del canal ruidoso
    fw, PSD = signal.welch(senal, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.title('Antes del canal ruidoso' )
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.show()

    # Después del canal ruidoso
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure()
    title = 'SNR = ' + str(SNR) + '. Despues del canal ruidoso' 
    plt.title(title)
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.show()


    ### PARTE 5 ################################

    # Inicialización del vector de bits recibidos
    bitsRx = np.zeros(bits.shape)

    # Decodificación de la señal por detección de energía
    for k, b in enumerate(bits):
        Ep = np.sum(Rx[k*p:(k+1)*p] * sinus)
        if (Ep > 0):
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0

    err = np.sum(np.abs(bits - bitsRx))
    BER = err/N
    print('SNR =', SNR, '. Hay un total de {} errores en {} bits para una tasa de error de {}.'.format(err, N, BER))
    BER_array.append(BER)
    SNR = SNR + 1

### PARTE 6 ################################
plt.figure()
SNR = np.linspace(-2,3,6)
BER = np.array(BER_array)
plt.xlabel('SNR')
plt.ylabel('BER')
plt.title('SNR vs. BER')
plt.plot(SNR, BER, 'ro')
plt.show()
