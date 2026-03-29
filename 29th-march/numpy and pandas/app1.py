import numpy as np
import pandas as pd

# numpy -> numerical python ( high level mathematical functions)
# pandas -> data analysis

# we need to load data
df = pd.read_excel('Employees.xlsx')

# df = pd.read_csv('Employees.csv')

# df -> variable (data frame)
# df.head() -> first 5 rows of the data frame
# df.tail() -> last 5 rows of the data frame

'''
print(df.head())
print("-----------------------------")
print(df.tail())
'''

# basic numpy operations
salaries = df['Salary'].to_numpy()
'''
salaries -> numpy array <- xl [Salary]
to_numpy() -> converts pandas series to numpy array
np (functional / maths) -> numpy array
hypothesis testing : M.Sc Maths (stats) / B.tech
h test / p test / t test 
'''


'''
# basic numpy operations
mean_salary = np.mean(salaries)
median_salary = np.median(salaries)
std_salary = np.std(salaries)
print("Mean Salary:", mean_salary)
print("Median Salary:", median_salary)
print("Standard Deviation of Salary:", std_salary)


# getting more information about the data frame
info_df = df.info()
print(info_df)

# describe about the data Frame
describe_df = df.describe()
print(describe_df)

'''

# filtering and soritng the data frame
eng = df[df['Department'] == 'Engineering']
print(eng)

print("-----------------------------")

# filtering only salary higher than 70000
high_salary = df[df['Salary'] > 70000]
print(high_salary)

print("-----------------------------")

# sorting the data frame by salary
sorted_df = df.sort_values(by='Salary', ascending=False)
print(sorted_df)
