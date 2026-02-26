import arrow
import json
import jwt
import pandas as pd
import pytest
import tempfile
import time
from cryptography.hazmat.primitives.asymmetric import rsa
from hypothesis import HealthCheck, given, settings, strategies as st
from meetup_query import format_response, sort_csv, sort_json
from pathlib import Path
from unittest.mock import patch

settings.register_profile("ci", max_examples=200)
settings.register_profile("dev", max_examples=50)
settings.load_profile("dev")

# -- Strategies --

event_node = st.fixed_dictionaries(
    {
        "node": st.fixed_dictionaries(
            {
                "dateTime": st.from_regex(r"2024-09-[12][0-9]T[01][0-9]:00:00-05:00", fullmatch=True),
                "title": st.text(min_size=1, max_size=100),
                "description": st.text(max_size=200),
                "eventUrl": st.from_regex(r"https://www\.meetup\.com/[a-z\-]+/events/[0-9]+/", fullmatch=True),
                "group": st.fixed_dictionaries(
                    {
                        "name": st.text(min_size=1, max_size=50),
                        "city": st.just("Oklahoma City"),
                        "urlname": st.from_regex(r"[a-z\-]{3,20}", fullmatch=True),
                    }
                ),
            }
        )
    }
)

self_response = st.fixed_dictionaries(
    {
        "data": st.fixed_dictionaries(
            {
                "self": st.fixed_dictionaries(
                    {"memberEvents": st.fixed_dictionaries({"edges": st.lists(event_node, min_size=0, max_size=5)})}
                )
            }
        )
    }
)

group_response = st.fixed_dictionaries(
    {
        "data": st.fixed_dictionaries(
            {
                "groupByUrlname": st.fixed_dictionaries(
                    {
                        "city": st.just("Oklahoma City"),
                        "events": st.fixed_dictionaries({"edges": st.lists(event_node, min_size=0, max_size=5)}),
                    }
                )
            }
        )
    }
)

malformed_response = st.one_of(
    st.fixed_dictionaries({}),
    st.fixed_dictionaries({"data": st.fixed_dictionaries({})}),
    st.fixed_dictionaries({"data": st.fixed_dictionaries({"self": st.fixed_dictionaries({})})}),
    st.fixed_dictionaries({"errors": st.lists(st.fixed_dictionaries({"message": st.text(min_size=1, max_size=50)}))}),
)

iso_datetime = st.from_regex(
    r"2024-09-[12][0-9]T[01][0-9]:00:00",
    fullmatch=True,
)


# -- format_response property tests --


@pytest.mark.property
class TestFormatResponse:
    @given(response=self_response)
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_self_response_returns_dataframe(self, response):
        with patch("arrow.now", return_value=arrow.get("2024-09-01").to("America/Chicago")):
            df = format_response(json.dumps(response))
        assert isinstance(df, pd.DataFrame)
        expected_cols = {"name", "date", "title", "description", "city", "eventUrl"}
        assert expected_cols == set(df.columns)

    @given(response=self_response)
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_self_response_filters_by_location(self, response):
        with patch("arrow.now", return_value=arrow.get("2024-09-01").to("America/Chicago")):
            df = format_response(json.dumps(response), location="Oklahoma City")
        if not df.empty:
            assert (df["city"] == "Oklahoma City").all()

    @given(response=group_response)
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_group_response_returns_dataframe(self, response):
        with patch("arrow.now", return_value=arrow.get("2024-09-01").to("America/Chicago")):
            df = format_response(json.dumps(response))
        assert isinstance(df, pd.DataFrame)

    @given(response=malformed_response)
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_malformed_response_no_crash(self, response):
        with patch("arrow.now", return_value=arrow.get("2024-09-01").to("America/Chicago")):
            df = format_response(json.dumps(response))
        assert isinstance(df, pd.DataFrame)
        assert df.empty


# -- sort_csv property tests --


@pytest.mark.property
class TestSortCsv:
    @given(
        dates=st.lists(iso_datetime, min_size=2, max_size=10, unique=True),
        urls=st.lists(
            st.from_regex(r"https://meetup\.com/[a-z]+/events/[0-9]{4}/", fullmatch=True),
            min_size=2,
            max_size=10,
            unique=True,
        ),
    )
    def test_output_sorted_by_date(self, dates, urls):
        n = min(len(dates), len(urls))
        dates, urls = dates[:n], urls[:n]
        df = pd.DataFrame({"date": dates, "eventUrl": urls, "name": ["g"] * n})
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            csv_file = Path(f.name)
            df.to_csv(f, index=False)

        try:
            sort_csv(csv_file)
            result = pd.read_csv(csv_file)
            parsed = [arrow.get(d, "ddd M/D h:mm a") for d in result["date"]]
            assert parsed == sorted(parsed)
        finally:
            csv_file.unlink(missing_ok=True)

    @given(
        dates=st.lists(iso_datetime, min_size=2, max_size=6),
        urls=st.lists(
            st.from_regex(r"https://meetup\.com/[a-z]+/events/[0-9]{4}/", fullmatch=True),
            min_size=2,
            max_size=6,
        ),
    )
    def test_duplicates_removed(self, dates, urls):
        n = min(len(dates), len(urls))
        dates, urls = dates[:n], urls[:n]
        doubled_dates = dates + dates
        doubled_urls = urls + urls
        df = pd.DataFrame({"date": doubled_dates, "eventUrl": doubled_urls, "name": ["g"] * len(doubled_dates)})
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            csv_file = Path(f.name)
            df.to_csv(f, index=False)

        try:
            sort_csv(csv_file)
            result = pd.read_csv(csv_file)
            assert len(result) == len(set(urls))
        finally:
            csv_file.unlink(missing_ok=True)


