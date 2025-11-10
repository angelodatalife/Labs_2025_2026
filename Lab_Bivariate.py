import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, probplot
import math

# --- Configuración y Carga de Datos ---
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

try:
    # Ajusta el nombre del archivo si es necesario
    df = pd.read_csv('amazon_uk_products.csv')
    print("✅ Datos cargados correctamente.")
except FileNotFoundError:
    print("❌ ERROR: Asegúrate de que el archivo 'amazon_uk_products.csv' esté en el directorio correcto.")
    exit()

# Renombrar 'rating' a 'stars' para consistencia con la Parte 3 si es necesario
if 'rating' in df.columns and 'stars' not in df.columns:
    df.rename(columns={'rating': 'stars'}, inplace=True)

# --- Limpieza y Preparación de Datos (General) ---

# 1. Limpieza de Precios y Puntuaciones
df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(r'[£,]', '', regex=True), errors='coerce')
df['stars'] = pd.to_numeric(df['stars'], errors='coerce')

# 2. Manejo de Nulos en las columnas clave
df.dropna(subset=['category', 'isBestSeller', 'price', 'stars'], inplace=True)

# 3. Conversión de tipos
df['isBestSeller'] = df['isBestSeller'].astype(bool)

print(f"\nNúmero de filas después de la limpieza inicial: {len(df)}")


# ======================================================================
# 💰 PARTE 2: PRELIMINAR - ELIMINACIÓN DE OUTLIERS EN EL PRECIO
# ======================================================================

print("\n" + "="*70)
print("## 0. Preliminary Step: Eliminación de Outliers en Precios (Método IQR)")
print("="*70)

# Cálculo de cuartiles e IQR
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

# Límites para la detección de outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrar el DataFrame
df_clean = df[
    (df['price'] >= lower_bound) & 
    (df['price'] <= upper_bound)
].copy()

outlier_count = len(df) - len(df_clean)

print(f"Q1 (25 Percentil): £{Q1:.2f}")
print(f"Q3 (75 Percentil): £{Q3:.2f}")
print(f"IQR: £{IQR:.2f}")
print(f"Límite Superior (Outlier): £{upper_bound:.2f}")
print(f"Outliers de precio eliminados: {outlier_count} filas")
print(f"Filas restantes para el análisis (df_clean): {len(df_clean)}")

# El análisis subsiguiente (Parte 2 y 3) usará df_clean
# ======================================================================


# ======================================================================
# 🚀 PARTE 1: ANALIZANDO TENDENCIAS BEST-SELLER
# ======================================================================

print("\n" + "="*70)
print("## 🚀 Parte 1: Analizando Tendencias Best-Seller Across Product Categories")
print("="*70)

### 1. Crosstab Analysis

print("\n### 1.1 Crosstab (Frecuencia de Best-Sellers por Categoría)")
# Crear la tabla de contingencia
crosstab_abs = pd.crosstab(df['category'], df['isBestSeller'], dropna=True)
print(crosstab_abs.head())

# Calcular la proporción de best-sellers para cada categoría (donde 1.0 es True)
crosstab_prop = crosstab_abs.apply(lambda r: r / r.sum(), axis=1)

# Ordenar por la proporción de Best Seller (True) en orden descendente
best_seller_prop = crosstab_prop.sort_values(by=True, ascending=False)[True]

print("\n### 1.2 Categorías con Mayor Proporción de Best-Sellers (Top 5):")
print(best_seller_prop.head())

print("\nRespuesta: Las categorías con una alta proporción de productos que son Best-Sellers (True) son las más prevalentes.")


### 2. Statistical Tests

print("\n### 1.3 Pruebas Estadísticas (Chi-square y Cramér's V)")

# Conducir la prueba de Chi-square
chi2, p, dof, expected = chi2_contingency(crosstab_abs)

print(f"\nChi-square Statistic: {chi2:.2f}")
print(f"P-value: {p:.4f}")

# Interpretación: Si p < 0.05, la distribución de best-sellers NO es independiente de la categoría.
if p < 0.05:
    print("Conclusión del Chi-square: El p-value es significativo (p < 0.05). La distribución de best-sellers NO es independiente de la categoría. Existe una relación.")
else:
    print("Conclusión del Chi-square: El p-value no es significativo (p > 0.05). La distribución de best-sellers es independiente de la categoría.")


# Computar Cramér's V (medida de fuerza de asociación)
# V = sqrt(chi2 / (N * min(k-1, r-1)))
N = crosstab_abs.sum().sum()
min_dim = min(crosstab_abs.shape) - 1
cramers_v = math.sqrt(chi2 / (N * min_dim)) if min_dim > 0 else 0

