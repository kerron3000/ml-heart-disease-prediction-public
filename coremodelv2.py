import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


#  Load Data
def train_and_save_optimized_rf(filename='Heart_Disease_Prediction.csv'):

    file_path = os.path.join(os.getcwd(), filename)
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found.")
        return

    df = pd.read_csv(file_path)

    # Encode Target Label
    target_col = 'Heart Disease'
    le = LabelEncoder()
    df[target_col] = le.fit_transform(df[target_col])

    # Feature defination
    categorical_features = [
        'Sex', 'Chest pain type', 'FBS over 120', 'EKG results',
        'Exercise angina', 'Slope of ST', 'Number of vessels fluro', 'Thallium'
    ]
    numeric_features = ['Age', 'BP', 'Cholesterol', 'Max HR', 'ST depression']

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # Create Preprocessing Pipeline (from sklearn)
    preprocessor = ColumnTransformer(
        transformers=[('num', StandardScaler(), numeric_features),
                      ('cat', OneHotEncoder(drop='first', sparse_output=False),
                       categorical_features)])

    # Create a Unified Pipeline
    # This bundles preprocessing and the model into one object
    full_pipeline = Pipeline([('preprocessor', preprocessor),
                              ('classifier',
                               RandomForestClassifier(random_state=42))])

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)  #pretty standard

    # Define Hyperparameter Grid for GridSearchCV
    # Note the prefix 'classifier__' to target the 'classifier' step in the pipeline
    param_grid = {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [None, 10, 20],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__criterion': ['gini', 'entropy']
    }

    # Run Grid Search with 5-Fold Cross-Validation
    print("Starting GridSearchCV... this may take a moment.")
    grid_search = GridSearchCV(full_pipeline,
                               param_grid,
                               cv=5,
                               scoring='f1',
                               n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Results
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best CV F1 Score: {grid_search.best_score_:.4f}")

    # Saving the 'best_estimator_' saves the entire pipeline (preprocessor + tuned model)
    model_data = {
        'pipeline': grid_search.best_estimator_,
        'target_mapping': le.classes_
    }

    joblib.dump(model_data, 'heart_disease_rf_optimized.pkl')
    print("Optimized Model Pipeline saved to 'heart_disease_rf_optimized.pkl'")


if __name__ == "__main__":
    train_and_save_optimized_rf()
