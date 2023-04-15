# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load and prepare the data
data = pd.read_csv('e-waste-data.csv')
X = data[['Population density', 'GDP',
          'Urbanization rate', 'E-waste generation rate']]
y = data['Inventory capacity']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(    
    X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

# Evaluate the model
y_pred = rf.predict(X_test)
score = rf.score(X_test, y_test)
print('R^2 score:', score)

# Save the model
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)

# Make recommendations based on input parameters


def recommend_locations(population_density, gdp, urbanization_rate, e_waste_gen_rate, n):
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    X_new = [[population_density, gdp, urbanization_rate, e_waste_gen_rate]]
    y_new = model.predict(X_new)
    recommendations = data.loc[data['Inventory capacity']
                               >= y_new[0]].nlargest(n, 'Inventory capacity')
    return recommendations[['Location', 'Inventory capacity']]