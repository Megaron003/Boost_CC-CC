import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 1. Definir parâmetros do projeto
Vin = 12.0       # Tensão de entrada [V]
Vout = 24.0      # Tensão de saída desejada [V]
Pout = 50.0      # Potência de saída [W]
fsw = 50e3       # Frequência de chaveamento [Hz]
Ts = 1/fsw       # Período de chaveamento [s]
delta_IL = 0.3   # Ondulação de corrente no indutor (30% da corrente média)
delta_Vout = 0.02 # Ondulação de tensão na saída (2% da tensão de saída)

# 2. Cálculos preliminares
D = 1 - (Vin / Vout)  # Razão cíclica
Iout = Pout / Vout     # Corrente de saída
Iin = Pout / Vin       # Corrente de entrada
Rload = Vout**2 / Pout # Resistência de carga

# 3. Dimensionamento dos componentes
L = (Vin * D * Ts) / (delta_IL * Iin)          # Indutância
C = (Iout * D * Ts) / (delta_Vout * Vout)      # Capacitância

print("Parâmetros do projeto:")
print(f"Razão cíclica D: {D:.4f}")
print(f"Indutância L: {L*1e6:.2f} µH")
print(f"Capacitância C: {C*1e6:.2f} µF")

# 4. Simulação do conversor
def boost_converter(x, t, D, Ts, Vin, Rload, L, C):
    iL, vC = x
    
    # Determina o estado do interruptor
    if (t % Ts) < (D * Ts):
        # Primeira etapa - S fechado
        diLdt = Vin / L
        dvCdt = -vC / (Rload * C)
    else:
        # Segunda etapa - S aberto
        diLdt = (Vin - vC) / L
        dvCdt = (iL - vC/Rload) / C
    
    return [diLdt, dvCdt]

# Configuração da simulação
t_sim = np.linspace(0, 0.01, 10000)  # 10ms de simulação
x0 = [Iin, Vin]  # Condições iniciais

# Executar simulação
sol = odeint(boost_converter, x0, t_sim, args=(D, Ts, Vin, Rload, L, C))
iL_sim, vC_sim = sol.T

# 5. Visualização dos resultados
plt.figure(figsize=(12, 8))

# Corrente no indutor
plt.subplot(2, 1, 1)
plt.plot(t_sim*1000, iL_sim)
plt.title('Corrente no Indutor')
plt.xlabel('Tempo [ms]')
plt.ylabel('Corrente [A]')
plt.grid(True)

# Tensão de saída
plt.subplot(2, 1, 2)
plt.plot(t_sim*1000, vC_sim)
plt.title('Tensão de Saída')
plt.xlabel('Tempo [ms]')
plt.ylabel('Tensão [V]')
plt.grid(True)

plt.tight_layout()
plt.show()

# 6. Análise em regime permanente
steady_state_start = int(0.8 * len(t_sim))
iL_ss = iL_sim[steady_state_start:]
vC_ss = vC_sim[steady_state_start:]

iL_avg = np.mean(iL_ss)
vC_avg = np.mean(vC_ss)
iL_ripple = np.max(iL_ss) - np.min(iL_ss)
vC_ripple = np.max(vC_ss) - np.min(vC_ss)

print("\nResultados em regime permanente:")
print(f"Tensão média de saída: {vC_avg:.2f} V (desejado: {Vout} V)")
print(f"Corrente média no indutor: {iL_avg:.2f} A (teórico: {Iin:.2f} A)")
print(f"Ripple de corrente no indutor: {iL_ripple:.2f} A ({iL_ripple/iL_avg*100:.1f}%)")
print(f"Ripple de tensão na saída: {vC_ripple:.2f} V ({vC_ripple/vC_avg*100:.1f}%)")