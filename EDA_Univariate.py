import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración para una mejor visualización de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100

# --- Carga de Datos ---
# Reemplaza 'amazon_uk_products.csv' con el nombre real de tu archivo
try:
    df = pd.read_csv('amazon_uk_products.csv')
    print("✅ Datos cargados correctamente.")
except FileNotFoundError:
    print("❌ ERROR: Asegúrate de que el archivo 'amazon_uk_products.csv' esté en el directorio correcto.")
    # Crea un DataFrame vacío para evitar errores si el archivo no se encuentra
    df = pd.DataFrame()

# Verificar si el DataFrame no está vacío antes de continuar
if df.empty:
    exit()

# Inspección inicial de las columnas para asegurar los nombres correctos
print("\n--- Inspección Inicial de Datos ---")
print(df.info())
print("\nPrimeras 5 filas:")
print(df.head())

# --- Limpieza/Preparación de Datos (General) ---
# El análisis univariado se centra en 'category', 'price' y 'rating'.
# Asumiremos que 'price' y 'rating' están en el formato correcto (numérico)
# y que no contienen muchos valores nulos.

# Manejo de valores nulos para las columnas clave (imputación simple o eliminación)
# Para 'price' y 'rating', eliminamos filas si los nulos son pocos.
df.dropna(subset=['price', 'rating', 'category'], inplace=True)

# Convertir la columna 'price' a un formato numérico si no lo está (e.g., si tiene '£')
# Si la columna 'price' contiene caracteres no numéricos, necesitamos limpiarla.
# Por ejemplo, si los precios se representan como '£12.99':
# df['price'] = df['price'].astype(str).str.replace(r'[£,]', '', regex=True).astype(float)
# Asumiremos que ya es float o se convierte fácilmente:
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.dropna(subset=['price'], inplace=True)


print(f"\nNúmero de filas después de la limpieza: {len(df)}")
# ----------------------------------------------------------------------
## 📊 Parte 1: Entendiendo las Categorías de Productos

print("\n" + "="*50)
print("## 📊 Parte 1: Entendiendo las Categorías de Productos")
print("="*50)

### 1. Tablas de Frecuencia
print("\n### 1.1 Frecuencia de Categorías")
# Generar la tabla de frecuencias para 'category'
category_counts = df['category'].value_counts()
print("\nTabla de Frecuencia de Categorías:")
print(category_counts)

# Top 5 categorías
top_5_categories = category_counts.head(5)
print("\nTop 5 Categorías más listadas:")
print(top_5_categories)

### 2. Visualizaciones

# Definir el subconjunto de categorías a utilizar para gráficos
categories_for_charts = top_5_categories.index.tolist()
df_subset = df[df['category'].isin(categories_for_charts)]


print("\n### 1.2 Gráfico de Barras y Pastel para Categorías")
plt.figure(figsize=(12, 6))

# Gráfico de barras para todas las categorías (o el top N si hay demasiadas)
if len(category_counts) > 50:
    # Usar el top 20 para que el gráfico sea legible
    sns.barplot(x=category_counts.head(20).index, y=category_counts.head(20).values, palette="viridis")
    plt.title('Distribución de Productos por Top 20 Categorías', fontsize=16)
else:
    # Si no hay demasiadas, se usan todas
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.title('Distribución de Productos por Categoría', fontsize=16)

