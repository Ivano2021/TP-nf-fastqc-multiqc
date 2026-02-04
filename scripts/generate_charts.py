#!/usr/bin/env python3
"""
Script para generar gráficos de los resultados del benchmark
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import numpy as np
import os

# Crear directorio para gráficos
os.makedirs('docs/charts', exist_ok=True)

# Datos del benchmark
datasets = ['10MB\n(20MB)', '50MB\n(99MB)', '100MB\n(197MB)', '500MB\n(984MB)']
datasets_simple = ['20MB', '99MB', '197MB', '984MB']
secuencial = [36.8, 48.5, 65.3, 140.0]
paralelo = [12.6, 15.1, 18.0, 30.0]
speedup = [2.9, 3.2, 3.6, 4.7]

# Colores
COLOR_SEQ = '#e74c3c'  # Rojo
COLOR_PAR = '#27ae60'  # Verde
COLOR_SPEEDUP = '#3498db'  # Azul

# ============================================
# GRÁFICO 1: Comparación de tiempos (barras)
# ============================================
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(datasets))
width = 0.35

bars1 = ax.bar(x - width/2, secuencial, width, label='Secuencial', color=COLOR_SEQ, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, paralelo, width, label='Paralelo', color=COLOR_PAR, edgecolor='black', linewidth=1.2)

# Etiquetas en las barras
for bar, val in zip(bars1, secuencial):
    ax.annotate(f'{val}s', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords='offset points', ha='center', fontsize=11, fontweight='bold')

for bar, val in zip(bars2, paralelo):
    ax.annotate(f'{val}s', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords='offset points', ha='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Tamaño de datos (por archivo / total)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de ejecución (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Comparación de Tiempos: Ejecución Secuencial vs Paralela\n(8 archivos FASTQ procesados con FASTP + FastQC + MultiQC)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(datasets, fontsize=11)
ax.legend(fontsize=12, loc='upper left')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 160)

plt.tight_layout()
plt.savefig('docs/charts/01_comparacion_tiempos.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 1: Comparación de tiempos")

# ============================================
# GRÁFICO 2: Speedup
# ============================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(datasets_simple, speedup, color=COLOR_SPEEDUP, edgecolor='black', linewidth=1.2, width=0.6)

# Etiquetas en las barras
for bar, val in zip(bars, speedup):
    ax.annotate(f'{val}x', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords='offset points', ha='center', fontsize=14, fontweight='bold')

ax.set_xlabel('Tamaño total de datos', fontsize=12, fontweight='bold')
ax.set_ylabel('Speedup (veces más rápido)', fontsize=12, fontweight='bold')
ax.set_title('Speedup: Paralelo vs Secuencial\n(Mayor es mejor)', fontsize=14, fontweight='bold', pad=15)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Baseline (sin mejora)')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 6)
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig('docs/charts/02_speedup.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 2: Speedup")

# ============================================
# GRÁFICO 3: Tiempo ahorrado
# ============================================
tiempo_ahorrado = [s - p for s, p in zip(secuencial, paralelo)]

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(datasets_simple, tiempo_ahorrado, color='#9b59b6', edgecolor='black', linewidth=1.2, width=0.6)

# Etiquetas en las barras
for bar, val in zip(bars, tiempo_ahorrado):
    ax.annotate(f'{val:.0f}s', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords='offset points', ha='center', fontsize=14, fontweight='bold')

ax.set_xlabel('Tamaño total de datos', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo ahorrado (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Tiempo Ahorrado usando Ejecución Paralela', fontsize=14, fontweight='bold', pad=15)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('docs/charts/03_tiempo_ahorrado.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 3: Tiempo ahorrado")

# ============================================
# GRÁFICO 4: Líneas - Tendencia de tiempos
# ============================================
fig, ax = plt.subplots(figsize=(10, 6))

data_sizes = [20, 99, 197, 984]

ax.plot(data_sizes, secuencial, 'o-', color=COLOR_SEQ, linewidth=3, markersize=12, label='Secuencial')
ax.plot(data_sizes, paralelo, 's-', color=COLOR_PAR, linewidth=3, markersize=12, label='Paralelo')

# Anotar puntos
for i, (x, y_seq, y_par) in enumerate(zip(data_sizes, secuencial, paralelo)):
    ax.annotate(f'{y_seq}s', (x, y_seq), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
    ax.annotate(f'{y_par}s', (x, y_par), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=10)

ax.set_xlabel('Tamaño total de datos (MB)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de ejecución (segundos)', fontsize=12, fontweight='bold')
ax.set_title('Escalabilidad: Tiempo vs Tamaño de Datos', fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1050)
ax.set_ylim(0, 160)

plt.tight_layout()
plt.savefig('docs/charts/04_escalabilidad.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 4: Escalabilidad")

# ============================================
# GRÁFICO 5: Gráfico combinado (dashboard)
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Barras de tiempo
ax1 = axes[0, 0]
x = np.arange(len(datasets_simple))
width = 0.35
ax1.bar(x - width/2, secuencial, width, label='Secuencial', color=COLOR_SEQ)
ax1.bar(x + width/2, paralelo, width, label='Paralelo', color=COLOR_PAR)
ax1.set_xlabel('Tamaño de datos')
ax1.set_ylabel('Tiempo (s)')
ax1.set_title('Tiempos de Ejecución', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(datasets_simple)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Subplot 2: Speedup
ax2 = axes[0, 1]
ax2.bar(datasets_simple, speedup, color=COLOR_SPEEDUP)
ax2.axhline(y=1, color='red', linestyle='--', alpha=0.5)
ax2.set_xlabel('Tamaño de datos')
ax2.set_ylabel('Speedup (x)')
ax2.set_title('Factor de Aceleración', fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
for i, v in enumerate(speedup):
    ax2.text(i, v + 0.1, f'{v}x', ha='center', fontweight='bold')

# Subplot 3: Líneas de tendencia
ax3 = axes[1, 0]
ax3.plot(data_sizes, secuencial, 'o-', color=COLOR_SEQ, linewidth=2, markersize=8, label='Secuencial')
ax3.plot(data_sizes, paralelo, 's-', color=COLOR_PAR, linewidth=2, markersize=8, label='Paralelo')
ax3.set_xlabel('Tamaño de datos (MB)')
ax3.set_ylabel('Tiempo (s)')
ax3.set_title('Tendencia de Escalabilidad', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Subplot 4: Porcentaje de mejora
ax4 = axes[1, 1]
mejora_pct = [(s-p)/s*100 for s, p in zip(secuencial, paralelo)]
colors = plt.cm.Greens(np.linspace(0.4, 0.8, len(mejora_pct)))
bars = ax4.bar(datasets_simple, mejora_pct, color=colors)
ax4.set_xlabel('Tamaño de datos')
ax4.set_ylabel('Reducción de tiempo (%)')
ax4.set_title('% de Tiempo Reducido', fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
for i, v in enumerate(mejora_pct):
    ax4.text(i, v + 1, f'{v:.0f}%', ha='center', fontweight='bold')

plt.suptitle('Dashboard de Resultados: Benchmark de Paralelismo\n(Pipeline FastQC + MultiQC con Nextflow y Docker)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('docs/charts/05_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 5: Dashboard completo")

# ============================================
# GRÁFICO 6: Pie chart - Distribución de tiempo (500MB)
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Secuencial
ax1 = axes[0]
labels = ['FASTP\n(8 archivos)', 'FastQC\n(8 archivos)', 'MultiQC']
# Tiempos aproximados del trace 500MB secuencial
sizes_seq = [56, 64, 2]  # ~8s x 7 + ~8s x 8 + ~2s
colors_seq = ['#e74c3c', '#f39c12', '#9b59b6']
ax1.pie(sizes_seq, labels=labels, autopct='%1.0f%%', colors=colors_seq, startangle=90)
ax1.set_title(f'Secuencial\n({sum(sizes_seq)}s total)', fontweight='bold')

# Paralelo
ax2 = axes[1]
sizes_par = [11, 10, 2]  # Todos en paralelo
colors_par = ['#27ae60', '#2ecc71', '#1abc9c']
ax2.pie(sizes_par, labels=labels, autopct='%1.0f%%', colors=colors_par, startangle=90)
ax2.set_title(f'Paralelo\n({sum(sizes_par)}s total)', fontweight='bold')

plt.suptitle('Distribución del Tiempo por Proceso (Set 500MB)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/charts/06_distribucion_tiempo.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Gráfico 6: Distribución de tiempo")

print("\n" + "="*50)
print("✅ Todos los gráficos generados en docs/charts/")
print("="*50)
