import streamlit as st
import subprocess
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

warnings.filterwarnings('ignore')


############ Data Preprocessing ################
file_path = "data/MFdata_ready.csv"
df = pd.read_csv(file_path)

df.drop(['30Days','90Days', '1Year', 'context'], axis=1, inplace=True)
df.dropna(inplace=True)

df['Amount in Cr'] = (df['Avg Price']*df['Quantity'])/10000000

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
df['Month'] = df['Month'].replace(month_names)

startDate = df['Date'].min()
endDate = df['Date'].max()


############ Page Config #################
st.set_page_config(page_title='Dashboard', page_icon=':bar_chart:', layout='wide')
st.title(" :bar_chart: Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


########### Date Filter ##################
col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df['Date'] >= date1) & (df['Date'] <= date2)].copy()

########## SideBar #################
st.sidebar.header("Choose your filter: ")

# Filter for Institution
institution = st.sidebar.multiselect("Pick Institutional Investor", df['Institution Name'].unique())

if not institution:
    df2 = df.copy()
else:
    df2 = df[df["Institution Name"].isin(institution)]

# Filter for Year
year = st.sidebar.multiselect("Pick any Year", df['Year'].unique())

if not year:
    df3 = df2.copy()
else:
    df3 = df2[df2["Year"].isin(year)]

# Filter for Month
month = st.sidebar.multiselect("Pick any Month", df['Month'].unique())

if not month:
    df4 = df3.copy()
else:
    df4 = df3[df3["Month"].isin(month)]

df4 = df4.sort_values(by='Date', ascending=False)


################### Data Segregation for Tabs ######################
amountsorted = df4.sort_values(by='Amount in Cr', ascending=False)
percentagesorted = df4.sort_values(by='Percentage Traded', ascending=False)
growth30d = df4.sort_values(by='30_days_growth', ascending=False)
growth90d = df4.sort_values(by='90_days_growth', ascending=False)
growth1y = df4.sort_values(by='1_year_growth', ascending=False)

if len(amountsorted) >= 20:
    amountsorted = amountsorted.head(20)
elif len(amountsorted) >= 10:
    amountsorted = amountsorted.head(10)
else:
    amountsorted = amountsorted.head()

if len(percentagesorted) >= 20:
    percentagesorted = percentagesorted.head(20)
elif len(percentagesorted) >= 10:
    percentagesorted = percentagesorted.head(10)
else:
    percentagesorted = percentagesorted.head()

if len(growth30d) >= 20:
    growth30d = growth30d.head(20)
elif len(growth30d) >= 10:
    growth30d = growth30d.head(10)
else:
    growth30d = growth30d.head()

if len(growth90d) >= 20:
    growth90d = growth90d.head(20)
elif len(growth90d) >= 10:
    growth90d = growth90d.head(10)
else:
    growth90d = growth90d.head()

if len(growth1y) >= 20:
    growth1y = growth1y.head(20)
elif len(growth1y) >= 10:
    growth1y = growth1y.head(10)
else:
    growth1y = growth1y.head()

########################## TABS #############################################
tabs = ["By Amount in Cr", "By Percentage Traded", "By Growth in 30 days", "By Growth in 90 days", "By Growth in 1 year"]

# Create the tabs
amounttab, perctab, g30dtab, g90dtab, g1yrtab = st.tabs(tabs)

