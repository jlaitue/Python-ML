import pandas
import numpy as np
from sklearn.linear_model import LinearRegression

# Since we have 3 categorical variables we need to create two dummy variables
df = pandas.read_csv("../../datasets/ecom-expense/Ecom Expense.csv")

# This is necessary in order to join with the new columns from the dummy variables
column_names = df.columns.values.tolist()

# With iloc we eliminate the first column of the dummy variable
# iloc[rows_range,columns_range]
dummy_gender = pandas.get_dummies(df["Gender"], prefix="Gender").iloc[:,1:]
dummy_city_tier = pandas.get_dummies(df["City Tier"], prefix="City").iloc[:,1:]


# We have to make a data join to add the dummy variables into the original dataset
df_new = df[column_names].join(dummy_gender)
column_names = df_new.columns.values.tolist()

df_new = df_new[column_names].join(dummy_city_tier)

# # We establish the variables that will be part of the prediction
feature_cols = ["Monthly Income", "Transaction Time", "Gender_Male",
    "City_Tier 2", "City_Tier 3", "Record"]

X = df_new[feature_cols] # Get only the columns in the dataset wanted for prediction
Y = df_new["Total Spend"] # Value to be predicted

lm = LinearRegression()
lm.fit(X, Y)
# Model obtained with best output for R^2, obtained and calculated with scklearn.
# Improved performance was due to iteration in selection of prediction variables
# Total_spend = 'Monthly Income' * 0.14753898049205721 + 'Transaction Time' * 0.1549461254958953
# 'Gender_Male' * 131.02501325554584 + 'Gender_Female' * -131.02501325554564
# 'City_Tier 1' * 76.76432601049557 + 'City_Tier 2' * 55.13897430923219
# 'City_Tier 3' * -131.9033003197276 + 'Record' * 772.2334457445637

print(lm.intercept_)
print(lm.coef_)
print(list(zip(feature_cols, lm.coef_))) # Joins each lm model column with its respective coefficient
print(lm.score(X, Y))
#
# df_new["prediction"] = df_new['Monthly Income'] * 0.14753898049205721 + df_new['Transaction Time'] * 0.1549461254958953 +  df_new['Gender_Male'] * 131.02501325554584 + df_new['Gender_Female'] * -131.02501325554564 + df_new['City_Tier 1'] * 76.76432601049557 + df_new['City_Tier 2'] * 55.13897430923219 + df_new['City_Tier 3'] * -131.9033003197276 + df_new['Record'] * 772.2334457445637
# print(df_new.head())
# SSD = np.sum((df_new["prediction"] -  df_new["Total Spend"]) ** 2)
# print(SSD)
#
# RSE = np.sqrt(SSD/(len(df_new)-len(feature_cols)-1)) # Desviación de los valores sobre la media
# spend_mean = np.mean(df_new["Total Spend"])
# print(RSE)
# error = RSE/spend_mean
# print(error)
# print(df_new.head())
