import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.pyplot import GridSpec
from matplotlib.dates import DateFormatter

##Company names
company_names = pd.DataFrame({'display_name':["Apple Inc", "Bank of America","Amazon.com","AT&T"],
    'options':["AAPL", "BAC", "AMZN", "T"]}) 

records = company_names.to_dict('records')

st.spinner(text="In progress...")

st.set_page_config(layout='wide')
st.markdown(
'''
<body>
    <h1
        style = 'font-size:50px;text-align:center;color:MidnightBlue;font-family:calibri;'>Stock Analysis
    </h1>
</body>

''',unsafe_allow_html=True)



select_row = st.beta_container()
intro_row = st.beta_container()
financials_row = st.beta_container()
performance_row = st.beta_container()
analytics_1_row = st.beta_container()
analytics_2_row = st.beta_container()
analytics_3_row = st.beta_container()


st.markdown(
    """
<style>
/* The input itself */
div[data-baseweb="select"] > div {
  background-color: Gold;
  font-size: 20px !important;
}

/* The list of choices */
li>span {
  color: Blue;
  font-size: 20px;
}
style>
""", unsafe_allow_html=True)

with select_row:
    comp_name_select = st.selectbox('Select Company Name',options=records,format_func=lambda records: f'{records["display_name"]}')

#get yfinance data
stock = yf.Ticker(comp_name_select['options'])
comp_info = stock.get_info(start ='2021-01-01',end = '2021-12-12')["longBusinessSummary"]
comp_prices = stock.history(period='5y')
comp_prices = comp_prices.dropna()
comp_prices['daily_return'] = comp_prices['Close'].pct_change()
comp_prices['10_days_moving_average'] = comp_prices['Volume'].rolling(10).mean()
comp_prices['20_days_moving_average'] = comp_prices['Volume'].rolling(20).mean()
comp_prices['50_days_moving_average'] = comp_prices['Volume'].rolling(50).mean()


#other companies data
other_companies = company_names[company_names['options'] != comp_name_select['options']]
other_companies = other_companies['options']
other_companies = other_companies.unique()


x_1 = other_companies[0]
x_2 = other_companies[1]
x_3 = other_companies[2]

other_companies = [x_1,x_2,x_3]
main_comp = comp_prices
main_comp[comp_name_select['options']] = main_comp['daily_return']
main_comp = main_comp[comp_name_select['options']]
for company in other_companies:
    x = company[0]
    x = yf.Ticker(company)
    other_comp_prices = x.history(period='5y')
    #other_comp_prices = other_comp_prices.dropna()
    other_comp_prices['daily_return'] = other_comp_prices['Close'].pct_change()
    other_comp_prices[company] = other_comp_prices['daily_return']
    other_comp_prices = other_comp_prices[company]
    main_comp = pd.concat([main_comp,other_comp_prices],axis=1)




with intro_row:

    st.markdown('''
    <ul  style = 'font-size:15px;background-color:PowderBlue;border-color:SlateBlue;border:0px solid;font-weight:300;font-family:calibri;'>
        I will get stock information, visualize different aspects of it, and finally look at a few ways of analyzing the risk of a stock, based on its previous performance history. I will also be predicting future stock prices through a Long Short Term Memory (LSTM) method. 
        <br> 
        I will attempt to answer the below questions: 
        <li>What is the change in price of the stock over time?</li>
        <li>What is the daily return of the stock on average?</li>
        <li>What is the moving average of the various stocks?</li>
        <li>What is the correlation between different stocks'?</li>
        <li>How much value do we put at risk by investing in a particular stock</li>
        <li>Predicting the closing price stock price using LSTM)</li>
    </ul>
    '''
    ,unsafe_allow_html=True)

    st.write(comp_info)


