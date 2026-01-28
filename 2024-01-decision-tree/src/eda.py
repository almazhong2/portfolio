import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = 'nkcore_ki_201903.csv'
df = pd.read_csv(data, encoding = 'windows-1252')

# Basic Descriptive Statistics
print(df.describe())

# Class Distribution
print(df['GSTATUS_KI'].value_counts())
df['GSTATUS_KI'].value_counts().plot(kind='bar')
plt.title('Class Distribution of Contracting Cancer')
plt.xlabel('Class')
plt.ylabel('Frequency')
plt.show()

# Feature Analysis
feature_cols = [
    'KDPI', 
    'AGE', 
    'CREAT_DON', 
    'BMI_DON_CALC', 
    'END_CPRA', 
    'DAYSWAIT_CHRON', 
    'HLAMIS', 
    'COLD_ISCH_KI'
]

# Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df[feature_cols].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Histograms/Boxplots for each feature
for col in feature_cols:
    df[col].plot(kind='hist', bins=20)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

    df.boxplot(column=col, by='malig')
    plt.title(f'{col} by Cancer/No Cancer')
    plt.xlabel('Class')
    plt.ylabel(col)
    plt.show()

# Pair Plots
sns.pairplot(df[feature_cols + ['malig']], hue='malig')
plt.show()

# Missing Data Analysis
print(df.isnull().sum())

# Outlier Detection
for col in feature_cols:
    sns.boxplot(x=df[col])
    plt.title(f'Outlier Detection in {col}')
    plt.show()