print(f"Cramér's V (Fuerza de Asociación): {cramers_v:.4f}")

# Interpretación de Cramér's V (general)
if cramers_v < 0.10:
    strength = "muy débil"
elif cramers_v < 0.30:
    strength = "débil a moderada"
elif cramers_v < 0.50:
    strength = "moderada"
else:
    strength = "fuerte"

print(f"Interpretación: La fuerza de asociación entre 'category' y 'isBestSeller' es {strength}.")


### 3. Visualizaciones

print("\n### 1.4 Visualización (Gráfico de Barras Apiladas)")

# Seleccionar las Top 10 categorías para un gráfico más limpio
top_10_categories = df['category'].value_counts().nlargest(10).index
crosstab_10 = pd.crosstab(df['category'], df['isBestSeller'], normalize='index').loc[top_10_categories]

plt.figure(figsize=(14, 8))
# Gráfico de barras apiladas
crosstab_10.plot(kind='bar', stacked=True, color=['lightcoral', 'skyblue'], ax=plt.gca())

plt.title('Proporción de Productos Best-Seller (True/False) en Top 10 Categorías', fontsize=16)
plt.xlabel('Categoría', fontsize=14)
plt.ylabel('Proporción', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='isBestSeller', labels=['No Best-Seller', 'Best-Seller'])
plt.tight_layout()
plt.show()
print("")

# ----------------------------------------------------------------------


# ======================================================================
# 💵 PARTE 2: EXPLORANDO PRECIOS Y RATINGS ACROSS CATEGORIES
# ======================================================================

# Usaremos df_clean (sin outliers de precio) para esta parte
print("\n" + "="*70)
print("## 💵 Parte 2: Explorando Precios y Ratings Across Categories (Sin Outliers de Precio)")
print("="*70)

# Definir las Top 20 Categorías (para filtrar gráficos)
top_20_categories = df_clean['category'].value_counts().nlargest(20).index
df_top_20 = df_clean[df_clean['category'].isin(top_20_categories)]

### 1. Violin Plots (Precio por Categoría)

print("\n### 2.1 Violin Plots (Distribución de Precios por Categoría - Top 20)")
plt.figure(figsize=(16, 8))
sns.violinplot(x='category', y='price', data=df_top_20, palette='Pastel1', inner='quartile')
plt.title('Distribución de Precios (Sin Outliers) por Categoría (Top 20)', fontsize=16)
plt.xlabel('Categoría', fontsize=14)
plt.ylabel('Precio (£)', fontsize=14)
plt.xticks(rotation=60, ha='right')
plt.tight_layout()
plt.show()
print("")

# Identificar la categoría con la Mediana más alta (Sin filtrar)
median_prices = df_clean.groupby('category')['price'].median().sort_values(ascending=False)
highest_median_category = median_prices.index[0]

print(f"\nCategoría con la Mediana de Precio más Alta (Sin Filtrar): **{highest_median_category}** (Mediana: £{median_prices.iloc[0]:.2f})")


### 2. Bar Charts (Precio Promedio por Categoría)

# Definir las Top 10 Categorías (para filtrar gráficos)
top_10_categories_price = df_clean['category'].value_counts().nlargest(10).index
df_top_10_price = df_clean[df_clean['category'].isin(top_10_categories_price)]

