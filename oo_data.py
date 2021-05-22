import pandas as pd
import datetime
import csv


file="Department of Surgery OT Log (Responses) - MasterDataLog.csv"

class data_op:
    
    def __init__(self,year):
        
        self.year = year
        self.working_year=int(self.year[0:4]) #extract year from self.year incase self year is a value with month/day included
                                         #eg. instead of "2020" , it "2020-4" --> so working_year only extract year for self.year variable
                                         #this is important when using self.age_function on the year different from 2021, the code will break, age calculation will be wrong
        self.readmaster = pd.read_csv(file, parse_dates=True, index_col="Timestamp")
        self.readmaster = pd.DataFrame(self.readmaster).drop_duplicates()
        self.readmaster=self.readmaster.loc[year]

        self.readmaster["Pre Operative Diagnosis"]=self.readmaster["Pre Operative Diagnosis"].str.lower()
        self.readmaster["Post Operative Diagnosis"]=self.readmaster["Post Operative Diagnosis"].str.lower()
        self.readmaster["Procedure"]=self.readmaster["Procedure"].str.lower()
        self.readmaster["Surgeon"]=self.readmaster["Surgeon"].str.lower()
        self.readmaster["Patient's Name"] = self.readmaster["Patient's Name"].str.lower()
    



    def operation_KPI_dx (self,diagnosis):
        """filter according to diagnosis"""
        operation = self.readmaster[self.readmaster["Post Operative Diagnosis"].str.contains(diagnosis)]

        operation = operation[["Date", "Patient's Name", "I/C Number", "Post Operative Diagnosis","Procedure", "Type of Operation"]].drop_duplicates(subset=["Patient's Name"])
        
        operation["Patient's Name"] = operation["Patient's Name"].str.title()

        return operation


    def operation_KPI_operation (self,oper):
        """filter according to type of operation"""
        operation = self.readmaster[self.readmaster["Procedure"].str.contains(oper)]

        operation = operation[["Date", "Patient's Name", "I/C Number", "Post Operative Diagnosis","Procedure", "Type of Operation"]].drop_duplicates(subset=["Patient's Name"])

        return operation

    def followmonth(self, a, operation):
        """calculate the operation done according to months"""
        name = [operation]
        space=[" "]
        monthlist =[]
        monthname = ["Jan","Feb","March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Total"]
        for month in range(1,13):
            try:
                print(month, "\t", len(a.loc[self.year+"-"+str(month)])) #i used this because when the value in a month is zero it become key error
                monthlist.append(len(a.loc[self.year+"-"+str(month)]))
                
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
        a = a[~a["Post Operative Diagnosis"].str.contains(diagnosisName)]
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
        operation = self.readmaster[self.readmaster["Patient's Name"].str.contains(name)]
        operation = operation[["Date", "Patient's Name", "I/C Number", "Pre Operative Diagnosis","Procedure", "Type of Operation"]].drop_duplicates(subset=["Patient's Name"])
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
                if self.working_year+1<=birth.year<=2068:
                    lis_age.append(self.working_year-birth.year+100)
                else:
                    lis_age.append(self.working_year-birth.year)     
        
            except ValueError:
                lis_age.append("non-malaysian ic")     
        age  = pd.DataFrame(lis_age,columns=["Age"], index=a.index)
        return age
    
    def generate_monthly_file(self,file):
    
        out_ = open(file)                     #i open back file into csv format because i dont know how to reindex the timestamp column.
        out_=pd.read_csv(out_)                #if i just reindex from the start i cannot read the data for a specific months/year
        out_=out_.drop(columns=["Timestamp"]) #so i decided to just maintain the statement of parsing the timestamp into datetime function
        out_=out_.set_index([pd.Index([i for i in range(1,len(out_)+1)]),"Date"])
        out_["Patient's Name"]=out_["Patient's Name"].str.title()
        out_.to_csv(file, encoding = "utf-8", index = True)

    #generalize code below.. used in peads cencus
    #orchi = pd.concat([orchi,age], axis=1).reindex(orchi.index)
    #orchi.loc[lambda orchi:orchi["age"]<18,:]

    #used in HPB census
    #cbde_t=cbde_t.sort_values("Timestamp")


    #setel :
    #1)hernia
    #2)colorectal
    #3)breast
    #4)HPB
    #5)thyroid
    #6)upperGIT
    #7)splenectomy
