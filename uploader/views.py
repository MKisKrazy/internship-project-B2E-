import pandas as pd
import numpy as np
from django.shortcuts import render
from .forms import UploadFileForm
from django.http import JsonResponse
import requests
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.metrics as sm
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-GUI environments
import matplotlib.pyplot as plt

def clean_file(file):
    content = file.read().decode('utf-8')
    cleaned_content = content.replace('\r\n', '\n').strip()
    return io.StringIO(cleaned_content)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                cleaned_file = clean_file(file)
                df = pd.read_csv(cleaned_file)
                preprocessed_data = preprocess_data(df)
                final_response_code = send_data_to_api(preprocessed_data)
                return render(request, 'uploader/success.html', {'data': df.head(), 'response_code': final_response_code})
            else:
                return JsonResponse({"error": "Invalid file type"})
    else:
        form = UploadFileForm()
    return render(request, 'uploader/upload.html', {'form': form})

def preprocess_data(df):
    df['TV'] = df['TV'].fillna(0)
    df['Radio'] = df['Radio'].fillna(0)
    df['Newspaper'] = df['Newspaper'].fillna(0)
    df['Sales'] = df['Sales'].fillna(0)
    return df

def send_data_to_api(df):
    api_url = 'https://api.apistudio.app/postapi/create/si_01_advertisement'
    headers = {'Content-Type': 'application/json'}
    success_count = 0
    total_requests = 0
    
    for _, row in df.iterrows():
        json_data = {
            "data": {
                "tv": str(row['TV']),
                "radio": str(row['Radio']),
                "newspaper": str(row['Newspaper']),
                "sales": str(row['Sales'])
            }
        }
        try:
            response = requests.post(api_url, json=json_data, headers=headers)
            total_requests += 1
            if response.status_code == 200:
                success_count += 1
        except Exception as e:
            total_requests += 1
    
    if success_count == total_requests:
        return 200
    elif success_count > 0:
        return 207
    else:
        return 500

def start_prediction(request):
    get_url = 'https://api.apistudio.app/getapi/si_01_advertisement/all'
    response = requests.get(get_url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
    else:
        return render(request, 'uploader/error.html', {'message': 'Failed to fetch data from the API'})

    duplicate_count = df.duplicated().sum()
    null_values = df.isna().sum()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    X = np.array(df['tv']).reshape(-1, 1)
    Y = np.array(df['sales']).reshape(-1, 1)
    N = np.array(df['newspaper']).reshape(-1, 1)
    R = np.array(df['radio']).reshape(-1, 1)

    axes[0].scatter(X, Y, color='red', label="TV corr")
    axes[0].set_xlabel('TV')
    axes[0].set_ylabel('Sales')
    axes[0].legend()

    axes[1].scatter(R, Y, color='green', label="Radio Corr")
    axes[1].set_xlabel('Radio')
    axes[1].set_ylabel('Sales')
    axes[1].legend()

    axes[2].scatter(N, Y, color='pink', label="Newspaper corr")
    axes[2].set_xlabel('Newspaper')
    axes[2].set_ylabel('Sales')
    axes[2].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    scatter_plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)
    model = LinearRegression()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(X_test, Y_test, color='blue', label="Data")
    ax.plot(X_test, Y_pred, color='black', label="Predicted")
    ax.set_xlabel('TV')
    ax.set_ylabel('Sales')
    ax.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    final_plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    mae, rmse, r2_square = evaluate_model(Y_test, Y_pred)
    responses, res_code = send_predictions_to_api(Y_test, Y_pred)
    
    return render(request, 'uploader/prediction_success.html', {
        'message': 'Prediction is successful and predicted values are successfully uploaded to the API.',
        'responses': responses,
        'mae': mae,
        'rmse': rmse,
        'r2_square': r2_square,
        'scatter_plot_data': scatter_plot_data,
        'final_plot_data': final_plot_data,
        'duplicate_count': duplicate_count,
        'null_values': null_values
    })

def evaluate_model(true, predicted):
    mae = sm.mean_absolute_error(true, predicted)
    mse = sm.mean_squared_error(true, predicted)
    rmse = np.sqrt(mse)
    r2_square = sm.r2_score(true, predicted)
    return mae, rmse, r2_square

def send_predictions_to_api(Y_test, Y_pred):
    api_url = 'https://api.apistudio.app/postapi/create/si_01_predictions'
    headers = {'Content-Type': 'application/json'}
    responses = []
    for actual, predicted in zip(Y_test, Y_pred):
        json_data = {
            "data": {
                "actual": str(actual[0]),
                "advertise_medium": "TV",
                "predicted": str(predicted[0])
            }
        }
        response = requests.post(api_url, json=json_data, headers=headers)
        responses.append(response.json())
    return responses, response.status_code

def predicted_data(request):
    return render(request, 'uploader/predicted_data.html')

def welcome(request):
    return render(request, 'uploader/home.html')
