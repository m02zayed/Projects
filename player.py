from dataclasses import dataclass, field
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv


@dataclass
class Player:
    name: str
    team: str
    nationalty: str
    position: list[str]
    matches_played: int
    starts: int
    minutes: int
    goals: int
    assists: int
    xG: float
    xA: float
    nineties: float = field(init=False)

    def __post_init__(self):
        self.nineties = round(self.minutes/90, 1)

    @staticmethod
    def get_urls(file_path: str) -> list[dict]:
        with open(file_path, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            urls = list(reader)
        return urls

    @staticmethod
    def get_raw_info(urls: list[dict]) -> pd.DataFrame:
        for url in urls:
            page = urlopen(url).read()
            soup = BeautifulSoup(page, features="html.parser")
            table = soup.find('tbody')
            pre_df = dict()
            features_wanted = ['player', 'nationality', 'position', 'age',
                               'games', 'games_starts', 'minutes',
                               'minutes_90s', 'goals', 'assists', 'xg',
                               'xg_assist']
            rows = table.find_all('tr')
            for row in rows:
                if (row.find('th', {"scope": "row"}) is not None):
                    for f in features_wanted:
                        if f == 'player':
                            cell = row.find("th", {"data-stat": f})
                            a = cell.text.strip().encode()
                            text = a.decode("utf-8")
                            if f.replace('_', ' ').title() in pre_df:
                                pre_df[f.replace('_', ' ').title()].append(text)
                            else:
                                pre_df[f.replace('_', ' ').title()] = [text]
                        else:
                            cell = row.find("td", {"data-stat": f})
                            a = cell.text.strip().encode()
                            text = a.decode("utf-8")
                            if f.replace('_', ' ').title() in pre_df:
                                pre_df[f.replace('_', ' ').title()].append(text)
                            else:
                                pre_df[f.replace('_', ' ').title()] = [text]
            df = pd.DataFrame(pre_df)
            new_cols = {'Games Starts': 'Starts', 'Minutes 90S': '90s',
                        'Xg': 'xG', 'Xg Assist': 'xA'}
            df.rename(columns=new_cols, inplace=True)
            return df

        @staticmethod
        def get_clean_info(df: pd.DataFrame) -> pd.DataFrame:
            nation_regex = r'([A-Z]{3})'
            nation_extract = df['Nationality'].str.extract(nation_regex,
                                                        expand=False)
            df['Nationality'] = nation_extract
            df['Position'] = df['Position'].str.split(',')
            age_regex = r'^(\d{2})'
            age_extract = df['Age'].str.extract(age_regex, expand=False)
            df['Age'] = age_extract
            return df


# df = Player.get_raw_info()
# df = Player.get_clean_info(df)
# # print(df)
# print(df.head())

