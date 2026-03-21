#!/usr/bin/env python3

import arrow
import httpx
import json
import os
import pandas as pd
import sys
from arrow import ParserError
from colorama import Fore
from decouple import config
from hishel import CacheOptions, SpecificationPolicy, SyncSqliteStorage
from hishel.httpx import SyncCacheClient
from icecream import ic
from pathlib import Path
from sign_jwt import main as gen_token

# verbose icecream
ic.configureOutput(includeContext=True)

# logging prefixes
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"

# pandas don't truncate output
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# env
home: Path = Path.home()
cwd: Path = Path.cwd()
script_dir: Path = Path(__file__).resolve().parents[0]
format = 'json'
cache_fn = config('CACHE_FN', default='raw/meetup_query')
csv_fn = config('CSV_FN', default='raw/output.csv')
json_fn = config('JSON_FN', default='raw/output.json')
days = config('DAYS', default=7, cast=int)
tz = config('TZ', default='America/Chicago')

groups_csv = script_dir / "groups.csv"
if not groups_csv.exists():
    groups_csv = cwd / "groups.csv"
    if not groups_csv.exists():
        raise FileNotFoundError(f"groups.csv not found in {script_dir} or {cwd}")

# time span (e.g., 3600 = 1 hour)
sec = 60  # n seconds
ttl = int(sec * 30)  # n minutes -> hours

# hishel cache client with SQLite storage (absolute path, no monkey-patching)
cache_db_path = script_dir / cache_fn
cache_db_path.parent.mkdir(parents=True, exist_ok=True)
_storage = SyncSqliteStorage(
    database_path=str(cache_db_path),
    default_ttl=float(ttl),
)
http_client = SyncCacheClient(
    storage=_storage,
    policy=SpecificationPolicy(
        cache_options=CacheOptions(
            shared=False,
            supported_methods=["GET", "HEAD", "POST"],
            allow_stale=False,
        )
    ),
)

# read groups from file via pandas
csv = pd.read_csv(groups_csv, header=0)

# remove `techlahoma-foundation` row
sans_tf = csv[csv['urlname'] != 'techlahoma-foundation']

# remove url column
groups = sans_tf.drop(columns=['url'])

# read groups `_values`
groups_array = groups['urlname']._values

# assign to `url_vars` as a list
url_vars = [group for group in groups_array]

# Techlahoma: search all affiliate groups for upcoming events (node doesn't expose name of affiliate group)
query = """
query {
    self {
        id
        name
        username
        memberUrl
        memberEvents(first: 10) {
            totalCount
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
"""
# shorthand for proNetwork id (unused in `self` query, but required in headers)
vars = '{ "id": "364335959210266624" }'

# unaffiliated groups
url_query = """
query($urlname: String!) {
    groupByUrlname(urlname: $urlname) {
        id
        description
        name
        urlname
        city
        link
        events(first: 10) {
            totalCount
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
"""


group_fields = """\
        id
        description
        name
        urlname
        city
        link
        events(first: 10) {
            totalCount
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
        }"""


def build_batched_group_query(urlnames: list[str]) -> str:
    """Build a single GraphQL query with aliases for multiple groups."""
    if not urlnames:
        return ""
    aliases = []
    for i, urlname in enumerate(urlnames):
        aliases.append(f'    group_{i}: groupByUrlname(urlname: "{urlname}") {{\n{group_fields}\n    }}')
    return "query {\n" + "\n".join(aliases) + "\n}"


