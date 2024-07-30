# Internship Project for B2E

#### Description/process:
This project uses a Dataset of Expenses for advertising and sales.
In this i have created a webpage to upload the dataset where we are fetching it and after preprocessing, the clean data is uploaded(POST) to the API created by the company.
Then i fetched the uploaded data to perform Linear regression on Sales and TV (expense for advertising). 
The reason to select TV is because it is more correlated to the sales.
A scatter plot is shown to show the difference between the Actual Sales Vs Pedicted Sales using my regression model.
Finally a webpage to showcase the plot and table of Actual vs Predicted.

**Note: This is only for the advertising csv used in this project as the API creation and prediction process is done according to the specific dataset**

# Steps to run it Locally:
Open the folder in an code editor for better experience

### Step 1 - Clone the repository:
```
https://github.com/MKisKrazy/internship-project-B2E-
```

### Step 2 - Install the required modules/libraries

```
pip install -r requirements.txt
```
## Step 3 - Run the server:
### Navigate to the *myproject* folder using 
``` cd myproject ```
### Run the server using the command:
```python manage.py runserver```

## Step 4- To view the webpage:
``` http://127.0.0.1:8000/```

Go to this url after starting the server.

Click the **To upload the advertsing expenses dataset** button to nagivate to next page

Choose the 'advertising.csv' file (which i have provided in the repository) and click **upload** buutton to upload.

It will take sometime to upload and you will navigated to next page and you will see response code: 200 and the preview of the dataset which indicated successful upload to API

#### To start the prediction process click on **Start Prediction** button
It will take some time to do the prediction process and you will be nagivated to new page where u will see the model's *evaluation metrics*,*preprocessing analysis*,*correlation plots* and *final prediction plot* 

Click on View prediction to see a comparison on Actual Vs Predicted values of the sales data

# To view those different pages directly:
### Go to this url to see prediction output with plot directly with the data from API
``` http://127.0.0.1:8000/start_prediction```
### Go to this url to see Actual vs Predicted data
``` http://127.0.0.1:8000/predicted_data```



**Dataset in provided in the repository**
