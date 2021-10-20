import pandas as pd
import datetime
import csv
from pandasgui import show
import re, os
from pathlib import Path

file = "Department_of_Surgery_Endoscopy_Log_(Responses).csv"
class data_op:
    
    def __init__(self,year):
        
        self.year = year
        self.year_age=int(self.year[0:4])
        self.readmaster = pd.read_csv(file, parse_dates=True, index_col="Timestamp")
        self.readmaster = self.readmaster.drop_duplicates(keep = 'first')
        self.readmaster=self.readmaster.loc[year]


    def logbook_ot_surgeon(self, surgeon):
        logbook = self.readmaster[self.readmaster["Surgeon"].str.contains(surgeon,flags = re.IGNORECASE, na=True, regex=True )]
        return logbook

    def logbook_ot_assistant(self, assistant):
        logbook = self.readmaster[self.readmaster["Assistant"].str.contains(assistant,flags=re.IGNORECASE, na=True, regex=True )]
        #show(logbook)
        return logbook

    def logbook_scope_surgeon(self, surgeon):
        logbook = self.readmaster[self.readmaster["Operator"].str.contains(surgeon,flags=re.IGNORECASE, na=True, regex=True )]
        #show(logbook)
        return logbook

    def logbook_scope_assist(self, assist):
        logbook = self.readmaster[self.readmaster["Assistant"].str.contains(assistant,flags=re.IGNORECASE, na=True, regex=True )]
        #show(logbook)
        return logbook
        

    def operation_KPI_dx (self,diagnosis):
        """filter according to diagnosis"""
        operation = self.readmaster[self.readmaster["Diagnosis Post Procedure"].str.contains(diagnosis, regex=True )]

        operation = operation[["Date", "Patient's Name", "I/C Number", "Diagnosis Post Procedure", "Type of Procedure"]].drop_duplicates(subset=["Patient's Name"])
        
        operation["Patient's Name"] = operation["Patient's Name"].str.title()

        return operation


    def operation_KPI_operation (self,oper):
        """filter according to type of operation"""
        operation = self.readmaster[self.readmaster["Procedure"].str.contains(oper, regex = True)]

        operation = operation[["Date", "Patient's Name", "I/C Number","Diagnosis Post Procedure","Procedure", "Type of Procedure"]].drop_duplicates(subset=["Patient's Name"])

        return operation

    def followmonth(self, a, operation):
        """calculate the operation done according to months"""
        name = [operation]
        space=[" "]
        monthlist =[]
        monthname = ["Jan","Feb","March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Total"]
        for month in range(1,13):
            try:
                print(month, "\t", len(a.loc[year+"-"+str(month)])) #i used this because when the value in a month is zero it become key error
                monthlist.append(len(a.loc[year+"-"+str(month)]))
                
            except KeyError:
                monthlist.append(0) # so this statementt is for counter the error
                
        monthlist.append(sum(monthlist))
        
        with open("file_bulanan.csv","a") as f:   #write to csv file.... 
            write = csv.writer(f)
            write.writerow(name)
            write.writerow(monthname)
            write.writerow(monthlist)
            write.writerow(space)
            f.close()


    def exclude_op(self,a,procedureName):   
        a = a[~a["Procedure"].str.contains(procedureName)]
        return a

    def exclude_dx(self,a,diagnosisName):
        a = a[~a["Diagnosis Post Procedure"].str.contains(diagnosisName)]
        return a

    def excluder(self,a,_column,exclude_name):
        """
        general excluder 
        """
        a = a[~a[_column].str.contains(exclude_name)]
        return a

    def includer(self,a,_column,exclude_name):
        a = a[a[_column].str.contains(exclude_name)]
        return a


    def search_name(self,name):
        operation = self.readmaster[self.readmaster["Patient's Name"].str.contains(name, flags = re.IGNORECASE,na=True, regex=True)]
        operation = operation[["Date", "Patient's Name", "I/C Number", "Diagnosis Post Procedure","Procedure", "Type of Procedure"]].drop_duplicates(subset=["Patient's Name"])
        operation["Patient's Name"] = operation["Patient's Name"].str.lower()
        return operation

    def age_(self,a):            #TODO : create a function to concatenate age 
        lis_age=[]
        z=""
        for ic in a["I/C Number"]:
            z = list(ic)
            try:
                birth = z[0]+z[1]+"-"+z[2]+z[3]+"-"+z[4]+z[5]
                birth = datetime.datetime.strptime(birth, "%y-%m-%d")
                if self.year_age+1<=birth.year<=2068:
                    lis_age.append(self.year_age-birth.year+100)
                else:
                    lis_age.append(self.year_age-birth.year)     
        
            except ValueError:
                lis_age.append("non-malaysian ic")
                
            except IndexError:
                lis_age.append("invalid ID")
                
        age  = pd.DataFrame(lis_age,columns=["Age"], index=a.index)
        return age
    
    def generate_monthly_file(self,file):
    
        out_ = open(file)                     #i open back file into csv format because i dont know how to reindex the timestamp column.
        out_=pd.read_csv(out_)                #if i just reindex from the start i cannot read the data for a specific months/year
        out_=out_.drop(columns=["Timestamp"]) #so i decided to just maintain the statement of parsing the timestamp into datetime function
        out_=out_.set_index([pd.Index([i for i in range(1,len(out_)+1)]),"Date"])
        out_["Patient's Name"]=out_["Patient's Name"].str.title()
        out_.to_csv(file, encoding = "utf-8", index = True)

    def generate_logbook(self,logbook, name):

        _path = Path.cwd()
        os.chdir(_path)
        
        pathlogbook = name+"_ot_"+self.year
        os.mkdir(pathlogbook)
        os.chdir(str(_path)+"/"+pathlogbook)
        logbook.to_csv(str(Path.cwd())+"/scope_"+name+".csv")
        
    
