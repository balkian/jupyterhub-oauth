from github import GitHub
import os
import sys
import json

ACCESS_TOKEN = os.environ.get("GH_ACCESS_TOKEN", None)
ORG = os.environ.get("GH_ORG", "gsi-upm")


gh = GitHub(access_token=ACCESS_TOKEN)

users = []

tfilter = sys.argv[1:]
allteams = gh.orgs(ORG).teams.get()
print(list(t["name"] for t in allteams))
tlist = list(t for t in allteams if t["name"] in tfilter)
print(tlist)

for t in tlist:
    print("Getting team: %s" % t["name"])
    t["members"] = gh.teams(t["id"]).members.get()
    for m in t["members"]:
        login = m["login"]
        users.append(login)

with open("userlist", "w") as f:
    for user in set(users):
        f.write(user)
        if user in ("oaraque", "balkian", "cif2cif"):
            f.write(" admin")
        f.write("\n")