# Add content to each tab
with amounttab:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Stocks by Amount in Cr")
        fig = px.bar(amountsorted, x="Stock", y="Amount in Cr", text = ['Rs.{:,.2f} Cr'.format(x) for x in amountsorted['Amount in Cr']], color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f"Investment Breakdown by Stock")
        st.write(f"Percentage of Investment made in each of the company out of the top few investments")
        # Create the donut chart
        fig = px.pie(amountsorted, values="Amount in Cr", names="Stock", title="Investment Distributions")
        # Customize the layout (optional)
        fig.update_traces(hole=0.5, hoverinfo="text+percent+value")
        fig.update_layout(title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Month-wise Data")
    month_data = df4.groupby('Month')['Date'].count().reset_index(name='Count')
    some_df = df4.groupby('Month')['Amount in Cr'].sum().reset_index()
    month_data = merged_df = pd.merge(month_data, some_df, on='Month')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Count'], name='# Investments', offsetgroup=1),
        secondary_y=False,
    )
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Amount in Cr'], name='Total Amount', offsetgroup=2),
        secondary_y=True,
    )
    # Add titles and labels
    fig.update_layout(
        title_text='# of Investments and Total Investment by Months',
        xaxis_title='Month'
    )
    fig.update_yaxes(title_text='# of Investments', secondary_y=False)
    fig.update_yaxes(title_text='Total Investment', secondary_y=True)
    fig.update_layout(height=600)  # Set the height of the chart)
    st.plotly_chart(fig, use_container_width=True)

    ######################## Data Table ##########################
    
    st.subheader("Need to see data of some particular stock?")
    st.write("Found some stock to be interesting in the charts above? Just select it from the dropdown below.")
    stock1 = st.multiselect("Pick Stocks", df4['Stock'].unique())
    stock1df = df4[df4["Stock"].isin(stock1)]

    st.table(stock1df)

with perctab:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Stocks by Percentage Traded")
        fig = px.bar(percentagesorted, x="Stock", y="Percentage Traded", text = [f'{x*100:.2f}%'.format(x) for x in percentagesorted['Percentage Traded']], color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f"Investment Breakdown by Stock")
        st.write(f"Percentage of Investment made in each of the company out of the top few investments")
        # Create the donut chart
        fig = px.pie(percentagesorted, values="Percentage Traded", names="Stock", title="Investment Distributions")
        # Customize the layout (optional)
        fig.update_traces(hole=0.5, hoverinfo="text+percent+value")
        fig.update_layout(title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Month-wise Data")
    month_data = df4.groupby('Month')['Date'].count().reset_index(name='Count')
    some_df = df4.groupby('Month')['Amount in Cr'].sum().reset_index()
    month_data = merged_df = pd.merge(month_data, some_df, on='Month')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Count'], name='# Investments', offsetgroup=1),
        secondary_y=False,
    )
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Amount in Cr'], name='Total Amount', offsetgroup=2),
        secondary_y=True,
    )
    # Add titles and labels
    fig.update_layout(
        title_text='# of Investments and Total Investment by Months',
        xaxis_title='Month'
    )
    fig.update_yaxes(title_text='# of Investments', secondary_y=False)
    fig.update_yaxes(title_text='Total Investment', secondary_y=True)
    fig.update_layout(height=600)  # Set the height of the chart)
    st.plotly_chart(fig, use_container_width=True)

    ######################## Data Table ##########################
    
    st.subheader("Need to see data of some particular stock?")
    st.write("Found some stock to be interesting in the charts above? Just select it from the dropdown below.")
    stock2 = st.multiselect("Pick Stocks", df4['Stock'].unique(), key="percentage_traded")
    stock2df = df4[df4["Stock"].isin(stock2)]

    st.table(stock2df)

with g30dtab:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Stocks by 30_days_growth")
        fig = px.bar(growth30d, x="Stock", y="30_days_growth", text = [f'{x:,.2f}%'.format(x) for x in growth30d['30_days_growth']], color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f"Growth Breakdown by Stock")
        st.write(f"Percentage of Investment made in each of the company out of the top few investments")
        # Create the donut chart
        fig = px.pie(growth30d, values="30_days_growth", names="Stock", title="Growth Breakdown")
        # Customize the layout (optional)
        fig.update_traces(hole=0.5, hoverinfo="text+percent+value")
        fig.update_layout(title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Month-wise Data")
    month_data = df4.groupby('Month')['Date'].count().reset_index(name='Count')
    some_df = df4.groupby('Month')['Amount in Cr'].sum().reset_index()
    month_data = merged_df = pd.merge(month_data, some_df, on='Month')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Count'], name='# Investments', offsetgroup=1),
        secondary_y=False,
    )
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Amount in Cr'], name='Total Amount', offsetgroup=2),
        secondary_y=True,
    )
    # Add titles and labels
    fig.update_layout(
        title_text='# of Investments and Total Investment by Months',
        xaxis_title='Month'
    )
    fig.update_yaxes(title_text='# of Investments', secondary_y=False)
    fig.update_yaxes(title_text='Total Investment', secondary_y=True)
    fig.update_layout(height=600)  # Set the height of the chart)
    st.plotly_chart(fig, use_container_width=True)

    ######################## Data Table ##########################
    st.subheader("Need to see data of some particular stock?")
    st.write("Found some stock to be interesting in the charts above? Just select it from the dropdown below.")
    stock3 = st.multiselect("Pick Stocks", df4['Stock'].unique(), key="30d_growth")
    stock3df = df4[df4["Stock"].isin(stock3)]

    st.table(stock3df)

