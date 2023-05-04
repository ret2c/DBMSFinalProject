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
    print("connection successful??") #REMOVE
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

curr = conn.cursor()

# Create your views here.
def updateContent(request):
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    # if request.is_ajax() and request.methof == "GET":
    option = request.GET.get('option')
    
    if option == "TournamentWinners":
        result = getWinningTeams()
    elif option == "MaleTeams":
        # result = "male teams works"
        result = teamsByGender('M')
        # result = "male teams"
        # option = "The selected Query was Query 2"
    elif option == "FemaleTeams":
        # result = "female teams works"
        result = teamsByGender('W')
        # option = "The selectedd query was Query 3"
    elif option == "TournamentWinnerInfo":
        result = tournamentWinnerInfo()
        option = "The selected Query was Query 4"
    elif option == "TeamRanks":
        result = teamRanks()
        option = "The selected Query was Query 5"


    resp_data = {
        'html' : result
    }
    print(resp_data) #REMOVE
    return JsonResponse(resp_data, status=200)

def getWinningTeams():
    curr.execute(
        "SELECT DISTINCT WinningTeamName FROM Plays LIMIT 10"
    )


    # results = ''.join([f'<td>{TeamName[0]}</td>' for TeamName in curr])

    results = ''.join([f'<div>{TeamName[0]}</div>' for TeamName in curr])
    results = '<h3>Tournament Winning Team Names</h3>' + results
    # table = f"<table><tr><th>Team Name</th></tr><tr>{results}</tr></table>"

    return results

def teamsByGender(g):
    curr.execute(
        "SELECT TeamName FROM Team WHERE Gender='{}'".format(g)
    )
    results = ''.join([f'<div>{TeamName[0]}</div>' for TeamName in curr])
    if g == 'M':
        results = '<h3>Male Teams in Database</h3>' + results
    else:
        results = '<h3>Female Teams in Database</h3>' + results

def tournamentWinnerInfo():
    curr.execute(
        "SELECT T.TeamName, P.Circuit, P.DATE FROM Plays P, Team T WHERE T.TeamName = P.WinningTeamName LIMIT 10"
    )
    results = ''.join(f'<div>{str(info[0])}&emsp;&emsp;&emsp;{str(info[1])}&emsp;&emsp;{str(info[2])}</div>' for info in curr)
    results = "<h3>Team Name&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Circuit&emsp;&emsp;Date</h3>" + results
    return results

def teamRanks():
    curr.execute(
        "SELECT R.teamName, R.Rank from Registered R, Team T WHERE R.teamName = T.teamName LIMIT 10"
    )
    results = ''.join(f'<div>{str(teamRank[0])}&emsp;&emsp;&emsp;&emsp;&emsp;{str(teamRank[1])}</div>' for teamRank in curr)
    results = "<h3>Team Name&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Team Rank</h3>" + results
    return results