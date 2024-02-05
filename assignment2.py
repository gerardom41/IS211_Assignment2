import argparse
import urllib.request
import logging
import datetime

logging.basicConfig(filename="errors.log", level=logging.ERROR)

def downloadData(url):
    """Downloads the data"""
    getData = urllib.request.urlopen(url)
    csvData = getData.read().decode('utf-8')

    return csvData

def processData(file_content):
    idNameBday = {}

    for line in file_content.split('\n'):
        if line:
            parts = line.split(',')
            try:
                personId, name, birthdayString = parts
                birthday = datetime.datetime.strptime(birthdayString, "%d/%m/%Y").date()
                idNameBday[int(personId)] = (name, birthday)

            except Exception:
                loggingError(personId)
                continue

    return idNameBday

def loggingError(personId):
    logging.error(f"Error processing line #{personId} for ID {personId}, where"\
        f" #{personId} and {personId} are the line number and ID,respectively,"\
        "of the person in the CSV file that has a mallformed date.")

def displayPerson(id, personData):
    for personId, (name, birthday) in personData.items():
        if id == personId:
            print(f"Person #{personId} is {name} with a birthday of {birthday}, where {personId} is"\
                f" the id the user requested,{name} is the name of the person from the file"\
                f" and {birthday} is the birthday of the user")

    if id not in personData:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")

    data = downloadData(url)
    idNameBday = processData(data)

    while data: 
        x = int(input("Enter an Id number: "))

        if x <= 0:
            exit()
        else:
            displayPerson(x, idNameBday)

    else:
        print("No data found")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
