# Files

## File: .devcontainer/.dockerignore
````
!poetry.lock
!pyproject.toml
.cache
.devcontainer
.git
.gitignore
.pytest_cache
.tool-versions
.venv
.vscode
**/__pycache__
Dockerfile*
README.md
````

## File: .devcontainer/devcontainer.json
````json
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/docker-existing-dockerfile
{
	"name": "Dev Environment",
	// "build": {
	// 	"context": "..",
	// 	"dockerfile": "../Dockerfile.web"
	// },
  "service": "meetup-bot",
  "workspaceFolder": "/app",
  "dockerComposeFile": "../docker-compose.yml",
  "overrideCommand": true,
  "shutdownAction": "stopCompose",
  "customizations": {
    "vscode": {
      "extensions": [
        "aaron-bond.better-comments",
        "codezombiech.gitignore",
        "eamodio.gitlens",
        "EditorConfig.EditorConfig",
        "foxundermoon.shell-format",
        "GitHub.copilot-chat",
        "GitHub.copilot",
        "jetpack-io.devbox",
        "mads-hartmann.bash-ide-vscode",
        "mechatroner.rainbow-csv",
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "ms-python.python",
        "ms-vscode.atom-keybindings",
        "ms-vsliveshare.vsliveshare",
        "redhat.ansible",
        "redhat.vscode-yaml",
        "ryu1kn.partial-diff",
        "timonwong.shellcheck",
        "yzhang.markdown-all-in-one"
      ]
    }
  },
	"forwardPorts": ["3000:3000"]
}
````

## File: .github/workflows/infosec.yml
````yaml
name: InfoSec

on:
  pull_request:
  push:
  workflow_dispatch:
  schedule:
    - cron: "0 4 * * *"

jobs:
  creds:
    name: gitleaks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
````

## File: .github/workflows/release-please.yml
````yaml
name: Release Please

on:
  push:
    branches:
      - 'main'

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest

    steps:
      - name: Release with release-please
        uses: googleapis/release-please-action@v4
        with:

          token: ${{ secrets.RELEASE_PLEASE_TOKEN }}

          config-file: release-please-config.json

          manifest-file: .release-please-manifest.json
````

## File: .task/checksum/repomix
````
f0e9ad0eb7768e7023b6bd01e697a31
````

## File: app/resources/templates/login.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="https://unpkg.com/twinklecss@1.1.0/twinkle.min.css"/>
</head>
<body>
    <div class="flex p-4 m-6 justify-center">
        <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" method="POST" action="/auth/login" >
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              Username
            </label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" name="username" type="text">
          </div>
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
              Password
            </label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" name="password" type="password">
          </div>
          <div class="flex items-center justify-between">
            <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              Sign In
            </button>
          </div>
        </form>
      </div>
</body>
</html>
````

## File: app/resources/MESSAGE.md
````markdown
* Thu 7/7 at 7:00 pm OK Game Devs <https://www.meetup.com/oklahoma-game-developers/events/286544018/|Virtual Demo Day> on Twitch
* Fri 7/8 at 12:30 pm <https://www.meetup.com/okccoffeeandcode/events/286920205/|Gray Owl Coffee and Code>
* Sat 7/9 at 2:00 pm <https://www.meetup.com/okccoffeeandcode/events/286873531/|10th Street Kamp's Coffee and Code>
* Sat 7/9 at 2:00 pm OKC OSH <https://www.meetup.com/okc-osh/events/286777681/|Hybrid In Person and Virtual Hangout!> at Kamp's and on Zoom
* Sat 7/16 at 5:00 pm <https://www.meetup.com/okccoffeeandcode/events/286873269/|8th Street Meet and Greet>
* Tue 7/19 at 11:30 am <https://www.meetup.com/okcwebdevs/events/286713247/|A Practical Take on Web3> with John Mosesman at Clevyr
* Thu 7/21 at 6:00 pm <https://www.meetup.com/nerdbeers/events/286591587/|Nerd Beers at Parlor OKC> - Alcohol: optional. Geekiness: required.  
We're also taking suggestions and sometimes planning impromptu meetups for the <https://www.meetup.com/okccoffeeandcode/|OKC Coffee and Code> group in the #okc-metro channel!
````

## File: app/channels.csv
````
name,id
testingchannel,C02SS2DKSQH
meetup-slack-api,C03DEPND2EN
okc-metro,CB0NNS7QD
events,C6Z1NU15F
````

## File: app/groups.csv
````
url,urlname
https://www.meetup.com/aws-oklahomacity/,aws-oklahomacity
https://www.meetup.com/nerdbeers/,nerdbeers
https://www.meetup.com/ok-golang/,ok-golang
https://www.meetup.com/okc-design-and-tech/,okc-design-and-tech
https://www.meetup.com/okc-devsecops/,okc-devsecops
https://www.meetup.com/okc-lugnuts/,okc-lugnuts
https://www.meetup.com/okc-osh/,okc-osh
https://www.meetup.com/okc-sharp/,okc-sharp
https://www.meetup.com/okc-wordpress-users-group/,okc-wordpress-users-group
https://www.meetup.com/okccoffeeandcode/,okccoffeeandcode
https://www.meetup.com/okcwebdevs/,okcwebdevs
https://www.meetup.com/oklahoma-city-issa/,oklahoma-city-issa
https://www.meetup.com/oklahoma-city-techlahoma/,oklahoma-city-techlahoma
https://www.meetup.com/oklahoma-game-developers/,oklahoma-game-developers
https://www.meetup.com/oklahoma-kafka/,oklahoma-kafka
https://www.meetup.com/oklahoma-power-bi-user-group/,oklahoma-power-bi-user-group
https://www.meetup.com/pythonistas/,pythonistas
https://www.meetup.com/shecodesokc/,shecodesokc
````

## File: app/gunicorn.conf.py
````python
workers = 4
threads = 2
bind = "0.0.0.0:3000"
accesslog = "-"
````

## File: app/meetup_queries.gql
````graphql
# techlahoma SELF_ID (graphql playground)
query { self { id name } }

# recon
query {
	self {
		id
		name
		username
		memberUrl
	}
}

# join first party events then filter group info
query {
	self {
		id
		name
		username
		memberUrl
		upcomingEvents {
			count
			pageInfo {
				endCursor
			}
			edges {
				node {
					id
					title
					description
					dateTime
					eventUrl
					group {
						id
						name
						urlname
						link
						city
					}
				}
			}
		}
	}
}

#  events by query var
# {"eventId":"285533748"}
query($eventId: ID) {
	event(id: $eventId) {
		title
		description
		dateTime
		eventUrl
		group {
			id
			name
			proNetwork {
				id
			}
		}
	}
}

# search all events by group proNetwork id
# { "group": { "proNetwork": { "id": "364335959210266624" } } }
{ "id": "364335959210266624" }
query($id: ID!) {
	proNetwork(id: $id) {
		eventsSearch(filter: { status: UPCOMING }, input: { first: 25 }) {
			count
			pageInfo {
				endCursor
			}
			edges {
				node {
					id
					title
					description
					dateTime
					eventUrl
				}
			}
		}
	}
}

# search for non pro network group by urlname
{"urlname":"pythonistas"}
query($urlname: String!) {
	groupByUrlname(urlname: $urlname) {
		id
		description
		name
		urlname
		city
		link
		upcomingEvents(input: { first: 3 }) {
			count
			pageInfo {
				endCursor
			}
			edges {
				node {
					id
					title
					description
					dateTime
					eventUrl
					group {
						id
						name
						urlname
						link
						city
					}
				}
			}
		}
	}
}


# TODO: QA node ID == group ID
# I.e., https://www.meetup.com/find/?suggested=true&source=GROUPS&keywords=programming&categoryId=546&distance=tenMiles&location=us--ok--Oklahoma%20City
# query OKC area for programming groups' IDs
# NOTE: unable to use vars for lat/lon and source (enum: EVENTS/GROUPS)
{
	"query": "programming",
	"city": "Oklahoma City"
}
query ($query: String!, $city: String!) {
	keywordSearch(
		filter: {query: $query, lat: 35.467560, lon: -97.516426, city: $city, source: GROUPS}
	) {
		count
		pageInfo {
			endCursor
		}
		edges {
			node {
				id
			}
		}
	}
}

# TODO: if group ID is found, get events for that group; else, use `requests` to parse `urlname` from URL
````

## File: app/Procfile
````
web: gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-3000} --log-file -
````

## File: app/runtime.txt
````
python-3.11.2
````

## File: app/scratch.py
````python
env = Path('.env')
⋮----
DB_URL = config('DB_URL')
DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_PORT = config('DB_PORT', default=5432, cast=int)
⋮----
DB_URL = os.getenv('DB_URL')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = int(os.getenv('DB_PORT', default=5432))
⋮----
class User(BaseModel)
⋮----
username: str
email: str | None = None
disabled: bool | None = None
⋮----
class UserInDB(User)
⋮----
hashed_password: str
⋮----
db = Database()
⋮----
def main()
⋮----
user = UserInDB(username='test', hashed_password='test')
⋮----
user = db.User.get(username='test')
````

## File: bin/install.sh
````bash
TLD="$(git rev-parse --show-toplevel)"
ENV_FILE="${TLD}/.env"
[[ -f "${ENV_FILE}" ]] && export $(grep -v '^#' ${ENV_FILE} | xargs)
export NODE_OPTIONS="--openssl-legacy-provider"

usage() { echo "Usage: task install -- <yarn|mega-linter|pre-commit>"; }

if [ $
	usage
	exit 0
else
	args=$1
fi


main() {
	case "$args" in
		pre-commit)
			pre-commit install
			;;
		""|*)
			usage
			;;
	esac
}
main "$@"

exit 0
````

## File: gitleaks.toml
````toml
# SOURCE: https://github.com/zricethezav/gitleaks/blob/master/config/gitleaks.toml

title = "gitleaks config"

# append allowed files/directories to paths list
[allowlist]
description = "global allow lists"
paths = [
    '''gitleaks.toml''',
    '''(.*?)(jpg|gif|doc|docx|zip|xls|pdf|bin|svg|socket)$''',
    '''(go.mod|go.sum)$''',
    '''node_modules''',
    '''vendor''',
    '''(.*?).example''',
]

[[rules]]
description = "Adafruit API Key"
id = "adafruit-api-key"
regex = '''(?i)(?:adafruit)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "adafruit",
]

[[rules]]
description = "Adobe Client ID (OAuth Web)"
id = "adobe-client-id"
regex = '''(?i)(?:adobe)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "adobe",
]

[[rules]]
description = "Adobe Client Secret"
id = "adobe-client-secret"
regex = '''(?i)\b((p8e-)(?i)[a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "p8e-",
]

[[rules]]
description = "Age secret key"
id = "age secret key"
regex = '''AGE-SECRET-KEY-1[QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L]{58}'''
keywords = [
    "age-secret-key-1",
]

[[rules]]
description = "Airtable API Key"
id = "airtable-api-key"
regex = '''(?i)(?:airtable)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{17})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "airtable",
]

[[rules]]
description = "Algolia API Key"
id = "algolia-api-key"
regex = '''(?i)(?:algolia)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "algolia",
]

[[rules]]
description = "Alibaba AccessKey ID"
id = "alibaba-access-key-id"
regex = '''(?i)\b((LTAI)(?i)[a-z0-9]{20})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "ltai",
]

[[rules]]
description = "Alibaba Secret Key"
id = "alibaba-secret-key"
regex = '''(?i)(?:alibaba)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{30})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "alibaba",
]

[[rules]]
description = "Asana Client ID"
id = "asana-client-id"
regex = '''(?i)(?:asana)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9]{16})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "asana",
]

[[rules]]
description = "Asana Client Secret"
id = "asana-client-secret"
regex = '''(?i)(?:asana)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "asana",
]

[[rules]]
description = "Atlassian API token"
id = "atlassian-api-token"
regex = '''(?i)(?:atlassian|confluence|jira)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{24})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "atlassian","confluence","jira",
]

[[rules]]
description = "AWS"
id = "aws-access-token"
regex = '''(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'''
keywords = [
    "akia","agpa","aida","aroa","aipa","anpa","anva","asia",
]

[[rules]]
description = "Bitbucket Client ID"
id = "bitbucket-client-id"
regex = '''(?i)(?:bitbucket)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "bitbucket",
]

[[rules]]
description = "Bitbucket Client Secret"
id = "bitbucket-client-secret"
regex = '''(?i)(?:bitbucket)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "bitbucket",
]

[[rules]]
description = "Bittrex Access Key"
id = "bittrex-access-key"
regex = '''(?i)(?:bittrex)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "bittrex",
]

[[rules]]
description = "Bittrex Secret Key"
id = "bittrex-secret-key"
regex = '''(?i)(?:bittrex)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "bittrex",
]

[[rules]]
description = "Beamer API token"
id = "beamer-api-token"
regex = '''(?i)(?:beamer)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(b_[a-z0-9=_\-]{44})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "beamer",
]

[[rules]]
description = "Codecov Access Token"
id = "codecov-access-token"
regex = '''(?i)(?:codecov)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "codecov",
]

[[rules]]
description = "Coinbase Access Token"
id = "coinbase-access-token"
regex = '''(?i)(?:coinbase)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "coinbase",
]

[[rules]]
description = "Clojars API token"
id = "clojars-api-token"
regex = '''(?i)(CLOJARS_)[a-z0-9]{60}'''
keywords = [
    "clojars",
]

[[rules]]
description = "Confluent Access Token"
id = "confluent-access-token"
regex = '''(?i)(?:confluent)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{16})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "confluent",
]

[[rules]]
description = "Confluent Secret Key"
id = "confluent-secret-key"
regex = '''(?i)(?:confluent)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "confluent",
]

[[rules]]
description = "Contentful delivery API token"
id = "contentful-delivery-api-token"
regex = '''(?i)(?:contentful)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{43})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "contentful",
]

[[rules]]
description = "Databricks API token"
id = "databricks-api-token"
regex = '''(?i)\b(dapi[a-h0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "dapi",
]

[[rules]]
description = "Datadog Access Token"
id = "datadog-access-token"
regex = '''(?i)(?:datadog)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "datadog",
]

[[rules]]
description = "Discord API key"
id = "discord-api-token"
regex = '''(?i)(?:discord)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "discord",
]

[[rules]]
description = "Discord client ID"
id = "discord-client-id"
regex = '''(?i)(?:discord)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9]{18})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "discord",
]

[[rules]]
description = "Discord client secret"
id = "discord-client-secret"
regex = '''(?i)(?:discord)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "discord",
]

[[rules]]
description = "Doppler API token"
id = "doppler-api-token"
regex = '''(dp\.pt\.)(?i)[a-z0-9]{43}'''
keywords = [
    "doppler",
]

[[rules]]
description = "Dropbox API secret"
id = "dropbox-api-token"
regex = '''(?i)(?:dropbox)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{15})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "dropbox",
]

[[rules]]
description = "Dropbox long lived API token"
id = "dropbox-long-lived-api-token"
regex = '''(?i)(?:dropbox)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{11}(AAAAAAAAAA)[a-z0-9\-_=]{43})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "dropbox",
]

[[rules]]
description = "Dropbox short lived API token"
id = "dropbox-short-lived-api-token"
regex = '''(?i)(?:dropbox)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(sl\.[a-z0-9\-=_]{135})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [
    "dropbox",
]

[[rules]]
description = "Droneci Access Token"
id = "droneci-access-token"
regex = '''(?i)(?:droneci)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "droneci",
]

[[rules]]
description = "Duffel API token"
id = "duffel-api-token"
regex = '''duffel_(test|live)_(?i)[a-z0-9_\-=]{43}'''
keywords = [
    "duffel",
]

[[rules]]
description = "Dynatrace API token"
id = "dynatrace-api-token"
regex = '''dt0c01\.(?i)[a-z0-9]{24}\.[a-z0-9]{64}'''
keywords = [
    "dynatrace",
]

[[rules]]
description = "EasyPost API token"
id = "easypost-api-token"
regex = '''EZAK(?i)[a-z0-9]{54}'''
keywords = [
    "ezak",
]

[[rules]]
description = "EasyPost test API token"
id = "easypost-test-api-token"
regex = '''EZTK(?i)[a-z0-9]{54}'''
keywords = [
    "eztk",
]

[[rules]]
description = "Etsy Access Token"
id = "etsy-access-token"
regex = '''(?i)(?:etsy)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{24})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "etsy",
]

[[rules]]
description = "Facebook"
id = "facebook"
regex = '''(?i)(?:facebook)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "facebook",
]

[[rules]]
description = "Fastly API key"
id = "fastly-api-token"
regex = '''(?i)(?:fastly)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "fastly",
]

[[rules]]
description = "Finicity Client Secret"
id = "finicity-client-secret"
regex = '''(?i)(?:finicity)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{20})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "finicity",
]

[[rules]]
description = "Finicity API token"
id = "finicity-api-token"
regex = '''(?i)(?:finicity)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "finicity",
]

[[rules]]
description = "Flickr Access Token"
id = "flickr-access-token"
regex = '''(?i)(?:flickr)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "flickr",
]

[[rules]]
description = "Finnhub Access Token"
id = "finnhub-access-token"
regex = '''(?i)(?:finnhub)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{20})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "finnhub",
]

[[rules]]
description = "Finicity Public Key"
id = "flutterwave-public-key"
regex = '''FLWPUBK_TEST-(?i)[a-h0-9]{32}-X'''
keywords = [
    "flwpubk_test",
]

[[rules]]
description = "Flutterwave Secret Key"
id = "flutterwave-secret-key"
regex = '''FLWSECK_TEST-(?i)[a-h0-9]{32}-X'''
keywords = [
    "flwseck_test",
]

[[rules]]
description = "Flutterwave Encryption Key"
id = "flutterwave-encryption-key"
regex = '''FLWSECK_TEST-(?i)[a-h0-9]{12}'''
keywords = [
    "flwseck_test",
]

[[rules]]
description = "Frame.io API token"
id = "frameio-api-token"
regex = '''fio-u-(?i)[a-z0-9\-_=]{64}'''
keywords = [
    "fio-u-",
]

[[rules]]
description = "Freshbooks Access Token"
id = "freshbooks-access-token"
regex = '''(?i)(?:freshbooks)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "freshbooks",
]

[[rules]]
description = "GoCardless API token"
id = "gocardless-api-token"
regex = '''(?i)(?:gocardless)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(live_(?i)[a-z0-9\-_=]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "live_","gocardless",
]

[[rules]]
description = "GCP API key"
id = "gcp-api-key"
regex = '''(?i)\b(AIza[0-9A-Za-z\\-_]{35})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "aiza",
]

[[rules]]
description = "GitHub Personal Access Token"
id = "github-pat"
regex = '''ghp_[0-9a-zA-Z]{36}'''
keywords = [
    "ghp_",
]

[[rules]]
description = "GitHub OAuth Access Token"
id = "github-oauth"
regex = '''gho_[0-9a-zA-Z]{36}'''
keywords = [
    "gho_",
]

[[rules]]
description = "GitHub App Token"
id = "github-app-token"
regex = '''(ghu|ghs)_[0-9a-zA-Z]{36}'''
keywords = [
    "ghu_","ghs_",
]

[[rules]]
description = "GitHub Refresh Token"
id = "github-refresh-token"
regex = '''ghr_[0-9a-zA-Z]{36}'''
keywords = [
    "ghr_",
]

[[rules]]
description = "GitLab Personal Access Token"
id = "gitlab-pat"
regex = '''glpat-[0-9a-zA-Z\-\_]{20}'''
keywords = [
    "glpat-",
]

[[rules]]
description = "Gitter Access Token"
id = "gitter-access-token"
regex = '''(?i)(?:gitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "gitter",
]

