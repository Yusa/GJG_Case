import names, requests, random, uuid, pprint, pycountry, json
import time


ENDPOINT = "http://127.0.0.1:8000/user/create/bulk/"
COUNT = 500000
EACH = 1000
HEADERS = {'Content-type': 'application/json'}



our_json = {"count": EACH, "users":[]}
last_score = 1000000000
sent_data_count = 0
for i in range(COUNT):
	if i != 0 and i%EACH == 0:
		start = time.time()
		r = requests.post(ENDPOINT, data=json.dumps(our_json), headers=HEADERS)
		end = time.time()
		print(f"[{i}] Status code: {r.status_code}. Elapsed time: {end - start}")
		with open("out.log", "a+") as f:
			pp = pprint.PrettyPrinter(indent=4, stream=f)
			pp.pprint(our_json)
		our_json = {"count": EACH, "users":[]}

	name = names.get_full_name()
	user_id = str(uuid.uuid4())
	country = list(pycountry.countries)[random.randint(0, len(pycountry.countries)-1)].alpha_2
	rank = i+1
	points = random.randint(last_score-5, last_score)
	last_score = points

	our_json["users"].append({"display_name":name,
							  "user_id":user_id,
							  "country":country.lower(),
							  "rank":rank,
							  "points":points})
