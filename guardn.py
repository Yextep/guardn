print("\033[1;94mInitializing GuardN...\033[0;94m")
from urllib.parse import urlencode
import requests, time, os, getpass, hashlib, json
try:

	print("""
 /~'$$$$$$$$$$$$$$$$$$$$$$\\
(    "$$$$$$$$$$$$$$$$$$$$$)
 |     "$$$$$$$$$$$$$$$$$$$
 $$,     "$$$$$$$$$$$$$$$$$
 $$$$,     "$$$$$$$$$$$$$$$
 '$$$$$,     "$$$$$$$$$$$$'        \033[5;1;39m_____                 ___  __\033[0;94m
  $$$$$$$,     "$$$$$$$$$$        \033[5;1;39m/ ___/_ _____ ________/ / |/ /\033[0;94m
  '$$$$$$$$,     "$$$$$$$'       \033[5;1;39m/ (_ / // / _ `/ __/ _  /    /\033[0;94m
   '$$$$$$$$$,     "$$$$'        \033[5;1;39m\\___/\\_,_/\\_,_/_/  \\_,_/_/|_/\033[0;94m
    '$$$$$$$$$$,     "$'
     '$$$$$$$$$$$,   /
      '$$$$$$$$$$$$/
        "$$$$$$$$$"
         '$$$$$$$'
           '"$$"
""")

	print("""Welcome to GuardN

\033[0m[1] Enable Facebook profile picture guard
[2] Disable Facebook profile picture guard
""")

	user_select = ""

	while user_select not in ["1", "2"]:
		user_select = input("\033[0;94mWhat do you want to do? [1-2]: \033[0m").strip()

	print()

	user_email = input("\033[0;94mEmail: \033[0m").strip()
	user_password = getpass.getpass("\033[0;94mPassword: \033[0m").strip()

	print()
	print("\033[0;94mLogging in to Facebook... ", end="", flush=True)

	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
	}
	data = {
		"api_key": "882a8490361da98702bf97a021ddc14d",
		"credentials_type": "password",
		"email": user_email,
		"format": "JSON",
		"generate_machine_id": "1",
		"locale": "en_US",
		"method": "auth.login",
		"password": user_password,
		"return_ssl_resources": "1",
		"v": "1.0"
	}

	sig = ""
	for key in data:
		sig += "%s=%s" % (key, data[key])
	sig += "62f8ce9f74b12f84c123cc23437a4a32"
	sig = hashlib.md5(sig.encode("utf-8")).hexdigest()
	data["sig"] = sig

	resp = requests.get("https://api.facebook.com/restserver.php?%s" % (urlencode(data)), headers=headers)
	if "access_token" in resp.text:
		access_token = resp.json()["access_token"]
		uid = resp.json()["uid"]
		print("Done")
	else:
		print("Failed")
		os._exit(1)

	print("%sabled profile picture guard... " % ("En" if user_select == "1" else "Dis"), end="", flush=True)

	resp = requests.post("https://graph.facebook.com/graphql", headers={"Authorization": "Bearer %s" % (access_token)}, data={"variables": json.dumps({"0": {"is_shielded": user_select == "1", "actor_id": uid, "client_mutation_id": "b0316dd6-3fd6-4beb-aed4-bb29c5dc64b0"}}), "doc_id": "1477043292367183"})
	if resp.status_code == 200:
		print("Done")
	else:
		print("Failed")
		os._exit(1)

	print("""\033[1;94m
Thanks for using GuardN. This project developed by Noxturnix
https://github.com/Noxturnix
\033[0m""")

except:
	print()
	os._exit(0)