with g90dtab:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Stocks by 90_days_growth")
        fig = px.bar(growth90d, x="Stock", y="90_days_growth", text = [f'{x:,.2f}%'.format(x) for x in growth90d['90_days_growth']], color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f"Growth Breakdown by Stock")
        st.write(f"Percentage of Investment made in each of the company out of the top few investments")
        # Create the donut chart
        fig = px.pie(growth90d, values="90_days_growth", names="Stock", title="Growth Breakdown")
        # Customize the layout (optional)
        fig.update_traces(hole=0.5, hoverinfo="text+percent+value")
        fig.update_layout(title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Month-wise Data")
    month_data = df4.groupby('Month')['Date'].count().reset_index(name='Count')
    some_df = df4.groupby('Month')['Amount in Cr'].sum().reset_index()
    month_data = merged_df = pd.merge(month_data, some_df, on='Month')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Count'], name='# Investments', offsetgroup=1),
        secondary_y=False,
    )
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Amount in Cr'], name='Total Amount', offsetgroup=2),
        secondary_y=True,
    )
    # Add titles and labels
    fig.update_layout(
        title_text='# of Investments and Total Investment by Months',
        xaxis_title='Month'
    )
    fig.update_yaxes(title_text='# of Investments', secondary_y=False)
    fig.update_yaxes(title_text='Total Investment', secondary_y=True)
    fig.update_layout(height=600)  # Set the height of the chart)
    st.plotly_chart(fig, use_container_width=True)

    ######################## Data Table ##########################
    
    st.subheader("Need to see data of some particular stock?")
    st.write("Found some stock to be interesting in the charts above? Just select it from the dropdown below.")
    stock4 = st.multiselect("Pick Stocks", df4['Stock'].unique(), key="90d_growth")
    stock4df = df4[df4["Stock"].isin(stock4)]


with g1yrtab:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Stocks by 1_year_growth")
        fig = px.bar(growth1y, x="Stock", y="1_year_growth", text = [f'{x:,.2f}%'.format(x) for x in growth1y['1_year_growth']], color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader(f"Growth Breakdown by Stock")
        st.write(f"Percentage of Investment made in each of the company out of the top few investments")
        # Create the donut chart
        fig = px.pie(growth1y, values="1_year_growth", names="Stock", title="Growth Breakdown")
        # Customize the layout (optional)
        fig.update_traces(hole=0.5, hoverinfo="text+percent+value")
        fig.update_layout(title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Month-wise Data")
    month_data = df4.groupby('Month')['Date'].count().reset_index(name='Count')
    some_df = df4.groupby('Month')['Amount in Cr'].sum().reset_index()
    month_data = merged_df = pd.merge(month_data, some_df, on='Month')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Count'], name='# Investments', offsetgroup=1),
        secondary_y=False,
    )
    # Add Total Benefit to the chart
    fig.add_trace(
        go.Bar(x=month_data['Month'], y=month_data['Amount in Cr'], name='Total Amount', offsetgroup=2),
        secondary_y=True,
    )
    # Add titles and labels
    fig.update_layout(
        title_text='# of Investments and Total Investment by Months',
        xaxis_title='Month'
    )
    fig.update_yaxes(title_text='# of Investments', secondary_y=False)
    fig.update_yaxes(title_text='Total Investment', secondary_y=True)
    fig.update_layout(height=600)  # Set the height of the chart)
    st.plotly_chart(fig, use_container_width=True)

    ######################## Data Table ##########################
    
    st.subheader("Need to see data of some particular stock?")
    st.write("Found some stock to be interesting in the charts above? Just select it from the dropdown below.")
    stock5 = st.multiselect("Pick Stocks", df4['Stock'].unique(), key="1y_growth")
    stock5df = df4[df4["Stock"].isin(stock5)]


