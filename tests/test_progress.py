from trace_grabber.progress import playlist_duration, parse_out_time, percent, parse_total_size

MEDIA = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:6
#EXTINF:6.006,
seg0.ts
#EXTINF:6.006,
seg1.ts
#EXTINF:3.000,
seg2.ts
#EXT-X-ENDLIST
"""

def test_playlist_duration_sums_extinf():
    assert abs(playlist_duration(MEDIA) - 15.012) < 0.001

def test_parse_out_time():
    assert abs(parse_out_time("out_time=00:00:12.500000") - 12.5) < 0.001
    assert parse_out_time("frame=10") is None

def test_percent_clamped():
    assert percent(0, 100) == 0
    assert percent(50, 100) == 50
    assert percent(150, 100) == 100
    assert percent(5, 0) == 0

def test_parse_total_size():
    assert parse_total_size("total_size=1048576") == 1048576
    assert parse_total_size("out_time=00:00:01.0") is None