plt.xlabel('Categoría', fontsize=14)
plt.ylabel('Frecuencia de Listings', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
print("")


# Gráfico de Pastel para las Top 5 categorías
plt.figure(figsize=(10, 10))
plt.pie(top_5_categories.values, labels=top_5_categories.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
plt.title('Proporción de Listados en las Top 5 Categorías', fontsize=16)
plt.axis('equal') # Para que el pastel sea un círculo
plt.show()
print("")

# ----------------------------------------------------------------------
## 💰 Parte 2: Profundizando en el Precio de los Productos

print("\n" + "="*50)
print("## 💰 Parte 2: Profundizando en el Precio de los Productos")
print("="*50)

### 1. Medidas de Centralidad
print("\n### 2.1 Medidas de Centralidad para el Precio")
price_mean = df['price'].mean()
price_median = df['price'].median()
price_mode = df['price'].mode().iloc[0] # mode() devuelve una Serie, tomamos el primer valor

print(f"Media (Promedio): £{price_mean:.2f}")
print(f"Mediana (Valor central): £{price_median:.2f}")
print(f"Moda (Más común): £{price_mode:.2f}")

print(f"\nComparación: El precio promedio (£{price_mean:.2f}) es {('mayor' if price_mean > price_mode else 'menor' if price_mean < price_mode else 'igual')} que el precio más común (£{price_mode:.2f}).")

### 2. Medidas de Dispersión
print("\n### 2.2 Medidas de Dispersión para el Precio")
price_variance = df['price'].var()
price_std = df['price'].std()
price_range = df['price'].max() - df['price'].min()
price_q1 = df['price'].quantile(0.25)
price_q3 = df['price'].quantile(0.75)
price_iqr = price_q3 - price_q1

print(f"Varianza: {price_variance:.2f}")
print(f"Desviación Estándar: £{price_std:.2f}")
print(f"Rango (Máx - Mín): £{price_range:.2f}")
print(f"Rango Intercuartílico (IQR): £{price_iqr:.2f}")

print(f"\nEl precio está muy variado, con una desviación estándar de £{price_std:.2f} y un rango de £{price_range:.2f}. El alto rango intercuartílico de £{price_iqr:.2f} también indica una dispersión significativa en la mitad central de los datos.")

### 3. Visualizaciones

print("\n### 2.3 Visualizaciones de Precios")

# 3.1 Histograma de Precios
plt.figure(figsize=(12, 6))
sns.histplot(df['price'], bins=50, kde=True, color='skyblue')
plt.title('Distribución de Precios de Productos (Histograma General)', fontsize=16)
plt.xlabel('Precio (£)', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
plt.show()
print("")

print("\n*Nota sobre la legibilidad del Histograma:* Si el gráfico anterior es difícil de leer (se ve un pico muy alto cerca de cero y el resto es plano), esto indica una **asimetría positiva extrema** (muchos productos baratos y pocos muy caros).")
print("Para solucionarlo y ver el detalle de la mayoría de los productos, se puede **limitar el eje X** a un rango más razonable (e.g., el 99% de los precios o el IQR superior) o aplicar una **transformación logarítmica**.")

# Histograma de precios con límite en el 99 percentil para una mejor visualización
price_limit = df['price'].quantile(0.99)
plt.figure(figsize=(12, 6))
sns.histplot(df.loc[df['price'] < price_limit, 'price'], bins=50, kde=True, color='salmon')
plt.title(f'Distribución de Precios (Limitado al 99 Percentil: £{price_limit:.2f})', fontsize=16)
plt.xlabel('Precio (£)', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
plt.show()
print("")

# 3.2 Box Plot de Precios
plt.figure(figsize=(12, 4))
sns.boxplot(x=df['price'], color='lightgreen')
plt.title('Box Plot de Precios de Productos (Detección de Outliers)', fontsize=16)
plt.xlabel('Precio (£)', fontsize=14)
plt.show()
print("")

print("\nEl Box Plot muestra una gran cantidad de puntos de datos individuales (outliers) que son **precios significativamente más altos** que la mayoría de los productos, confirmando la gran dispersión y asimetría identificada anteriormente.")


# ----------------------------------------------------------------------
## ⭐ Parte 3: Analizando la Puntuación de los Productos

print("\n" + "="*50)
print("## ⭐ Parte 3: Analizando la Puntuación de los Productos")
print("="*50)

### 1. Medidas de Centralidad
print("\n### 3.1 Medidas de Centralidad para la Puntuación")
rating_mean = df['rating'].mean()
rating_median = df['rating'].median()
# La moda es más relevante si las puntuaciones son discretas (e.g., 4.5, 4.0)
rating_mode = df['rating'].mode().iloc[0]

print(f"Media (Promedio): {rating_mean:.2f}")
print(f"Mediana (Valor central): {rating_median:.2f}")
print(f"Moda (Más común): {rating_mode:.2f}")

print("\nGeneralmente, los clientes califican los productos con un promedio alto, indicando una tendencia positiva en la satisfacción.")

### 2. Medidas de Dispersión
print("\n### 3.2 Medidas de Dispersión para la Puntuación")
rating_variance = df['rating'].var()
rating_std = df['rating'].std()
rating_q1 = df['rating'].quantile(0.25)
rating_q3 = df['rating'].quantile(0.75)
rating_iqr = rating_q3 - rating_q1

print(f"Varianza: {rating_variance:.4f}")
print(f"Desviación Estándar: {rating_std:.4f}")
print(f"Rango Intercuartílico (IQR): {rating_iqr:.4f}")

print(f"\nLa Desviación Estándar es relativamente baja ({rating_std:.4f}), lo que indica que las puntuaciones son **bastante consistentes** y se agrupan fuertemente alrededor de la media. El IQR bajo confirma esta baja variación.")


### 3. Forma de la Distribución
print("\n### 3.3 Forma de la Distribución (Skewness y Kurtosis)")
rating_skewness = df['rating'].skew()
rating_kurtosis = df['rating'].kurt()

print(f"Asimetría (Skewness): {rating_skewness:.4f}")
print(f"Curtosis (Kurtosis): {rating_kurtosis:.4f}")

# Interpretación
if rating_skewness < 0:
    skew_interpretation = "negativa (sesgada hacia la izquierda), lo que significa que la cola se extiende hacia valores bajos. La mayoría de las puntuaciones se encuentran en el extremo superior (puntuaciones altas)."
elif rating_skewness > 0:
    skew_interpretation = "positiva (sesgada hacia la derecha), lo que significa que la cola se extiende hacia valores altos. La mayoría de las puntuaciones se encuentran en el extremo inferior (puntuaciones bajas)."
else:
    skew_interpretation = "cercana a cero (simétrica)."

if rating_kurtosis > 0:
    kurt_interpretation = "positiva (Leptocúrtica), lo que indica colas más pesadas y un pico más agudo que una distribución normal (más valores en las colas y en el centro)."
elif rating_kurtosis < 0:
    kurt_interpretation = "negativa (Platicúrtica), lo que indica colas más ligeras y un pico más plano que una distribución normal (los valores están más dispersos)."
else:
    kurt_interpretation = "cercana a cero (Mesocúrtica - similar a la distribución normal)."

print(f"\n*Análisis de la Forma:*")
print(f"Asimetría: La distribución es {skew_interpretation}")
print(f"Curtosis: La distribución es {kurt_interpretation}")

### 4. Visualización

# Histograma de Puntuaciones
print("\n### 3.4 Visualización de Puntuaciones")
plt.figure(figsize=(10, 6))
# Se usa un número limitado de bins si las ratings son discretas (e.g., 0.5 en 0.5)
sns.histplot(df['rating'], bins=np.arange(df['rating'].min(), df['rating'].max() + 0.1, 0.1), kde=True, color='darkviolet')
plt.title('Distribución de Puntuaciones de Productos', fontsize=16)
plt.xlabel('Puntuación del Producto', fontsize=14)
plt.ylabel('Frecuencia', fontsize=14)
plt.xlim(df['rating'].min(), df['rating'].max())
plt.show()
print("")

print(f"\nEl histograma confirma que la puntuación más común (la moda de {rating_mode:.2f}) se encuentra en el extremo superior. La forma de la distribución está claramente sesgada hacia las puntuaciones más altas (4.0 a 5.0).")