[[rules]]
description = "HashiCorp Terraform user/org API token"
id = "hashicorp-tf-api-token"
regex = '''(?i)[a-z0-9]{14}\.atlasv1\.[a-z0-9\-_=]{60,70}'''
keywords = [
    "atlasv1",
]

[[rules]]
description = "Heroku API Key"
id = "heroku-api-key"
regex = '''(?i)(?:heroku)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "heroku",
]

[[rules]]
description = "HubSpot API Token"
id = "hubspot-api-key"
regex = '''(?i)(?:hubspot)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "hubspot",
]

[[rules]]
description = "Intercom API Token"
id = "intercom-api-key"
regex = '''(?i)(?:intercom)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{60})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "intercom",
]

[[rules]]
description = "Kraken Access Token"
id = "kraken-access-token"
regex = '''(?i)(?:kraken)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9\/=_\+\-]{80,90})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "kraken",
]

[[rules]]
description = "Kucoin Access Token"
id = "kucoin-access-token"
regex = '''(?i)(?:kucoin)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{24})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "kucoin",
]

[[rules]]
description = "Kucoin Secret Key"
id = "kucoin-secret-key"
regex = '''(?i)(?:kucoin)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "kucoin",
]

[[rules]]
description = "Launchdarkly Access Token"
id = "launchdarkly-access-token"
regex = '''(?i)(?:launchdarkly)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "launchdarkly",
]

[[rules]]
description = "Linear API Token"
id = "linear-api-key"
regex = '''lin_api_(?i)[a-z0-9]{40}'''
keywords = [
    "lin_api_",
]

[[rules]]
description = "Linear Client Secret"
id = "linear-client-secret"
regex = '''(?i)(?:linear)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "linear",
]

[[rules]]
description = "LinkedIn Client ID"
id = "linkedin-client-id"
regex = '''(?i)(?:linkedin|linked-in)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{14})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "linkedin","linked-in",
]

[[rules]]
description = "LinkedIn Client secret"
id = "linkedin-client-secret"
regex = '''(?i)(?:linkedin|linked-in)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{16})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "linkedin","linked-in",
]

[[rules]]
description = "Lob API Key"
id = "lob-api-key"
regex = '''(?i)(?:lob)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}((live|test)_[a-f0-9]{35})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "test_","live_",
]

[[rules]]
description = "Lob Publishable API Key"
id = "lob-pub-api-key"
regex = '''(?i)(?:lob)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}((test|live)_pub_[a-f0-9]{31})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "test_pub","live_pub","_pub",
]

[[rules]]
description = "Mailchimp API key"
id = "mailchimp-api-key"
regex = '''(?i)(?:mailchimp)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{32}-us20)(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mailchimp",
]

[[rules]]
description = "Mailgun public validation key"
id = "mailgun-pub-key"
regex = '''(?i)(?:mailgun)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(pubkey-[a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mailgun",
]

[[rules]]
description = "Mailgun private API token"
id = "mailgun-private-api-token"
regex = '''(?i)(?:mailgun)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(key-[a-f0-9]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mailgun",
]

[[rules]]
description = "Mailgun webhook signing key"
id = "mailgun-signing-key"
regex = '''(?i)(?:mailgun)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mailgun",
]

[[rules]]
description = "MapBox API token"
id = "mapbox-api-token"
regex = '''(?i)(?:mapbox)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(pk\.[a-z0-9]{60}\.[a-z0-9]{22})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mapbox",
]

[[rules]]
description = "Mattermost Access Token"
id = "mattermost-access-token"
regex = '''(?i)(?:mattermost)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{26})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "mattermost",
]

[[rules]]
description = "MessageBird API token"
id = "messagebird-api-token"
regex = '''(?i)(?:messagebird|message-bird|message_bird)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{25})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "messagebird","message-bird","message_bird",
]

[[rules]]
description = "MessageBird client ID"
id = "messagebird-client-id"
regex = '''(?i)(?:messagebird|message-bird|message_bird)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "messagebird","message-bird","message_bird",
]

[[rules]]
description = "Netlify Access Token"
id = "netlify-access-token"
regex = '''(?i)(?:netlify)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{40,46})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "netlify",
]

[[rules]]
description = "New Relic user API Key"
id = "new-relic-user-api-key"
regex = '''(?i)(?:new-relic|newrelic|new_relic)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(NRAK-[a-z0-9]{27})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "nrak",
]

[[rules]]
description = "New Relic user API ID"
id = "new-relic-user-api-id"
regex = '''(?i)(?:new-relic|newrelic|new_relic)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "new-relic","newrelic","new_relic",
]

[[rules]]
description = "New Relic ingest browser API token"
id = "new-relic-browser-api-token"
regex = '''(?i)(?:new-relic|newrelic|new_relic)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(NRJS-[a-f0-9]{19})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "nrjs-",
]

[[rules]]
description = "npm access token"
id = "npm-access-token"
regex = '''(?i)\b(npm_[a-z0-9]{36})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "npm_",
]

[[rules]]
description = "Nytimes Access Token"
id = "nytimes-access-token"
regex = '''(?i)(?:nytimes|new-york-times,|newyorktimes)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{32})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "nytimes","new-york-times","newyorktimes",
]

[[rules]]
description = "Okta Access Token"
id = "okta-access-token"
regex = '''(?i)(?:okta)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9=_\-]{42})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "okta",
]

[[rules]]
description = "Plaid Client ID"
id = "plaid-client-id"
regex = '''(?i)(?:plaid)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{24})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "plaid",
]

[[rules]]
description = "Plaid Secret key"
id = "plaid-secret-key"
regex = '''(?i)(?:plaid)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{30})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "plaid",
]

[[rules]]
description = "Plaid API Token"
id = "plaid-api-token"
regex = '''(?i)(?:plaid)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(access-(?:sandbox|development|production)-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "plaid",
]

[[rules]]
description = "PlanetScale password"
id = "planetscale-password"
regex = '''(?i)\b(pscale_pw_(?i)[a-z0-9=\-_\.]{32,64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "pscale_pw_",
]

[[rules]]
description = "PlanetScale API token"
id = "planetscale-api-token"
regex = '''(?i)\b(pscale_tkn_(?i)[a-z0-9=\-_\.]{32,64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "pscale_tkn_",
]

[[rules]]
description = "PlanetScale OAuth token"
id = "planetscale-oauth-token"
regex = '''(?i)\b(pscale_oauth_(?i)[a-z0-9=\-_\.]{32,64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "pscale_oauth_",
]

[[rules]]
description = "Postman API token"
id = "postman-api-token"
regex = '''(?i)\b(PMAK-(?i)[a-f0-9]{24}\-[a-f0-9]{34})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "pmak-",
]

[[rules]]
description = "Private Key"
id = "private-key"
regex = '''(?i)-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY-----[\s\S-]*KEY----'''
keywords = [
    "-----begin",
]

[[rules]]
description = "Pulumi API token"
id = "pulumi-api-token"
regex = '''(?i)\b(pul-[a-f0-9]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "pul-",
]

[[rules]]
description = "PyPI upload token"
id = "pypi-upload-token"
regex = '''pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,1000}'''
keywords = [
    "pypi-ageichlwas5vcmc",
]

[[rules]]
description = "Rubygem API token"
id = "rubygems-api-token"
regex = '''(?i)\b(rubygems_[a-f0-9]{48})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "rubygems_",
]

[[rules]]
description = "RapidAPI Access Token"
id = "rapidapi-access-token"
regex = '''(?i)(?:rapidapi)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9_-]{50})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "rapidapi",
]

[[rules]]
description = "Sendbird Access ID"
id = "sendbird-access-id"
regex = '''(?i)(?:sendbird)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sendbird",
]

[[rules]]
description = "Sendbird Access Token"
id = "sendbird-access-token"
regex = '''(?i)(?:sendbird)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sendbird",
]

[[rules]]
description = "SendGrid API token"
id = "sendgrid-api-token"
regex = '''(?i)\b(SG\.(?i)[a-z0-9=_\-\.]{66})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sg.",
]

[[rules]]
description = "Sendinblue API token"
id = "sendinblue-api-token"
regex = '''(?i)\b(xkeysib-[a-f0-9]{64}\-(?i)[a-z0-9]{16})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "xkeysib-",
]

[[rules]]
description = "Sentry Access Token"
id = "sentry-access-token"
regex = '''(?i)(?:sentry)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-f0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sentry",
]

[[rules]]
description = "Shippo API token"
id = "shippo-api-token"
regex = '''(?i)\b(shippo_(live|test)_[a-f0-9]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "shippo_",
]

[[rules]]
description = "Shopify access token"
id = "shopify-access-token"
regex = '''shpat_[a-fA-F0-9]{32}'''
keywords = [
    "shpat_",
]

[[rules]]
description = "Shopify custom access token"
id = "shopify-custom-access-token"
regex = '''shpca_[a-fA-F0-9]{32}'''
keywords = [
    "shpca_",
]

[[rules]]
description = "Shopify private app access token"
id = "shopify-private-app-access-token"
regex = '''shppa_[a-fA-F0-9]{32}'''
keywords = [
    "shppa_",
]

[[rules]]
description = "Shopify shared secret"
id = "shopify-shared-secret"
regex = '''shpss_[a-fA-F0-9]{32}'''
keywords = [
    "shpss_",
]

[[rules]]
description = "Slack token"
id = "slack-access-token"
regex = '''xox[baprs]-([0-9a-zA-Z]{10,48})'''
keywords = [
    "xoxb","xoxa","xoxp","xoxr","xoxs",
]

[[rules]]
description = "Slack Webhook"
id = "slack-web-hook"
regex = '''https:\/\/hooks.slack.com\/services\/[A-Za-z0-9+\/]{44,46}'''
keywords = [
    "hooks.slack.com",
]

[[rules]]
description = "Stripe"
id = "stripe-access-token"
regex = '''(?i)(sk|pk)_(test|live)_[0-9a-z]{10,32}'''
keywords = [
    "sk_test","pk_test","sk_live","pk_live",
]

[[rules]]
description = "Square Access Token"
id = "square-access-token"
regex = '''(?i)\b(sq0atp-[0-9A-Za-z\-_]{22})(?:['|\"|\n|\r|\s|\x60]|$)'''
keywords = [

]

[[rules]]
description = "Squarespace Access Token"
id = "squarespace-access-token"
regex = '''(?i)(?:squarespace)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "squarespace",
]

[[rules]]
description = "SumoLogic Access ID"
id = "sumologic-access-id"
regex = '''(?i)(?:sumo)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{14})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sumo",
]

[[rules]]
description = "SumoLogic Access Token"
id = "sumologic-access-token"
regex = '''(?i)(?:sumo)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{64})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "sumo",
]

[[rules]]
description = "Travis CI Access Token"
id = "travisci-access-token"
regex = '''(?i)(?:travis)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{22})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "travis",
]

[[rules]]
description = "Twilio API Key"
id = "twilio-api-key"
regex = '''SK[0-9a-fA-F]{32}'''
keywords = [
    "twilio",
]

[[rules]]
description = "Twitch API token"
id = "twitch-api-token"
regex = '''(?i)(?:twitch)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{30})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitch",
]

[[rules]]
description = "Twitter API Key"
id = "twitter-api-key"
regex = '''(?i)(?:twitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{25})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitter",
]

[[rules]]
description = "Twitter API Secret"
id = "twitter-api-secret"
regex = '''(?i)(?:twitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{50})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitter",
]

[[rules]]
description = "Twitter Access Token"
id = "twitter-access-token"
regex = '''(?i)(?:twitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9]{15,25}-[a-zA-Z0-9]{20,40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitter",
]

[[rules]]
description = "Twitter Access Secret"
id = "twitter-access-secret"
regex = '''(?i)(?:twitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{45})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitter",
]

[[rules]]
description = "Twitter Bearer Token"
id = "twitter-bearer-token"
regex = '''(?i)(?:twitter)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(A{22}[a-zA-Z0-9%]{80,100})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "twitter",
]

[[rules]]
description = "Typeform API token"
id = "typeform-api-token"
regex = '''(?i)(?:typeform)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(tfp_[a-z0-9\-_\.=]{59})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "tfp_",
]

[[rules]]
description = "Yandex API Key"
id = "yandex-api-key"
regex = '''(?i)(?:yandex)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(AQVN[A-Za-z0-9_\-]{35,38})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "yandex",
]

[[rules]]
description = "Yandex AWS Access Token"
id = "yandex-aws-access-token"
regex = '''(?i)(?:yandex)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(YC[a-zA-Z0-9_\-]{38})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "yandex",
]

[[rules]]
description = "Yandex Access Token"
id = "yandex-access-token"
regex = '''(?i)(?:yandex)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}(t1\.[A-Z0-9a-z_-]+[=]{0,2}\.[A-Z0-9a-z_-]{86}[=]{0,2})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "yandex",
]

