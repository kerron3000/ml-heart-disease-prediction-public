import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (f1_score, confusion_matrix,
                             ConfusionMatrixDisplay, roc_curve, roc_auc_score,
                             classification_report)


def evaluate_optimized_model(model_path='heart_disease_rf_optimized.pkl',
                             data_path='Heart_Disease_Prediction.csv'):
    # Load the saved Pipeline
    try:
        model_data = joblib.load(model_path)
        pipeline = model_data['pipeline']
        target_mapping = model_data['target_mapping']
    except FileNotFoundError:
        print(
            f"Error: {model_path} not found. Run the optimized training script first."
        )
        return

    # Load and Split Data
    # Consistency is key: use the same split logic as the training script
    df = pd.read_csv(data_path)
    target_col = 'Heart Disease'

    # Encode target to match the numeric output of the model
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df[target_col] = le.fit_transform(df[target_col])

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    _, X_test, _, y_test = train_test_split(X,
                                            y,
                                            test_size=0.2,
                                            random_state=42)

    # Predictions using the Pipeline
    # The pipeline automatically applies the StandardScaler and OneHotEncoder
    y_pred = pipeline.predict(X_test)
    y_probs = pipeline.predict_proba(X_test)[:, 1]

    # Calculate Metrics
    f1 = f1_score(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_probs)

    print("--- Optimized Model Evaluation ---")
    print(f"F1 Score: {f1:.4f}")
    print(f"AUC-ROC Score: {auc_roc:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=target_mapping))

    # Visualizations
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=target_mapping)
    disp.plot(cmap='Greens', ax=ax1)
    ax1.set_title("Confusion Matrix (Optimized Model)")

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_probs)
    ax2.plot(fpr, tpr, color='blue', lw=2, label=f'ROC area = {auc_roc:.2f}')
    ax2.plot([0, 1], [0, 1], color='gray', linestyle='--')
    ax2.set_xlabel('False Positive Rate')
    ax2.set_ylabel('True Positive Rate')
    ax2.set_title('ROC Curve')
    ax2.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig('optimized_evaluation_results.png')
    print("\nEvaluation results saved to 'optimized_evaluation_results.png'")


if __name__ == "__main__":
    evaluate_optimized_model()
