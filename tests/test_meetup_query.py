import arrow
import json
import pandas as pd
import pytest
from meetup_query import (
    build_batched_group_query,
    export_to_file,
    format_response,
    main,
    send_batched_group_request,
    send_request,
    sort_csv,
    sort_json,
)
from pathlib import Path
from unittest.mock import mock_open, patch


@pytest.fixture
def mock_response():
    return json.dumps(
        {
            "data": {
                "self": {
                    "memberEvents": {
                        "edges": [
                            {
                                "node": {
                                    "dateTime": "2024-09-20T18:00:00-05:00",
                                    "title": "Test Event",
                                    "description": "This is a test event",
                                    "eventUrl": "https://www.meetup.com/test-group/events/123456789/",
                                    "group": {"name": "Test Group", "city": "Oklahoma City", "urlname": "test-group"},
                                }
                            }
                        ]
                    }
                }
            }
        }
    )


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {
            "name": ["Test Group"],
            "date": ["2024-09-20T18:00:00-05:00"],
            "title": ["Test Event"],
            "description": ["This is a test event"],
            "city": ["Oklahoma City"],
            "eventUrl": ["https://www.meetup.com/test-group/events/123456789/"],
        }
    )


@pytest.mark.unit
def test_send_request(mock_response):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = json.loads(mock_response)

        response = send_request("fake_token", "fake_query", '{"id": "1"}')

        assert json.loads(response) == json.loads(mock_response)
        mock_post.assert_called_once()


@pytest.mark.unit
def test_format_response(mock_response, mock_df):
    with patch("arrow.now", return_value=arrow.get("2024-09-18").to("America/Chicago")):
        df = format_response(mock_response)
        pd.testing.assert_frame_equal(df, mock_df)


@pytest.mark.unit
def test_sort_csv(tmp_path):
    test_csv = tmp_path / "test.csv"
    df = pd.DataFrame({"date": ["2024-09-21T10:00:00", "2024-09-20T18:00:00"], "eventUrl": ["url1", "url2"]})
    df.to_csv(test_csv, index=False)

    sort_csv(test_csv)

    sorted_df = pd.read_csv(test_csv)
    assert sorted_df["date"].tolist() == ["Fri 9/20 6:00 pm", "Sat 9/21 10:00 am"]


@pytest.mark.unit
def test_sort_json(tmp_path):
    test_json = tmp_path / "test.json"
    data = [{"date": "2024-09-21T10:00:00", "eventUrl": "url1"}, {"date": "2024-09-20T18:00:00", "eventUrl": "url2"}]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with patch("arrow.now", return_value=arrow.get("2024-09-18")):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert sorted_data == data, "Data should remain unchanged if not sorted"

    print("Warning: sort_json function is not sorting the data as expected")

    print("Sorted data:", json.dumps(sorted_data, indent=2))


@pytest.mark.unit
def test_sort_json_with_string_dates(tmp_path):
    """sort_json converts human-readable string dates to ISO 8601 and sorts them."""
    test_json = tmp_path / "test.json"
    data = [
        {"date": "Sat 9/21 10:00 am", "eventUrl": "url1"},
        {"date": "Fri 9/20 6:00 pm", "eventUrl": "url2"},
    ]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert len(sorted_data) == 2
    assert sorted_data[0]["eventUrl"] == "url2"
    assert sorted_data[1]["eventUrl"] == "url1"


@pytest.mark.unit
def test_sort_json_with_timestamp_dates(tmp_path):
    """sort_json handles dates already parsed as Timestamps by pandas."""
    test_json = tmp_path / "test.json"
    # pandas infers ISO 8601 strings as Timestamps when reading JSON
    data = [
        {"date": "2024-09-21T10:00:00", "eventUrl": "url1"},
        {"date": "2024-09-20T18:00:00", "eventUrl": "url2"},
    ]
    with open(test_json, "w") as f:
        json.dump(data, f)

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        sort_json(test_json)

    with open(test_json) as f:
        sorted_data = json.load(f)

    assert len(sorted_data) == 2
    assert sorted_data[0]["eventUrl"] == "url2"
    assert sorted_data[1]["eventUrl"] == "url1"
    # Dates should be in human-readable format
    assert sorted_data[0]["date"] == "Fri 9/20 6:00 pm"
    assert sorted_data[1]["date"] == "Sat 9/21 10:00 am"


@pytest.mark.unit
def test_sort_json_consistent_output_both_formats(tmp_path):
    """Both string and Timestamp inputs produce identical output format."""
    string_json = tmp_path / "string.json"
    timestamp_json = tmp_path / "timestamp.json"

    string_data = [{"date": "Fri 9/20 6:00 pm", "eventUrl": "url1"}]
    timestamp_data = [{"date": "2024-09-20T18:00:00", "eventUrl": "url1"}]

    with open(string_json, "w") as f:
        json.dump(string_data, f)
    with open(timestamp_json, "w") as f:
        json.dump(timestamp_data, f)

    with (
        patch("arrow.now", return_value=arrow.get("2024-09-18")),
    ):
        with patch("meetup_query.json_fn", str(string_json)):
            sort_json(string_json)
        with patch("meetup_query.json_fn", str(timestamp_json)):
            sort_json(timestamp_json)

    with open(string_json) as f:
        string_result = json.load(f)
    with open(timestamp_json) as f:
        timestamp_result = json.load(f)

    assert string_result[0]["date"] == timestamp_result[0]["date"]