with performance_row:
    #plot 1
    st.markdown(
    '''
    <h2 style = 'font-size:25px;text-align:center;color:MidnightBlue;font-family:calibri;background-color:PowderBlue;'> Change in price of the stock over time
    </h2>
    ''',unsafe_allow_html=True)

    sns.set_style('dark')
    fig, axes = plt.subplots(figsize = (20,5))
    gs = GridSpec(nrows = 1, ncols = 2)
    for ax in fig.get_axes():
        ax.tick_params(bottom = False,labelbottom=False,left=False,labelleft=False)
    
    ax1 = fig.add_subplot(gs[0,0])
    ax1 = sns.lineplot(data=comp_prices[['Close','High','Low']],palette= "tab10")
    ax1.set_title('Closing Prices', color = 'Red')
    date_form = DateFormatter("%Y-%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.patch.set_facecolor('Khaki')
    ax1.set(ylabel=None)
    ax1.set(ylabel=None)

    ax2 = fig.add_subplot(gs[0,1])
    ax2 = sns.lineplot(data=comp_prices['Volume'],palette= "tab10")
    ax2.set_title('Volume', color = 'Blue')
    #date_form = DateFormatter("%Y")
    #ax2.xaxis.set_major_formatter(date_form)
    ax2.patch.set_facecolor('Khaki')
    ax2.set(ylabel=None)
    ax2.set(xlabel=None)

    st.write(fig)
    
    #plot 2
    st.markdown(
    '''
    <h2 style = 'font-size:25px;text-align:center;color:MidnightBlue;font-family:calibri;background-color:PowderBlue;'> Daily return of the stock on average
    </h2>
    ''',unsafe_allow_html=True)

    st.write(''' Below is a histogram showing the daily price and a line plot showing the Moving Average''')

    sns.set_style('dark')
    fig2, axes = plt.subplots(figsize = (20,5))
    gs = GridSpec(nrows = 1, ncols = 2)
    for ax in fig2.get_axes():
        ax.tick_params(bottom = False,labelbottom=False,left=False,labelleft=False)
    
    ax1 = fig2.add_subplot(gs[0,0])
    #ax1 = sns.lineplot(comp_prices['daily_return'], bins=100, color='purple')
    ax1 = sns.lineplot(data=comp_prices[['daily_return']],palette= "tab10")
    ax1.set_title('daily price return', color = 'Red')
    #date_form = DateFormatter("%Y")
    #ax1.xaxis.set_major_formatter(date_form)
    ax1.patch.set_facecolor('Khaki')
    #ax1.set(ylabel=None)
    #ax1.set(ylabel=None)

    ax2 = fig2.add_subplot(gs[0,1])
    ax2 = sns.lineplot(data=comp_prices[['10_days_moving_average','20_days_moving_average','50_days_moving_average']],palette= "tab10")
    ax2.set_title('10,20,50 days MA', color = 'Blue')
    #date_form = DateFormatter("%Y")
    #ax2.xaxis.set_major_formatter(date_form)
    ax2.patch.set_facecolor('Khaki')
    #ax2.set(ylabel=None)
   # ax2.set(xlabel=None)

    st.write(fig2)

    #plot 3
    st.markdown(
    '''
    <h2 style = 'font-size:25px;text-align:center;color:MidnightBlue;font-family:calibri;background-color:PowderBlue;'> Correlation Between the study Stock Returns and Other Major Stock Returns
    </h2>
    ''',unsafe_allow_html=True)

    sns.set_style('dark')
    fig3, axes = plt.subplots(figsize = (10,5))
    gs = GridSpec(nrows = 1, ncols = 1)
    for ax in fig3.get_axes():
        ax.tick_params(bottom = False,labelbottom=False,left=False,labelleft=False)


    ax1 = fig3.add_subplot(gs[0,0])
    #ax4 = sns.regplot(x = main_comp.iloc[:,3],y = main_comp.iloc[:,0],data = main_comp,color='seagreen')
    ax1 = sns.heatmap(main_comp.iloc[:,1:4].corr(),annot=True,cmap='summer')
    #date_form = DateFormatter("%Y")
    #ax4.xaxis.set_major_formatter(date_form)
    #ax4.patch.set_facecolor('Khaki')
    #ax4.set(ylabel=None)
    #ax4.set(xlabel=None)

    st.write(fig3)

    st.markdown(
    '''
    <h2 style = 'font-size:25px;text-align:center;color:MidnightBlue;font-family:calibri;background-color:PowderBlue;'> How much value do we put at risk by investing in the stock?
    </h2>
    ''',unsafe_allow_html=True)
    st.write(
    '''
    We will do this by comparing the expected return with the standard deviation of the daily returns.
    ''')

    sns.set_style('dark')
    fig4, axes = plt.subplots(figsize = (10,5))
    gs = GridSpec(nrows = 1, ncols = 1)
    for ax in fig4.get_axes():
        ax.tick_params(bottom = False,labelbottom=False,left=False,labelleft=False)


    ax1 = fig4.add_subplot(gs[0,0])
    #ax4 = sns.regplot(x = main_comp.iloc[:,3],y = main_comp.iloc[:,0],data = main_comp,color='seagreen')
    ax1 = sns.scatterplot(data=comp_prices[['daily_return']],x = comp_prices[['daily_return']].std(),y = comp_prices[['daily_return']].mean())
    ax1.set(ylabel='Expected Return')
    ax1.set(xlabel='Risk')

    st.write(fig4)


    st.markdown(
    '''
    <h2 style = 'font-size:25px;text-align:center;color:MidnightBlue;font-family:calibri;background-color:PowderBlue;'> Predicting the Stock Closing Price
    </h2>
    ''',unsafe_allow_html=True)
    st.write(
    '''
    We will do this by using tensorflow. To Update soon -- Ariel jumba
    ''')