[[rules]]
description = "Zendesk Secret Key"
id = "zendesk-secret-key"
regex = '''(?i)(?:zendesk)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([a-z0-9]{40})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
keywords = [
    "zendesk",
]

[[rules]]
description = "Generic API Key"
id = "generic-api-key"
regex = '''(?i)(?:key|api|token|secret|client|passwd|password|auth|access)(?:[0-9a-z\-_\t .]{0,20})(?:[\s|']|[\s|"]){0,3}(?:=|>|:=|\|\|:|<=|=>|:)(?:'|\"|\s|=|\x60){0,5}([0-9a-z\-_.=]{10,150})(?:['|\"|\n|\r|\s|\x60]|$)'''
secretGroup = 1
entropy = 3.5
keywords = [
    "key","api","token","secret","client","passwd","password","auth","access",
]
[rules.allowlist]
stopwords= [
    "client",
    "endpoint",
    "vpn",
    "_ec2_",
    "aws_",
    "authorize",
    "author",
    "define",
    "config",
    "credential",
    "setting",
    "sample",
    "xxxxxx",
    "000000",
    "buffer",
    "delete",
    "aaaaaa",
    "fewfwef",
    "getenv",
    "env_",
    "system",
    "example",
    "ecdsa",
    "sha256",
    "sha1",
    "sha2",
    "md5",
    "alert",
    "wizard",
    "target",
    "onboard",
    "welcome",
    "page",
    "exploit",
    "experiment",
    "expire",
    "rabbitmq",
    "scraper",
    "widget",
    "music",
    "dns_",
    "dns-",
    "yahoo",
    "want",
    "json",
    "action",
    "script",
    "fix_",
    "fix-",
    "develop",
    "compas",
    "stripe",
    "service",
    "master",
    "metric",
    "tech",
    "gitignore",
    "rich",
    "open",
    "stack",
    "irc_",
    "irc-",
    "sublime",
    "kohana",
    "has_",
    "has-",
    "fabric",
    "wordpres",
    "role",
    "osx_",
    "osx-",
    "boost",
    "addres",
    "queue",
    "working",
    "sandbox",
    "internet",
    "print",
    "vision",
    "tracking",
    "being",
    "generator",
    "traffic",
    "world",
    "pull",
    "rust",
    "watcher",
    "small",
    "auth",
    "full",
    "hash",
    "more",
    "install",
    "auto",
    "complete",
    "learn",
    "paper",
    "installer",
    "research",
    "acces",
    "last",
    "binding",
    "spine",
    "into",
    "chat",
    "algorithm",
    "resource",
    "uploader",
    "video",
    "maker",
    "next",
    "proc",
    "lock",
    "robot",
    "snake",
    "patch",
    "matrix",
    "drill",
    "terminal",
    "term",
    "stuff",
    "genetic",
    "generic",
    "identity",
    "audit",
    "pattern",
    "audio",
    "web_",
    "web-",
    "crud",
    "problem",
    "statu",
    "cms-",
    "cms_",
    "arch",
    "coffee",
    "workflow",
    "changelog",
    "another",
    "uiview",
    "content",
    "kitchen",
    "gnu_",
    "gnu-",
    "gnu.",
    "conf",
    "couchdb",
    "client",
    "opencv",
    "rendering",
    "update",
    "concept",
    "varnish",
    "gui_",
    "gui-",
    "gui.",
    "version",
    "shared",
    "extra",
    "product",
    "still",
    "not_",
    "not-",
    "not.",
    "drop",
    "ring",
    "png_",
    "png-",
    "png.",
    "actively",
    "import",
    "output",
    "backup",
    "start",
    "embedded",
    "registry",
    "pool",
    "semantic",
    "instagram",
    "bash",
    "system",
    "ninja",
    "drupal",
    "jquery",
    "polyfill",
    "physic",
    "league",
    "guide",
    "pack",
    "synopsi",
    "sketch",
    "injection",
    "svg_",
    "svg-",
    "svg.",
    "friendly",
    "wave",
    "convert",
    "manage",
    "camera",
    "link",
    "slide",
    "timer",
    "wrapper",
    "gallery",
    "url_",
    "url-",
    "url.",
    "todomvc",
    "requirej",
    "party",
    "http",
    "payment",
    "async",
    "library",
    "home",
    "coco",
    "gaia",
    "display",
    "universal",
    "func",
    "metadata",
    "hipchat",
    "under",
    "room",
    "config",
    "personal",
    "realtime",
    "resume",
    "database",
    "testing",
    "tiny",
    "basic",
    "forum",
    "meetup",
    "yet_",
    "yet-",
    "yet.",
    "cento",
    "dead",
    "fluentd",
    "editor",
    "utilitie",
    "run_",
    "run-",
    "run.",
    "box_",
    "box-",
    "box.",
    "bot_",
    "bot-",
    "bot.",
    "making",
    "sample",
    "group",
    "monitor",
    "ajax",
    "parallel",
    "cassandra",
    "ultimate",
    "site",
    "get_",
    "get-",
    "get.",
    "gen_",
    "gen-",
    "gen.",
    "gem_",
    "gem-",
    "gem.",
    "extended",
    "image",
    "knife",
    "asset",
    "nested",
    "zero",
    "plugin",
    "bracket",
    "mule",
    "mozilla",
    "number",
    "act_",
    "act-",
    "act.",
    "map_",
    "map-",
    "map.",
    "micro",
    "debug",
    "openshift",
    "chart",
    "expres",
    "backend",
    "task",
    "source",
    "translate",
    "jbos",
    "composer",
    "sqlite",
    "profile",
    "mustache",
    "mqtt",
    "yeoman",
    "have",
    "builder",
    "smart",
    "like",
    "oauth",
    "school",
    "guideline",
    "captcha",
    "filter",
    "bitcoin",
    "bridge",
    "color",
    "toolbox",
    "discovery",
    "new_",
    "new-",
    "new.",
    "dashboard",
    "when",
    "setting",
    "level",
    "post",
    "standard",
    "port",
    "platform",
    "yui_",
    "yui-",
    "yui.",
    "grunt",
    "animation",
    "haskell",
    "icon",
    "latex",
    "cheat",
    "lua_",
    "lua-",
    "lua.",
    "gulp",
    "case",
    "author",
    "without",
    "simulator",
    "wifi",
    "directory",
    "lisp",
    "list",
    "flat",
    "adventure",
    "story",
    "storm",
    "gpu_",
    "gpu-",
    "gpu.",
    "store",
    "caching",
    "attention",
    "solr",
    "logger",
    "demo",
    "shortener",
    "hadoop",
    "finder",
    "phone",
    "pipeline",
    "range",
    "textmate",
    "showcase",
    "app_",
    "app-",
    "app.",
    "idiomatic",
    "edit",
    "our_",
    "our-",
    "our.",
    "out_",
    "out-",
    "out.",
    "sentiment",
    "linked",
    "why_",
    "why-",
    "why.",
    "local",
    "cube",
    "gmail",
    "job_",
    "job-",
    "job.",
    "rpc_",
    "rpc-",
    "rpc.",
    "contest",
    "tcp_",
    "tcp-",
    "tcp.",
    "usage",
    "buildout",
    "weather",
    "transfer",
    "automated",
    "sphinx",
    "issue",
    "sas_",
    "sas-",
    "sas.",
    "parallax",
    "jasmine",
    "addon",
    "machine",
    "solution",
    "dsl_",
    "dsl-",
    "dsl.",
    "episode",
    "menu",
    "theme",
    "best",
    "adapter",
    "debugger",
    "chrome",
    "tutorial",
    "life",
    "step",
    "people",
    "joomla",
    "paypal",
    "developer",
    "solver",
    "team",
    "current",
    "love",
    "visual",
    "date",
    "data",
    "canva",
    "container",
    "future",
    "xml_",
    "xml-",
    "xml.",
    "twig",
    "nagio",
    "spatial",
    "original",
    "sync",
    "archived",
    "refinery",
    "science",
    "mapping",
    "gitlab",
    "play",
    "ext_",
    "ext-",
    "ext.",
    "session",
    "impact",
    "set_",
    "set-",
    "set.",
    "see_",
    "see-",
    "see.",
    "migration",
    "commit",
    "community",
    "shopify",
    "what'",
    "cucumber",
    "statamic",
    "mysql",
    "location",
    "tower",
    "line",
    "code",
    "amqp",
    "hello",
    "send",
    "index",
    "high",
    "notebook",
    "alloy",
    "python",
    "field",
    "document",
    "soap",
    "edition",
    "email",
    "php_",
    "php-",
    "php.",
    "command",
    "transport",
    "official",
    "upload",
    "study",
    "secure",
    "angularj",
    "akka",
    "scalable",
    "package",
    "request",
    "con_",
    "con-",
    "con.",
    "flexible",
    "security",
    "comment",
    "module",
    "flask",
    "graph",
    "flash",
    "apache",
    "change",
    "window",
    "space",
    "lambda",
    "sheet",
    "bookmark",
    "carousel",
    "friend",
    "objective",
    "jekyll",
    "bootstrap",
    "first",
    "article",
    "gwt_",
    "gwt-",
    "gwt.",
    "classic",
    "media",
    "websocket",
    "touch",
    "desktop",
    "real",
    "read",
    "recorder",
    "moved",
    "storage",
    "validator",
    "add-on",
    "pusher",
    "scs_",
    "scs-",
    "scs.",
    "inline",
    "asp_",
    "asp-",
    "asp.",
    "timeline",
    "base",
    "encoding",
    "ffmpeg",
    "kindle",
    "tinymce",
    "pretty",
    "jpa_",
    "jpa-",
    "jpa.",
    "used",
    "user",
    "required",
    "webhook",
    "download",
    "resque",
    "espresso",
    "cloud",
    "mongo",
    "benchmark",
    "pure",
    "cakephp",
    "modx",
    "mode",
    "reactive",
    "fuel",
    "written",
    "flickr",
    "mail",
    "brunch",
    "meteor",
    "dynamic",
    "neo_",
    "neo-",
    "neo.",
    "new_",
    "new-",
    "new.",
    "net_",
    "net-",
    "net.",
    "typo",
    "type",
    "keyboard",
    "erlang",
    "adobe",
    "logging",
    "ckeditor",
    "message",
    "iso_",
    "iso-",
    "iso.",
    "hook",
    "ldap",
    "folder",
    "reference",
    "railscast",
    "www_",
    "www-",
    "www.",
    "tracker",
    "azure",
    "fork",
    "form",
    "digital",
    "exporter",
    "skin",
    "string",
    "template",
    "designer",
    "gollum",
    "fluent",
    "entity",
    "language",
    "alfred",
    "summary",
    "wiki",
    "kernel",
    "calendar",
    "plupload",
    "symfony",
    "foundry",
    "remote",
    "talk",
    "search",
    "dev_",
    "dev-",
    "dev.",
    "del_",
    "del-",
    "del.",
    "token",
    "idea",
    "sencha",
    "selector",
    "interface",
    "create",
    "fun_",
    "fun-",
    "fun.",
    "groovy",
    "query",
    "grail",
    "red_",
    "red-",
    "red.",
    "laravel",
    "monkey",
    "slack",
    "supported",
    "instant",
    "value",
    "center",
    "latest",
    "work",
    "but_",
    "but-",
    "but.",
    "bug_",
    "bug-",
    "bug.",
    "virtual",
    "tweet",
    "statsd",
    "studio",
    "path",
    "real-time",
    "frontend",
    "notifier",
    "coding",
    "tool",
    "firmware",
    "flow",
    "random",
    "mediawiki",
    "bosh",
    "been",
    "beer",
    "lightbox",
    "theory",
    "origin",
    "redmine",
    "hub_",
    "hub-",
    "hub.",
    "require",
    "pro_",
    "pro-",
    "pro.",
    "ant_",
    "ant-",
    "ant.",
    "any_",
    "any-",
    "any.",
    "recipe",
    "closure",
    "mapper",
    "event",
    "todo",
    "model",
    "redi",
    "provider",
    "rvm_",
    "rvm-",
    "rvm.",
    "program",
    "memcached",
    "rail",
    "silex",
    "foreman",
    "activity",
    "license",
    "strategy",
    "batch",
    "streaming",
    "fast",
    "use_",
    "use-",
    "use.",
    "usb_",
    "usb-",
    "usb.",
    "impres",
    "academy",
    "slider",
    "please",
    "layer",
    "cros",
    "now_",
    "now-",
    "now.",
    "miner",
    "extension",
    "own_",
    "own-",
    "own.",
    "app_",
    "app-",
    "app.",
    "debian",
    "symphony",
    "example",
    "feature",
    "serie",
    "tree",
    "project",
    "runner",
    "entry",
    "leetcode",
    "layout",
    "webrtc",
    "logic",
    "login",
    "worker",
    "toolkit",
    "mocha",
    "support",
    "back",
    "inside",
    "device",
    "jenkin",
    "contact",
    "fake",
    "awesome",
    "ocaml",
    "bit_",
    "bit-",
    "bit.",
    "drive",
    "screen",
    "prototype",
    "gist",
    "binary",
    "nosql",
    "rest",
    "overview",
    "dart",
    "dark",
    "emac",
    "mongoid",
    "solarized",
    "homepage",
    "emulator",
    "commander",
    "django",
    "yandex",
    "gradle",
    "xcode",
    "writer",
    "crm_",
    "crm-",
    "crm.",
    "jade",
    "startup",
    "error",
    "using",
    "format",
    "name",
    "spring",
    "parser",
    "scratch",
    "magic",
    "try_",
    "try-",
    "try.",
    "rack",
    "directive",
    "challenge",
    "slim",
    "counter",
    "element",
    "chosen",
    "doc_",
    "doc-",
    "doc.",
    "meta",
    "should",
    "button",
    "packet",
    "stream",
    "hardware",
    "android",
    "infinite",
    "password",
    "software",
    "ghost",
    "xamarin",
    "spec",
    "chef",
    "interview",
    "hubot",
    "mvc_",
    "mvc-",
    "mvc.",
    "exercise",
    "leaflet",
    "launcher",
    "air_",
    "air-",
    "air.",
    "photo",
    "board",
    "boxen",
    "way_",
    "way-",
    "way.",
    "computing",
    "welcome",
    "notepad",
    "portfolio",
    "cat_",
    "cat-",
    "cat.",
    "can_",
    "can-",
    "can.",
    "magento",
    "yaml",
    "domain",
    "card",
    "yii_",
    "yii-",
    "yii.",
    "checker",
    "browser",
    "upgrade",
    "only",
    "progres",
    "aura",
    "ruby_",
    "ruby-",
    "ruby.",
    "polymer",
    "util",
    "lite",
    "hackathon",
    "rule",
    "log_",
    "log-",
    "log.",
    "opengl",
    "stanford",
    "skeleton",
    "history",
    "inspector",
    "help",
    "soon",
    "selenium",
    "lab_",
    "lab-",
    "lab.",
    "scheme",
    "schema",
    "look",
    "ready",
    "leveldb",
    "docker",
    "game",
    "minimal",
    "logstash",
    "messaging",
    "within",
    "heroku",
    "mongodb",
    "kata",
    "suite",
    "picker",
    "win_",
    "win-",
    "win.",
    "wip_",
    "wip-",
    "wip.",
    "panel",
    "started",
    "starter",
    "front-end",
    "detector",
    "deploy",
    "editing",
    "based",
    "admin",
    "capture",
    "spree",
    "page",
    "bundle",
    "goal",
    "rpg_",
    "rpg-",
    "rpg.",
    "setup",
    "side",
    "mean",
    "reader",
    "cookbook",
    "mini",
    "modern",
    "seed",
    "dom_",
    "dom-",
    "dom.",
    "doc_",
    "doc-",
    "doc.",
    "dot_",
    "dot-",
    "dot.",
    "syntax",
    "sugar",
    "loader",
    "website",
    "make",
    "kit_",
    "kit-",
    "kit.",
    "protocol",
    "human",
    "daemon",
    "golang",
    "manager",
    "countdown",
    "connector",
    "swagger",
    "map_",
    "map-",
    "map.",
    "mac_",
    "mac-",
    "mac.",
    "man_",
    "man-",
    "man.",
    "orm_",
    "orm-",
    "orm.",
    "org_",
    "org-",
    "org.",
    "little",
    "zsh_",
    "zsh-",
    "zsh.",
    "shop",
    "show",
    "workshop",
    "money",
    "grid",
    "server",
    "octopres",
    "svn_",
    "svn-",
    "svn.",
    "ember",
    "embed",
    "general",
    "file",
    "important",
    "dropbox",
    "portable",
    "public",
    "docpad",
    "fish",
    "sbt_",
    "sbt-",
    "sbt.",
    "done",
    "para",
    "network",
    "common",
    "readme",
    "popup",
    "simple",
    "purpose",
    "mirror",
    "single",
    "cordova",
    "exchange",
    "object",
    "design",
    "gateway",
    "account",
    "lamp",
    "intellij",
    "math",
    "mit_",
    "mit-",
    "mit.",
    "control",
    "enhanced",
    "emitter",
    "multi",
    "add_",
    "add-",
    "add.",
    "about",
    "socket",
    "preview",
    "vagrant",
    "cli_",
    "cli-",
    "cli.",
    "powerful",
    "top_",
    "top-",
    "top.",
    "radio",
    "watch",
    "fluid",
    "amazon",
    "report",
    "couchbase",
    "automatic",
    "detection",
    "sprite",
    "pyramid",
    "portal",
    "advanced",
    "plu_",
    "plu-",
    "plu.",
    "runtime",
    "git_",
    "git-",
    "git.",
    "uri_",
    "uri-",
    "uri.",
    "haml",
    "node",
    "sql_",
    "sql-",
    "sql.",
    "cool",
    "core",
    "obsolete",
    "handler",
    "iphone",
    "extractor",
    "array",
    "copy",
    "nlp_",
    "nlp-",
    "nlp.",
    "reveal",
    "pop_",
    "pop-",
    "pop.",
    "engine",
    "parse",
    "check",
    "html",
    "nest",
    "all_",
    "all-",
    "all.",
    "chinese",
    "buildpack",
    "what",
    "tag_",
    "tag-",
    "tag.",
    "proxy",
    "style",
    "cookie",
    "feed",
    "restful",
    "compiler",
    "creating",
    "prelude",
    "context",
    "java",
    "rspec",
    "mock",
    "backbone",
    "light",
    "spotify",
    "flex",
    "related",
    "shell",
    "which",
    "clas",
    "webapp",
    "swift",
    "ansible",
    "unity",
    "console",
    "tumblr",
    "export",
    "campfire",
    "conway'",
    "made",
    "riak",
    "hero",
    "here",
    "unix",
    "unit",
    "glas",
    "smtp",
    "how_",
    "how-",
    "how.",
    "hot_",
    "hot-",
    "hot.",
    "debug",
    "release",
    "diff",
    "player",
    "easy",
    "right",
    "old_",
    "old-",
    "old.",
    "animate",
    "time",
    "push",
    "explorer",
    "course",
    "training",
    "nette",
    "router",
    "draft",
    "structure",
    "note",
    "salt",
    "where",
    "spark",
    "trello",
    "power",
    "method",
    "social",
    "via_",
    "via-",
    "via.",
    "vim_",
    "vim-",
    "vim.",
    "select",
    "webkit",
    "github",
    "ftp_",
    "ftp-",
    "ftp.",
    "creator",
    "mongoose",
    "led_",
    "led-",
    "led.",
    "movie",
    "currently",
    "pdf_",
    "pdf-",
    "pdf.",
    "load",
    "markdown",
    "phalcon",
    "input",
    "custom",
    "atom",
    "oracle",
    "phonegap",
    "ubuntu",
    "great",
    "rdf_",
    "rdf-",
    "rdf.",
    "popcorn",
    "firefox",
    "zip_",
    "zip-",
    "zip.",
    "cuda",
    "dotfile",
    "static",
    "openwrt",
    "viewer",
    "powered",
    "graphic",
    "les_",
    "les-",
    "les.",
    "doe_",
    "doe-",
    "doe.",
    "maven",
    "word",
    "eclipse",
    "lab_",
    "lab-",
    "lab.",
    "hacking",
    "steam",
    "analytic",
    "option",
    "abstract",
    "archive",
    "reality",
    "switcher",
    "club",
    "write",
    "kafka",
    "arduino",
    "angular",
    "online",
    "title",
    "don't",
    "contao",
    "notice",
    "analyzer",
    "learning",
    "zend",
    "external",
    "staging",
    "busines",
    "tdd_",
    "tdd-",
    "tdd.",
    "scanner",
    "building",
    "snippet",
    "modular",
    "bower",
    "stm_",
    "stm-",
    "stm.",
    "lib_",
    "lib-",
    "lib.",
    "alpha",
    "mobile",
    "clean",
    "linux",
    "nginx",
    "manifest",
    "some",
    "raspberry",
    "gnome",
    "ide_",
    "ide-",
    "ide.",
    "block",
    "statistic",
    "info",
    "drag",
    "youtube",
    "koan",
    "facebook",
    "paperclip",
    "art_",
    "art-",
    "art.",
    "quality",
    "tab_",
    "tab-",
    "tab.",
    "need",
    "dojo",
    "shield",
    "computer",
    "stat",
    "state",
    "twitter",
    "utility",
    "converter",
    "hosting",
    "devise",
    "liferay",
    "updated",
    "force",
    "tip_",
    "tip-",
    "tip.",
    "behavior",
    "active",
    "call",
    "answer",
    "deck",
    "better",
    "principle",
    "ches",
    "bar_",
    "bar-",
    "bar.",
    "reddit",
    "three",
    "haxe",
    "just",
    "plug-in",
    "agile",
    "manual",
    "tetri",
    "super",
    "beta",
    "parsing",
    "doctrine",
    "minecraft",
    "useful",
    "perl",
    "sharing",
    "agent",
    "switch",
    "view",
    "dash",
    "channel",
    "repo",
    "pebble",
    "profiler",
    "warning",
    "cluster",
    "running",
    "markup",
    "evented",
    "mod_",
    "mod-",
    "mod.",
    "share",
    "csv_",
    "csv-",
    "csv.",
    "response",
    "good",
    "house",
    "connect",
    "built",
    "build",
    "find",
    "ipython",
    "webgl",
    "big_",
    "big-",
    "big.",
    "google",
    "scala",
    "sdl_",
    "sdl-",
    "sdl.",
    "sdk_",
    "sdk-",
    "sdk.",
    "native",
    "day_",
    "day-",
    "day.",
    "puppet",
    "text",
    "routing",
    "helper",
    "linkedin",
    "crawler",
    "host",
    "guard",
    "merchant",
    "poker",
    "over",
    "writing",
    "free",
    "classe",
    "component",
    "craft",
    "nodej",
    "phoenix",
    "longer",
    "quick",
    "lazy",
    "memory",
    "clone",
    "hacker",
    "middleman",
    "factory",
    "motion",
    "multiple",
    "tornado",
    "hack",
    "ssh_",
    "ssh-",
    "ssh.",
    "review",
    "vimrc",
    "driver",
    "driven",
    "blog",
    "particle",
    "table",
    "intro",
    "importer",
    "thrift",
    "xmpp",
    "framework",
    "refresh",
    "react",
    "font",
    "librarie",
    "variou",
    "formatter",
    "analysi",
    "karma",
    "scroll",
    "tut_",
    "tut-",
    "tut.",
    "apple",
    "tag_",
    "tag-",
    "tag.",
    "tab_",
    "tab-",
    "tab.",
    "category",
    "ionic",
    "cache",
    "homebrew",
    "reverse",
    "english",
    "getting",
    "shipping",
    "clojure",
    "boot",
    "book",
    "branch",
    "combination",
    "combo",
]
````

## File: heroku.yml
````yaml
setup:
  addons:
    - plan: scheduler
      as: SCHEDULER
    - plan: heroku-postgresql
      as: DATABASE
    - plan: coralogix
      as: CORALOGIX
  config:
    APP_NAME: meetup-bot-bot
build:
  docker:
    web: ./Dockerfile.web
````

## File: Makefile
````makefile
#!/usr/bin/make -f

.DEFAULT_GOAL := help

.ONESHELL:

# ENV VARS
export SHELL := $(shell which sh)
export UNAME := $(shell uname -s)
export ASDF_VERSION := v0.13.1

# check commands and OS
ifeq ($(UNAME), Darwin)
	export XCODE := $(shell xcode-select -p 2>/dev/null)
	export HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK := 1
else ifeq ($(UNAME), Linux)
    include /etc/os-release
endif

export ASDF := $(shell command -v asdf 2>/dev/null)
export BREW := $(shell command -v brew 2>/dev/null)
export GIT := $(shell command -v git 2>/dev/null)
export PRE_COMMIT := $(shell command -v pre-commit 2>/dev/null)
export TASK := $(shell command -v task 2>/dev/null)

# colors
GREEN := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE := $(shell tput -Txterm setaf 7)
CYAN := $(shell tput -Txterm setaf 6)
RESET := $(shell tput -Txterm sgr0)

# targets
.PHONY: all
all: help asdf xcode brew pre-commit task ## run all targets

xcode: ## install xcode command line tools
ifeq ($(UNAME), Darwin)
	@if [ -z "${XCODE}" ]; then \
		echo "Installing Xcode command line tools..."; \
		xcode-select --install; \
	else \
		echo "xcode already installed."; \
	fi
else
	@echo "xcode not supported."
endif

brew: xcode ## install homebrew
ifeq ($(UNAME), Darwin)
	@if [ -z "${BREW}" ]; then \
		echo "Installing Homebrew..."; \
		/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
	else \
		echo "brew already installed."; \
	fi
else
	@echo "brew not supported."
endif

asdf: xcode ## install asdf
ifeq ($(UNAME), Darwin)
	@if [ -z "${ASDF}" ]; then \
		echo "Installing asdf..."; \
		git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch ${ASDF_VERSION}; \
		echo "To use asdf, add the following to your shell rc (.bashrc/.zshrc):"; \
		echo "export PATH=\"$$HOME/.asdf/shims:$$PATH\""; \
		echo ". $$HOME/.asdf/asdf.sh"; \
		echo ". $$HOME/.asdf/completions/asdf.bash"; \
	else \
		echo "asdf already installed."; \
	fi
else
	@echo "asdf not supported."
endif

pre-commit: brew ## install pre-commit
	@if [ -z "${PRE_COMMIT}" ] && [ -n "${BREW}" ]; then \
		echo "Installing pre-commit..."; \
		brew install pre-commit; \
	elif [ -z "${PRE_COMMIT}" ] && [ "${ID_LIKE}" = "debian" ]; then \
		echo "Installing pre-commit..."; \
		sudo apt-get install -y pre-commit; \
	else \
		echo "pre-commit already installed."; \
	fi

task: ## install taskfile
ifeq ($(UNAME), Darwin)
	@if [ -z "${TASK}" ] && [ ! -z "${BREW}" ]; then \
		echo "Installing taskfile..."; \
		brew install go-task; \
	else \
		echo "taskfile already installed."; \
	fi
else ifeq ($(UNAME), Linux)
	@if [ -z "${TASK}" ] && [ "${ID_LIKE}" = "debian" ]; then \
		echo "Installing taskfile..."; \
		sudo snap install task --classic; \
	else \
		echo "taskfile already installed."; \
	fi
else
	@echo "taskfile not supported."
endif

install: xcode asdf brew pre-commit task ## install dependencies

help: ## show this help
	@echo ''
	@echo 'Usage:'
	@echo '    ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} { \
		if (/^[a-zA-Z_-]+:.*?##.*$$/) {printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2} \
		else if (/^## .*$$/) {printf "  ${CYAN}%s${RESET}\n", substr($$1,4)} \
		}' $(MAKEFILE_LIST)
````

## File: release-please-config.json
````json
{
  "packages": {
    ".": {
      "changelog-path": "CHANGELOG.md",
      "release-type": "python",
      "bump-minor-pre-major": false,
      "bump-patch-for-minor-pre-major": false,
      "draft": false,
      "prerelease": false
    }
  },
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json"
}
````

## File: .github/workflows/hooks/pre-commit.py
````python
def gitleaksEnabled()
⋮----
out = subprocess.getoutput("git config --bool hooks.gitleaks")
⋮----
exitCode = os.WEXITSTATUS(os.system('gitleaks protect -v --staged'))
````

## File: app/capture_groups.py
````python
base_url = "https://www.meetup.com"
⋮----
distance = "tenMiles"
source = "GROUPS"
category_id = "546"
location = "us--ok--Oklahoma%20City"
⋮----
url = base_url + "/find/?distance=" + distance + "&source=" + source + "&categoryId=" + category_id + "&location=" + location
⋮----
def run(playwright: Playwright) -> None
⋮----
browser = playwright.chromium.launch(headless=True)
⋮----
context = browser.new_context(
⋮----
page = context.new_page()
⋮----
handles = []
⋮----
handles = [group.get_property("href") for group in page.query_selector_all("#group-card-in-search-results")]
⋮----
def process(handles)
⋮----
exclusions = [
⋮----
handles = [str(handle) for handle in handles]
⋮----
handles = [handle for handle in handles if handle.split("/")[-2] not in exclusions]
⋮----
df = pd.DataFrame(handles)
⋮----
df = pd.read_csv("raw/scratch.csv")
⋮----
df = df.sort_values(by=["urlname"])
⋮----
def main()
⋮----
handles = run(playwright)
````

## File: app/schedule.py
````python
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", default=5432, cast=int)
TZ = config("TZ", default="America/Chicago")
LOCAL_TIME = config("LOCAL_TIME", default="09:00")
⋮----
loc_time = arrow.now().to(TZ)
⋮----
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
enabled_days = ["Monday", "Wednesday", "Friday"]
⋮----
db = Database()
⋮----
class Schedule(db.Entity)
⋮----
_table_ = "schedule"
id = PrimaryKey(int, auto=True)
day = Required(str, unique=True)
schedule_time = Required(str)
timezone = Required(str)
enabled = Required(bool, default=True)
snooze_until = Optional(datetime)
original_schedule_time = Optional(str)
last_changed = Required(datetime, default=datetime.utcnow)
⋮----
DB_PASS = DB_PASS.strip('"')
⋮----
def local_to_utc(local_time_str, timezone)
⋮----
local_time = arrow.get(local_time_str, "HH:mm")
local_datetime = arrow.now(timezone).replace(hour=local_time.hour, minute=local_time.minute)
utc_datetime = local_datetime.to("UTC")
⋮----
def get_current_schedule_time(schedule)
⋮----
utc_time = schedule.schedule_time
local_time = LOCAL_TIME
⋮----
@db_session
def update_schedule(day, timezone=None, enabled=None)
⋮----
schedule = Schedule.get(day=day)
updated = False
⋮----
updated = True
⋮----
should_be_enabled = day in enabled_days
⋮----
utc_time = local_to_utc(LOCAL_TIME, timezone or TZ)
⋮----
@db_session
def initialize_schedule()
⋮----
"""Initialize the schedule table with default values"""
⋮----
@db_session
def update_all_schedules(new_timezone=None)
⋮----
"""Update all schedules with new timezone"""
⋮----
@db_session
def get_schedule(day)
⋮----
"""Get the schedule for a specific day"""
⋮----
@db_session
def snooze_schedule(duration)
⋮----
"""Snooze the schedule for the specified duration"""
current_time = arrow.now(TZ)
current_day = current_time.format("dddd")
schedule = Schedule.get(day=current_day)
⋮----
schedule_time = arrow.get(schedule.schedule_time, "HH:mm").replace(tzinfo="UTC")
schedule_time = schedule_time.to(schedule.timezone)
⋮----
snooze_until = current_time.shift(minutes=5)
new_schedule_time = snooze_until.to("UTC").format("HH:mm")
⋮----
snooze_until = schedule_time.shift(days=1)
⋮----
snooze_until = schedule_time
new_schedule_time = schedule.schedule_time
⋮----
days_until_sunday = (7 - current_time.weekday()) % 7
snooze_until = current_time.shift(days=days_until_sunday).replace(hour=0, minute=0, second=0, microsecond=0)
⋮----
@db_session
def check_and_revert_snooze()
⋮----
"""Check if any snoozes need to be reverted and revert them if necessary"""
⋮----
@db_session
def check_and_update_env_changes()
⋮----
"""Check for changes in environment variables and update schedules if necessary"""
current_timezone = TZ
⋮----
sample_schedule = Schedule.get(day="Monday")
⋮----
def main()
⋮----
max_day_length = max(len(day) for day in days)
⋮----
schedule = get_schedule(day)
⋮----
status = "[Enabled]" if schedule.enabled else "[Disabled]"
snooze_info = (
⋮----
local_now = arrow.now(TZ)
utc_now = arrow.utcnow()
````

## File: app/scheduler.py
````python
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"
⋮----
env = Path('.env')
⋮----
HOST = config('HOST')
PORT = config('PORT', default=3000, cast=int)
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
⋮----
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', default=3000))
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
⋮----
TZ = config('TZ', default='America/Chicago')
loc_time = arrow.now().to(TZ)
⋮----
sched = BackgroundScheduler()
⋮----
@sched.scheduled_job('interval', minutes=30, id='gen_token')
def get_token()
⋮----
url = f"http://{HOST}:{PORT}/token"
⋮----
payload = f"username={DB_USER}&password={DB_PASS}"
⋮----
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
⋮----
res = requests.request("POST", url, headers=headers, data=payload)
⋮----
raw = res.json()
⋮----
# @sched.scheduled_job(trigger='cron', hour='9,17,20,23', id='post_slack')      # 9am, 5pm, 8pm, 11pm
@sched.scheduled_job(trigger='cron', hour='*', id='post_slack')  # every hour
# @sched.scheduled_job(trigger='cron', minute='*/30', id='post_slack')          # every n minutes
def post_to_slack()
⋮----
"""Post to Slack"""
⋮----
access_token = get_token()
⋮----
url = f"http://{HOST}:{PORT}/api/slack"
⋮----
payload = urlencode({'location': 'Oklahoma City', 'exclusions': 'Tulsa'})
⋮----
headers = {'Authorization': f'Bearer {access_token}', 'accept': 'application/json'}
⋮----
def main()
⋮----
"""Main function"""
⋮----
# port = next_free_port()
````

## File: app/startup.sh
````bash
script_dir=$(cd "$(dirname "$0")" && pwd)
top_dir=$(cd "${script_dir}/.." && pwd)

if [ "$(uname -s)" = "Darwin" ]; then
	export VENV="${top_dir}/.venv"
else
	export VENV="/opt/venv"
fi
export PATH="${VENV}/bin:$HOME/.asdf/bin:$HOME/.asdf/shims:$PATH"

server() {
	gunicorn \
		-w 2 \
		-k uvicorn.workers.UvicornWorker main:app \
		-b "0.0.0.0:${PORT:-3000}" \
		--log-file -
}

main() {
	server
}
main "$@"
````

## File: taskfiles/deno.yml
````yaml
version: "3.0"

set: ['e', 'u', 'pipefail']
shopt: ['globstar']

vars:
  FRONTEND_DIR: "app/frontend"

tasks:
  install:
    desc: "Install dependencies via Deno (8x faster than npm ci)"
    cmds:
      - deno install --node-modules-dir=auto --frozen
    sources:
      - "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}/package.json"
      - "{{.ROOT_DIR}}/deno.lock"
    generates:
      - "{{.ROOT_DIR}}/node_modules/**/*"
    status:
      - test -d "{{.ROOT_DIR}}/node_modules"
    silent: true

  clean:
    desc: "Clean deno artifacts"
    cmds:
      - rm -rf {{.ROOT_DIR}}/node_modules
    silent: true

  outdated:
    desc: "Check for outdated dependencies (uses npm)"
    dir: "{{.FRONTEND_DIR}}"
    cmds:
      - npm outdated || true
    silent: true

  audit:
    desc: "Run security audit (uses npm)"
    dir: "{{.FRONTEND_DIR}}"
    cmds:
      - npm audit

  audit-fix:
    desc: "Fix security vulnerabilities (uses npm)"
    dir: "{{.FRONTEND_DIR}}"
    cmds:
      - npm audit fix

  cache-clean:
    desc: "Clean deno cache"
    cmds:
      - deno cache --reload
    silent: true

  list:
    desc: "List installed packages"
    dir: "{{.FRONTEND_DIR}}"
    cmds:
      - deno info --json package.json | head -50
    silent: true

  lint:
    desc: "Run Deno linter"
    cmds:
      - deno lint

  format:
    desc: "Format TypeScript/JavaScript code"
    cmds:
      - deno fmt

  check-deps:
    desc: "Check if deno is installed"
    cmds:
      - |
        echo "Checking deno dependencies..."
        if ! command -v deno &> /dev/null; then
          echo "deno not found. Install from https://deno.com"
          exit 1
        fi
        echo "deno version: $(deno --version | head -1)"
    silent: true


  dev:
    desc: "Run Vite dev server via Deno"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - deno run -A npm:vite {{.CLI_ARGS}}

  build:
    desc: "Build frontend via Deno (2.2x faster than npm)"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - deno run -A npm:vite build {{.CLI_ARGS}}

  preview:
    desc: "Preview production build via Deno"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - deno run -A npm:vite preview {{.CLI_ARGS}}


  test:
    desc: "Run Vitest unit/property tests (uses Node - Vitest requires native workers)"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - npm test {{.CLI_ARGS}}

  test:watch:
    desc: "Run Vitest in watch mode (uses Node)"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - npm run test:watch {{.CLI_ARGS}}

  test:e2e:
    desc: "Run Playwright E2E tests (uses Node - Playwright requires native Node)"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    env:
      E2E_MODE: '{{.E2E_MODE | default "fast"}}'
    cmds:
      - npx playwright test {{.CLI_ARGS}}

  test:e2e:ui:
    desc: "Run Playwright E2E tests in UI mode (uses Node)"
    deps: [install]
    dir: "{{.ROOT_DIR}}/{{.FRONTEND_DIR}}"
    cmds:
      - npx playwright test --ui {{.CLI_ARGS}}
````

## File: taskfiles/uv.yml
````yaml
version: "3.0"

set: ['e', 'u', 'pipefail']
shopt: ['globstar']

env:
  UV_PROJECT_ENVIRONMENT: ".venv"

tasks:
  install-uv:
    desc: "Install uv"
    cmds:
      - curl -LsSf https://astral.sh/uv/install.sh | sh
    status:
      - command -v uv 2>/dev/null

  venv:
    desc: "Create a virtual environment"
    cmds:
      - uv venv
    dir: "{{.ROOT_DIR}}"
    status:
      - test -d "{{.ROOT_DIR}}/{{.UV_PROJECT_ENVIRONMENT}}"

  install:
    desc: "Install project dependencies"
    cmds:
      - uv pip install -r pyproject.toml --all-extras
    dir: "{{.ROOT_DIR}}"

  lock:
    desc: "Update the project's lockfile."
    summary: |
      If the project lockfile (uv.lock) does not exist, it will be created. If a lockfile is present, its contents will be used as preferences for the resolution.

      If there are no changes to the project's dependencies, locking will have no effect unless the --upgrade flag is provided.
    cmds:
      - uv lock
    dir: "{{.ROOT_DIR}}"

  sync:
    desc: "Sync dependencies with lockfile"
    summary: |
      Syncing ensures that all project dependencies are installed and up-to-date with the lockfile.

      By default, an exact sync is performed: uv removes packages that are not declared as dependencies of the project.
    cmds:
      - uv sync --frozen
    dir: "{{.ROOT_DIR}}"

  update-deps:
    desc: "Update dependencies"
    summary: |
      Allow package upgrades, ignoring pinned versions in any existing output file. Implies --refresh
    cmds:
      - uv lock --upgrade

  export-reqs:
    desc: "Export requirements.txt"
    summary: |
      Export the project dependencies to a requirements.txt file.
    cmds:
      - uv pip freeze > {{.ROOT_DIR}}/requirements.txt
    ignore_error: true
````

## File: .dive-ci
````
rules:
  lowestEfficiency: 0.97          # ratio between 0-1
  highestWastedBytes: 20MB        # B, KB, MB, and GB
  highestUserWastedPercent: 0.20  # ratio between 0-1
````

## File: .roborev.toml
````toml
# * Overrides ~/.roborev/config.toml
# https://www.roborev.io/configuration/

agent = "claude-code"
default_model = "claude-opus-4-6"
default_backup_agent = "opencode"
````

## File: CONTRIBUTING.md
````markdown
# Contributing to meetup_bot

Welcome! Thank you in advance for your interest in contributing to `meetup_bot`!

## The Basics

`meetup_bot` welcomes contributions in the form of pull requests.

For small changes (e.g., bug fixes), feel free to submit a PR.

For larger changes (e.g., new functionality, new configuration options), consider creating an [**issue**](https://github.com/pythoninthegrass/meetup_bot/issues) outlining your proposed change.

### Prerequisites

<!-- TODO -->

### Development

<!-- TODO -->

## Adding yourself to the contributors listed in the meetup_bot README

If you'd like to be included in the list of contributors, you can follow [these instructions](https://allcontributors.org/docs/en/bot/usage) to do so!
````

## File: requirements-dev.txt
````
certifi==2024.8.30 ; python_version >= "3.11" and python_version < "3.13"
charset-normalizer==3.3.2 ; python_version >= "3.11" and python_version < "3.13"
colorama==0.4.6 ; python_version >= "3.11" and python_version < "3.13" and sys_platform == "win32"
coverage[toml]==7.6.1 ; python_version >= "3.11" and python_version < "3.13"
execnet==2.1.1 ; python_version >= "3.11" and python_version < "3.13"
idna==3.10 ; python_version >= "3.11" and python_version < "3.13"
iniconfig==2.0.0 ; python_version >= "3.11" and python_version < "3.13"
packaging==24.1 ; python_version >= "3.11" and python_version < "3.13"
pluggy==1.5.0 ; python_version >= "3.11" and python_version < "3.13"
pytest-asyncio==0.24.0 ; python_version >= "3.11" and python_version < "3.13"
pytest-cov==5.0.0 ; python_version >= "3.11" and python_version < "3.13"
pytest-datafiles==3.0.0 ; python_version >= "3.11" and python_version < "3.13"
pytest-xdist==3.6.1 ; python_version >= "3.11" and python_version < "3.13"
pytest==8.3.3 ; python_version >= "3.11" and python_version < "3.13"
requests-mock==1.12.1 ; python_version >= "3.11" and python_version < "3.13"
requests==2.32.3 ; python_version >= "3.11" and python_version < "3.13"
urllib3==2.2.3 ; python_version >= "3.11" and python_version < "3.13"
````

## File: SECURITY.md
````markdown
# Security Policy

* [Security Policy](#security-policy)
  * [Reporting Security Problems](#reporting-security-problems)
  * [Security Point of Contact](#security-point-of-contact)
  * [Incident Response Process](#incident-response-process)
    * [1. Containment](#1-containment)
    * [2. Response](#2-response)
    * [3. Remediation](#3-remediation)

<a name="reporting"></a>

## Reporting Security Problems

**DO NOT CREATE AN ISSUE** to report a security problem. Instead, please
send an email to <burrows_remix6p@icloud.com>.

<a name="contact"></a>

## Security Point of Contact

The security point of contact is Lance Stephens. Lance responds to security incident reports as fast as possible, within one business day 
at the latest.

If they don't respond within two days, please try emailing again.

<a name="process"></a>

## Incident Response Process

In case an incident is discovered or reported, I will follow the following
process to contain, respond and remediate:

### 1. Containment

The first step is to find out the root cause, nature and scope of the incident.

* Is still ongoing? If yes, first priority is to stop it.
* Is the incident outside of my influence? If yes, first priority is to contain it.
* Find out knows about the incident and who is affected.
* Find out what data was potentially exposed.

### 2. Response

After the initial assessment and containment to my best abilities, I will
document all actions taken in a response plan.

I will create a comment in [the issues](https://github.com/pythoninthegrass/meetup_bot/issues) to inform users about
the incident and what I actions I took to contain it.

### 3. Remediation

Once the incident is confirmed to be resolved, I will summarize the lessons learned from the incident and create a list of actions I will
take to prevent it from happening again.
````

## File: .github/workflows/smoke-test.yml
````yaml
name: Pytest Smoke Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_run:
    workflows: ["Build Docker image"]
    types:
      - completed
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      app:
        image: ghcr.io/${{ github.repository }}:latest
        credentials:
           username: ${{ github.actor }}
           password: ${{ secrets.GITHUB_TOKEN }}
        ports:
          - 3000:3000
        env:
          URL: http://localhost
          PORT: 3000

    steps:
    - uses: actions/checkout@v4

    - name: Install pytest
      run: |
        python -m pip install pytest requests python-decouple

    - name: Run pytest
      run: |
        pytest ./tests/test_smoke.py
      env:
        URL: http://localhost
        PORT: 3000
````

## File: .github/renovate.json5
````json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Renovate configuration that updates dependencies every Saturday at 10:00 AM Central Time",
  "timezone": "America/Chicago",
  "lockFileMaintenance": {
    "enabled": true
  },
  "packageRules": [
    {
      "matchManagers": ["pep621"],
      "enabled": true
    }
  ],
  "schedule": [
    "* 10 * * SAT"
  ],
  "prConcurrentLimit": 5,
  "rangeStrategy": "update-lockfile"
}
````

## File: app/scheduler.sh
````bash
if [ $(uname) = "Darwin" ]; then
	export $(grep -v '^#' .env | xargs)
	URL="localhost:${PORT:-3000}"
fi



DB_USER=$(echo "$DB_USER" | sed -e 's/^"//' -e 's/"$//')
DB_PASS=$(echo "$DB_PASS" | sed -e 's/^"//' -e 's/"$//')


exec_curl() {
	method="$1"
	url="$2"
	shift 2
	curl --no-progress-meter --location \
		--request "$method" \
		"$url" \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		"$@"
}


smoke_test() {
	exec_curl GET "${URL}/healthz" \
		--header "accept: application/json" > /dev/null 2>&1
}


gen_token() {
	raw=$(exec_curl POST "${URL}/token" \
		--data-urlencode "username=${DB_USER}" \
		--data-urlencode "password=${DB_PASS}")

	access_token=$(echo "${raw}" | cut -d '"' -f 4)
}


send_request() {
	endpoint="$1"
	data="$2"

	set -e

	case "$endpoint" in
		healthz)
			if smoke_test; then
				echo "Successfully reached ${URL}/healthz"
				exit 0
			else
				echo "Failed to reach ${URL}/healthz"
				exit 1
			fi
			;;
		events)
			gen_token
			exec_curl GET "${URL}/api/events" \
				--header "accept: application/json" \
				--header "Authorization: Bearer ${access_token}"
			;;
		slack)
			gen_token
			exec_curl POST "${URL}/api/slack" \
				--header "accept: application/json" \
				--header "Authorization: Bearer ${access_token}" \
				--data-urlencode "override=${OVERRIDE:-false}" \
				${data:+--data-urlencode "$data"}
			;;
		*)
			echo "Invalid endpoint. Use 'healthz', 'events', or 'slack'."
			exit 1
			;;
	esac

	set +e
}

main() {
	case $
		0)

			endpoint="slack"
			data="override=${OVERRIDE:-false}"
			;;
		2)

			endpoint="$1"
			data="$2"
			;;
		1)

			endpoint="$1"
			data=""
			;;
		*)
			echo "Invalid number of arguments."
			echo "Usage: $(basename $0) [endpoint] [data]"
			exit 1
			;;
	esac
	send_request "$endpoint" "$data"
}

main "$@"
````

## File: app/sign_jwt.py
````python
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"
⋮----
priv_key = Path('jwt_priv.pem')
pub_key = Path('jwt_pub.key')
⋮----
priv_key = config('PRIV_KEY_B64')
pub_key = config('PUB_KEY_B64')
⋮----
SELF_ID = config('SELF_ID')
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
SIGNING_KEY_ID = config('SIGNING_KEY_ID')
SIGNING_SECRET = config('SIGNING_SECRET')
TOKEN_URL = config('TOKEN_URL')
REDIRECT_URI = config('REDIRECT_URI')
JWT_LIFE_SPAN = config('JWT_LIFE_SPAN', default=120, cast=int)
⋮----
private_key = serialization.load_pem_private_key(data=f.read(), password=None, backend=default_backend())
⋮----
private_key = base64.b64decode(priv_key)
⋮----
private_key = serialization.load_pem_private_key(data=private_key, password=None, backend=default_backend())
⋮----
public_key = serialization.load_pem_public_key(data=f.read(), backend=default_backend())
⋮----
public_key = base64.b64decode(pub_key)
⋮----
public_key = serialization.load_pem_public_key(data=public_key, backend=default_backend())
⋮----
headers = {"alg": 'RS256', "typ": 'JWT', "Accept": 'application/json', "Content-Type": 'application/x-www-form-urlencoded'}
⋮----
def gen_payload_data()
⋮----
payload_data = {"sub": SELF_ID, "iss": CLIENT_ID, "aud": "api.meetup.com", "exp": int(time.time() + JWT_LIFE_SPAN)}
⋮----
def sign_token()
⋮----
jwt_headers = {"kid": SIGNING_KEY_ID, "typ": "JWT", "alg": "RS256"}
⋮----
payload_data = gen_payload_data()
⋮----
payload = jwt.encode(headers=jwt_headers, payload=payload_data, key=private_key, algorithm='RS256')
⋮----
def verify_token(token)
⋮----
def get_access_token(token)
⋮----
"""Post token to auth server to get access token"""
⋮----
# Headers for the token request
request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
⋮----
payload = {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": token}
payload = urlencode(payload)
⋮----
response = requests.request("POST", TOKEN_URL, headers=request_headers, data=payload)
⋮----
def main()
⋮----
"""Generate signed JWT, verify, and get access token"""
⋮----
# sign JWT
token = sign_token()
⋮----
# verify JWT
⋮----
tokens = get_access_token(token)
````

## File: app/slackbot.py
````python
home = Path.home()
cwd = Path.cwd()
csv_fn = config('CSV_FN', default='raw/output.csv')
json_fn = config('JSON_FN', default='raw/output.json')
groups_csv = Path('groups.csv')
tz = config('TZ', default='America/Chicago')
loc_time = arrow.now().to(tz)
⋮----
USER_TOKEN = config('USER_TOKEN')
BOT_USER_TOKEN = config('BOT_USER_TOKEN')
SLACK_WEBHOOK = config('SLACK_WEBHOOK')
CHANNEL = config('CHANNEL', default='testingchannel')
TTL = config('TTL', default=3600, cast=int)
HOST = config('HOST', default='localhost')
⋮----
CHANNEL = CHANNEL.strip('"')
⋮----
chan = pd.read_csv('channels.csv', header=0)
⋮----
chan_dict = {}
⋮----
channel_name = CHANNEL
channel_id = chan_dict[CHANNEL]
⋮----
hard_chan = ''
⋮----
# add hard-coded channel
⋮----
hard_id = chan_dict[hard_chan]
channels = {channel_name: channel_id, hard_chan: hard_id}
⋮----
channels = {channel_name: channel_id}
⋮----
# python sdk
client = WebClient(token=BOT_USER_TOKEN)
⋮----
def fmt_json(filename)
⋮----
# read json file
data = json.load(open(filename))
⋮----
# create dataframe
df = pd.DataFrame(data)
⋮----
# handle empty dataframe case
⋮----
# add column: 'message' with date, name, title, eventUrl
⋮----
# convert message column to list of strings (avoids alignment shenanigans)
msg = df['message'].tolist()
⋮----
def send_message(message, channel_id)
⋮----
response = client.chat_postMessage(
⋮----
def main()
⋮----
msg = fmt_json(json_fn)
````

## File: taskfiles/docker.yml
````yaml
version: "3.0"

set: ['e', 'u', 'pipefail']
shopt: ['globstar']

env:
  COMPOSE_FILE: "{{.TLD}}/docker-compose.yml"
  DOCKERFILE: "{{.TLD}}/Dockerfile.web"
  PLATFORM:
    sh: "echo ${PLATFORM:-linux/amd64}"
  REGISTRY:
    sh: "echo ${REGISTRY:-ghcr.io}"
  USER_NAME:
    sh: "echo ${USER_NAME:-pythoninthegrass}"
  SERVICE: "meetup_bot"
  VERSION:
    sh: "echo ${VERSION:-latest}"

tasks:
  net:
    desc: "Create docker network"
    cmds:
      - |
        docker network create \
          --driver bridge \
          app-tier
    status:
      - |
        docker network ls --format \{\{.Name\}\} \
          | grep -q '^app-tier$'

  vol:
    desc: "Create docker volume"
    cmds:
      - |
        docker volume create \
          --driver local \
          {{.SERVICE}}-vol
    status:
      - |
        docker volume ls --format \{\{.Name\}\} \
          | grep -q '^{{.SERVICE}}-vol$'

  build:
    desc: "Build the docker image"
    summary: |
      Build the docker image with the specified dockerfile.

      The default dockerfile is Dockerfile.web.

      USAGE
        task docker:build
    cmds:
      - |
        docker build \
          -f {{.DOCKERFILE}} \
          -t {{.SERVICE}} \
          --platform {{.PLATFORM}} \
          .

  login:
    desc: "Login to the container registry"
    cmds:
      - |
        echo "{{.REGISTRY_PASS}}" | docker login \
          -u {{.USER_NAME}} \
          --password-stdin {{.REGISTRY_URL}}
    run: once
    silent: true

  push:
    desc: "Push the docker image to the registry"
    deps:
      - login
      - build
    cmds:
      - docker push {{.REGISTRY_URL}}/{{.USER_NAME}}/{{.SERVICE}}

  up:
    desc: "Start the project with docker compose"
    cmds:
      - |
        docker compose -f {{.COMPOSE_FILE}} up -d \
        --build \
        --remove-orphans

  exec:
    desc: "Shell into a running container"
    cmds:
      - docker exec -it {{.SERVICE}} sh

  logs:
    desc: "Follow the logs of a running container"
    cmds:
      - docker compose logs -tf {{.SERVICE}}

  stop:
    desc: "Stop the project with docker compose"
    cmds:
      - docker compose -f {{.COMPOSE_FILE}} stop

  down:
    desc: "Stop and remove containers, networks, and volumes with docker compose"
    cmds:
      - |
        docker compose -f {{.COMPOSE_FILE}} down \
        --volumes

  prune:
    desc: "Prune docker"
    cmds:
      - docker system prune --all --force
      - docker builder prune --all --force
````

## File: taskfiles/heroku.yml
````yaml
version: "3.0"

set: ['e', 'u', 'pipefail']
shopt: ['globstar']

tasks:
  login:
    desc: "Login to Heroku"
    cmds:
      - |
        heroku auth:login
        heroku container:login
    run: "once"
    silent: true
    status:
      - heroku auth:whoami >/dev/null 2>&1

  env:
    desc: Upload .env file to Heroku
    cmds:
      - |
        heroku config:set $(cat {{.TLD}}/app/.env | grep -Ev '(^#|^HEROKU_)' | xargs)

  stats:
    desc: "Show the stats of the project"
    cmds:
      - |
        heroku ps
        heroku status
        heroku builds
        heroku releases

  logs:
    desc: "Follow the logs of the project"
    cmds:
      - heroku logs --tail

  open:
    desc: "Open the project in the browser"
    cmds:
      - heroku open

  release:
    desc: "Release the project"
    cmds:
      - heroku container:release web --app ${HEROKU_APP}
      - task heroku:stats

  push:
    desc: "Push the project to Heroku"
    cmds:
      - |
        heroku container:push web --app ${HEROKU_APP}
        task heroku:stats

  pull:
    desc: "Pull the project from Heroku"
    deps:
      - login
    cmds:
      - |
        heroku container:pull web --app ${HEROKU_APP}
````

## File: .all-contributorsrc
````
{
  "projectName": "meetup_bot",
  "projectOwner": "pythoninthegrass",
  "repoType": "github",
  "repoHost": "https://github.com",
  "files": [
    "README.md"
  ],
  "imageSize": 50,
  "commit": true,
  "commitConvention": "angular",
  "contributors": [
    {
      "login": "alex-code4okc",
      "name": "Alex Ayon",
      "avatar_url": "https://avatars.githubusercontent.com/u/17677369?v=4",
      "profile": "https://github.com/alex-code4okc",
      "contributions": [
        "code"
      ]
    }
  ],
  "contributorsPerLine": 7,
  "linkToUsage": true
}
````

## File: .env.example
````
ALGORITHM=HS256
APP_TOKEN=xapp-apptoken
AUTH_BASE_URL=https://secure.meetup.com/oauth2/authorize
BOT_USER_TOKEN=xoxb-botusertoken
CACHE_FN=/tmp/meetup_query
CHANNEL=okc-metro
CHANNEL2=events
CLIENT_ID=securesuperkey
CLIENT_SECRET=secretsecuresuper
CSV_FN=/tmp/output.csv
DAYS=7
DB_HOST=localoraws
DB_NAME=herokuawsstring
DB_PASS=anothercredgoeshere
DB_PORT=5432
DB_URL=ridiculousdbconnection
DB_USER=someuser
ENDPOINT=emoji.list
HEROKU_APP=herokuapp
HOST=localhost
JSON_FN=/tmp/output.json
JWT_LIFE_SPAN=120
MEETUP_EMAIL=username@acme.com
MEETUP_PASS=supersecurepassword
POETRY=1.7.1
PORT=3000
PRIV_KEY_B64=base64_encoded_private_pem_key
PUB_KEY_B64=base64_encoded_public_pem_key
PY_VER=3.11.6
REDIRECT_URI=https://acme.com
REGISTRY_URL=docker.io
REGISTRY_PASS=containerregistrytoken
RUN_TIME=1400
SECRET_KEY=secretmeetinginthebasementofmybrain
SELF_ID=techlahomauserid
SERVICE=meetup-bot
SIGNING_KEY_ID=activejwtkeyid
SIGNING_SECRET=33characterstringthatImm1micking!
SLACK_WEBHOOK=incomingwebhook
TAG=registry.heroku.com/${HEROKU_APP}/web:latest
TIME_DELTA=1
TOKEN_EXPIRE=30
TOKEN_URL="https://secure.meetup.com/oauth2/access"
TTL=3600
TZ=America/Chicago
URL=https://dyno-name.herokuapp.com
URLNAME=Techlahoma-Foundation
USER_NAME=containerregistryusername
USER_TOKEN=xoxp-usertoken

# Taskfile Env Precedence
# * Manipulate venv path
# * https://taskfile.dev/docs/experiments/env-precedence
TASK_X_ENV_PRECEDENCE=1
````

## File: .release-please-manifest.json
````json
{
  ".": "1.1.2"
}
````

## File: CHANGELOG.md
````markdown
# Changelog

## [1.1.2](https://github.com/pythoninthegrass/meetup_bot/compare/v1.1.1...v1.1.2) (2025-05-13)


### Documentation

* add [@alex-code4okc](https://github.com/alex-code4okc) as a contributor ([7feccfa](https://github.com/pythoninthegrass/meetup_bot/commit/7feccfa439115616c7fdb760c15043ff3e6d858e))
* contributing ([fd2c294](https://github.com/pythoninthegrass/meetup_bot/commit/fd2c294a018e6943b4b6b66af74b8eaa14db0c0c))
* update readme ([437d81a](https://github.com/pythoninthegrass/meetup_bot/commit/437d81a528e7e63b98d8f9ab7e1086d2a11023b7))

## [1.1.1](https://github.com/pythoninthegrass/meetup_bot/compare/v1.1.0...v1.1.1) (2024-08-26)


### Bug Fixes

* override schedule times ([f18718b](https://github.com/pythoninthegrass/meetup_bot/commit/f18718b62b403fabf7dce0921c9056dd96defba1))

## [1.1.0](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.4...v1.1.0) (2024-08-21)


### Features

* add scheduling ([800acda](https://github.com/pythoninthegrass/meetup_bot/commit/800acda371006760724ca67e6b0a70260b39b0b1))

## [1.0.4](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.3...v1.0.4) (2024-06-26)


### Bug Fixes

* print exception error ([96c3c40](https://github.com/pythoninthegrass/meetup_bot/commit/96c3c404b1268401f2a4bbfc803f32849cc54d98))
* remove buildkit ([bd7ecc1](https://github.com/pythoninthegrass/meetup_bot/commit/bd7ecc125d188e5bf4fc526f267282dd5492a19d))
* remove hard-coded .env path ([bc05636](https://github.com/pythoninthegrass/meetup_bot/commit/bc056360e81968c7d086fce4744f807b9093c0e3))
* wrong dockerfile directory ([b77daf5](https://github.com/pythoninthegrass/meetup_bot/commit/b77daf51d5b1ae3d4fae406b3513ae8a201bce30))


### Documentation

* update readme ([899cb27](https://github.com/pythoninthegrass/meetup_bot/commit/899cb279d2ee87acb154edf612e196b6f9b1b541))

## [1.0.3](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.2...v1.0.3) (2024-03-22)


### Bug Fixes

* heroku stats ([79977ab](https://github.com/pythoninthegrass/meetup_bot/commit/79977ab5549de6d11d888b229fd3b7f0d1b352e0))


### Documentation

* update README.md ([11239c0](https://github.com/pythoninthegrass/meetup_bot/commit/11239c098f59acc35ed006610fd8b4031520f953))
* update README.md ([9038532](https://github.com/pythoninthegrass/meetup_bot/commit/903853252fcf1bfa0d28540eed8e1fb45c6ddaa1))
* update README.md ([a752c67](https://github.com/pythoninthegrass/meetup_bot/commit/a752c673f073d8cf355bf399416d8b4dcda05b4b))

## [1.0.2](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.1...v1.0.2) (2024-02-24)


### Bug Fixes

* docker ([be44104](https://github.com/pythoninthegrass/meetup_bot/commit/be44104c8caa7197eeb12123873ab64aa7677ef8))

## [1.0.1](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.0...v1.0.1) (2024-02-19)


### Bug Fixes

* poetry package error ([a9a24ac](https://github.com/pythoninthegrass/meetup_bot/commit/a9a24ac14d7ef2ce86ed517e744ada7128ebc6d1))


### Documentation

* update README.md ([489ba54](https://github.com/pythoninthegrass/meetup_bot/commit/489ba540d873ee79863b57e31ab3fa4fa2f1fcca))
* update README.md ([84e891a](https://github.com/pythoninthegrass/meetup_bot/commit/84e891a468a74532518c95c26190c0f2ade614be))

## 1.0.0 (2024-02-19)


### Bug Fixes

* indentation ([3a47e6c](https://github.com/pythoninthegrass/meetup_bot/commit/3a47e6c245164d085b69cfc9d27081b75a9f308d))


### Miscellaneous Chores

* release 1.0.0 ([116b45f](https://github.com/pythoninthegrass/meetup_bot/commit/116b45f03d246b7ad5cf11f54bb99330311bf1dd))
````

## File: devbox.json
````json
{
  "packages": {
    "gh":   "latest",
    "git":  "latest",
    "glib": "latest",
    "glibcLocalesUtf8": {
      "version": "latest",
      "platforms": [
        "x86_64-linux",
        "aarch64-linux"
      ]
    },
    "gnumake":    "latest",
    "go-task":    "latest",
    "kubectl":    "latest",
    "nodejs":     "latest",
    "openssl":    "latest",
    "pre-commit": "latest",
    "ruff":       "latest",
    "tilt":       "latest",
    "uv":         "latest"
  },
  "env": {
    "VENV_DIR":            ".venv",
    "UV_HTTP_TIMEOUT":     "90",
    "UV_COMPILE_BYTECODE": "1",
    "UV_LINK_MODE":        "copy",
    "LANG":                "en_US.UTF-8",
    "LC_ALL":              "en_US.UTF-8",
    "LANGUAGE":            "en_US.UTF-8"
  },
  "shell": {
    "init_hook": [
      "[ -d ${VENV_DIR} ] || uv venv ${VENV_DIR}",
      ". $VENV_DIR/bin/activate",
      "uv pip install -r pyproject.toml --all-extras"
    ],
    "scripts": {
      "install":     "uv pip install -r pyproject.toml --all-extras",
      "export-reqs": "uv pip freeze | uv pip compile - -o requirements.txt",
      "venv":        "uv venv ${VENV_DIR}",
      "test":        "pytest"
    }
  }
}
````

## File: devbox.lock
````
{
  "lockfile_version": "1",
  "packages": {
    "gh@latest": {
      "last_modified": "2025-05-02T02:23:51Z",
      "resolved": "github:NixOS/nixpkgs/032bc6539bd5f14e9d0c51bd79cfe9a055b094c3#gh",
      "source": "devbox-search",
      "version": "2.72.0",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/qzh3pln071d8zs11bb6ppnmfx7w5gkqf-gh-2.72.0",
              "default": true
            }
          ],
          "store_path": "/nix/store/qzh3pln071d8zs11bb6ppnmfx7w5gkqf-gh-2.72.0"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/lpp3rmb04fcxas70yf9g4kkzq4ag61i4-gh-2.72.0",
              "default": true
            }
          ],
          "store_path": "/nix/store/lpp3rmb04fcxas70yf9g4kkzq4ag61i4-gh-2.72.0"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/kgsgb0rk2qxj9fxa2chra1dyrkwlxsyf-gh-2.72.0",
              "default": true
            }
          ],
          "store_path": "/nix/store/kgsgb0rk2qxj9fxa2chra1dyrkwlxsyf-gh-2.72.0"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/aapnxgvkl1xx1s13c93k8d18f3vlg9r0-gh-2.72.0",
              "default": true
            }
          ],
          "store_path": "/nix/store/aapnxgvkl1xx1s13c93k8d18f3vlg9r0-gh-2.72.0"
        }
      }
    },
    "git@latest": {
      "last_modified": "2025-04-17T05:47:26Z",
      "resolved": "github:NixOS/nixpkgs/ebe4301cbd8f81c4f8d3244b3632338bbeb6d49c#git",
      "source": "devbox-search",
      "version": "2.49.0",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/s5b9rm8fjxggjak0yl2dkxzswfpzl8p8-git-2.49.0",
              "default": true
            },
            {
              "name": "doc",
              "path": "/nix/store/2hygrabh741w0ynwcb6gy2922cx4fnj3-git-2.49.0-doc"
            }
          ],
          "store_path": "/nix/store/s5b9rm8fjxggjak0yl2dkxzswfpzl8p8-git-2.49.0"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/rs24n34brzvcmgld6mgfg0dd7ynv26pp-git-2.49.0",
              "default": true
            },
            {
              "name": "debug",
              "path": "/nix/store/wgki5jsxgg6lxqh98jgbj9dnwv7f68cw-git-2.49.0-debug"
            },
            {
              "name": "doc",
              "path": "/nix/store/3h7fnw0qhy92c8iyrv2i64r6wywsnjsa-git-2.49.0-doc"
            }
          ],
          "store_path": "/nix/store/rs24n34brzvcmgld6mgfg0dd7ynv26pp-git-2.49.0"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/0zv7h6mzrxk0sarvis22imr9nmnmqlpg-git-2.49.0",
              "default": true
            },
            {
              "name": "doc",
              "path": "/nix/store/yiy6g5pi9jvp2nzgd4ncfwbhs13nwwz1-git-2.49.0-doc"
            }
          ],
          "store_path": "/nix/store/0zv7h6mzrxk0sarvis22imr9nmnmqlpg-git-2.49.0"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/z8z1mhfnvw40dwljqazxv0343sv5ds2g-git-2.49.0",
              "default": true
            },
            {
              "name": "debug",
              "path": "/nix/store/w547h0xwq9489xnqg1ddqlh1v71xvng8-git-2.49.0-debug"
            },
            {
              "name": "doc",
              "path": "/nix/store/rjjf5h1qcwgdxs9w23h6p0bhavgaknyh-git-2.49.0-doc"
            }
          ],
          "store_path": "/nix/store/z8z1mhfnvw40dwljqazxv0343sv5ds2g-git-2.49.0"
        }
      }
    },
    "github:NixOS/nixpkgs/nixpkgs-unstable": {
      "last_modified": "2025-05-12T14:38:58Z",
      "resolved": "github:NixOS/nixpkgs/eaeed9530c76ce5f1d2d8232e08bec5e26f18ec1?lastModified=1747060738&narHash=sha256-ByfPRQuqj%2BnhtVV0koinEpmJw0KLzNbgcgi9EF%2BNVow%3D"
    },
    "glib@latest": {
      "last_modified": "2025-05-04T22:22:57Z",
      "resolved": "github:NixOS/nixpkgs/ed30f8aba41605e3ab46421e3dcb4510ec560ff8#glib",
      "source": "devbox-search",
      "version": "2.82.5",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/72aqkmc1ff8331clw056fygmf5156wap-glib-2.82.5-bin",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/699g20v1iry0x3xiybp57hjw1bfm2g06-glib-2.82.5-dev"
            },
            {
              "name": "devdoc",
              "path": "/nix/store/jk5ynpv2jrjrjjxxcp3vs47aldr50qma-glib-2.82.5-devdoc"
            },
            {
              "name": "out",
              "path": "/nix/store/b9zka1ymsxvhkzxs75gyz78jjm1d5vza-glib-2.82.5"
            }
          ],
          "store_path": "/nix/store/72aqkmc1ff8331clw056fygmf5156wap-glib-2.82.5-bin"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/s768z7syvlq6h9841nygaaqpczvc87q0-glib-2.82.5-bin",
              "default": true
            },
            {
              "name": "debug",
              "path": "/nix/store/8gf3qys1cr0s1slhf96y8by0w3hvsb02-glib-2.82.5-debug"
            },
            {
              "name": "dev",
              "path": "/nix/store/0r2f4i3xsnky3r5rgqxbh2rvjr2d42j1-glib-2.82.5-dev"
            },
            {
              "name": "devdoc",
              "path": "/nix/store/dids3si315rb12ifbardxrdz46n0gskf-glib-2.82.5-devdoc"
            },
            {
              "name": "out",
              "path": "/nix/store/mm42al2wq9b5d3dg1xil8321102z205v-glib-2.82.5"
            }
          ],
          "store_path": "/nix/store/s768z7syvlq6h9841nygaaqpczvc87q0-glib-2.82.5-bin"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/q07br5vhha9mibyf94figj1zkg4mdxlp-glib-2.82.5-bin",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/k9lp8mnjspfdm8rrgdlmazcwiw3ngk2r-glib-2.82.5-dev"
            },
            {
              "name": "devdoc",
              "path": "/nix/store/zaa8fs038c3680cwyrlc74grfsxvqkp6-glib-2.82.5-devdoc"
            },
            {
              "name": "out",
              "path": "/nix/store/jn1xrhhf6rg2nn8vdlxvmpnvm5y25zbb-glib-2.82.5"
            }
          ],
          "store_path": "/nix/store/q07br5vhha9mibyf94figj1zkg4mdxlp-glib-2.82.5-bin"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/s3insilxvj11miid5pf1mbp4fawykaal-glib-2.82.5-bin",
              "default": true
            },
            {
              "name": "out",
              "path": "/nix/store/ysm6ybv02ms2v6lzsx7fnqi2cy937l9x-glib-2.82.5"
            },
            {
              "name": "debug",
              "path": "/nix/store/7wfaswffg76il1v7ilkz6wcnx6z447hz-glib-2.82.5-debug"
            },
            {
              "name": "dev",
              "path": "/nix/store/xiwx6867gn8yzy575hkyszdkmyv2i59r-glib-2.82.5-dev"
            },
            {
              "name": "devdoc",
              "path": "/nix/store/j2cvjbkb9jq3wh6cxjxyjrs0d196qjr3-glib-2.82.5-devdoc"
            }
          ],
          "store_path": "/nix/store/s3insilxvj11miid5pf1mbp4fawykaal-glib-2.82.5-bin"
        }
      }
    },
    "gnumake@latest": {
      "last_modified": "2024-06-12T20:55:33Z",
      "resolved": "github:NixOS/nixpkgs/a9858885e197f984d92d7fe64e9fff6b2e488d40#gnumake",
      "source": "devbox-search",
      "version": "4.4.1",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/qkkliqj6qhzlkchlkqc6n2iry22gi78q-gnumake-4.4.1",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/dmwcjbixs9hd9yrhfccbnac5macnbk8v-gnumake-4.4.1-man",
              "default": true
            },
            {
              "name": "info",
              "path": "/nix/store/79r1gy3hy993aj4f37wd83ad36j3bq52-gnumake-4.4.1-info"
            }
          ],
          "store_path": "/nix/store/qkkliqj6qhzlkchlkqc6n2iry22gi78q-gnumake-4.4.1"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/8pynb9b4k67r27hizrcj9gjr432y8a1y-gnumake-4.4.1",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/9k1jrb18rjngqraz5d289yabfpji3z5c-gnumake-4.4.1-man",
              "default": true
            },
            {
              "name": "debug",
              "path": "/nix/store/nmfk05y35amg7wayngr1c2c2jzhmlgfg-gnumake-4.4.1-debug"
            },
            {
              "name": "info",
              "path": "/nix/store/8q2ns2k33zs2fh50fnjn8615m92gw5lm-gnumake-4.4.1-info"
            }
          ],
          "store_path": "/nix/store/8pynb9b4k67r27hizrcj9gjr432y8a1y-gnumake-4.4.1"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/dkhhxf3ym48qig17psd17nnk9i6w70j1-gnumake-4.4.1",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/7f3p4cgy7qw4x6fwjxmlvx3nynz1i1g6-gnumake-4.4.1-man",
              "default": true
            },
            {
              "name": "info",
              "path": "/nix/store/1galikm5wxwhhwghvl93b76d5q8wj96d-gnumake-4.4.1-info"
            }
          ],
          "store_path": "/nix/store/dkhhxf3ym48qig17psd17nnk9i6w70j1-gnumake-4.4.1"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/ggk94mjyn9zw716lqh0bb0ipl9xl271k-gnumake-4.4.1",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/nq33rh3k81skrdz6v6j5dq0z56p8ai37-gnumake-4.4.1-man",
              "default": true
            },
            {
              "name": "debug",
              "path": "/nix/store/zk2mrdl72rb81302scnj0rhb7d2dwk5a-gnumake-4.4.1-debug"
            },
            {
              "name": "info",
              "path": "/nix/store/pciwycm9jbbfbhsa9wfasqbs7113m70z-gnumake-4.4.1-info"
            }
          ],
          "store_path": "/nix/store/ggk94mjyn9zw716lqh0bb0ipl9xl271k-gnumake-4.4.1"
        }
      }
    },
    "go-task@latest": {
      "last_modified": "2024-06-12T20:55:33Z",
      "resolved": "github:NixOS/nixpkgs/a9858885e197f984d92d7fe64e9fff6b2e488d40#go-task",
      "source": "devbox-search",
      "version": "3.37.2",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/xj1p4vb2b09610dpyn1wh7qg6axicdw9-go-task-3.37.2",
              "default": true
            }
          ],
          "store_path": "/nix/store/xj1p4vb2b09610dpyn1wh7qg6axicdw9-go-task-3.37.2"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/i7rv367d2p5yj6hhsbja96rlkvj7fvm5-go-task-3.37.2",
              "default": true
            }
          ],
          "store_path": "/nix/store/i7rv367d2p5yj6hhsbja96rlkvj7fvm5-go-task-3.37.2"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/vqas5d4fd44paghrjyyj5wa52mv5inr5-go-task-3.37.2",
              "default": true
            }
          ],
          "store_path": "/nix/store/vqas5d4fd44paghrjyyj5wa52mv5inr5-go-task-3.37.2"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/gy9vnx7dm5chq2isyi6ig9x908hb7kd6-go-task-3.37.2",
              "default": true
            }
          ],
          "store_path": "/nix/store/gy9vnx7dm5chq2isyi6ig9x908hb7kd6-go-task-3.37.2"
        }
      }
    },
    "kubectl@latest": {
      "last_modified": "2025-05-03T10:49:23Z",
      "resolved": "github:NixOS/nixpkgs/b6aef6c3553f849e1e6c08f1bcd3061df2b69fc4#kubectl",
      "source": "devbox-search",
      "version": "1.33.0",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/ca0rizbf9qc8rqmn3cqzzy65k2il9dz8-kubectl-1.33.0",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/2nj939rw1s5a7n9ky3r7rzpw9mvn0pgm-kubectl-1.33.0-man",
              "default": true
            },
            {
              "name": "convert",
              "path": "/nix/store/4skllfm7pi9fvbrjxc77pwwnkvzbbk9d-kubectl-1.33.0-convert"
            }
          ],
          "store_path": "/nix/store/ca0rizbf9qc8rqmn3cqzzy65k2il9dz8-kubectl-1.33.0"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/7zg6c6ia3qvpl90xdpf8ky2wn2kcg42h-kubectl-1.33.0",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/4jh2hs3iawrsfbsih2ddzr42gbhbyixc-kubectl-1.33.0-man",
              "default": true
            },
            {
              "name": "convert",
              "path": "/nix/store/krdav16jc0jvrgpivgwyprkrpvfsmk5n-kubectl-1.33.0-convert"
            }
          ],
          "store_path": "/nix/store/7zg6c6ia3qvpl90xdpf8ky2wn2kcg42h-kubectl-1.33.0"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/j6s7v31ss9qlc79ac363vqnq28p62l8c-kubectl-1.33.0",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/i919x98v35viisiylbgskyi5imjm2ppg-kubectl-1.33.0-man",
              "default": true
            },
            {
              "name": "convert",
              "path": "/nix/store/3rbhqv054ijp51zzh60lbws6ia7madj1-kubectl-1.33.0-convert"
            }
          ],
          "store_path": "/nix/store/j6s7v31ss9qlc79ac363vqnq28p62l8c-kubectl-1.33.0"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/9rn354l23mr9kh840kn94c3p9bns4wd4-kubectl-1.33.0",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/sakg9rw3pdg0d0pbpjizvy8vcyydqxrc-kubectl-1.33.0-man",
              "default": true
            },
            {
              "name": "convert",
              "path": "/nix/store/8bs481ic0gwaa5m3qz6hqzxrxnskv3zw-kubectl-1.33.0-convert"
            }
          ],
          "store_path": "/nix/store/9rn354l23mr9kh840kn94c3p9bns4wd4-kubectl-1.33.0"
        }
      }
    },
    "nodejs@latest": {
      "last_modified": "2025-06-14T12:19:57Z",
      "plugin_version": "0.0.2",
      "resolved": "github:NixOS/nixpkgs/41da1e3ea8e23e094e5e3eeb1e6b830468a7399e#nodejs_24",
      "source": "devbox-search",
      "version": "24.1.0",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/2q5an9rpdq4vhc5ag04ajxnzxxqsqchq-nodejs-24.1.0",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/hb25vqffnqd3hl7glmm1y4n54bmpfppr-nodejs-24.1.0-dev"
            },
            {
              "name": "libv8",
              "path": "/nix/store/jw04y4lzw7x0v2yh437s3l6cri5l50vv-nodejs-24.1.0-libv8"
            }
          ],
          "store_path": "/nix/store/2q5an9rpdq4vhc5ag04ajxnzxxqsqchq-nodejs-24.1.0"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/1ypnf27d1amna71zl7jgjpli4r2xqzx9-nodejs-24.1.0",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/3alphvmg91jin165pj9q5zfk7j40azbg-nodejs-24.1.0-dev"
            },
            {
              "name": "libv8",
              "path": "/nix/store/z1cbkwmgw0f94rhvc40v3k8z1rg9zkzf-nodejs-24.1.0-libv8"
            }
          ],
          "store_path": "/nix/store/1ypnf27d1amna71zl7jgjpli4r2xqzx9-nodejs-24.1.0"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/plga9910l27vbg30ajmdsmccyj2a3pxm-nodejs-24.1.0",
              "default": true
            },
            {
              "name": "libv8",
              "path": "/nix/store/d6cq633qq8jr8liaip97fjwpv9r15ivb-nodejs-24.1.0-libv8"
            },
            {
              "name": "dev",
              "path": "/nix/store/4b8xp5vrd08ca1im5b607x1wwvy4njjx-nodejs-24.1.0-dev"
            }
          ],
          "store_path": "/nix/store/plga9910l27vbg30ajmdsmccyj2a3pxm-nodejs-24.1.0"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/wnayblhh0555nwfccnzcqkzph52y4yby-nodejs-24.1.0",
              "default": true
            },
            {
              "name": "libv8",
              "path": "/nix/store/4paqvzbw7jjzvn64liv5wwzc7fdsr7k7-nodejs-24.1.0-libv8"
            },
            {
              "name": "dev",
              "path": "/nix/store/8ydr7k53w188y9fhskl7ahl8ibchx7w8-nodejs-24.1.0-dev"
            }
          ],
          "store_path": "/nix/store/wnayblhh0555nwfccnzcqkzph52y4yby-nodejs-24.1.0"
        }
      }
    },
    "openssl@latest": {
      "last_modified": "2025-05-03T19:26:05Z",
      "resolved": "github:NixOS/nixpkgs/f21e4546e3ede7ae34d12a84602a22246b31f7e0#openssl",
      "source": "devbox-search",
      "version": "3.4.1",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/w870sgdxlfs0qj3ns87lq553yhm38yd8-openssl-3.4.1-bin",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/3jg2vq3njzz6wx5q2kym7zjpaznb4w4g-openssl-3.4.1-man",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/vg5hxgrz9af5kak1ramgfpxn0cl29s8h-openssl-3.4.1-dev"
            },
            {
              "name": "doc",
              "path": "/nix/store/ih0n1hvk5gapn780hknq1z15ac43fhsq-openssl-3.4.1-doc"
            },
            {
              "name": "out",
              "path": "/nix/store/8kgyrgfpdgx1kvgaaw9j4cyf3731zh3f-openssl-3.4.1"
            }
          ],
          "store_path": "/nix/store/w870sgdxlfs0qj3ns87lq553yhm38yd8-openssl-3.4.1-bin"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/h7bimy1mcc1nfh5g5qmm4mrg2mh2viar-openssl-3.4.1-bin",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/zkn38yg3nj1xy2hbsxpa9y3fqcxibycy-openssl-3.4.1-man",
              "default": true
            },
            {
              "name": "out",
              "path": "/nix/store/nggnlzwnhqjdlwr1i3pagd1lixac844l-openssl-3.4.1"
            },
            {
              "name": "debug",
              "path": "/nix/store/wv23r1yc6sdn7bz358nl2v5z5ix8wq55-openssl-3.4.1-debug"
            },
            {
              "name": "dev",
              "path": "/nix/store/qinywls876bwkpj3pdq5ds99mb1wxpk4-openssl-3.4.1-dev"
            },
            {
              "name": "doc",
              "path": "/nix/store/96ravrb9rmkla59ka49006l4ch00c3c6-openssl-3.4.1-doc"
            }
          ],
          "store_path": "/nix/store/h7bimy1mcc1nfh5g5qmm4mrg2mh2viar-openssl-3.4.1-bin"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/9yqbv06jcq1h5kd96j69njc729wly5rk-openssl-3.4.1-bin",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/ykkd6jdwfhkxqyxsp1pmr1b5y4gwmsqw-openssl-3.4.1-man",
              "default": true
            },
            {
              "name": "dev",
              "path": "/nix/store/qfman48d4n44gl3a80ak3s88fs15lzp6-openssl-3.4.1-dev"
            },
            {
              "name": "doc",
              "path": "/nix/store/4w7cw7knbddz8bhf4b1p875lw4nni67p-openssl-3.4.1-doc"
            },
            {
              "name": "out",
              "path": "/nix/store/2xfksl6axmhk1i853f5z30bjdzrizvkf-openssl-3.4.1"
            }
          ],
          "store_path": "/nix/store/9yqbv06jcq1h5kd96j69njc729wly5rk-openssl-3.4.1-bin"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "bin",
              "path": "/nix/store/6ixac5i91likh5njdkrj8g4m2bhfgzcf-openssl-3.4.1-bin",
              "default": true
            },
            {
              "name": "man",
              "path": "/nix/store/mdc7slc6rzngkzlcn7pq70vghknvpsjq-openssl-3.4.1-man",
              "default": true
            },
            {
              "name": "doc",
              "path": "/nix/store/wwymhrqycz6wrzkvxn23qb47lc07zfq2-openssl-3.4.1-doc"
            },
            {
              "name": "out",
              "path": "/nix/store/xy8x4g472i5n1bh24c5ixhbnk6qlm9vz-openssl-3.4.1"
            },
            {
              "name": "debug",
              "path": "/nix/store/zpbbcc0agw4rqc89ihyjq2yqq1dswjdp-openssl-3.4.1-debug"
            },
            {
              "name": "dev",
              "path": "/nix/store/jv45xs1p8v9mcychfgkv6vxridcn532h-openssl-3.4.1-dev"
            }
          ],
          "store_path": "/nix/store/6ixac5i91likh5njdkrj8g4m2bhfgzcf-openssl-3.4.1-bin"
        }
      }
    },
    "pre-commit@latest": {
      "last_modified": "2025-04-29T04:24:43Z",
      "resolved": "github:NixOS/nixpkgs/ffa0bb043c25cfc79ff3bc20ba2e44c3724499b1#pre-commit",
      "source": "devbox-search",
      "version": "4.0.1",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/3qcg99ylsvnpgjz6mraychq1cq7h0hqy-pre-commit-4.0.1",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/2kfsh11nmbfb4p0swc8fbd64zx8yxk2m-pre-commit-4.0.1-dist"
            }
          ],
          "store_path": "/nix/store/3qcg99ylsvnpgjz6mraychq1cq7h0hqy-pre-commit-4.0.1"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/ncrrahxiwhhbfhlahhchn4vjjbbx2bki-pre-commit-4.0.1",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/hs6q88mzrg7ahs0q8zrpzdhcjx3q7hby-pre-commit-4.0.1-dist"
            }
          ],
          "store_path": "/nix/store/ncrrahxiwhhbfhlahhchn4vjjbbx2bki-pre-commit-4.0.1"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/4cawf7w6kan4hk8fm7fd61r6wrcx1pql-pre-commit-4.0.1",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/i66khaa7g5v722lp1lb1sf9ahzlsdbhl-pre-commit-4.0.1-dist"
            }
          ],
          "store_path": "/nix/store/4cawf7w6kan4hk8fm7fd61r6wrcx1pql-pre-commit-4.0.1"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/8y3rszv7dpch6l6hbixfhmdwmki75mqq-pre-commit-4.0.1",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/xaxz96ykrhz5rw55p9i5qvykd06zz285-pre-commit-4.0.1-dist"
            }
          ],
          "store_path": "/nix/store/8y3rszv7dpch6l6hbixfhmdwmki75mqq-pre-commit-4.0.1"
        }
      }
    },
    "ruff@latest": {
      "last_modified": "2025-05-02T02:23:51Z",
      "resolved": "github:NixOS/nixpkgs/032bc6539bd5f14e9d0c51bd79cfe9a055b094c3#ruff",
      "source": "devbox-search",
      "version": "0.11.8",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/8f8fjng4nk137h2f4bh232096kyaxnlj-ruff-0.11.8",
              "default": true
            }
          ],
          "store_path": "/nix/store/8f8fjng4nk137h2f4bh232096kyaxnlj-ruff-0.11.8"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/l5rcgzyrzi65454k5rf4xf8j19cr5524-ruff-0.11.8",
              "default": true
            }
          ],
          "store_path": "/nix/store/l5rcgzyrzi65454k5rf4xf8j19cr5524-ruff-0.11.8"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/z8kvg9ci66k53xraa2xgidn34rf82vky-ruff-0.11.8",
              "default": true
            }
          ],
          "store_path": "/nix/store/z8kvg9ci66k53xraa2xgidn34rf82vky-ruff-0.11.8"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/8wb0brfxm0l78zq0nnyqgnv6p1waap41-ruff-0.11.8",
              "default": true
            }
          ],
          "store_path": "/nix/store/8wb0brfxm0l78zq0nnyqgnv6p1waap41-ruff-0.11.8"
        }
      }
    },
    "tilt@latest": {
      "last_modified": "2024-06-16T13:15:37Z",
      "resolved": "github:NixOS/nixpkgs/683aa7c4e385509ca651d49eeb35e58c7a1baad6#tilt",
      "source": "devbox-search",
      "version": "0.33.10",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/gzwq36y6jkihjkjbc23wgg8b2s7j1ng6-tilt-0.33.10",
              "default": true
            }
          ],
          "store_path": "/nix/store/gzwq36y6jkihjkjbc23wgg8b2s7j1ng6-tilt-0.33.10"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/2gaw5amxl27jarn82ia5nwxasn2m2p0p-tilt-0.33.10",
              "default": true
            }
          ],
          "store_path": "/nix/store/2gaw5amxl27jarn82ia5nwxasn2m2p0p-tilt-0.33.10"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/haxd3aa1h4z7i55kgzqhc12hva007y2z-tilt-0.33.10",
              "default": true
            }
          ],
          "store_path": "/nix/store/haxd3aa1h4z7i55kgzqhc12hva007y2z-tilt-0.33.10"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/2z7zm1h4rgd69hkda6j73ibpibbzzp1l-tilt-0.33.10",
              "default": true
            }
          ],
          "store_path": "/nix/store/2z7zm1h4rgd69hkda6j73ibpibbzzp1l-tilt-0.33.10"
        }
      }
    },
    "uv@latest": {
      "last_modified": "2024-06-19T22:49:28Z",
      "resolved": "github:NixOS/nixpkgs/98053e7c05285b3079af95e99aef97d9455faef7#uv",
      "source": "devbox-search",
      "version": "0.2.13",
      "systems": {
        "aarch64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/yajrm9558dvh5x88dxkswja6n4m9ny1i-uv-0.2.13",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/hz49i3q4kdh4yrvmxcmq34xqs471210a-uv-0.2.13-dist"
            }
          ],
          "store_path": "/nix/store/yajrm9558dvh5x88dxkswja6n4m9ny1i-uv-0.2.13"
        },
        "aarch64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/hcfz60ykxfdc2cx47df0g75z86m9bd8f-uv-0.2.13",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/5lfi4cjq56yynvx9cddv56cf90zm4i8b-uv-0.2.13-dist"
            }
          ],
          "store_path": "/nix/store/hcfz60ykxfdc2cx47df0g75z86m9bd8f-uv-0.2.13"
        },
        "x86_64-darwin": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/p5qz3lqla85sxa5rivgfqgkzixrirgym-uv-0.2.13",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/kajmw58jlalq9mlr0z6py2haqni4s8fm-uv-0.2.13-dist"
            }
          ],
          "store_path": "/nix/store/p5qz3lqla85sxa5rivgfqgkzixrirgym-uv-0.2.13"
        },
        "x86_64-linux": {
          "outputs": [
            {
              "name": "out",
              "path": "/nix/store/qb455hfjwy16c160d2qfyd9gc2nxlsp0-uv-0.2.13",
              "default": true
            },
            {
              "name": "dist",
              "path": "/nix/store/dxqw3bavjr647ks6v1cd7zz20z9n9fqv-uv-0.2.13-dist"
            }
          ],
          "store_path": "/nix/store/qb455hfjwy16c160d2qfyd9gc2nxlsp0-uv-0.2.13"
        }
      }
    }
  }
}
````