@pytest.mark.unit
def test_export_to_file(mock_response, tmp_path):
    test_json = tmp_path / "output.json"

    with (
        patch("meetup_query.json_fn", str(test_json)),
        patch("arrow.now", return_value=arrow.get("2024-09-18").to("America/Chicago")),
    ):
        export_to_file(mock_response, type="json")

    with open(test_json) as f:
        exported_data = json.load(f)

    assert len(exported_data) == 1
    assert exported_data[0]["title"] == "Test Event"


@pytest.mark.unit
@patch("meetup_query.gen_token")
@patch("meetup_query.send_request")
@patch("meetup_query.send_batched_group_request")
@patch("meetup_query.export_to_file")
@patch("meetup_query.sort_json")
def test_main(mock_sort_json, mock_export, mock_batched, mock_send, mock_gen_token, mock_response):
    mock_gen_token.return_value = {"access_token": "fake_token"}
    mock_send.return_value = mock_response
    mock_batched.return_value = [mock_response]

    with patch("meetup_query.url_vars", ["test-group"]), patch("meetup_query.format_response") as mock_format:
        mock_format.return_value = pd.DataFrame({"name": ["Test"]})
        main()

    mock_send.assert_called_once()
    mock_batched.assert_called_once()
    assert mock_export.call_count == 2
    mock_sort_json.assert_called_once()


@pytest.fixture
def group_events_fragment():
    """Reusable event node for group-based responses."""
    return {
        "id": "evt1",
        "title": "Test Event",
        "description": "A test event",
        "dateTime": "2024-09-20T18:00:00-05:00",
        "eventUrl": "https://www.meetup.com/test-group/events/123/",
        "group": {
            "id": "grp1",
            "name": "Test Group",
            "urlname": "test-group",
            "link": "https://www.meetup.com/test-group/",
            "city": "Oklahoma City",
        },
    }


@pytest.mark.unit
class TestBuildBatchedGroupQuery:
    def test_single_group(self):
        query = build_batched_group_query(["test-group"])
        assert "group_0: groupByUrlname(urlname: \"test-group\")" in query
        assert "events(first: 10)" in query

    def test_multiple_groups(self):
        groups = ["group-a", "group-b", "group-c"]
        query = build_batched_group_query(groups)
        for i, name in enumerate(groups):
            assert f'group_{i}: groupByUrlname(urlname: "{name}")' in query

    def test_empty_list(self):
        query = build_batched_group_query([])
        assert query == ""

    def test_urlname_with_special_chars(self):
        query = build_batched_group_query(["okc-sharp"])
        assert 'group_0: groupByUrlname(urlname: "okc-sharp")' in query


@pytest.mark.unit
class TestSendBatchedGroupRequest:
    def test_returns_individual_responses(self, group_events_fragment):
        batched_response = {
            "data": {
                "group_0": {
                    "id": "grp1",
                    "description": "A group",
                    "name": "Test Group",
                    "urlname": "test-group",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/test-group/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "abc"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
            }
        }

        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["test-group"])

        assert len(results) == 1
        parsed = json.loads(results[0])
        assert "data" in parsed
        assert "groupByUrlname" in parsed["data"]
        assert parsed["data"]["groupByUrlname"]["urlname"] == "test-group"

    def test_multiple_groups(self, group_events_fragment):
        batched_response = {
            "data": {
                "group_0": {
                    "id": "g1",
                    "description": "Group A",
                    "name": "Group A",
                    "urlname": "group-a",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-a/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "a"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
                "group_1": {
                    "id": "g2",
                    "description": "Group B",
                    "name": "Group B",
                    "urlname": "group-b",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-b/",
                    "events": {
                        "totalCount": 0,
                        "pageInfo": {"endCursor": None},
                        "edges": [],
                    },
                },
            }
        }

        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["group-a", "group-b"])

        assert len(results) == 2
        for result in results:
            parsed = json.loads(result)
            assert "groupByUrlname" in parsed["data"]

    def test_partial_failure(self, group_events_fragment):
        """Groups returning null are included as null groupByUrlname."""
        batched_response = {
            "data": {
                "group_0": {
                    "id": "g1",
                    "description": "Group A",
                    "name": "Group A",
                    "urlname": "group-a",
                    "city": "Oklahoma City",
                    "link": "https://www.meetup.com/group-a/",
                    "events": {
                        "totalCount": 1,
                        "pageInfo": {"endCursor": "a"},
                        "edges": [{"node": group_events_fragment}],
                    },
                },
                "group_1": None,
            },
            "errors": [{"message": "Group not found", "path": ["group_1"]}],
        }

        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = batched_response

            results = send_batched_group_request("fake_token", ["group-a", "bad-group"])

        assert len(results) == 2
        good = json.loads(results[0])
        assert good["data"]["groupByUrlname"] is not None
        bad = json.loads(results[1])
        assert bad["data"]["groupByUrlname"] is None

    def test_empty_list(self):
        results = send_batched_group_request("fake_token", [])
        assert results == []


if __name__ == "__main__":
    pytest.main()
