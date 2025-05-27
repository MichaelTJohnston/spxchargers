import time
import streamlit as st
import pandas as pd

refresh = 300

@st.cache_data(ttl=refresh)
def check_avail():
	import requests
	siteUrl = "https://chargers.kitu.io/api/site/8"

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

	chargeStatus = {
		'charging': 'charging',
		'not charging': 'available'
	}

	print("Checking chargers...")

	stations = requests.get(siteUrl).json()['stations']
	stations = sorted(stations, key = lambda station: station['gatewayId'])

	stationStats = [] # Cleaned up list of stations with status

	floor = 0

	for station in stations:
		stats = {
			'charger': station['name'],
			'chargeStatus': chargeStatus[station['info']['chargeStatus']] if station['info']['status'] == 'online' else 'unknown',
			'status': station['info']['status'],
			'floor': gateway2FloorDict[station['gatewayId']],
			}
		stationStats.append(stats)

	return stationStats

def badge_color(station):

	badge_colors = {
		'not charging': 'green',
		'available': 'green',
		'charging': 'red',
		'offline': 'grey',
	}

	if station['status'] == 'offline':
		return badge_colors['offline']

	if station['chargeStatus'] == 'not charging' or station['chargeStatus'] == 'available':
		return badge_colors['not charging']
	else:
		return badge_colors['charging']

st.set_page_config(
	page_title = "Blue Lot J1772 Charger Dashboard",
	page_icon = "",
	layout = "wide",
	)

st.write("#### Blue Lot J1772 Charger Dashboard")
st.write(f"Last update: {pd.Timestamp.now():%Y-%m-%d %H:%M:%S} – Auto refreshing...")

prog_cont = st.empty()
with prog_cont:
	st.progress(1)

stations = check_avail()
stationlist = st.empty()
floor_cols = {1:0,2:1,3:2,5:3,6:4}
with stationlist.container():
	columns = st.columns(5)
	floor = ''
	for station in stations:
		col = columns[floor_cols[station['floor']]]
		if floor is not station['floor']:
			col.write(f"##### Floor {station['floor']}")
			floor = station['floor']

		col.markdown(f":{badge_color(station)}-badge[{station['charger']}: {station['chargeStatus'].title()} ({station['status']})]")

with prog_cont:
	for i in range(refresh):
		st.progress(1-i/refresh)
		time.sleep(1)
		if i == refresh-1:
			st.rerun()
