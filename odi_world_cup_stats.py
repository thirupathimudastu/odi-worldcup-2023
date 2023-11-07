import requests
from bs4 import BeautifulSoup

import pandas as pd

# URL to fetch
url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;orderby=start;spanmin1=05+Oct+2023;spanval1=span;template=results;type=batting;view=innings"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
    
#  function to use
column_to_drop = ''
def clean_numeric_columns(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)
    return df

def extract_team_and_clean_player(df, player_column_name):
    df['Team'] = df[player_column_name].str.extract(r'\((.*?)\)')
    df[player_column_name] = df[player_column_name].str.replace(r' \([A-Z]+\)', '')
    return df

def drop_column(df, column_name):
    if column_name in df.columns:
        df = df.drop(columns=[column_name])
    return df




def find_page_element(tag):
    return (
        tag.name == 'td' and
        tag.get('class') == ['left'] and
        'Page' in tag.get_text()
    )

page_element = soup.find(find_page_element)

if page_element:
    text = page_element.get_text()
    last_page = text.split()[-1]
    print(last_page)
else:
    print("Element not found.")


batter_list = []
for i in range(int(last_page)):
    if i==None:
        pass
            
    else:
        url=f'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;orderby=start;page={i+1};spanmin1=05+Oct+2023;spanval1=span;template=results;type=batting;view=innings'
        print(url)
        response1 = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            
            table = soup.find('tbody')
            table_html = str(table)
            
            
            for tr in table.find_all('tr'):
                row_items = []  # Store items in this row
                # Iterate through the <td> (table data) elements within the current row
                for td in tr.find_all('td'):
                    row_items.append(td.text.strip())  # Append the text content to the row_items list
                batter_list.append(row_items)  # Append the row items to the main items list

        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)


columns = ["Player", "Runs","Time_spend","Balls","Fours","Sixes","Strike_rate","Innings_number","","Oppositions","City","Date",""]
batter_df = pd.DataFrame(batter_list, columns=columns)
#-------------------------------------------------------------------------------------------
url="https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;orderby=start;spanmin1=05+Oct+2023;spanval1=span;template=results;type=bowling;view=innings"


response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

def find_page_element(tag):
    return (
        tag.name == 'td' and
        tag.get('class') == ['left'] and
        'Page' in tag.get_text()
    )

page_element = soup.find(find_page_element)

if page_element:
    text = page_element.get_text()
    last_page = text.split()[-1]
    print(last_page)
else:
    print("Element not found.")




bowler_list = []
for i in range(int(last_page)):
    print(i)
    if i==None:
        pass
            
    else:
        url=f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;orderby=start;page={i+1};spanmin1=05+Oct+2023;spanval1=span;template=results;type=bowling;view=innings"

        print(url)
        response1 = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            
            table = soup.find('tbody')
            table_html = str(table)
            
            
            for tr in table.find_all('tr'):
                row_items = []  # Store items in this row
                # Iterate through the <td> (table data) elements within the current row
                for td in tr.find_all('td'):
                    row_items.append(td.text.strip())  # Append the text content to the row_items list
                bowler_list.append(row_items)  # Append the row items to the main items list

        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)

bowler_columns=["Bowler","Overs","madin","Runs","Wickets","Economy","Innings","","Opposition","City","Date",""]
bowler_df = pd.DataFrame(bowler_list,columns=bowler_columns)





# ------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup

import pandas as pd

# URL to fetch
url = "https://www.espncricinfo.com/series/icc-cricket-world-cup-2023-24-1367856/points-table-standings"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('tbody')
    table_html = str(table)

points_table_list=[]
for tr in table.find_all('tr'):
    row_items = []
    for td in tr.find_all('td'):
        row_items.append(td.text.strip())
    points_table_list.append(row_items)
    
    
points_table_columns=["Team","matches","Win","Lost","Tie","no_result","Points","Net_run_rate","Series_form","Nxt_match","",""]
alternate_points_table_list = points_table_list[::2]
points_table_df = pd.DataFrame(alternate_points_table_list, columns=points_table_columns)


### !------------------------------trasnsformation
t_batter_df=batter_df
t_bowler_df=bowler_df
t_points_table_df=points_table_df


t_batter_df['Runs'] = t_batter_df['Runs'].str.replace('*', '')
t_batter_df['Runs'] = pd.to_numeric(t_batter_df['Runs'], errors='coerce')
t_batter_df['Runs'] = t_batter_df['Runs'].fillna(0)


# t_batter_df['Team'] = t_batter_df['Player'].str.extract(r'\((.*?)\)')
# t_batter_df['Player'] = t_batter_df['Player'].str.replace(r' \([A-Z]+\)', '')


batter_columns_to_clean = ['Runs','Time_spend','Balls','Fours','Sixes','Innings_number']
bowler_columns_to_clean=['madin','Runs','Wickets','Innings']
points_table_columns_to_clean=['matches','Win','Lost','Tie','no_result','Points']

t_batter_df = clean_numeric_columns(t_batter_df, batter_columns_to_clean)
t_bowler_df = clean_numeric_columns(t_bowler_df, bowler_columns_to_clean)
t_points_table_df = clean_numeric_columns(t_points_table_df, points_table_columns_to_clean)



t_batter_df = drop_column(t_batter_df, column_to_drop)
t_bowler_df = drop_column(t_bowler_df, column_to_drop)
t_points_table_df = drop_column(t_points_table_df, column_to_drop)

t_batter_df = extract_team_and_clean_player(t_batter_df, 'Player')
t_bowler_df = extract_team_and_clean_player(t_bowler_df, 'Bowler')


t_batter_df = drop_column(t_batter_df, column_to_drop)
t_bowler_df = drop_column(t_bowler_df, column_to_drop)
t_points_table_df=drop_column(t_points_table_df,column_to_drop)


t_points_table_df['Team'] = t_points_table_df['Team'].str.replace(r'\d', '', regex=True)


# #  loading starts from here 
# connection_string = "mssql+pyodbc://SS_TMudastu:kpugPn&p33$fY@OTUSDPSQL:1433/HandsOnPractice?driver=SQL Server"
# from sqlalchemy import create_engine
# engine = create_engine(connection_string)
# t_bowler_df.to_sql(name='bowler', con=engine, if_exists='replace', index=False)
# t_batter_df.to_sql(name='batter', con=engine, if_exists='replace', index=False)
# t_points_table_df.to_sql(name='points_table', con=engine, if_exists='replace', index=False)
