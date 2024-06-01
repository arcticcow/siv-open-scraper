from django.shortcuts import render
import requests
import json

def home(request):
    # Specify the URL of the page to scrape
    apiUrl = 'https://ctfd.uscybergames.com/api/v1/scoreboard'

    # Send a GET request to the URL
    #response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    #soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the raw text from the page
    #raw_text = soup.get_text
    arg= "<<PUT YOUR API TOKEN HERE>>"
    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Token {arg}"

    S = requests.Session()
    X = S.get(f"{apiUrl}", headers=headers).text
    userlist = json.loads(X)


    # Extracting name and id as tuples
    users = [(entry['name'], entry['account_url'], entry['score']) for entry in userlist['data']]

    results = []

    # Printing the tuples
    for x in range(0,49):
        userscore = users[x][2]
        solveURL = 'https://ctfd.uscybergames.com/api/v1' + users[x][1] + '/solves'
        s = S.get(f"{solveURL}", headers=headers).text
        solvelist = json.loads(s)
        points = [(entry['challenge']) for entry in solvelist['data']]
        for item in points:
            if item['category'] == "Season IV Beginner\'s Game Room":
                userscore -=150

        results.append([users[x][0], userscore])

        print(userscore)
    context = { 'results':results }
    return render(request, 'index.html', context)