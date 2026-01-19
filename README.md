# Heart IQ

A machine learning system for predicting the absence/presence of heart disease using patient health data.

## Project Structure

```
heart-iq/
├── Dockerfile                           # Docker container configuration
├── Heart_Disease_Prediction.csv        # Heart disease dataset -> available on Kaggle
├── app1_2.py                            # Application interface (version 1.2) -> uses Streamlit
├── coremodelv2.py                       # Core ML model implementation (v2)
├── heart_disease_rf_optimized.pkl      # Optimized Random Forest model
├── model-evalv2.py                      # Model evaluation script (v2)
└── requirements.txt                     # Python dependencies
```

## Description

Heart IQ is a machine learning application that predicts the likelihood of heart disease based on patient health metrics.

## Features

- Heart disease risk prediction
- Optimized Random Forest classifier
- Model evaluation and performance metrics
- Dockerized deployment
- Web-based application interface

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://gitlab.com/kerron3000/heart-iq.git
cd heart-iq
```

2. Install dependencies:

### Linux
```bash
python -m venv .venv
source .venv/bin/activate
make install
```
### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app1_2.py
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t heart-iq .
```

2. Run the container:
```bash
docker run -p 8501:8501 heart-iq

or

Public DockerHub url: https://hub.docker.com/r/kerron3000/heart-iq

docker pull kerron3000/heart-iq:v1.2

docker run -p 8501:8501 kerron3000/heart-iq:v1.2
```

## Usage

Once the application is running, access it through your web browser at `http://localhost:8501` (or the appropriate port).

Input patient health metrics to receive a heart disease risk prediction.

## Model Information

- **Algorithm**: Random Forest Classifier (Optimized)
- **Model File**: `heart_disease_rf_optimized.pkl`
- **Dataset**: `Heart_Disease_Prediction.csv`

## Components

- **app1_2.py**: Main application interface for user interaction
- **coremodelv2.py**: Core machine learning model implementation
- **model-evalv2.py**: Scripts for evaluating model performance
- **heart_disease_rf_optimized.pkl**: Pre-trained and optimized Random Forest model
- **Heart_Disease_Prediction.csv**: Training and validation dataset

## Requirements

See `requirements.txt` for a complete list of Python package dependencies.

## Model Evaluation

To evaluate the model performance:
```bash
python model-evalv2.py
```

## License

[The Apache License 2.0 ]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment.

## Contact

[kerron3773@yahoo.com]
