#write functions

import json
import pandas as pd
import numpy as np
import requests
import re
from matplotlib import pyplot as plt
#Function number one: API extract library 
class FSstore(): 
    def __init__ (self, EIN):
        self.EIN = EIN
    
    def apiextract(self):
        tax_return_code = self.EIN #enter assertion if the ein starts with 0, user may need to put ein in paranteshsis
        url = f"https://projects.propublica.org/nonprofits/api/v2/organizations/{tax_return_code}.json"
        r = requests.get(url)
        r_text = r.text
        response = json.loads(r_text)
        re = response['filings_with_data']
        
        financialyear=[]
        for i in re:
            financialyear.append (i['tax_prd_yr'])
        totalasset=[]
        for i in re: 
            totalasset.append (i['totassetsend'])
        totalrev=[]
        for i in re: 
            totalrev.append (i['totrevenue'])
        funcexp=[]
        for i in re: 
            funcexp.append (i['totfuncexpns'])
        totallia=[]
        for i in re: 
            totallia.append (i['totliabend'])
        totalcontri=[]
        for i in re:
            totalcontri.append(i['totcntrbgfts'])
        totalprgrev=[]
        for i in re: 
            totalprgrev.append(i['totprgmrevnue'])
        fundexp=[]
        for i in re:
            fundexp.append(i['lessdirfndrsng'])
        otherrev=[]
        for i in re:
            otherrev.append(i['miscrevtot11e'])
        FSdf = pd.DataFrame(data=re, columns=["tax_prd_yr","totassetsend",'totrevenue','totfuncexpns','totliabend','totcntrbgfts','totprgmrevnue','lessdirfndrsng','miscrevtot11e'])
        FSdf.columns = ['Financial_year','Total_Asset','Total_Revenue','Total_Functional_Expense','Total_Liability','Total_Contribution','Total_program_revenue','Fundarising_Expense','Other_Revenue']
        FSdf=FSdf.set_index('Financial_year')
        return FSdf

#Function number two: Calculating ratios 
def fsratio(EIN):
    """
    This function can help to calculate your nonprofit fundraising efficiency ratio, profit margin, leverages
    
    Parameter 
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    
    Examples 
    ----------
    >>> fsratio(131644147)
    The function will return to a dataframe that consisted of fundraising efficiency ratio, profit margin, leverages ratios from past years 
    """
    #enter assertion if the ein starts with 0, user may need to put ein in paranteshsis
    exmaple1 = FSstore(EIN)
    FSdf=exmaple1.apiextract()
    #1. Fundaraising Efficiency
    FSdf['Fundraising_Efficiency'] = FSdf['Total_Contribution']/FSdf['Fundarising_Expense']
    FSdf.replace([np.inf, -np.inf], 0, inplace=True)
    #2. Profit Margin: (TotalRev - TotalExp)/TotalRev
    FSdf['Profit_Margin'] = (FSdf['Total_Revenue']-FSdf['Total_Functional_Expense'])/FSdf['Total_Revenue']
    #3. Leverages: TotalLia / TotalAsset
    FSdf['Leverages'] = FSdf['Total_Liability'] / FSdf['Total_Asset']
    Ratiodf = FSdf[['Fundraising_Efficiency','Profit_Margin','Leverages']]
    return(Ratiodf) 

#Function for calculating Fundraising Efficiency
def fudeff(EIN, year=2020):
    """
    This function can calculate the fundraising efficiency for the year and organization you are interested in. 

    Parameter
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    year: year you want to look up

    Examples
    ----------
    >>> fudeff('131644147',year = 2017)
    466.5765
    """
    exmaple1 = FSstore(EIN)
    df1=exmaple1.apiextract()
    df1=df1.reset_index()
    df1['Fundraising_Efficiency'] = df1['Total_Contribution']/df1['Fundarising_Expense']
    df1.replace([np.inf, -np.inf], 0, inplace=True)
    print('Fundraising efficiency is the amount a nonprofit organization spends to raise $1')
    print('The higher the result, the more efficient the organization is at raising money.')
    if year in df1['Financial_year'].values:
       df1 = df1.loc[df1['Financial_year']==year]
       num = df1['Fundraising_Efficiency'].values[0]
       return(round(num,4))
    else:
        print('Ratio Not Available')
    print('jfkansld')

#Function for calculating Profit Margin
def pm(EIN, year=2020):
    """
    This function can calculate the profit margin for the year and organization you are interested in. 

    Parameter
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    year: year you want to look up

    Examples
    ----------
    >>> pm('131644147',year = 2017)
    0.1345
    """
    exmaple1 = FSstore(EIN)
    df1=exmaple1.apiextract()
    df1=df1.reset_index()
    df1['Profit_Margin'] = (df1['Total_Revenue']-df1['Total_Functional_Expense'])/df1['Total_Revenue']
    df1.replace([np.inf, -np.inf], 0, inplace=True)
    print('profit margin stands of the percentage of revenue that has turned into profits')
    print('Profit Margin is usually compared with company performance from past years')
    if year in df1['Financial_year'].values:
       df1 = df1.loc[df1['Financial_year']==year]
       ans = (df1['Profit_Margin'].values[0])
       return(round(ans,4))
    else:
        print('Ratio Not Available')


