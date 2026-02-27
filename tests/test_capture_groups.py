import pandas as pd
import pytest
from capture_groups import (
    TECHLAHOMA_PRO_NETWORK_ID,
    filter_groups,
    parse_search_response,
    write_groups_csv,
)
from pathlib import Path
from unittest.mock import MagicMock, patch

SAMPLE_RESPONSE = {
    "data": {
        "groupSearch": {
            "totalCount": 4,
            "pageInfo": {"endCursor": "cursor123", "hasNextPage": False},
            "edges": [
                {
                    "node": {
                        "id": "1",
                        "urlname": "pythonistas",
                        "name": "OKC Pythonistas",
                        "city": "Oklahoma City",
                        "proNetwork": None,
                    }
                },
                {
                    "node": {
                        "id": "2",
                        "urlname": "techlahoma-foundation",
                        "name": "Techlahoma Foundation",
                        "city": "Oklahoma City",
                        "proNetwork": {"id": "364335959210266624"},
                    }
                },
                {
                    "node": {
                        "id": "3",
                        "urlname": "okc-sharp",
                        "name": "OKC Sharp",
                        "city": "Oklahoma City",
                        "proNetwork": {"id": "364335959210266624"},
                    }
                },
                {
                    "node": {
                        "id": "4",
                        "urlname": "ok-golang",
                        "name": "OK Golang",
                        "city": "Oklahoma City",
                        "proNetwork": None,
                    }
                },
            ],
        }
    }
}


@pytest.mark.unit
class TestParseSearchResponse:
    def test_extracts_groups_from_response(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        assert len(groups) == 4
        assert groups[0]["urlname"] == "pythonistas"
        assert groups[1]["urlname"] == "techlahoma-foundation"

    def test_includes_pro_network_id(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        assert groups[0]["pro_network_id"] is None
        assert groups[1]["pro_network_id"] == TECHLAHOMA_PRO_NETWORK_ID

    def test_empty_response(self):
        response = {"data": {"groupSearch": {"totalCount": 0, "edges": []}}}
        groups = parse_search_response(response)
        assert groups == []

    def test_error_response(self):
        response = {"errors": [{"message": "bad query"}]}
        groups = parse_search_response(response)
        assert groups == []


@pytest.mark.unit
class TestFilterGroups:
    def test_filters_techlahoma_affiliated_groups(self):
        groups = parse_search_response(SAMPLE_RESPONSE)
        filtered = filter_groups(groups)
        urlnames = [g["urlname"] for g in filtered]
        assert "pythonistas" in urlnames
        assert "ok-golang" in urlnames
        assert "techlahoma-foundation" not in urlnames
        assert "okc-sharp" not in urlnames

    def test_keeps_all_when_no_pro_network(self):
        groups = [
            {"urlname": "group-a", "pro_network_id": None},
            {"urlname": "group-b", "pro_network_id": None},
        ]
        filtered = filter_groups(groups)
        assert len(filtered) == 2

    def test_custom_exclude_id(self):
        groups = [
            {"urlname": "group-a", "pro_network_id": "other-network"},
            {"urlname": "group-b", "pro_network_id": None},
        ]
        filtered = filter_groups(groups, exclude_pro_network="other-network")
        assert len(filtered) == 1
        assert filtered[0]["urlname"] == "group-b"


@pytest.mark.unit
class TestWriteGroupsCsv:
    def test_writes_csv_with_correct_format(self, tmp_path):
        groups = [
            {"urlname": "pythonistas", "pro_network_id": None},
            {"urlname": "ok-golang", "pro_network_id": None},
        ]
        output = tmp_path / "groups.csv"
        write_groups_csv(groups, str(output))

        df = pd.read_csv(output)
        assert list(df.columns) == ["url", "urlname"]
        assert df.iloc[0]["urlname"] == "ok-golang"
        assert df.iloc[0]["url"] == "https://www.meetup.com/ok-golang/"
        assert df.iloc[1]["urlname"] == "pythonistas"

    def test_sorts_by_urlname(self, tmp_path):
        groups = [
            {"urlname": "zebra-group", "pro_network_id": None},
            {"urlname": "alpha-group", "pro_network_id": None},
        ]
        output = tmp_path / "groups.csv"
        write_groups_csv(groups, str(output))

        df = pd.read_csv(output)
        assert list(df["urlname"]) == ["alpha-group", "zebra-group"]

    def test_empty_groups(self, tmp_path):
        output = tmp_path / "groups.csv"
        write_groups_csv([], str(output))

        df = pd.read_csv(output)
        assert list(df.columns) == ["url", "urlname"]
        assert len(df) == 0
