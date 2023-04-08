from telethon.sync import TelegramClient
from telethon import functions, types, errors
import csv
import pandas as pd
import os


api_id = 000
api_hash = "abcdefg"
session_name = "my_session"

with TelegramClient(session_name, api_id, api_hash) as client:
    try:
        with client.takeout(contacts=True) as takeout:
            result = takeout(functions.contacts.GetSavedRequest())
            with open('contacts_temp.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                header = ["Name", "Given Name", "Additional Name", "Family Name", "Yomi Name", "Given Name Yomi", "Additional Name Yomi", "Family Name Yomi", "Name Prefix", "Name Suffix", "Initials", "Nickname", "Short Name", "Maiden Name", "Birthday", "Gender", "Location", "Billing Information", "Directory Server",
                          "Mileage", "Occupation", "Hobby", "Sensitivity", "Priority", "Subject", "Notes", "Language", "Photo", "Group Membership", "E-mail 1 - Type", "E-mail 1 - Value", "IM 1 - Type", "IM 1 - Service", "IM 1 - Value", "Phone 1 - Type", "Phone 1 - Value", "Website 1 - Type", "Website 1 - Value"]
                writer.writerow(header)
                for x in result:
                    name = f"{x.first_name} {x.last_name or ''}"
                    phone_number = x.phone
                    if phone_number.startswith("+"):
                        phone_number = phone_number[1:]
                    if phone_number.startswith("0"):
                        pass
                    elif phone_number.startswith("98"):
                        phone_number = "+" + phone_number
                    else:
                        phone_number = "0" + phone_number
                    row = [name, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                           None, None, None, None, None, None, None, None, "* myContacts", None, None, None, None, None, "Mobile", phone_number, None, ]
                    row = [cell.encode('utf-8-sig').decode('utf-8-sig') if cell else "" for cell in row]
                    writer.writerow(row)
    except errors.TakeoutInitDelayError as e:
        print('Must wait', e.seconds, 'before takeout')

df = pd.read_csv("contacts_temp.csv", sep=",", quotechar='"')

df["Phone 1 - Value"] = df["Phone 1 - Value"].astype(str).apply(lambda x: x.replace("+", ""))

df.loc[~df["Phone 1 - Value"].str.startswith("98") & ~df["Phone 1 - Value"].str.startswith("0"), "Phone 1 - Value"] = "0" + df["Phone 1 - Value"]

df.loc[df["Phone 1 - Value"].str.startswith("98"), "Phone 1 - Value"] = "+" + df["Phone 1 - Value"]

df.to_csv("contacts.csv", index=False)

if os.path.exists('contacts_temp.csv'):
    os.remove('contacts_temp.csv')
