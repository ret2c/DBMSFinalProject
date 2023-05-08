from django.shortcuts import render
from django.http import JsonResponse
import mariadb

try:
    conn = mariadb.connect(
        user="roobtj11",
        password="tr4003",
        host="washington.uww.edu",
        port=3306,
        database="cs366-2231_roobtj11"
    )
    # print("Connection Sucessful") #Uncomment for Database Connection Debugging
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

curr = conn.cursor()

def updateContent(request):
    option = request.GET.get('option')
    
    if option == "TournamentWinners":
        result = getWinningTeams()

    elif option == "MaleTeams":
        result = teamsByGender('M')

    elif option == "FemaleTeams":
        result = teamsByGender('W')

    elif option == "TournamentWinnerInfo":
        result = tournamentWinnerInfo()

    elif option == "TeamRanks":
        result = teamRanks()

    elif option == "PosStats":
        result = posPlayerStats()

    elif option == "ErrorStats":
        result = errorStats()

    elif option == "PlayedTogether":
        result = playedTogether()

    elif "registeredTournaments" in option:
        print(option)
        name = option[21:]
        name = name.strip()
        result = registeredTournaments(name)
    
    elif "playerInfo" in option:
        name = option[10:]
        name = name.strip()
        result = playerInfo(name)

    elif "playerHeight" in option:
        height = option[12:]
        height = height.strip()
        result = teamsOverHeight(height)

    elif "teamsAgeRange" in option:
        ageRange = option[13:]
        ageRange = ageRange.strip()
        ageRange = ageRange.split('-')
        minAge = ageRange[0]
        maxAge = ageRange[1]
        result = teamsAgeRange(minAge, maxAge)

    elif "countryRanks" in option:
        country = option[12:]
        country = country.strip()
        result = ranksByCountry(country)
    
    elif "gameDuration" in option:
        duration = option[12:]
        duration = duration.strip()
        duration = int(duration)

        hours = duration // 60
        minutes = duration % 60
        duration = '{:02d}:{:02d}:00'.format(hours, minutes)

        result = gameStatsDuration(duration)

    resp_data = {
        'html' : result
    }

    # print(resp_data) #UNCOMMENT FOR DEBUGGING
    return JsonResponse(resp_data, status=200)

debugLim = ' LIMIT 20000' #variable for testing query times based on result size. change variable to '' for no lim

def getWinningTeams():
    curr.execute(
        "SELECT DISTINCT WinningTeamName, TournamentName FROM Plays"
    )

    results = ''.join(f"<tr><td>{TeamName[0]}</td><td>{str(TeamName[1])}</td></tr>" for TeamName in curr)
    headers = ["Team Name", "Tournament Won"]
    table = createTable(headers, results)

    return table

def teamsByGender(g):
    curr.execute(
        "SELECT TeamName FROM Team WHERE Gender='{}'".format(g)
    )
    results = ''.join([f'<tr><td>{TeamName[0]}</td></tr>' for TeamName in curr])
    if g == 'M':
        headers = ["Male Teams in Database (By Team Name)"]
    else:
        headers = ["Female Teams in Database (By Team Name)"]
    
    table = createTable(headers, results)

    return table