## File: Dockerfile.dev
````
# syntax=docker/dockerfile:1.7.0

ARG PYTHON_VERSION=3.11.9

FROM python:${PYTHON_VERSION}-alpine AS builder

RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    python3-dev

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ENV VENV="/opt/venv"
ENV PATH="$VENV/bin:$PATH"

WORKDIR /app

COPY requirements-dev.txt .

RUN python -m venv $VENV \
    && . $VENV/bin/activate \
    && python -m pip install --upgrade pip \
    && python -m pip install -r requirements-dev.txt

FROM python:${PYTHON_VERSION}-alpine AS runner

ENV TZ=${TZ:-"America/Chicago"}
RUN apk add --no-cache tzdata \
    && ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime \
    && echo "$TZ" > /etc/timezone

ENV USER_NAME=appuser
ENV VENV="/opt/venv"

ENV PATH="${VENV}/bin:${VENV}/lib/python${PYTHON_VERSION}/site-packages:/usr/local/bin:${HOME}/.local/bin:/bin:/usr/bin:/usr/share/doc:$PATH"

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

ARG UID=10001
RUN adduser -D -u ${UID} ${USER_NAME}

USER ${USER_NAME}

WORKDIR /app

COPY --chown=${USER_NAME} ./app .
COPY --from=builder --chown=${USER_NAME} "$VENV" "$VENV"

