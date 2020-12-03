import bs4
import requests
import pandas as pd
from datetime import datetime as dt
from math import ceil


class SequimCovid:
    """Contains webscraper and csv updater for the SequimCovid class."""
    def __init__(self):
        """Initialises attributes for Sequim covid class. Scrapes table off website, grabs plain text of desired area,
        separates out row information and daily data, splits final large row into separate rows, filters extra spaces. """
        self.my_data = []
        self.my_df = pd.read_csv('my_covid_data.csv', index_col=0)
        self.df = pd.read_csv('sequim_covid_data.csv', index_col=0)
        self.res = requests.get('http://www.clallam.net/coronavirus/')
        self.res.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')
        self.elems = self.soup.find_all('td')
        self.info = self.elems[5:-9]  # Coronavirus table
        self.info = [x.text for x in self.info]  # drops tag names, only inner text
        self.row_names = ['New Cases']
        for x in self.info[:-2:2]:
            self.row_names.append(x)
        # titles alternates lines with data
        self.daily_data = ['0']
        for x in self.info[1:-2:2]:
            self.daily_data.append(x)

        # separates the combined last row on the website to three separate rows, splits off \n
        # and uses a list comprehension to remove the empty space.
        last_row_names = [i for i in str(self.info[-2]).split('\n') if i]
        for n in last_row_names:
            self.row_names.append(n)
        last_col_data = str(self.info[-1]).split('\n')
        for d in last_col_data:
            self.daily_data.append(d)

    def get_new_cases(self):
        """Takes todays total cases and subtracts yesterdays total cases, today's data gets updated from it's placeholder
        then the daily_data is added to the main dataframe as a new column with today's date as the header. This is then
        saved."""
        new_cases = int(self.daily_data[1]) - int(self.df.iloc[1,-1])  # today's total minus yesterdays total
        self.daily_data[0] = str(new_cases)
        self.df[dt.today().strftime('%m/%d/%Y')] = self.daily_data  # saves as today's date
        self.df.to_csv('sequim_covid_data.csv')
        print('Complete 1/2')

    def get_my_data(self):
        """grabs new dataframe with today's data, grabs the last two weeks of new cases and sums them up. This gets
        stored in the list called my_data, that value is also multiplied by 1.29 and rounded up with ceiling and also
        added to my_data. Finally my_data is added as a new column to my_df and saved."""
        updated_frame = pd.read_csv('sequim_covid_data.csv', index_col=0)
        cases_two_weeks = updated_frame.iloc[0, -14:]
        sum_cases = 0
        for x in cases_two_weeks:
            sum_cases += int(x)
        self.my_data.append(sum_cases)  # takes previous two week slice and adds total together
        per_one_hundred = ceil(sum_cases*1.29)  # multiplies by 1.29 to get cases per 100k
        self.my_data.append(per_one_hundred)
        self.my_df[dt.today().strftime('%m/%d/%Y')] = self.my_data
        self.my_df.to_csv('my_covid_data.csv')
        print('Complete 2/2')

    def create_dataframe(self):
        """Used to get dataframes up and running, just a storage space for important lines for now."""
        #df2[dt.today().strftime('%m/%d/%Y')] = self.daily_data  # DO NOT DELETE IMPORTANT FOR CREATING NEW COLUMNS
        #self.df.iloc[0,-2] = '0'  #  GOOD FOR REWRITING SINGLE CELLS
        pass

    def update_csv(self):
        """This is the main function of the class, it directs the writing of data to csv."""
        if self.df.columns[-1] == dt.today().strftime('%m/%d/%Y'):
            return print("Data up to date")
        else:
            self.get_new_cases()
            self.get_my_data()
            #df2[dt.today().strftime('%m/%d/%Y')] = self.daily_data  # DO NOT DELETE IMPORTANT FOR CREATING NEW COLUMNS
            return print('Complete')

    def input_date(self):
        """This is a function I use to enter in the handwritten spreadsheet with initial data, it loops and gets
        input for each of the rows that added that column to a dataframe"""
        running = True
        rows2 = ['New Cases for Two Weeks', 'Per 100,000']
        df2 = pd.DataFrame(index=rows2)
        print(df2)
        while running:
            date_data = []
            more_dates = input('Enter in date to add, n to quit [n]: ')
            if more_dates == 'n':
                break
            else:
                for title in rows2:
                    question = input(f"{title}: ")
                    if question:
                        date_data.append(question)
                    else:
                        date_data.append('N/A')
                df2[more_dates] = date_data
        # df2.to_csv('my_covid_data.csv')
        #return df2


# sequim = SequimCovid()
# sequim.update_csv()
