# Salary Prediction Using Random Forest

## Dataset
- Source: Salary dataset containing employee information such as education, experience, job title, and location.
- The dataset is downloaded automatically using **gdown** as `expected_ctc.csv`.
- Link: https://drive.google.com/file/d/<YOUR_FILE_ID>/view?usp=sharing

This project predicts employee salaries using a **Random Forest Regressor**. It applies data preprocessing, exploratory data analysis (EDA), feature engineering, and ensemble machine learning techniques to estimate salaries based on employee attributes. The model is evaluated using regression metrics to ensure accurate and reliable predictions.

## Key Features
1. Data cleaning and preprocessing
2. Handling missing values and categorical encoding
3. Exploratory Data Analysis (EDA) with visualizations
4. Feature engineering and selection
5. Salary prediction using Random Forest Regression
6. Model evaluation using MAE and RMSE
7. Salary prediction for new employee input
8. Interactive prediction workflow

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Random Forest Regressor
- gdown (dataset download)

## Usage
1. Open `Salary_Prediction_Using_Random_Forest.ipynb` in **Jupyter Notebook** or **Google Colab**.
2. Install the required dependencies:
   ```bash
   pip install gdown pandas numpy matplotlib scikit-learn
   ```
3. Run all notebook cells. The dataset (`expected_ctc.csv`) will be downloaded automatically using **gdown**.
4. Train the Random Forest model and evaluate its performance.
5. Use the trained model to predict salaries for new employee data.

## Model Evaluation
The model is evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

These metrics help assess the prediction accuracy and overall performance of the Random Forest Regression model.