def tournamentWinnerInfo():
    curr.execute(
        "SELECT T.TeamName, P.TournamentName, P.Circuit, P.DATE FROM Plays P, Team T WHERE T.TeamName = P.WinningTeamName"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td><td>{str(info[3])}</td></tr>" for info in curr)
    headers = ["Team Name", "Tournament Name", "Circuit", "Date"]
    table = createTable(headers, results)
    return table

def teamRanks():
    curr.execute(
        "SELECT R.teamName, R.TournamentName, R.Rank from Registered R, Team T WHERE R.teamName = T.teamName"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td></tr>" for info in curr)
    headers = ["Team Name", "Tournament", "Team Rank"]
    table = createTable(headers, results)

    return table

def posPlayerStats():
    curr.execute(
        "SELECT DISTINCT L.PlayerName, P.TournamentName, P.GameNumber, P.HittingPercentage, P.Attacks, P.Kills, P.Aces FROM Player L, Performed P WHERE L.PlayerName = P.PlayerName" + debugLim
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td><td>{info[3]}</td><td>{str(info[4])}</td><td>{str(info[5])}</td><td>{str(info[6])}</td></tr>" for info in curr)
    headers = ["Player Name", "Tournament", "Game Number", "Hitting Percentage", "Attacks", "Kills", "Aces"]
    table = createTable(headers, results)

    return table

def errorStats():
    curr.execute(
        "SELECT DISTINCT L.PlayerName, P.TournamentName, P.GameNumber, P.HittingPercentage, P.ServingErrors, P.Errors FROM Player L, Performed P WHERE L.PlayerName = P.PlayerName" + debugLim
    )
    
    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td><td>{str(info[3])}</td><td>{str(info[4])}</td><td>{str(info[5])}</td></tr>" for info in curr)
    headers = ["Player Name", "Tournament", "Game Number", "Hitting Percentage", "Serving Errors", "Errors"]
    table = createTable(headers, results)
    
    return table

def playedTogether():
    curr.execute(
        "SELECT pt.Player1Name, pt.Player2Name, pt.TeamName FROM PlayTogether pt INNER JOIN Player p1 ON pt.Player1Name = p1.PlayerName INNER JOIN Player p2 ON pt.Player2Name = p2.PlayerName"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td></tr>" for info in curr)
    headers = ["Player 1 Name", "Player 2 Name", "Team Name"]
    table = createTable(headers, results)

    return table

def registeredTournaments(name):
    curr.execute(
        f"CALL playersRegisteredTournaments('{name}')"
    )
    
    results = ''.join(f"<tr><td>{str(tournamentName[0])}</td></tr>" for tournamentName in curr)
    if len(results) == 0:
        table = f"No Matching Player Found Under Name '{name}'."
    else:
        headers = [f"{name}'s Registered Tournaments"]
        table = createTable(headers, results)
        results = f"<h3>{name}'s Registered Tournaments</h3>" + results

    return table

def playerInfo(name):
    curr.execute(
        f"CALL getPlayerInfo('{name}')"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td><td>{str(info[3])}</td><td>{str(info[4])}</td></tr>" for info in curr)
    if len(results) == 0:
        table = f"No Matching Player Found Under Name '{name}'."
    else:
        headers = ["Name", "Gender", "DOB", "Height (inches)", "Country"]
        table = createTable(headers, results)

    return table

def teamsOverHeight(height):
    curr.execute(
        f"CALL teamsOverHeight({height})"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td><td>{str(info[2])}</td><td>{str(info[3])}</td></tr>" for info in curr)
    if len(results) == 0:
        table = "No Teams Found in this Height Range."
    else:
        headers = ["Player 1 Name", "Player 1 Height (in.)", "Player 2 Name", "Player 2 Height (in.)"]
        table = createTable(headers, results)

    return table

def teamsAgeRange(minAge, maxAge):
    curr.execute(
        f"CALL teamsInAgeRange({minAge}, {maxAge})"
    )

    results = ''.join(f"<tr><td>{str(team[0])}</td><td>{str(team[1])}</td><td>{str(team[2])}</td><td>{str(team[3])}</td></tr>" for team in curr)
    if len(results) == 0:
        table = "No Teams Found in This Age Range."
    else:
        headers = ["Player 1 Name", "Player 1 Age", "Player 2 Name", "Player 2 Age"]
        table = createTable(headers, results)

    return table

def ranksByCountry(country):
    curr.execute(
        f"CALL teamRanksByCountry('{country}')"
    )

    results = ''.join(f"<tr><td>{str(info[0])}</td><td>{str(info[1])}</td></tr>" for info in curr)
    if len(results) == 0:
        table = f"No results for country '{country}.'"
    else:
        headers = [f"Team Names ({country})", "Rank"]
        table = createTable(headers, results)

    return table

def gameStatsDuration(duration):
    curr.execute(
        f"SELECT DISTINCT G.TournamentName, G.GameNumber, G.ScoreSet1, G.ScoreSet2, G.ScoreSet3, G.Duration from Game G, Performed P WHERE G.GameNumber = P.GameNumber AND G.Duration LIKE '{duration}'"
    )

    results = ''.join(f"<tr><td>{str(score[0])}</td><td>{str(score[1])}</td><td>{str(score[2])}</td><td>{str(score[3])}</td><td>{str(score[4])}</td><td>{str(score[5])}</td></tr>" for score in curr)
    if len(results) == 0:
        table = f"No Games in Database Over Duration {duration}."
    else:
        headers = ["Tournament", "Game Number", "Game Score Set 1", "Game Score Set 2", "Game Score Set 3", "Game Duration (HH:MM:SS)"]
        table = createTable(headers, results)
    
    return table

def createTable(headers, results):
    tableHeaders = ''.join(f"<th>{header}</th>" for header in headers)
    print(tableHeaders)
    table = f"<table><thead><tr>{tableHeaders}</tr><tbody>{results}</tbody></table>"
    return table