def send_batched_group_request(token: str, urlnames: list[str]) -> list[str]:
    """Send a batched GraphQL query and return individual response strings.

    Each returned string is a JSON object matching the format expected by
    format_response: {"data": {"groupByUrlname": ...}}
    """
    if not urlnames:
        return []

    batched_query = build_batched_group_query(urlnames)
    endpoint = 'https://api.meetup.com/gql-ext'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}

    try:
        r = http_client.post(endpoint, json={'query': batched_query}, headers=headers)
        print(f"{Fore.GREEN}{info:<10}{Fore.RESET}Batched response HTTP: {r.status_code} ({len(urlnames)} groups)")
        response_data = r.json()
    except httpx.HTTPError as e:
        print(f'HTTP Request failed:\n{e}')
        sys.exit(1)

    if 'errors' in response_data:
        for err in response_data['errors']:
            print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}GraphQL error: {err.get('message', err)}")

    data = response_data.get('data', {})
    results = []
    for i in range(len(urlnames)):
        alias = f'group_{i}'
        group_data = data.get(alias)
        individual = json.dumps({"data": {"groupByUrlname": group_data}}, indent=2, sort_keys=False)
        results.append(individual)

    return results


def send_request(token, query, vars) -> str:
    """
    Request

    POST https://api.meetup.com/gql-ext
    """

    endpoint = 'https://api.meetup.com/gql-ext'

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}

    try:
        variables = json.loads(vars) if isinstance(vars, str) else vars

        r = http_client.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
        print(f"{Fore.GREEN}{info:<10}{Fore.RESET}Response HTTP Response Body: {r.status_code}")

        # pretty prints json response content but skips sorting keys as it rearranges graphql response
        pretty_response = json.dumps(r.json(), indent=2, sort_keys=False)
    except httpx.HTTPError as e:
        print(f'HTTP Request failed:\n{e}')
        sys.exit(1)

    return pretty_response


# optional exclusion string parameter
def format_response(response, location: str = "Oklahoma City", exclusions: str = ""):
    """
    Format response for Slack
    """

    # create dataframe columns
    df = pd.DataFrame(columns=['name', 'date', 'title', 'description', 'city', 'eventUrl'])

    # convert response to json
    response_json = json.loads(response)

    # TODO: add arg for `self` or `groupByUrlname`
    # extract data from json
    data = None

    # Check if response has expected structure
    if 'data' not in response_json:
        print(
            f"{Fore.RED}{error:<10}{Fore.RESET}GraphQL response missing 'data' key. Response: {json.dumps(response_json, indent=2)[:500]}"
        )
        data = ""
    else:
        try:
            data = response_json['data']['self']['memberEvents']['edges']
            if data and len(data) > 0 and data[0]['node']['group']['city'] != location:
                print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}Skipping event outside of {location}")
        except KeyError:
            try:
                if response_json['data'].get('groupByUrlname') is None:
                    data = ""
                    print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}Skipping group due to empty response")
                else:
                    data = response_json['data']['groupByUrlname']['events']['edges']
                    if response_json['data']['groupByUrlname']['city'] != location:
                        print(f"{Fore.RED}{error:<10}{Fore.RESET}No data for {location} found")
            except KeyError as e:
                print(f"{Fore.RED}{error:<10}{Fore.RESET}KeyError accessing GraphQL data: {e}")
                print(f"{Fore.RED}{error:<10}{Fore.RESET}Response structure: {json.dumps(response_json, indent=2)[:500]}")
                data = ""

    # append data to rows
    if data:
        for i in range(len(data)):
            df.loc[i, 'name'] = data[i]['node']['group']['name']
            df.loc[i, 'date'] = data[i]['node']['dateTime']
            df.loc[i, 'title'] = data[i]['node']['title']
            df.loc[i, 'description'] = data[i]['node']['description']
            df.loc[i, 'city'] = data[i]['node']['group']['city']
            df.loc[i, 'eventUrl'] = data[i]['node']['eventUrl']

    # filter rows by city
    df = df[df['city'] == location]

    # TODO: control for mislabeled event locations (e.g. 'Techlahoma Foundation')
    # TODO: exclude by `urlname` instead of `name`
    # * data[0]['node']['group']['urlname'] == 'nerdygirlsokc'
    # filtered rows to exclude keywords by regex OR operator
    if exclusions:
        print(f"{Fore.GREEN}{info:<10}{Fore.RESET}Excluded keywords: {exclusions}".format(exclusions=exclusions))
        df = df[~df['name'].str.contains('|'.join(exclusions))]
        df = df[~df['title'].str.contains('|'.join(exclusions))]

    # TODO: cutoff time by day _and_ hour (currently only day)
    # filter rows that aren't within the next n days
    time_span = arrow.now(tz=tz).shift(days=days)
    df = df[df['date'] <= time_span.isoformat()]

    return df


