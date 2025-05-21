import requests
import time

gateway2FloorDict = {
	8: 1,
	9: 2,
	10: 2,
	11: 3,
	12: 3,
	13: 5,
	14: 5,
	15: 6,
	16: 6
}

def check_avail():
	siteUrl = "https://chargers.kitu.io/api/site/8"

	stations = requests.get(siteUrl).json()['stations']
	stations = sorted(stations, key = lambda station: station['gatewayId'])

	floor = 0
	for station in stations:
		stationFloor = gateway2FloorDict[station['gatewayId']]
		if floor is not stationFloor:
			floor = stationFloor
			print(f"-- Floor {stationFloor}")

		if station['info']['chargeStatus'] != "charging" and  station['info']['status'] != "offline":
			print(f"Charger {station['name']}: {station['info']['chargeStatus']} ({station['info']['status']})")

if __name__ == '__main__':
	while True:
		print("Checking for available spots...")
		check_avail()
		print("Sleeping...")
		time.sleep(300)