CMD [ "sleep", "infinity" ]

LABEL org.opencontainers.image.title="meetup_bot"
LABEL org.opencontainers.image.version="test"
LABEL org.opencontainers.image.description="meetup_bot image for running tests in CI"
````

## File: package.json
````json
{
  "devDependencies": {
    "all-contributors-cli": "^6.26.1",
    "cz-conventional-changelog": "^3.3.0"
  },
  "config": {
    "commitizen": {
      "path": "./node_modules/cz-conventional-changelog"
    }
  },
  "scripts": {
    "contributors:add": "all-contributors add",
    "contributors:generate": "all-contributors generate"
  }
}
````

## File: ruff.toml
````toml
# Fix without reporting on leftover violations
fix-only = true

# Enumerate all fixed violations
show-fixes = true

# Indent width (default: 4)
indent-width = 4

# Black (default: 88)
line-length = 130

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    "dist",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    "__pycache__",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]

# Assume Python 3.11
target-version = "py311"

[format]
# Use spaces instead of tabs
indent-style = "space"

# Use `\n` line endings for all files
line-ending = "lf"

# Set quote style for strings
quote-style = "preserve"

[lint]
select = [
    # pycodestyle
    "E",
    # Pyflakes
    "F",
    # pyupgrade
    "UP",
    # flake8-bugbear
    "B",
    # flake8-simplify
    "SIM",
    # isort
    "I",
]
ignore = ["D203", "E203", "E251", "E266", "E401", "E402", "E501", "F401", "F403", "F841"]

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Allow autofix for all enabled rules (when `--fix`) is provided.
fixable = ["A", "B", "C", "D", "E", "F", "G", "I", "N", "Q", "S", "T", "W", "ANN", "ARG", "BLE", "COM", "DJ", "DTZ", "EM", "ERA", "EXE", "FBT", "ICN", "INP", "ISC", "NPY", "PD", "PGH", "PIE", "PL", "PT", "PTH", "PYI", "RET", "RSE", "RUF", "SIM", "SLF", "TID", "TRY", "UP", "YTT"]

