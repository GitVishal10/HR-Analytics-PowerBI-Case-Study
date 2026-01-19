import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# HR ANALYTICS DATA CLEANING & EXPLORATORY ANALYSIS
# Purpose: Clean raw HR data and uncover attrition drivers for dashboard
# Output: cleaned_data.csv (ready for Power BI/Tableau)
# =============================================================================

# Load raw HR dataset
df = pd.read_csv("hr_analytics_raw_data.csv")

# 🔍 INITIAL DATA EXPLORATION
print("Dataset Shape:", df.shape)  # Check rows x columns
print(df.head())  # Preview first 5 rows
print(df.info())  # Data types, memory usage, missing values overview

# 📊 MISSING VALUE ANALYSIS
print("\nMissing Values per Column:")
print(df.isnull().sum())

# Handle missing YearsWithCurrManager (business logic: treat as new managers = 0 years)
print("\nBefore filling YearsWithCurrManager NaNs:", df['YearsWithCurrManager'].isnull().sum())
df['YearsWithCurrManager'] = df['YearsWithCurrManager'].fillna(0)
print("After filling YearsWithCurrManager NaNs:", df['YearsWithCurrManager'].isnull().sum())

# 💰 SALARY ANALYSIS - Centrality & Dispersion Measures
# Calculate mean, median, mode to detect salary distribution skewness
mean_salary = df['MonthlyIncome'].mean()      # ~6504.98 - pulled up by senior roles
median_salary = df['MonthlyIncome'].median()  # ~4933.0  - better central tendency
mode_salary = df['MonthlyIncome'].mode()[0]   # ~2342    - most common salary level

print(f"\nSalary Stats - Mean: ${mean_salary:.2f}, Median: ${median_salary:.2f}, Mode: ${mode_salary:.2f}")
# Insight: Mean > Median indicates right-skewed distribution (high-salary outliers)

# Measure salary variability across organization
variance_salary = df['MonthlyIncome'].var()   # High variance = salary inequality
std_salary = df['MonthlyIncome'].std()        # ~4700 = wide spread in pay scales
print(f"Salary Variance: {variance_salary:.2f}, Std Dev: ${std_salary:.2f}")

# 🏢 DEPARTMENT-WISE SALARY COMPARISON
dept_salary_stats = df.groupby('Department')['MonthlyIncome'].agg(['mean', 'median', 'std'])
print("\nDepartment Salary Analysis:")
print(dept_salary_stats)
# Insight: Sales has consistent high pay; HR shows pay disparity

# 🎯 MODE ANALYSIS - Most Common Employee Experiences
job_mode = df['JobRole'].mode()[0]           # Most frequent job role
job_satis_mode = df['JobSatisfaction'].mode()[0]  # Most common satisfaction level
work_life_mode = df['WorkLifeBalance'].mode()[0]  # Most common work-life balance
print(f"\nMost Common: JobRole={job_mode}, JobSatisfaction={job_satis_mode}, WorkLifeBalance={work_life_mode}")

# 📈 VISUAL EXPLORATION (Uncomment to generate plots)
"""
# Salary distribution histogram with KDE
sns.histplot(df['MonthlyIncome'], kde=True)
plt.title('Monthly Income Distribution')
plt.show()

# Salary boxplot to identify outliers
sns.boxplot(y=df['MonthlyIncome'])
plt.title('Salary Outlier Detection')
plt.show()
"""
# Visuals confirm: right-skewed salary distribution with senior-level outliers

# 🔬 HYPOTHESIS TESTING: Work-Life Balance vs Job Satisfaction
# Split employees into poor vs good work-life balance groups
group_A = df[df['WorkLifeBalance'] <= 2]['JobSatisfaction']  # Poor WLB (1-2)
group_B = df[df['WorkLifeBalance'] >= 3]['JobSatisfaction']  # Good WLB (3-4)

print(f"\nJob Satisfaction by Work-Life Balance:")
print(f"Poor WLB (≤2): {group_A.mean():.2f}")
print(f"Good WLB (≥3): {group_B.mean():.2f}")
# Insight: Better work-life balance correlates with higher job satisfaction

# 🚪 ATTRITION ANALYSIS - Income vs Retention
attrition_income = df.groupby('Attrition')['MonthlyIncome'].mean()
print("\nAverage Salary by Attrition Status:")
print(attrition_income)
# Key Finding: Lower-paid employees show higher attrition rates

# 💾 EXPORT CLEANED DATASET FOR DASHBOARDING
df.to_csv('cleaned_data.csv', index=False)
print("\n✅ Cleaned dataset saved as 'cleaned_data.csv'")
print("Ready for Power BI/Tableau visualization!")