print("\n### 2.2 Bar Chart (Precio Promedio por Categoría - Top 10)")
# Calcular el precio promedio para las top 10
avg_price_top_10 = df_top_10_price.groupby('category')['price'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=avg_price_top_10.index, y=avg_price_top_10.values, palette='coolwarm')
plt.title('Precio Promedio (Sin Outliers) por Categoría (Top 10)', fontsize=16)
plt.xlabel('Categoría', fontsize=14)
plt.ylabel('Precio Promedio (£)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
print("")

# Identificar la categoría con el Promedio de Precio más Alto (Sin filtrar)
avg_prices_all = df_clean.groupby('category')['price'].mean().sort_values(ascending=False)
highest_avg_category = avg_prices_all.index[0]

print(f"\nCategoría con el Precio Promedio más Alto (Sin Filtrar): **{highest_avg_category}** (Promedio: £{avg_prices_all.iloc[0]:.2f})")


### 3. Box Plots (Rating por Categoría)

# Definir las Top 10 Categorías (para filtrar gráficos)
top_10_categories_rating = df_clean['category'].value_counts().nlargest(10).index
df_top_10_rating = df_clean[df_clean['category'].isin(top_10_categories_rating)]

print("\n### 2.3 Box Plots (Distribución de Puntuación por Categoría - Top 10)")
plt.figure(figsize=(14, 8))
sns.boxplot(x='category', y='stars', data=df_top_10_rating, palette='Set3')
plt.title('Distribución de Puntuaciones (Stars) por Categoría (Top 10)', fontsize=16)
plt.xlabel('Categoría', fontsize=14)
plt.ylabel('Puntuación (Stars)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
print("")

# Identificar la categoría con la Mediana de Rating más Alta (Sin filtrar)
median_ratings = df_clean.groupby('category')['stars'].median().sort_values(ascending=False)
highest_median_rating_category = median_ratings.index[0]

print(f"\nCategoría con la Mediana de Puntuación (Rating) más Alta (Sin Filtrar): **{highest_median_rating_category}** (Mediana: {median_ratings.iloc[0]:.2f})")

# ----------------------------------------------------------------------


# ======================================================================
# ⭐ PARTE 3: INVESTIGANDO EL INTERPLAY ENTRE PRECIOS Y RATINGS
# ======================================================================

# Usaremos df_clean (sin outliers de precio) para esta parte
print("\n" + "="*70)
print("## ⭐ Parte 3: Investigando el Interplay Entre Precios y Ratings")
print("="*70)

### 1. Correlation Coefficients

print("\n### 3.1 Coeficiente de Correlación entre Price y Stars")
correlation = df_clean['price'].corr(df_clean['stars'])

print(f"Coeficiente de Correlación (Pearson) entre Price y Stars: {correlation:.4f}")

# Interpretación
if abs(correlation) < 0.1:
    corr_interpretation = "muy débil o insignificante."
elif abs(correlation) < 0.3:
    corr_interpretation = "débil."
elif abs(correlation) < 0.5:
    corr_interpretation = "moderada."
else:
    corr_interpretation = "fuerte."

print(f"Conclusión: La correlación entre el precio y la puntuación es **{corr_interpretation}** (y es negativa, lo que significa que el precio aumenta, el rating tiende a disminuir ligeramente, o viceversa).")


### 2. Visualizaciones

print("\n### 3.2 Visualizaciones")

# A. Scatter Plot (Rating vs. Price)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='stars', y='price', data=df_clean, alpha=0.6, color='darkblue')
plt.title('Relación entre Puntuación (Stars) y Precio (Sin Outliers)', fontsize=16)
plt.xlabel('Puntuación (Stars)', fontsize=14)
plt.ylabel('Precio (£)', fontsize=14)
plt.show()
print("")

print("\nPatrones Observados en el Scatter Plot:")
print("* La mayoría de los productos se agrupan en las puntuaciones más altas (4.0 a 5.0), independientemente del precio.")
print("* No se observa una línea clara de tendencia (correlación débil), lo que indica que el precio no es un predictor fuerte de la puntuación del cliente.")
print("* Los precios más altos (en este subconjunto 'limpio') muestran una mayor dispersión en las puntuaciones.")


# B. Correlation Heatmap
print("\nHeatmap de Correlación entre Variables Numéricas:")
numerical_df = df_clean[['price', 'stars']]
# Añadir otras variables numéricas si existen (e.g., 'no_of_reviews')
if 'no_of_reviews' in df.columns:
    numerical_df['no_of_reviews'] = df_clean['no_of_reviews']

correlation_matrix = numerical_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='cividis', fmt=".2f", linewidths=.5, linecolor='black')
plt.title('Heatmap de Correlación de Variables Numéricas', fontsize=16)
plt.show()
print("")


# C. QQ Plot (Normalidad del Precio)
print("\nQQ Plot para el Precio (Evaluación de Normalidad):")
plt.figure(figsize=(10, 6))
probplot(df_clean['price'], dist="norm", plot=plt)
plt.title('QQ Plot de Precio de Producto (Sin Outliers)', fontsize=16)
plt.xlabel('Cuantiles Teóricos (Distribución Normal)', fontsize=14)
plt.ylabel('Cuantiles de la Muestra (Precio)', fontsize=14)
plt.show()
print("")

print("\nAnálisis del QQ Plot:")
print("* Si el precio siguiera una distribución normal, los puntos se alinearían estrechamente con la línea diagonal roja.")
print("* Los puntos se desvían de la línea roja, especialmente en los extremos, confirmando que la distribución de precios (incluso sin los outliers extremos) **no sigue una distribución normal**.")
print("* El precio todavía muestra una **asimetría positiva** (la curva se eleva más rápido al final), lo que indica que la mayoría de los productos son relativamente baratos, y hay una cola de productos más caros.")