import requests
from bs4 import BeautifulSoup
import os

url = "https://fbref.com/en/comps/24/Serie-A-Stats#all_results2024241"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def create_dataset(component, filename):
    table = soup.find(id=component)
    tbody = table.find('tbody')
    data = tbody.find_all('tr')

    if os.path.exists(filename):
        os.remove(filename)

    f = open(filename, 'wt')


    th = data[0].find('th')
    tds = data[0].find_all('td')
    f.write(th.get('data-stat'))
    for td in tds:
        f.write(', ' + td.get('data-stat'))

    f.write('\n')

    for team_data in data:
        f.write(team_data.find('th').find('a').get_text())
        for td in team_data.find_all('td'):
            f.write(', ' + td.get_text())
        f.write('\n')

#Create dataset for passes
create_dataset('stats_squads_passing_for', '2024-passes.csv') 

# Create dataset for defensive actions
create_dataset('stats_squads_defense_for', '2024-defensive-actions.csv')

# Create dataset for possession 
create_dataset('stats_squads_possession_for', '2024-possesion.csv')

# Create dataset for shoots
create_dataset('stats_squads_shooting_for', '2024-shoots.csv')

# Create dataset for defense
create_dataset('stats_squads_keeper_for', '2024-defense.csv')
