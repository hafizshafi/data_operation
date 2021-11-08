import ezsheets, os
from pathlib import Path
import pandas as pd
import re

def main():

    _path = Path.cwd()

    os.chdir(_path)

    ezsheets.init()
    
    titles = ezsheets.listSpreadsheets()
    
    print(titles.keys)
    
    
    for k,v in titles.items():
        if v=="Department of Surgery OT Log (Responses)":
            target_sheet = ezsheets.Spreadsheet(str(k))
            
    print(target_sheet.title)
    
    target_sheet.refresh()
    
    target_sheet.downloadAsCSV()
    
    print("successful download data")
    
    ################################append old data ##############################################
    
    print("appending data........")
    
    file1="Department_of_Surgery_OT_Log_(Responses)_asal.csv"
    file2 ="Department_of_Surgery_OT_Log_(Responses).csv"
    file3 = "Department_of_Surgery_Endoscopy_Log_(Responses).csv"
    
    read1 = pd.read_csv(file1, parse_dates=True, index_col="Timestamp")
    read1 = read1.rename(columns={"Patient's Name":"Patient Name", "I/C Number": "IC / Passport", "Post Operative Diagnosis":"Diagnosis Post Procedure"})
    read1 = read1.fillna(1)
    read1 = read1.drop(columns = "Pre Operative Diagnosis")
    read1 = read1.drop(columns = 'Unnamed: 14')
    
    read2 = pd.read_csv(file2, parse_dates=True, index_col="Timestamp")
    
    read3 = pd.read_csv(file3, parse_dates=True, index_col="Timestamp")
    read3=read3.rename(columns={"Patient's Name":"Patient Name", 
                                "I/C Number": "IC / Passport", 
                                "Operator":"Surgeon", 
                                "Type of Procedure": "Type of Operation", 
                                "Category of Operator": "Category of Surgeon",
                                "Complication (if any)":"Complications (if any)"
                               })
                               
    read3=read3[[  'Date', 
                   'Patient Name', 
                   'IC / Passport',
                   'Diagnosis Post Procedure',
                   'Procedure', 
                   'Complications (if any)', 
                   'Type of Operation', 
                   'Surgeon', 
                   'Assistant', 
                   'Category of Surgeon', 
                   'Supervisor', 
                   'Notes']]

    read_old = pd.concat([read3,read1])

    read_old = read_old.sort_index()
     
    read_old=read_old.rename(columns={ 
                            "Diagnosis Post Procedure":"Post Operative Diagnosis", 
                            "Type of Operation":"Operation Status", 
                            "Category of Operator": "Category of Surgeon"
                           })
                           
     #messing up with time
    read2['Time Start']=pd.to_datetime(read2['Time Start'], utc=False)
    read2['Time Start'] = read2['Time Start'].dt.date
    read2 = read2.rename(columns = {'Time Start':'Date',
                                'Complication':'Complications (if any)'
                               })
    read2 = read2.drop(['Time End','Remarks','RN / Registration Number','Sample Taken'], axis=1)
    read2 = read2[['Date', 'Patient Name', 'IC / Passport', 'Post Operative Diagnosis',
       'Procedure','Complications (if any)','Operation Status', 'Surgeon', 'Assistant',
       'Category of Surgeon', 'Supervisor']]
    read_old = read_old.drop(['Notes'], axis=1)
     
    read_total = read_old.append(read2)

    read_total.to_csv("Department_of_Surgery_OT_Endoscopy_Census1.csv")
     
    print("successfully appending data")
    

main()
