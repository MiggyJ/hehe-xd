from csv import DictReader
import os

with open('response.csv') as file:
    response = DictReader(file)

    for e in response:
        os.system(f'git clone {e["Repo"]} ./{e["Subsystem"].replace(" ","_").lower()}/{e["Module Acronym"].lower()}')