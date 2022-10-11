from scheduling_formatter.time_formatter import format_time


def test_format_time():
    # Given several seconds
    seconds_list = [0, 3 * 3600, 5 * 3600 + 20 * 60, 14 * 3600 + 15 * 60 + 30]

    # And the expected formatted times
    expected_list = ["12 AM", "3 AM", "5:20 AM", "2:15:30 PM"]

    # When format
    result = list(map(lambda s: format_time(s), seconds_list))

    # Then the result is the expected
    assert result == expected_list
