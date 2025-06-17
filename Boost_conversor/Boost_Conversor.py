import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do conversor Boost
Vin = 12              # Tensão de entrada [V]
Vout = 36             # Tensão de saída [V]
Po = 108              # Potência de saída [W]
fs = 100e3            # Frequência de chaveamento [Hz]
T = 1 / fs            # Período de chaveamento [s]

# 1. Razão cíclica
D = 1 - (Vin / Vout)

# 2. Corrente de saída
Io = Po / Vout

# 3. Corrente de entrada média
Iin = Po / Vin

# 4. Ondulação no indutor (30%)
delta_IL = 0.3 * Iin

# 5. Indutância
L = (Vin * D) / (fs * delta_IL)

# 6. Ondulação na tensão de saída (2%)
delta_Vo = 0.02 * Vout

# 7. Capacitância mínima
C = (Io * D) / (fs * delta_Vo)

# Mostrar valores calculados
print(f"Razão Cíclica (D): {D:.4f}")
print(f"Corrente de entrada: {Iin:.2f} A")
print(f"Corrente de saída: {Io:.2f} A")
print(f"Ondulação de corrente: {delta_IL:.2f} A")
print(f"Indutor necessário: {L * 1e6:.2f} µH")
print(f"Capacitor necessário: {C * 1e6:.2f} µF")

# 8. Simulação do comportamento do indutor
t = np.linspace(0, 2*T, 1000)  # 2 ciclos
IL = Iin + (delta_IL/2) * np.sign(np.sin(2 * np.pi * fs * t))  # Corrente idealizada

# 9. Tensão de saída com ondulação simulada
Vo = Vout + (delta_Vo/2) * np.sin(2 * np.pi * fs * t)

# 10. Corrente no diodo
Id = np.where(np.mod(t, T) > D*T, IL, 0)

# Gráficos
plt.figure(figsize=(12, 8))

# Corrente no indutor
plt.subplot(3, 1, 1)
plt.plot(t * 1e6, IL, label='Corrente no Indutor', color='blue')
plt.ylabel('Corrente [A]')
plt.title('Corrente no Indutor')
plt.grid(True)
plt.legend()

# Tensão de saída com ondulação
plt.subplot(3, 1, 2)
plt.plot(t * 1e6, Vo, label='Tensão de Saída', color='green')
plt.ylabel('Tensão [V]')
plt.title('Tensão de Saída com Ondulação')
plt.grid(True)
plt.legend()

# Corrente no diodo
plt.subplot(3, 1, 3)
plt.plot(t * 1e6, Id, label='Corrente no Diodo', color='red')
plt.xlabel('Tempo [µs]')
plt.ylabel('Corrente [A]')
plt.title('Corrente no Diodo')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