#Function for calculating Leverages
def lvg(EIN, year=2020):
    """
    This function can calculate the leverage for the year and organization you are interested in. 

    Parameter
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    year: year you want to look up

    Examples
    ----------
    >>> lvg('131644147',year = 2017)
    0.1912
    """
    exmaple1 = FSstore(EIN)
    df1=exmaple1.apiextract()
    df1=df1.reset_index()
    df1['Leverages'] = df1['Total_Liability'] / df1['Total_Asset']
    df1.replace([np.inf, -np.inf], 0, inplace=True)
    print('leverage measures how reliant is an organization on debt?')
    print('A lower score is better here, with the top-rated charities generally having ratios of less than 5% to 10%.')
    if year in df1['Financial_year'].values:
       df1 = df1.loc[df1['Financial_year']==year]
       ans2 = (df1['Leverages'].values[0])
       return(round(ans2,4))
    else:
        print('Ratio Not Available')

    
#Function number three: Calculating growth and loss 
def fsgrowthloss(EIN):
    """
    This function can help to calculate the growth and loss for your nonprofit fundraising efficiency ratio, profit margin, leverages

    Parameter
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    year: year you want to look up

    Examples
    ----------
    >>> fsgrowthloss('131644147')
    The function will return to a dataframe that consisted of the growth or loss for fundraising efficiency ratio, profit margin, leverages ratios from past years 
    """
    #enter assertion if the ein starts with 0, user may need to put ein in paranteshsis
    Ratiodf1 = fsratio(EIN).copy()
    Ratiodf1['Fundraising_Efficiency_Growth/Loss']=(Ratiodf1['Fundraising_Efficiency'] -Ratiodf1['Fundraising_Efficiency'].shift(1))/Ratiodf1['Fundraising_Efficiency'].shift(1)
    Ratiodf1['Profit_Margin_Growth/Loss'] = (Ratiodf1['Profit_Margin']-Ratiodf1['Profit_Margin'].shift(1))/Ratiodf1['Profit_Margin'].shift(1)
    Ratiodf1['Leverages_Growth/Loss'] = (Ratiodf1['Leverages']-Ratiodf1['Leverages'].shift(1))/Ratiodf1['Leverages'].shift(1)
    Ratiodf1 = Ratiodf1.fillna(0)
    Ratiodf1=Ratiodf1.reset_index()
    Ratiodf1 = Ratiodf1[['Financial_year','Fundraising_Efficiency_Growth/Loss','Profit_Margin_Growth/Loss','Leverages_Growth/Loss']]
    return Ratiodf1

#Function number four: illustration
def illustrate(EIN):
    """
    This function can help to illustrate the growth and loss for your nonprofit fundraising efficiency ratio, profit margin, leverages

    Parameter
    ----------
    EIN: input an Empolyer Identificaion Number of the organization you are interested in 
    year: year you want to look up

    Examples
    ----------
    >>> illustrate('131644147')
    The function will return to three graphs that consisted of the growth or loss for fundraising efficiency ratio, profit margin, leverages ratios from past years 
    """
    #enter assertion if the ein starts with 0, user may need to put ein in paranteshsis
    Ratiodf1 = fsgrowthloss(EIN)
    
    fig, axs = plt.subplots(3,sharex=True,figsize=(8, 10))
    axs[0].bar(x=Ratiodf1['Financial_year'],height=Ratiodf1['Fundraising_Efficiency_Growth/Loss'])
    axs[0].plot(Ratiodf1['Financial_year'],Ratiodf1['Fundraising_Efficiency_Growth/Loss'])
    #plt.xlabel('Financial Year')
    #plt.ylabel('Growth/Loss Ratio Percentage')
    axs[0].set_title("Fundraising Efficiency Growth/Loss")

    axs[1].bar(x=Ratiodf1['Financial_year'],height=Ratiodf1['Profit_Margin_Growth/Loss'])
    axs[1].plot(Ratiodf1['Financial_year'],Ratiodf1['Profit_Margin_Growth/Loss'])
    #plt.xlabel('Financial Year')
    #plt.ylabel('Growth/Loss Ratio Percentage')
    axs[1].set_title("Profit Margin Growth/Loss")
    
    axs[2].bar(x=Ratiodf1['Financial_year'],height=Ratiodf1['Leverages_Growth/Loss'])
    axs[2].plot(Ratiodf1['Financial_year'],Ratiodf1['Leverages_Growth/Loss'])
    #plt.xlabel('Financial Year')
    #plt.ylabel('Growth/Loss Ratio Percentage')
    axs[2].set_title("Leverages Growth/Loss")

    plt.show()
    
