#! /usr/bin/python3

import psycopg2
import os
from config import config
from flask import Flask, render_template, request, redirect, url_for

class BuildingStruct():
	def __init__(self, name, btype, area, specs, time):
		self.name = name
		self.btype = btype
		self.area = area
		self.specs = specs
		self.time = time
		
buildingList = []
outputCost = 0
outputUsage = 0
namelist = []

#append in form "buildingList.append( BuildingStruct(nameval, btypeval, areaval,specsval, timeval) )"

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
	
	global outputCost
	global outputUsage
	global namelist
	 
	return render_template('my-form.html', cost=outputCost, usage=outputUsage, namelist=namelist)

# handle venue POST and serve result web page
@app.route('/building-handler', methods=['POST'])
def venue_handler():

	global outputCost
	global outputUsage
	global namelist

	if request.method == "POST":
		
		tempArray = [0, 0, 0, 0, 0]
		newBuilding = BuildingStruct(request.form["bname"], request.form["btype"], request.form["barea"], tempArray, 0)
		buildingList.append(newBuilding)

		tempArray[0] = 	float(request.form["btype"])
		tempArray[1] = 	float(request.form["bfood"])
		tempArray[2] = 	float(request.form["bstem"])
		tempArray[3] = 	float(request.form["bheat"])
		tempArray[4] = 	float(request.form["bac"])

	namelist = []
	outputCost = 0
	outputUsage = 0

	if buildingList:
		# List contains values
		for building in buildingList:
			a = outputCost + ((0.8330704 + 0.0000144 * float(building.area) + 0.2238008 * building.specs[0] - 0.2465293 * building.specs[1] + 0.1069584 * building.specs[2] + 1.1789412 * building.specs[3] + 0.0165981 * building.specs[4]) ** 3)
			b = outputUsage + ((2.9866395 + 0.0000517 * float(building.area) + 0.8023478 * building.specs[0] - 0.8838317 * building.specs[1] + 0.3834563 * building.specs[2] + 4.2266201 * building.specs[3] + 0.0595057 * building.specs[4]) ** 3)
			
			outputCost = round(a, 2)
			outputUsage = round(b, 2)	


			namelist.append(building.name)


	# Take input from building spec and add to a new building
	return redirect(url_for('form'))

# handle deleting buildig values
@app.route('/delete-handler', methods=['POST'])
def delete_handler():
	global outputCost
	global outputUsage
	global buildingList
	global namelist

	if request.method == "POST":
		outputCost = 0
		outputUsage = 0
		buildingList.clear()
		namelist.clear()

	return redirect(url_for('form'))

# serve form web page
@app.route('/average-handler', methods=['POST'])
def average_handler():

	if str(request.form['avBuild']) == "0":
		return redirect(url_for('form'))

	areaQuery = connect('SELECT gross_floor_area FROM Building WHERE property_name = '+ '\''+ request.form['avBuild'] + '\'' + ';')
	for row in areaQuery:
		totalArea = float(row[0])

	scoreQuery= connect('SELECT factor FROM Building WHERE property_name = '+ '\''+ request.form['avBuild'] + '\'' + ';')
	for row in scoreQuery:
		sScore = float(row[0])

	avCost = round(totalArea * 0.000433913130169089 * sScore, 2)
	avUsage = round(totalArea * 0.0199942919273583 * sScore, 2)
	
	nameQuery = connect('SELECT property_name FROM Building WHERE property_name = '+ '\''+ request.form['avBuild'] + '\'' + ';')
	for row in nameQuery:
		pName = str(row[0])

	ssWord = ""
	if sScore == 1:
		ssWord = "Average"
	if sScore == 1.25:
		ssWord = "Low"
	if sScore == 0.75:
		ssWord = "High"

	totalArea = int(totalArea)

	return render_template('my-averages.html', propName=pName, propArea=totalArea, costA=avCost, usageA=avUsage, scoreA=ssWord)

# handle returing to the main page
@app.route('/return-handler', methods=['POST'])
def return_handler():

	return redirect(url_for('form'))

# handle query POST and serve result web page
@app.route('/query-handler', methods=['POST'])
def query_handler():

	if str(request.form['query']) == "0":
		return redirect(url_for('form'))

	testrows = connect('SELECT * FROM Meter_Entry WHERE meter_name = '+ '\''+ request.form['query'] + '\'' + ';')
	testheads = ['Meter Consumption ID', 'Usage/Quantity', 'Cost($)', 'Start Date', 'End Date', 'Meter Name' ]
	return render_template('my-result.html', heads=testheads, rows=testrows)

if __name__ == '__main__':
    app.run(debug = True)
