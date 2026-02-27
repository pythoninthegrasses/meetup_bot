#!/usr/bin/env python3

import json
import pandas as pd
import sys
from colorama import Fore
from pathlib import Path
from sign_jwt import main as gen_token

info = "INFO:"
error = "ERROR:"
warning = "WARNING:"

TECHLAHOMA_PRO_NETWORK_ID = "364335959210266624"
TECHNOLOGY_TOPIC_CATEGORY_ID = "546"
BASE_URL = "https://www.meetup.com"

SEARCH_QUERY = """
query ($query: String!, $topicCategoryId: ID) {
    groupSearch(
        filter: {query: $query, lat: 35.467560, lon: -97.516426, topicCategoryId: $topicCategoryId}
        first: 50
    ) {
        totalCount
        pageInfo {
            endCursor
            hasNextPage
        }
        edges {
            node {
                id
                name
                urlname
                city
                proNetwork {
                    id
                }
            }
        }
    }
}
"""

SEARCH_VARS = {"query": "programming", "topicCategoryId": TECHNOLOGY_TOPIC_CATEGORY_ID}


def parse_search_response(response: dict) -> list[dict]:
    """Extract group data from a groupSearch GraphQL response."""
    if "errors" in response:
        for err in response["errors"]:
            print(f"{Fore.YELLOW}{warning:<10}{Fore.RESET}GraphQL error: {err.get('message', err)}")
        return []

    edges = response.get("data", {}).get("groupSearch", {}).get("edges", [])
    groups = []
    for edge in edges:
        node = edge.get("node", {})
        urlname = node.get("urlname")
        if not urlname:
            continue
        pro_network = node.get("proNetwork")
        groups.append(
            {
                "urlname": urlname,
                "pro_network_id": pro_network["id"] if pro_network else None,
            }
        )
    return groups


def filter_groups(groups: list[dict], exclude_pro_network: str = TECHLAHOMA_PRO_NETWORK_ID) -> list[dict]:
    """Filter out groups affiliated with a pro network (default: Techlahoma Foundation)."""
    return [g for g in groups if g.get("pro_network_id") != exclude_pro_network]


def write_groups_csv(groups: list[dict], output_path: str = "groups.csv") -> None:
    """Write groups to CSV with url,urlname columns, sorted by urlname."""
    df = pd.DataFrame(groups)
    if df.empty:
        df = pd.DataFrame(columns=["url", "urlname"])
    else:
        df["url"] = df["urlname"].apply(lambda x: f"{BASE_URL}/{x}/")
        df = df[["url", "urlname"]].sort_values(by="urlname")
    df.to_csv(output_path, index=False)


def search_groups(token: str, query: str = SEARCH_QUERY, variables: dict = SEARCH_VARS) -> dict:
    """Send keywordSearch GraphQL request and return raw response."""
    from meetup_query import http_client

    endpoint = "https://api.meetup.com/gql-ext"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}

    try:
        r = http_client.post(endpoint, json={"query": query, "variables": variables}, headers=headers)
        print(f"{Fore.GREEN}{info:<10}{Fore.RESET}groupSearch HTTP: {r.status_code}")
        return r.json()
    except Exception as e:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}HTTP request failed: {e}")
        sys.exit(1)


def main():
    tokens = gen_token()
    if not tokens:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to get access tokens")
        sys.exit(1)

    access_token = tokens.get("access_token")
    if not access_token:
        print(f"{Fore.RED}{error:<10}{Fore.RESET}No access token in response")
        sys.exit(1)

    response = search_groups(access_token)
    groups = parse_search_response(response)
    groups = filter_groups(groups)

    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / "groups.csv"
    write_groups_csv(groups, str(output_path))

    print(f"{Fore.GREEN}{info:<10}{Fore.RESET}Wrote {len(groups)} groups to {output_path}")


if __name__ == "__main__":
    main()
