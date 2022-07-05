import requests


def main():

    choice = input("[R]eport weather or [g]et all reports? ")

    while choice:
        if choice.lower().strip() == "r":
            report_event()

        elif choice.lower().strip() == "g":
            see_all_reports()
        else:
            print(f"Don't know what to do with {choice}")

        # Ask the user
        choice = input("[R]eport weather or [g]et all reports? ")


def report_event():
    desc = input("What is the weather like? ")
    city = input("What is the city? ")
    data = {
        "description": desc,
        "location": {
            "city": city  
        }
    }
    url = "http://127.0.0.1:8000/api/reports"
    response = requests.post(url, json=data)
    response.raise_for_status()
    print(f"Response reported for new event: {response.json()}")
    


def see_all_reports():
    url = "http://127.0.0.1:8000/api/reports"
    response = requests.get(url)
    # Check if everything is okay
    response.raise_for_status()
    # Convert from text to json
    reports = response.json()
    for report in reports:
        print(f"{report.get('location').get('city')} has {report.get('description')}")


if __name__ == "__main__":
    main()