# TODO: QA
def sort_csv(filename) -> None:
    """
    Sort CSV by date
    """

    # read csv
    df = pd.read_csv(filename, header=0)

    # drop duplicates by event url
    df = df.drop_duplicates(subset='eventUrl')

    # sort by date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])

    # convert date to human readable format (Thu 5/26 at 11:30 am)
    df['date'] = df['date'].apply(lambda x: arrow.get(x).format('ddd M/D h:mm a'))

    # write csv
    df.to_csv(filename, index=False)


def sort_json(filename) -> None:
    """
    Sort JSON keys
    """
    # Check if file exists and has content
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}No events found to sort")
        return

    # pandas remove duplicate keys by eventUrl key
    df = pd.read_json(filename, orient='records')

    # Check if DataFrame is empty
    if df.empty:
        print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}No events found to sort")
        return

    df = df.drop_duplicates(subset='eventUrl')

    # replace '1-07-19 17:00:00' with current year '2022-07-19 17:00:00' via regex
    # * negative lookahead only matches first digit at the beginning of the line (e.g., 1/0001 vs. 2022)
    # date_regex = r'^1(?![\d])|^0001(?![\d])'

    # choose current year if 7 days from now is before EOY
    # if arrow.now().year == arrow.now().shift(days=7).year:
    #     year = str(arrow.now(TZ).year)
    # else:
    #     year = str(arrow.now(TZ).shift(days=7).year)

    # convert date column to iso8601, handling both raw strings and pre-parsed Timestamps
    dates = df['date'].to_dict()
    for key, value in dates.items():
        if isinstance(value, pd.Timestamp):
            dates[key] = value.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(value, str):
            try:
                parsed = arrow.get(value, 'ddd M/D h:mm a')
                if parsed.year == 1:
                    parsed = parsed.replace(year=arrow.now(tz).year)
                dates[key] = parsed.format('YYYY-MM-DDTHH:mm:ss')
            except ParserError:
                try:
                    dates[key] = arrow.get(value).format('YYYY-MM-DDTHH:mm:ss')
                except ParserError:
                    print(f"{Fore.RED}{error:<10}{Fore.RESET}Unparseable date: {value!r}")
                    dates[key] = None
        else:
            print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}Unexpected date type {type(value).__name__}: {value!r}")
            dates[key] = None
    df['date'] = pd.Series(dates)

    # control for timestamp edge case `1-07-21 18:00:00` || `1-01-25 10:00:00` raising OutOfBoundsError
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')

    # convert datetimeindex to datetime
    df['date'] = df['date'].dt.tz_localize(None)

    # replace NaT with epoch time to avoid float TypeError
    df['date'] = df['date'].apply(lambda x: x.replace(year=1970, month=1, day=1) if pd.isnull(x) else x)

    # sort by date
    df = df.sort_values(by=['date'])

    # drop events by date when they are older than the current time
    df = df[df['date'] >= arrow.now(tz).format('YYYY-MM-DDTHH:mm:ss')]
    df = df.reset_index(drop=True)

    # convert date to human readable format (Thu 5/26 at 11:30 am)
    df['date'] = df['date'].apply(lambda x: arrow.get(x).format('ddd M/D h:mm a'))

    # export to json (convert escaped unicode to utf-8 encoding first)
    data = json.loads(df.to_json(orient='records', force_ascii=False))
    with open(json_fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def prepare_events(df) -> list[dict]:
    """Deduplicate, sort, filter past events, and format dates on a DataFrame. Returns list of dicts."""
    if df.empty:
        return []

    df = df.drop_duplicates(subset='eventUrl').copy()

    dates = df['date'].to_dict()
    for key, value in dates.items():
        if isinstance(value, pd.Timestamp):
            dates[key] = value.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(value, str):
            try:
                parsed = arrow.get(value, 'ddd M/D h:mm a')
                if parsed.year == 1:
                    parsed = parsed.replace(year=arrow.now(tz).year)
                dates[key] = parsed.format('YYYY-MM-DDTHH:mm:ss')
            except ParserError:
                try:
                    dates[key] = arrow.get(value).format('YYYY-MM-DDTHH:mm:ss')
                except ParserError:
                    print(f"{Fore.RED}{error:<10}{Fore.RESET}Unparseable date: {value!r}")
                    dates[key] = None
        else:
            print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}Unexpected date type {type(value).__name__}: {value!r}")
            dates[key] = None
    df['date'] = pd.Series(dates)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')
    df['date'] = df['date'].dt.tz_localize(None)
    df['date'] = df['date'].apply(lambda x: x.replace(year=1970, month=1, day=1) if pd.isnull(x) else x)

    df = df.sort_values(by=['date'])
    df = df[df['date'] >= arrow.now(tz).format('YYYY-MM-DDTHH:mm:ss')]
    df = df.reset_index(drop=True)

    df['date'] = df['date'].apply(lambda x: arrow.get(x).format('ddd M/D h:mm a'))

    return json.loads(df.to_json(orient='records', force_ascii=False))


