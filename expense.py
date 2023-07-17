import csv
import pandas as pd

def add_expense(data):
    filepath = "expenses\expenses.csv"
    try:
        with open(filepath,'a',newline='') as file:
            expense = data
            writer = csv.writer(file)
            writer.writerow(expense)
            return 1
    except IOError:
        return 0



def delete_expense(data):
    data = data.split(" ")
    filepath = "expenses\expenses.csv"
    try:
        with open(filepath,'r') as file:
            lines = file.readlines()
            if len(lines)==0:
                return 2
            else:
                for line in lines:
                    expense = line.split(",")
                    if data[0]==expense[0] and data[1]==expense[1] and data[2]+'\n'==expense[3]:
                        lines.remove(line)
                        entries = []
                        for i in lines:
                            entries.append(i.split("\n")[0].split(","))
                        with open(filepath, 'w', newline='') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerows(entries)
                            return 1
                return 3
    except IOError:
        return 0
                    
def monthly_expense(month):
    filepath = "expenses\expenses.csv"
    df = pd.read_csv(filepath)
    df = df[df['month']==month]
    df = df.groupby('category')['amt'].sum().reset_index()
    return df.values.tolist()


def daily_expense(month):
    filepath = "expenses\expenses.csv"
    df = pd.read_csv(filepath)
    df = df[df['month']==month].iloc[:,1:]
    df = df.groupby('date').apply(lambda x: {k: v for k, v in zip(x['category'], x['amt'])}).reset_index()
    df.columns = ['date', 'category_amount_dict']
    return df.values.tolist()

