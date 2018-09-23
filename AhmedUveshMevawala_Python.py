
# coding: utf-8

# In[24]:

# Code written w.r.t Python 3.6 Standards
# importing required python library
import pandas as pd
import numpy as np
import json


# In[25]:

# change the directory as per machine on which the code is running
your_local_path="D:/Users/Uvesh/Desktop/UPX/Ubs/"


# In[26]:

#Read the Start of Day Position file
try:
    input = pd.read_csv(your_local_path+"Input_StartOfDay_Positions.txt")
except IOError:
    print ("Error: can\'t find file or read data")

#Reading transaction file
try:
    trans = pd.read_json(your_local_path+"1537277231233_Input_Transactions.txt")
except IOError:
    print ("Error: can\'t find file or read data")


# In[27]:

# Checking the values of the Input file w.r.t allowed values,data type

# Quantity has to be Interger numbers only - if not print error
if((input['Quantity'].dtypes != 'int64' )):
    print("Only Integer Numbers allowed in Quantity column of Input File")

# Account Type has to be either I(Internal),E(External) only - if not print error    
elif (not(input['AccountType'].isin(['E','I','e','i']).all())):
    print("Only I,E is allowed in AccountType Column of Input File")

# Account has to be Interger numbers only - if not print error    
elif((input['Account'].dtypes != 'int64' )):
    print("Only Integer Numbers allowed in Account column of Input File")

# Transaction Type has to be either B(Buy),S(Sell) only - if not print error    
if (not(trans['TransactionType'].isin(['B','S','b','s']).all())):
    print("Only B,S is allowed in Transaction Type Column of Transaction File")
    
# Transaction Qty has to be Interger numbers only - if not print error       
elif((trans['TransactionQuantity'].dtypes != 'int64' )):
    print("Only Integer Numbers allowed in TransactionQuantity column of Input File")


# In[28]:


    
#Separating the External & Intrnal Account type
df_E_acct = pd.DataFrame(input[input['AccountType']=='E'])
df_I_acct = pd.DataFrame(input[input['AccountType']=='I'])

#Column to calculate the end of day Quantity - Setting up with default value of start of day quantity 
df_I_acct['EOD_Qty']=df_I_acct['Quantity']
df_E_acct['EOD_Qty']=df_E_acct['Quantity']



# In[ ]:

# changing the index
df_E_acct=df_E_acct.set_index('Instrument')
df_I_acct=df_I_acct.set_index('Instrument')

#Creating delta feature to identify change in Quanity - setting up with initial value as 0
df_E_acct['Delta']=0
df_I_acct['Delta']=0


# In[29]:

# Initial values of before running the Process
print(df_E_acct)
print(df_I_acct)


# In[ ]:

#This is the main logic of Process

# Iterate over transaction file
for index, row in trans.iterrows():
    if(trans.loc[index,'TransactionType']=='B'): #if its Buy Transaction
        df_E_acct.loc[row['Instrument'],'EOD_Qty']=df_E_acct.loc[row['Instrument'],'EOD_Qty']+trans.loc[index,'TransactionQuantity']
        df_I_acct.loc[row['Instrument'],'EOD_Qty']=df_I_acct.loc[row['Instrument'],'EOD_Qty']-trans.loc[index,'TransactionQuantity']
    elif(trans.loc[index,'TransactionType']=='S'): #If its Sell Transaction
        df_E_acct.loc[row['Instrument'],'EOD_Qty']=df_E_acct.loc[row['Instrument'],'EOD_Qty']-trans.loc[index,'TransactionQuantity']
        df_I_acct.loc[row['Instrument'],'EOD_Qty']=df_I_acct.loc[row['Instrument'],'EOD_Qty']+trans.loc[index,'TransactionQuantity']
    


# In[ ]:



#calculating delta value for each instrument of External Account type
for index, row in df_E_acct.iterrows():
    df_E_acct.loc[index,'Delta'] = df_E_acct.loc[index,'EOD_Qty']-df_E_acct.loc[index,'Quantity']

#calculating delta value for each instrument of Internal Account type
for index, row in df_E_acct.iterrows():
    df_I_acct.loc[index,'Delta'] = df_I_acct.loc[index,'EOD_Qty']-df_I_acct.loc[index,'Quantity'] 


# In[31]:

#After running the process checking the WOD,Qty,Delta for each of the account type
print(trans)
print(df_E_acct)
print(df_I_acct)


# In[37]:

#preparing o combine the two dataframe
df_E_acct.reset_index(inplace=True)
df_I_acct.reset_index(inplace=True)

#concatinating the External,Internal account type dataframe
df_final = pd.concat([df_E_acct,df_I_acct],axis=0)
df_final.sort_values(by="Instrument",inplace=True)

#writing to csv file
df_final.to_csv(your_local_path+"End_Of_Day.txt",columns=['Instrument','Account','AccountType','EOD_Qty','Delta'],index=False)


# In[38]:


#calculating the Highest , Lowest Net transaction Instruments based on delta value
df_f = df_final[df_final['Delta']>0]


print("Lowest Volume Instrument: ",  df_f.loc[df_f['Delta'].idxmin()]['Instrument'])
print("Lowest Volume : ",df_f.loc[df_f['Delta'].idxmin()]['Delta'])


print("Highest Volume Instrument: ",  df_f.loc[df_f['Delta'].idxmax()]['Instrument'])
print("Highest Volume : ",df_f.loc[df_f['Delta'].idxmax()]['Delta'])


# In[34]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