[lint.isort]
combine-as-imports = true
from-first = false
no-sections = true
order-by-type = true

[lint.flake8-quotes]
docstring-quotes = "double"

[lint.mccabe]
# Unlike Flake8, default to a complexity level of 10.
max-complexity = 10
````

## File: taskfile.yml
````yaml
version: "3.0"

set: ['e', 'u', 'pipefail']
shopt: ['globstar']

dotenv: ['./app/.env']

env:
  VENV_DIR: "{{.ROOT_DIR}}/.venv"
  PATH: "{{.VENV_DIR}}/bin:{{.PATH}}"

vars:

includes:
  docker:
    taskfile: ./taskfiles/docker.yml
  heroku:
    taskfile: ./taskfiles/heroku.yml
  uv:
    taskfile: ./taskfiles/uv.yml

tasks:
  default:
    desc: "Default task"
    cmds:
      - task --list

  install:
    desc: "Install project dependencies"
    cmds:
      - |
        {{.INSTALL}} {{.CLI_ARGS}}

  pre-commit:
    desc: "Run pre-commit hooks"
    cmds:
      - prek run

  lint:
    desc: "Run linters"
    cmds:
      - ruff check --fix --respect-gitignore

  format:
    desc: "Run formatters"
    cmds:
      - ruff format --respect-gitignore

  test:
    desc: "Run tests"
    cmds:
      - pytest

  pyclean:
    desc: "Remove .pyc and __pycache__"
    cmds:
      - |
        args=(
          .
          --debris
          --verbose
          -i .devbox
        )
        case "{{.CLI_ARGS}}" in
          dry-run)
            pyclean "${args[@]}" --dry-run
            ;;
          *)
            pyclean "${args[@]}"
            ;;
        esac

  checkbash:
    desc: "Check bash scripts"
    cmds:
      - checkbashism -x {{.ROOT_DIR}}/app/*.sh

  repomix:
    desc: "Create llm snapshot of repo"
    preconditions:
      - sh: command -v repomix 2>/dev/null
        msg: "repomix is not installed. Install with: npm install -g repomix"
    cmds:
      - |
        repomix \
          --style markdown \
          --compress \
          --remove-comments \
          --remove-empty-lines \
          --truncate-base64
    sources:
      - "**/*.py"
      - "**/*.toml"
      - "**/*.yml"
      - "**/*.yaml"
      - "**/*.md"
      - "**/*.json"
      - ".repomix*"
    generates:
      - repomix-output.md
