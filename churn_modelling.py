import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTEENN
from sklearn.tree import DecisionTreeClassifier
import joblib

warnings.filterwarnings("ignore")

full_df=pd.read_csv("https://raw.githubusercontent.com/carlosfab/dsnp2/master/datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv")
label_encoded_df=full_df.copy()

le = LabelEncoder()
for col in ["gender" , "Partner"  , "Dependents" , "PhoneService" , 'PaperlessBilling' , 'Churn']:
    label_encoded_df[col]=le.fit_transform(label_encoded_df[col])

def col_encoder(col_val):
    if col_val == "Yes":
        return 1
    else:
        return 0
col_no_service = ['MultipleLines' , 'OnlineSecurity' , 'OnlineBackup' , 'DeviceProtection' , 'TechSupport' , 'StreamingTV' , 'StreamingMovies']
for col in  col_no_service:
    label_encoded_df[col] = label_encoded_df[col].apply(col_encoder)

labelled_df = label_encoded_df.copy()

total_charges_obj_df = label_encoded_df.copy()
total_charges_obj_df['TotalCharges']=pd.to_numeric(total_charges_obj_df['TotalCharges'] , errors="coerce")
blank_total_charges=total_charges_obj_df[total_charges_obj_df['TotalCharges'].isnull()].index

label_encoded_df=label_encoded_df.drop(blank_total_charges , axis=0)
before_floats = label_encoded_df.copy()
before_floats['TotalCharges']=pd.to_numeric(before_floats['TotalCharges'] , errors ='coerce')
label_encoded_df = before_floats.copy()
string_df = label_encoded_df[['InternetService' , 'Contract' , 'PaymentMethod']]
int_df = label_encoded_df.drop(['InternetService' , 'Contract' , 'PaymentMethod'],axis=1)

string_df_dummies = pd.get_dummies(string_df)
string_df_dummies = string_df_dummies.astype(int)

final_df =  pd.concat([int_df , string_df_dummies] , axis=1)

df=final_df.drop('customerID',axis=1)

X= df.drop('Churn' , axis=1)
y=df['Churn']

sm=SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(X,y)
resampled_X_train , resampled_X_test , resampled_y_train , resampled_y_test = train_test_split(X_resampled , y_resampled , test_size=0.2 , random_state=42)

from sklearn.svm import LinearSVC
smote_grid_svc_final = LinearSVC(penalty='l1',C=2 ,loss='squared_hinge',max_iter=7000 , dual ='auto') 
smote_grid_svc_final.fit(resampled_X_train,resampled_y_train)
smote_preds_grid_svc_final = smote_grid_svc_final.predict(resampled_X_test)

joblib.dump(smote_grid_svc_final, 'churn_prediction_model.joblib')

print(classification_report(resampled_y_test , smote_preds_grid_svc_final))