# -- sort_json property tests --


@pytest.mark.property
class TestSortJson:
    @given(
        dates=st.lists(iso_datetime, min_size=2, max_size=10, unique=True),
        urls=st.lists(
            st.from_regex(r"https://meetup\.com/[a-z]+/events/[0-9]{4}/", fullmatch=True),
            min_size=2,
            max_size=10,
            unique=True,
        ),
    )
    def test_output_sorted_by_date(self, dates, urls):
        n = min(len(dates), len(urls))
        dates, urls = dates[:n], urls[:n]
        data = [{"date": d, "eventUrl": u, "name": "g"} for d, u in zip(dates, urls, strict=False)]
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            json_file = Path(f.name)
            json.dump(data, f)

        try:
            with (
                patch("arrow.now", return_value=arrow.get("2024-09-01")),
                patch("meetup_query.json_fn", str(json_file)),
            ):
                sort_json(json_file)

            with open(json_file) as f:
                result = json.load(f)

            if len(result) >= 2:
                parsed = [arrow.get(r["date"], "ddd M/D h:mm a") for r in result]
                assert parsed == sorted(parsed)
        finally:
            json_file.unlink(missing_ok=True)

    @given(
        dates=st.lists(iso_datetime, min_size=2, max_size=6),
        urls=st.lists(
            st.from_regex(r"https://meetup\.com/[a-z]+/events/[0-9]{4}/", fullmatch=True),
            min_size=2,
            max_size=6,
        ),
    )
    def test_duplicates_removed(self, dates, urls):
        n = min(len(dates), len(urls))
        dates, urls = dates[:n], urls[:n]
        data = [{"date": d, "eventUrl": u, "name": "g"} for d, u in zip(dates, urls, strict=False)]
        data = data + data
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            json_file = Path(f.name)
            json.dump(data, f)

        try:
            with (
                patch("arrow.now", return_value=arrow.get("2024-09-01")),
                patch("meetup_query.json_fn", str(json_file)),
            ):
                sort_json(json_file)

            with open(json_file) as f:
                result = json.load(f)

            assert len(result) <= len(set(urls))
        finally:
            json_file.unlink(missing_ok=True)


# -- JWT roundtrip property tests --


@pytest.fixture(scope="module")
def rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.mark.property
class TestJwtRoundtrip:
    @given(
        sub=st.from_regex(r"[0-9]{6,12}", fullmatch=True),
        iss=st.from_regex(r"[a-z0-9]{8,16}", fullmatch=True),
        lifespan=st.integers(min_value=60, max_value=3600),
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_encode_decode_roundtrip(self, sub, iss, lifespan, rsa_keypair):
        private_key, public_key = rsa_keypair
        aud = "api.meetup.com"
        payload = {
            "sub": sub,
            "iss": iss,
            "aud": aud,
            "exp": int(time.time()) + lifespan,
        }
        headers = {"kid": "test-key-id", "typ": "JWT", "alg": "RS256"}

        token = jwt.encode(headers=headers, payload=payload, key=private_key, algorithm="RS256")
        decoded = jwt.decode(jwt=token, key=public_key, issuer=iss, audience=aud, algorithms=["RS256"])

        assert decoded["sub"] == sub
        assert decoded["iss"] == iss
        assert decoded["aud"] == aud

    @given(
        sub=st.from_regex(r"[0-9]{6,12}", fullmatch=True),
        iss=st.from_regex(r"[a-z0-9]{8,16}", fullmatch=True),
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_expired_token_rejected(self, sub, iss, rsa_keypair):
        private_key, public_key = rsa_keypair
        aud = "api.meetup.com"
        payload = {
            "sub": sub,
            "iss": iss,
            "aud": aud,
            "exp": int(time.time()) - 10,
        }

        token = jwt.encode(payload=payload, key=private_key, algorithm="RS256")

        with pytest.raises(jwt.exceptions.ExpiredSignatureError):
            jwt.decode(jwt=token, key=public_key, issuer=iss, audience=aud, algorithms=["RS256"])

    @given(
        sub=st.from_regex(r"[0-9]{6,12}", fullmatch=True),
        iss=st.from_regex(r"[a-z0-9]{8,16}", fullmatch=True),
        wrong_iss=st.from_regex(r"[a-z0-9]{8,16}", fullmatch=True),
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_wrong_issuer_rejected(self, sub, iss, wrong_iss, rsa_keypair):
        if iss == wrong_iss:
            return
        private_key, public_key = rsa_keypair
        aud = "api.meetup.com"
        payload = {
            "sub": sub,
            "iss": iss,
            "aud": aud,
            "exp": int(time.time()) + 300,
        }

        token = jwt.encode(payload=payload, key=private_key, algorithm="RS256")

        with pytest.raises(jwt.exceptions.InvalidIssuerError):
            jwt.decode(jwt=token, key=public_key, issuer=wrong_iss, audience=aud, algorithms=["RS256"])