````

## File: .dockerignore
````
**/__pycache__
**/.classpath
**/.dockerignore
**/.DS_Store
**/.editorconfig
**/.env
**/.git
**/.github
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.venv
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.example
**/*.jfm
**/*.py#
**/*.py~
**/*.pyc
**/azds.yaml
**/bin
**/capture_groups.py
**/charts
**/compose*
**/csv
**/django
**/docker-compose*
**/Dockerfile*
**/heroku.yml
**/htmlcov
**/img
**/jsonwebtoken_test
**/justfile
**/jwt_priv.pem
**/jwt_pub.key
**/kubernetes.yml
**/meetup_queries.gql
**/node_modules
**/npm-debug.log
**/obj
**/pre-commit-config.yaml
**/Procfile
**/redis-data
**/redis-insight
**/redis.conf*
**/runtime.txt
**/scratch.*
**/secrets.dev.yaml
**/terraform
**/values.dev.yaml
````

## File: .pre-commit-config.yaml
````yaml
fail_fast: true

repos:

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.30.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.3
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=1024']
      - id: check-executables-have-shebangs
        files: \.(py|sh)$
      - id: check-merge-conflict
      - id: check-shebang-scripts-are-executable
        files: \.(py|sh)$
      - id: check-symlinks
      - id: debug-statements
      - id: destroyed-symlinks
      - id: detect-private-key
      - id: end-of-file-fixer
        files: \.(py|sh)$
      - id: fix-byte-order-marker
      - id: mixed-line-ending
        files: \.(py|sh)$
      - id: requirements-txt-fixer
        files: requirements.txt
      - id: check-toml
        files: \.toml$
      - id: check-yaml
        args: [--unsafe]
        files: \.(yaml|yml)$
      - id: pretty-format-json

        args: ['--autofix', '--indent=2', '--no-sort-keys']
        files: \.(json|jsonc)$
        exclude: |
            (?x)^(
                .devcontainer/devcontainer.json|
                .vscode/launch.json|
                .vscode/settings.json|
                .vscode/extensions.json|
            )$
````

## File: TODO.md
````markdown
# TODO

* Move exclusions to either
  * GraphQL
  * Filter by url (e.g., `https://www.meetup.com/project3810/events/308160679/`)
* Convert code base to golang
* Refactor authentication
  * Store auth in browser session vs. memory
* Scheduling
  * Couple scheduling with locations (e.g., Norman vs. OKC)
* Norman events
  * Get Norman events from existing GraphQL API
    * Coded as `Oklahoma City`
    * Will need to modify the query to get title and body content
  * Post to `#norman`
    * M-F

## Stretch Goals

* Indicate online vs. in-person
* Time Frame 
  * 2 hours before
* Slash commands to manually call:
  * Next `n` events
  * This week's events
  * Create new events
````

## File: app/meetup_query.py
````python
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"
⋮----
home: Path = Path.home()
cwd: Path = Path.cwd()
script_dir: Path = Path(__file__).resolve().parents[0]
format = 'json'
cache_fn = config('CACHE_FN', default='raw/meetup_query')
csv_fn = config('CSV_FN', default='raw/output.csv')
json_fn = config('JSON_FN', default='raw/output.json')
days = config('DAYS', default=7, cast=int)
tz = config('TZ', default='America/Chicago')
⋮----
groups_csv = script_dir / "groups.csv"
⋮----
groups_csv = cwd / "groups.csv"
⋮----
# time span (e.g., 3600 = 1 hour)
sec = 60  # n seconds
ttl = int(sec * 30)  # n minutes -> hours
⋮----
# cache the requests as script basename, expire after n time
⋮----
# read groups from file via pandas
csv = pd.read_csv(groups_csv, header=0)
⋮----
# remove `techlahoma-foundation` row
sans_tf = csv[csv['urlname'] != 'techlahoma-foundation']
⋮----
# remove url column
groups = sans_tf.drop(columns=['url'])
⋮----
# read groups `_values`
groups_array = groups['urlname']._values
⋮----
# assign to `url_vars` as a list
url_vars = [group for group in groups_array]
⋮----
# Techlahoma: search all affiliate groups for upcoming events (node doesn't expose name of affiliate group)
query = """
# shorthand for proNetwork id (unused in `self` query, but required in headers)
vars = '{ "id": "364335959210266624" }'
⋮----
# unaffiliated groups
url_query = """
⋮----
def send_request(token, query, vars) -> str
⋮----
"""
    Request

    POST https://api.meetup.com/gql-ext
    """
⋮----
endpoint = 'https://api.meetup.com/gql-ext'
⋮----
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
⋮----
variables = json.loads(vars)
⋮----
variables = vars
⋮----
r = requests.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
⋮----
# pretty prints json response content but skips sorting keys as it rearranges graphql response
pretty_response = json.dumps(r.json(), indent=2, sort_keys=False)
⋮----
# formatted response
# print('Response HTTP Response Body:\n{content}'.format(content=pretty_response))
⋮----
# optional exclusion string parameter
def format_response(response, location: str = "Oklahoma City", exclusions: str = "")
⋮----
"""
    Format response for Slack
    """
⋮----
# create dataframe columns
df = pd.DataFrame(columns=['name', 'date', 'title', 'description', 'city', 'eventUrl'])
⋮----
# convert response to json
response_json = json.loads(response)
⋮----
# TODO: add arg for `self` or `groupByUrlname`
# extract data from json
data = None
⋮----
# Check if response has expected structure
⋮----
data = ""
⋮----
data = response_json['data']['self']['memberEvents']['edges']
⋮----
data = response_json['data']['groupByUrlname']['events']['edges']
⋮----
# append data to rows
⋮----
# filter rows by city
df = df[df['city'] == location]
⋮----
# TODO: control for mislabeled event locations (e.g. 'Techlahoma Foundation')
# TODO: exclude by `urlname` instead of `name`
# * data[0]['node']['group']['urlname'] == 'nerdygirlsokc'
# filtered rows to exclude keywords by regex OR operator
⋮----
df = df[~df['name'].str.contains('|'.join(exclusions))]
df = df[~df['title'].str.contains('|'.join(exclusions))]
⋮----
# TODO: cutoff time by day _and_ hour (currently only day)
# filter rows that aren't within the next n days
time_span = arrow.now(tz=tz).shift(days=days)
df = df[df['date'] <= time_span.isoformat()]
⋮----
# TODO: QA
def sort_csv(filename) -> None
⋮----
"""
    Sort CSV by date
    """
⋮----
# read csv
df = pd.read_csv(filename, header=0)
⋮----
# drop duplicates by event url
df = df.drop_duplicates(subset='eventUrl')
⋮----
# sort by date
⋮----
df = df.sort_values(by=['date'])
⋮----
# convert date to human readable format (Thu 5/26 at 11:30 am)
⋮----
# write csv
⋮----
def sort_json(filename) -> None
⋮----
"""
    Sort JSON keys
    """
# Check if file exists and has content
⋮----
df = pd.read_json(filename, orient='records')
⋮----
dates = df['date'].to_dict()
⋮----
df = df[df['date'] >= arrow.now(tz).format('YYYY-MM-DDTHH:mm:ss')]
df = df.reset_index(drop=True)
⋮----
data = json.loads(df.to_json(orient='records', force_ascii=False))
⋮----
def export_to_file(response, type: str = 'json', exclusions: str = '') -> None
⋮----
"""
    Export to CSV or JSON
    """
⋮----
df = format_response(response, exclusions=exclusions)
⋮----
df = format_response(response)
⋮----
# If DataFrame is empty, return early
⋮----
# Create directory if it doesn't exist
⋮----
data_json = json.load(f)
⋮----
def main()
⋮----
tokens = gen_token()
⋮----
access_token = tokens.get('access_token')
⋮----
exclusions = ['36\u00b0N', 'Tulsa', 'Nerdy Girls', 'Bitcoin']
⋮----
response = send_request(access_token, query, vars)
⋮----
output = []
⋮----
response = send_request(access_token, url_query, f'{{"urlname": "{url}"}}')
# append to output dict if the response is not empty
````

## File: .tool-versions
````
deno   2.5.1
nodejs 24.5.0
prek   0.3.2
python 3.11.13
ruby   3.4.5
ruff   0.12.11
uv     0.8.8
````