def export_to_file(response, type: str = 'json', exclusions: str = '', df=None) -> None:
    """
    Export to CSV or JSON
    """
    if df is None:
        df = format_response(response, exclusions=exclusions) if exclusions != '' else format_response(response)

    # If DataFrame is empty, return early
    if df.empty:
        return

    # Create directory if it doesn't exist
    Path('raw').mkdir(parents=True, exist_ok=True)

    if type == 'csv':
        df.to_csv(Path(csv_fn), mode='a', header=False, index=False)
    elif type == 'json':
        # convert escaped unicode to utf-8 encoding
        data = json.loads(df.to_json(orient='records', force_ascii=False))

        # if file exists, is less than n minutes old, append to file
        if (
            Path(json_fn).exists()
            and (arrow.now() - arrow.get(os.path.getmtime(json_fn))).seconds < ttl
            and os.stat(json_fn).st_size > 0
        ):
            # append to json
            with open(json_fn) as f:
                data_json = json.load(f)
                data_json.extend(data)
                with open(json_fn, 'w', encoding='utf-8') as f:
                    json.dump(data_json, f, indent=2)
        else:
            # create/overwrite json
            with open(json_fn, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
    else:
        print('Invalid export file type')


# TODO: disable in prod (use `main.py`)
def main():
    tokens = gen_token()
    if not tokens:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to get access tokens")
        sys.exit(1)

    access_token = tokens.get('access_token')
    if not access_token:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}No access token in response")
        sys.exit(1)

    # exclude keywords in event name and title (will miss events with keyword in description)
    exclusions = ['36\u00b0N', 'Tulsa', 'Nerdy Girls', 'Bitcoin']

    # first-party query
    response = send_request(access_token, query, vars)
    # format_response(response, exclusions=exclusions)                      # don't need if exporting to file
    export_to_file(response, format, exclusions=exclusions)  # csv/json

    # third-party query (batched)
    responses = send_batched_group_request(access_token, url_vars)
    output = []
    for i, response in enumerate(responses):
        if len(format_response(response, exclusions=exclusions)) > 0:
            output.append(response)
        else:
            print(f'{Fore.GREEN}{info:<10}{Fore.RESET}No upcoming events for {url_vars[i]} found')
    for resp in output:
        export_to_file(resp, format)

    # cleanup output file
    if format == 'csv':
        sort_csv(csv_fn)
    elif format == 'json':
        sort_json(json_fn)

    return response


if __name__ == '__main__':
    main()
