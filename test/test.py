from fastapi.testclient import TestClient


from app.main import app

client = TestClient(app)


def test_400_for_invalid_datetime_string():
    # Test with a valid datetime iso string
    response = client.get("/invalid-datetime-string")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid datetime format. Use ISO format."


expected_responses = {
    "2023-04-01T09:30:43": [
        {
            "name": "Char Grill",
            "operating_hours": "Mon-Fri 11:30 am - 10 pm  / Sat-Sun 7 am - 3 pm"
        },
        {
            "name": "Dashi",
            "operating_hours": "Mon-Fri 10 am - 9:30 pm  / Sat-Sun 9:30 am - 9:30 pm"
        },
        {
            "name": "Tupelo Honey",
            "operating_hours": "Mon-Thu, Sun 9 am - 10 pm  / Fri-Sat 9 am - 11 pm"
        }
    ],
    "2023-04-03T01:59:43": [
        {
            "name": "42nd Street Oyster Bar",
            "operating_hours": "Mon-Sat 11 am - 12 am  / Sun 12 pm - 2 am"
        },
        {
            "name": "Seoul 116",
            "operating_hours": "Mon-Sun 11 am - 4 am"
        }
    ],
    "2023-04-01T09:00:43": [
        {
            "name": "Char Grill",
            "operating_hours": "Mon-Fri 11:30 am - 10 pm  / Sat-Sun 7 am - 3 pm"
        },
        {
            "name": "Tupelo Honey",
            "operating_hours": "Mon-Thu, Sun 9 am - 10 pm  / Fri-Sat 9 am - 11 pm"
        }
    ]
}


def test_expected_openings():
    for datestring, expected_response in expected_responses.items():
        response = client.get("/%s" % datestring)
        assert response.json() == expected_response