## File: .github/workflows/pytest.yml
````yaml
name: Run pytest

on:












  workflow_dispatch:

env:
  REGISTRY_URL: ${{ vars.REGISTRY_URL }}
  REGISTRY_USER: ${{ github.repository_owner }}
  IMAGE: ${{ vars.IMAGE }}
  ALGORITHM: ${{ vars.ALGORITHM }}
  BOT_USER_TOKEN: ${{ secrets.BOT_USER_TOKEN }}
  CHANNEL: ${{ vars.CHANNEL }}
  CLIENT_ID: ${{ secrets.CLIENT_ID }}
  CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
  CSV_FN: ${{ vars.CSV_FN }}
  DAYS: ${{ vars.DAYS }}
  DB_HOST: ${{ secrets.DB_HOST }}
  DB_NAME: ${{ secrets.DB_NAME }}
  DB_PASS: ${{ secrets.DB_PASS }}
  DB_PORT: ${{ vars.DB_PORT }}
  DB_USER: ${{ secrets.DB_USER }}
  JSON_FN: ${{ vars.JSON_FN }}
  PORT: ${{ vars.PORT }}
  PRIV_KEY_B64: ${{ secrets.PRIV_KEY_B64 }}
  PUB_KEY_B64: ${{ secrets.PUB_KEY_B64 }}
  REDIRECT_URI: ${{ vars.REDIRECT_URI }}
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
  SELF_ID: ${{ secrets.SELF_ID }}
  SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
  SIGNING_KEY_ID: ${{ secrets.SIGNING_KEY_ID }}
  SIGNING_SECRET: ${{ secrets.SIGNING_SECRET }}
  TOKEN_URL: ${{ vars.TOKEN_URL }}
  TZ: ${{ vars.TZ }}
  USER_TOKEN: ${{ secrets.USER_TOKEN }}

jobs:
  test:
    runs-on: ubuntu-latest


    services:
      server:
        image: ghcr.io/pythoninthegrass/meetup_bot:latest
        ports:
          - 3000:3000
        env:
          ALGORITHM: ${{ env.ALGORITHM }}
          BOT_USER_TOKEN: ${{ env.BOT_USER_TOKEN }}
          CHANNEL: ${{ env.CHANNEL }}
          CLIENT_ID: ${{ env.CLIENT_ID }}
          CLIENT_SECRET: ${{ env.CLIENT_SECRET }}
          CSV_FN: ${{ env.CSV_FN }}
          DAYS: ${{ env.DAYS }}
          DB_HOST: ${{ env.DB_HOST }}
          DB_NAME: ${{ env.DB_NAME }}
          DB_PASS: ${{ env.DB_PASS }}
          DB_PORT: ${{ env.DB_PORT }}
          DB_USER: ${{ env.DB_USER }}
          JSON_FN: ${{ env.JSON_FN }}
          PORT: ${{ env.PORT }}
          PRIV_KEY_B64: ${{ env.PRIV_KEY_B64 }}
          PUB_KEY_B64: ${{ env.PUB_KEY_B64 }}
          REDIRECT_URI: ${{ env.REDIRECT_URI }}
          SECRET_KEY: ${{ env.SECRET_KEY }}
          SELF_ID: ${{ env.SELF_ID }}
          SIGNING_KEY_ID: ${{ env.SIGNING_KEY_ID }}
          SIGNING_SECRET: ${{ env.SIGNING_SECRET }}
          SLACK_WEBHOOK: ${{ env.SLACK_WEBHOOK }}
          TOKEN_URL: ${{ env.TOKEN_URL }}
          TZ: ${{ env.TZ }}
          USER_TOKEN: ${{ env.USER_TOKEN }}

    container:
      image: ghcr.io/pythoninthegrass/meetup_bot:test

    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true

    steps:
    - uses: actions/checkout@v4

    - name: Run pytest
      run: pytest -s
      env:
        URL: http://server:3000
````

## File: docker-compose.yml
````yaml
services:
  meetup-bot:

    image: ghcr.io/pythoninthegrass/meetup-bot
    build:
      context: .
      dockerfile: Dockerfile.web
    platform: ${PLATFORM:-linux/amd64}
    tty: false
    stdin_open: false
    env_file:
      - .env
    volumes:
      - ./app:/app
    ports:
      - ${PORT:-3100}:3100
    networks:
      - default

networks:
  default:
    driver: bridge
````

## File: README.md
````markdown
<img alt="gitleaks badge" src="https://img.shields.io/badge/protected%20by-gitleaks-blue">

# meetup_bot

**Table of Contents**

* [meetup\_bot](#meetup_bot)
  * [Summary](#summary)
  * [Minimum Requirements](#minimum-requirements)
  * [Recommended Requirements](#recommended-requirements)
  * [Quickstart](#quickstart)
    * [Python only](#python-only)
    * [Shell wrapper](#shell-wrapper)
    * [Devbox](#devbox)
    * [Docker](#docker)
    * [Docker Compose](#docker-compose)
  * [Contributors](#contributors)
  * [Further Reading](#further-reading)

## Summary

Use Meetup Pro API to send Slack messages before events occur.

## Minimum Requirements

* [Python 3.11+](https://www.python.org/downloads/)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* [Create a Meetup API key](https://secure.meetup.com/meetup_api/key/)
* Slack
  * [Create a Slack app](https://api.slack.com/apps)
  * [Create a Slack bot](https://api.slack.com/bot-users)

## Recommended Requirements

* [Devbox](https://www.jetpack.io/devbox/docs/quickstart/)
* [Docker](https://www.docker.com/products/docker-desktop)

## Quickstart

* Clone repo
* Copy `.env.example` to `.env` and fill out environment variables

### Python only

```bash
python -m venv .venv
source .venv/bin/activate

cd ./app

# run individual app
python <sign_jwt|meetup_query|slackbot|main>.py

# run only main app
python main.py
```

### Shell wrapper

```bash
cd ./app

# standalone server w/hard-coded port (default: 3000)
./startup.sh

# standalone server w/port argument
./startup.sh 3000

# server used with scheduled job (e.g., cron job)
./scheduler.sh
```

### Devbox

I.e., [Nix Package Manager](https://search.nixos.org/packages)
```bash
# enter dev environment
devbox shell

# run individual app
python <sign_jwt|meetup_query|slackbot|main>.py

# exit dev environment
exit

# run standalone server
devbox run start

# run tests
devbox run test
```

### Docker

```bash
cd ./app

# build image
docker build -f Dockerfile.web --progress=plain -t meetup_bot:latest .

# run image
docker run --name meetup_bot -it --rm --env-file .env -p 3000:3000 meetup_bot bash
```

### Docker Compose

```bash
cd ./app

# build image
docker-compose build --remove-orphans

# run image
docker-compose up -d

# enter server container
docker exec -it meetup_bot-cont bash

# exit server container
exit

# stop image
docker-compose stop

# remove image
docker-compose down --volumes
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alex-code4okc"><img src="https://avatars.githubusercontent.com/u/17677369?v=4?s=50" width="50px;" alt="Alex Ayon"/><br /><sub><b>Alex Ayon</b></sub></a><br /><a href="https://github.com/pythoninthegrass/meetup_bot/commits?author=alex-code4okc" title="Code">💻</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Further Reading

[API Doc Authentication | Meetup](https://www.meetup.com/api/authentication/#p04-jwt-flow-section)

[How to Handle JWTs in Python](https://auth0.com/blog/how-to-handle-jwt-in-python/)

[Building a Basic Authorization Server using Authorization Code Flow (PKCE) | by Ratros Y. | Medium](https://medium.com/@ratrosy/building-a-basic-authorization-server-using-authorization-code-flow-pkce-3155e843466)

[How to cancel a Heroku build | remarkablemark](https://remarkablemark.org/blog/2021/05/05/heroku-cancel-build/)

[OAuth2 with Password (and hashing), Bearer with JWT tokens - FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

[Python bcrypt - hashing passwords in Python with bcrypt](https://zetcode.com/python/bcrypt/)

[MushroomMaula/fastapi_login](https://github.com/MushroomMaula/fastapi_login)

[FastAPI Auth + Login Page](https://dev.to/athulcajay/fastapi-auth-login-page-48po)

[checkbashisms](https://command-not-found.com/checkbashisms)

[Building Docker images in Kubernetes | Snyk](https://snyk.io/blog/building-docker-images-kubernetes/)

[Kaniko, How to Build Container Image with SSH | by Yossi Cohn | HiredScore Engineering | Medium](https://medium.com/hiredscore-engineering/kaniko-builds-with-private-repository-634d5e7fa4a5)
````

## File: .github/workflows/docker.yml
````yaml
name: Publish Docker image

on:
  push:
    branches:
      - 'main'
      - 'master'
    tags:
      - '*.*.*'
    paths:
      - 'Dockerfile'
      - 'pyproject.toml'
      - 'poetry.lock'
      - 'requirements.txt'
      - '**/*.py'
      - '**/*.sh'
      - '**/*.js'
      - '**/*.css'
      - '.dockerignore'
      - '.env.example'
      - '.github/workflows/**'
      - 'static/**'





env:
  REGISTRY_URL: ghcr.io
  REGISTRY_USER: ${{ github.repository_owner }}
  IMAGE: ${{ vars.IMAGE }}

jobs:
  push_to_registry:
    name: Push Docker image to container registry



    runs-on: ubuntu-latest
    strategy:
      matrix:
        dockerfile: [Dockerfile.web]
    concurrency:
      group: ${{ github.workflow }}-${{ github.event.workflow_run.head_branch || github.ref }}
      cancel-in-progress: true
    permissions:
      packages: write
      contents: read
    steps:
      - name: Check out the repo
        uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY_URL }}
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            name=${{ env.REGISTRY_URL }}/${{ env.REGISTRY_USER }}/${{ env.IMAGE }}
          tags: |
            type=raw,value=latest,enable=${{ endsWith(github.ref, 'main') }}
            type=ref,event=branch,enable=${{ !endsWith(github.ref, 'main') }}
            type=semver,pattern={{version}}
          flavor: |
            latest=false

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ${{ matrix.dockerfile }}
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64/v8
          cache-from: type=gha
          cache-to: type=gha,mode=max
````

## File: Dockerfile.web
````
# syntax=docker/dockerfile:1.7.0

# full semver just for python base image
ARG PYTHON_VERSION=3.11.11

FROM python:${PYTHON_VERSION}-slim-bookworm as builder

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt-get -qq update \
    && apt-get -qq install \
    --no-install-recommends -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# pip env vars
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# venv
ARG UV_PROJECT_ENVIRONMENT="/opt/venv"
ENV VENV="${UV_PROJECT_ENVIRONMENT}"
ENV PATH="$VENV/bin:$PATH"

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./app .
COPY ./README.md .
COPY pyproject.toml .

RUN uv venv $UV_PROJECT_ENVIRONMENT \
    && uv pip install -r pyproject.toml

FROM python:${PYTHON_VERSION}-slim-bookworm as runner

# set timezone
ENV TZ=${TZ:-"America/Chicago"}
RUN ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime && echo "$TZ" > /etc/timezone

# setup standard non-root user for use downstream
ENV USER_NAME=appuser
ARG VENV="/opt/venv"
ENV PATH=$VENV/bin:$HOME/.local/bin:$PATH

# standardise on locale, don't generate .pyc, enable tracebacks on seg faults
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# workers per core
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/blob/master/README.md#web_concurrency
ENV WEB_CONCURRENCY=2

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt-get -qq update \
    && apt-get -qq install \
    --no-install-recommends -y \
    curl \
    lsof \
    && rm -rf /var/lib/apt/lists/*

# add non-root user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    ${USER_NAME}

USER ${USER_NAME}

WORKDIR /app

COPY --chown=${USER_NAME} ./app .
COPY --from=builder --chown=${USER_NAME} "$VENV" "$VENV"

ARG PORT=${PORT:-3100}
EXPOSE $PORT

CMD ["/bin/sh", "startup.sh"]

LABEL org.opencontainers.image.title="meetup_bot"
LABEL org.opencontainers.image.version="latest"
````

## File: app/main.py
````python
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"
⋮----
home = Path.home()
cwd = Path.cwd()
csv_fn = config("CSV_FN", default="raw/output.csv")
json_fn = config("JSON_FN", default="raw/output.json")
tz = config("TZ", default="America/Chicago")
bypass_schedule = config("OVERRIDE", default=False, cast=bool)
⋮----
current_time_local = arrow.now(tz)
current_time_utc = arrow.utcnow()
current_day = current_time_local.format("dddd")
⋮----
templates = Jinja2Templates(directory=Path("resources/templates"))
⋮----
TTL = config("TTL", default=3600, cast=int)
HOST = config("HOST")
PORT = config("PORT", default=3000, cast=int)
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
TOKEN_EXPIRE = config("TOKEN_EXPIRE", default=30, cast=int)
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", default=5432, cast=int)
⋮----
class IPConfig(BaseModel)
⋮----
whitelist: list[str] = ["localhost", "127.0.0.1"]
public_ips: list[str] = []
⋮----
ip_config = IPConfig()
⋮----
def is_ip_allowed(request: Request)
⋮----
client_host = request.client.host
⋮----
app = FastAPI(title="meetup_bot API", openapi_url="/meetup_bot.json")
⋮----
api_router = APIRouter(prefix="/api")
⋮----
origins = [
⋮----
db = Database()
⋮----
class UserInfo(db.Entity)
⋮----
username = Required(str, unique=True)
hashed_password = Required(str)
email = Optional(str)
⋮----
DB_PASS = DB_PASS.strip('"')
⋮----
class Token(BaseModel)
⋮----
access_token: str
token_type: str
⋮----
class TokenData(BaseModel)
⋮----
username: str | None = None
⋮----
class User(BaseModel)
⋮----
username: str
email: str | None = None
disabled: bool | None = None
⋮----
class UserInDB(User)
⋮----
hashed_password: str
⋮----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
⋮----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
⋮----
def verify_password(plain_password, hashed_password)
⋮----
def get_password_hash(password)
⋮----
def get_user(username: str)
⋮----
user = UserInfo.get(username=username)
⋮----
def authenticate_user(username: str, password: str)
⋮----
user = get_user(username)
⋮----
def create_access_token(data: dict, expires_delta: timedelta | None = None)
⋮----
to_encode = data.copy()
⋮----
expire = datetime.utcnow() + expires_delta
⋮----
expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
⋮----
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
⋮----
async def get_current_user(token: str = Depends(oauth2_scheme))
⋮----
credentials_exception = HTTPException(
⋮----
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
username: str = payload.get("sub")
⋮----
token_data = TokenData(username=username)
⋮----
user = get_user(username=token_data.username)
⋮----
async def get_current_active_user(current_user: User = Depends(get_current_user))
⋮----
async def ip_whitelist_or_auth(request: Request, current_user: User = Depends(get_current_active_user))
⋮----
def check_auth(auth: dict | User) -> None
⋮----
@app.post("/token", response_model=Token)
async def login_for_oauth_token(form_data: OAuth2PasswordRequestForm = Depends())
⋮----
user = authenticate_user(form_data.username, form_data.password)
⋮----
oauth_token_expires = timedelta(minutes=TOKEN_EXPIRE)
oauth_token = create_access_token(data={"sub": user.username}, expires_delta=oauth_token_expires)
⋮----
def load_user(username: str)
⋮----
@app.on_event("startup")
def startup_event()
⋮----
hashed_password = get_password_hash(DB_PASS)
⋮----
@app.get("/healthz", status_code=200)
def health_check()
⋮----
@app.get("/", response_class=HTMLResponse)
def index(request: Request)
⋮----
@app.post("/auth/login")
def login(request: Request, username: str = Form(...), password: str = Form(...))
⋮----
@api_router.get("/token")
def generate_token(current_user: User = Depends(get_current_active_user))
⋮----
tokens = gen_token()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]
⋮----
exclusion_list = [
⋮----
exclusions = exclusions.split(",")
exclusion_list = exclusion_list + exclusions
⋮----
response = send_request(access_token, query, vars)
⋮----
output = []
⋮----
response = send_request(access_token, url_query, f'{{"urlname": "{url}"}}')
# append to output dict if the response is not empty
⋮----
# loop through output and append to file
⋮----
# cleanup output file
⋮----
# check if file exists after sorting
⋮----
@api_router.get("/check-schedule")
def should_post_to_slack(auth: dict = Depends(ip_whitelist_or_auth), request: Request = None)
⋮----
schedule = get_schedule(current_day)
⋮----
schedule_time_local = (
⋮----
time_diff = abs((schedule_time_local - current_time_local).total_seconds() / 60)
time_diff_rounded = ceil(time_diff)
⋮----
should_post = time_diff_rounded <= 90
⋮----
msg = fmt_json(json_fn)
⋮----
channel_id = chan_dict[channel_name]
⋮----
# TODO: test IP whitelisting
⋮----
@api_router.get("/schedule")
def get_current_schedule(auth: dict | User = Depends(ip_whitelist_or_auth))
⋮----
schedules = []
⋮----
schedule = get_schedule(day)
⋮----
def main()
````

## File: pyproject.toml
````toml
[project]
name = "meetup_bot"
version = "1.1.2"
description = "Use Meetup Pro API to send Slack messages before events occur."
authors = [
    { name = "pythoninthegrass", email = "4097471+pythoninthegrass@users.noreply.github.com" }
]
readme = "README.md"
license = "Unlicense"

requires-python = ">=3.11,<3.12"

dependencies = [
    "arrow>=1.3.0,<2",
    "bcrypt==4.0.1",
    "colorama>=0.4.5,<0.5",
    "exceptiongroup>=1.2.2,<2",
    "fastapi>=0.115.6",
    "gunicorn>=23.0.0,<24",
    "icecream>=2.1.3,<3",
    "Jinja2>=3.1.5,<4",
    "jose>=1.0.0,<2",
    "numpy>=2.2.1,<3",
    "pandas>=2.2.3,<3",
    "passlib[bcrypt]>=1.7.4,<2",
    "pony>=0.7.16,<0.8",
    "psycopg2-binary>=2.9.10,<3",
    "PyJWT[crypto]>=2.10.1,<3",
    "python-decouple~=3.8",
    "python-jose[cryptography]>=3.3.0,<4",
    "python-multipart>=0.0.9,<0.0.10",
    "requests>=2.32.3,<3",
    "requests-cache>=1.2.1,<2",
    "slack-sdk>=3.34.0,<4",
    "uvicorn>=0.29.0,<0.30",
    "wheel>=0.43.0,<0.44",
]

[project.optional-dependencies]
dev = [
    "argcomplete<4.0.0,>=3.5.0",
    "deptry<1.0.0,>=0.23.0",
    "icecream<3.0.0,>=2.1.3",
    "ipython<9.0.0,>=8.27.0",
    "mypy<2.0.0,>=1.14.1",
    "pyclean<4.0.0,>=3.0.0",
    "pytest-asyncio<1.0.0,>=0.25.2",
    "pytest-cov<7.0.0,>=6.0.0",
    "pytest<9.0.0,>=8.3.4",
    "rich<14.0.0,>=13.8.1",
    "ruff>=0.9.5",
]
test = [
    "coverage<8.0.0,>=7.6.1",
    "hypothesis[cli]<7.0.0,>=6.112.1",
    "pytest<9.0.0,>=8.3.3",
    "pytest-asyncio<1.0.0,>=0.24.0",
    "pytest-cov>=6.1.1",
    "pytest-datafiles<4.0.0,>=3.0.0",
    "pytest-xdist<4.0.0,>=3.6.1",
]

[tool.deptry]
# DEP003: transitive deps
ignore = [
    "DEP003"
]

[tool.deptry.per_rule_ignores]
# DEP002: not used in codebase (excluding dev deps)
DEP002 = [
    "deptry",
    "mypy",
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "uvicorn"
]
````