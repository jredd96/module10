import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "0fb81da1b84240329af93a39344eb572"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
  # prepare inputs for use
  if unit_type == "elevators":
    wmata_unit_type = "ELEVATOR"
  elif unit_type == "escalators":
    wmata_unit_type = "ESCALATOR"

  # create an empty list called 'incidents'
  incidents = []

  # use 'requests' to do a GET request to the WMATA Incidents API
  response = requests.get(INCIDENTS_URL, headers=headers)

  # retrieve the JSON from the response
  response_json = response.json()["ElevatorIncidents"]

  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
  # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition     
  #   -StationCode, StationName, UnitType, UnitName
  for incident in response_json:
     if incident["UnitType"] == wmata_unit_type:
        curr_inc_dict = dict(StationCode = incident["StationCode"], 
                             StationName = incident["StationName"],
                             UnitType = incident["UnitType"],
                             UnitName = incident["UnitName"])
        
        # add each incident dictionary object to the 'incidents' list
        incidents.append(curr_inc_dict)

  # return the list of incident dictionaries using json.dumps()
  return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)
