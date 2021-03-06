from unittest import TestCase
from publisher.selector import Selector
from publisher.selectionlibrary import SelectionLibrary
from publisher.selectiontrack import SelectionTrack


tracks = []
for i in range(6):
    track = {
        "album": {
          "id": "album{}".format(i),
        },
        "artists": [
            {
                "id": "artist{}".format(i)
            }
        ],
        "id": "song{}".format(i),
        "popularity": i
    }
    tracks.append(track)


libraries = [
    SelectionLibrary(tracks[0:4]),
    SelectionLibrary(tracks[2:6])
]
request = {
    'target_no_songs': 3,
    'libraries': libraries
}


class TestSelector(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selector = Selector()
        cls.tracks = cls.selector.choose_tracks(request)

    def test_choose_tracks_invalid_req_type(self):
        """should raise a TypeError if the request is not a dict"""
        with self.assertRaises(TypeError):
            self.selector.choose_tracks("")

    def test_choose_tracks_invalid_req_values(self):
        bad_request = {
            "libraries": [[]]
        }
        with self.assertRaises(ValueError):
            self.selector.choose_tracks(bad_request)

    def test_choose_tracks_return_type(self):
        """should return a list of strings"""
        self.assertIs(type(self.tracks), list)
        self.assertIs(type(self.tracks[0]), str)

    def test_choose_tracks_subset(self):
        """should return a subset of all members tracks"""
        all_tracks = libraries[0].get_tracks() + libraries[1].get_tracks()
        universal = set([track.get_id() for track in all_tracks])
        for track in self.tracks:
            if track not in universal:
                self.fail("{} not found in {}".format(track, universal))

    def test_choose_tracks_no_duplicates(self):
        """returned tracks should not invclude any duplicates"""
        seen = []
        for track in self.tracks:
            if track in seen:
                self.fail("duplicate tracks in {}".format(self.tracks))
            else:
                seen.append(track)

    def test_choose_tracks_selection(self):
        """should return the tracks with the highest score
        
        tracks with indices 2 and 3 are in both libs so should be returned.
        the higher the index the higher the popularity,
        so later indices should be returned otherwise.
        Do not need to be returned in order.
        """
        self.assertIn(tracks[2]['id'], self.tracks)
        self.assertIn(tracks[3]['id'], self.tracks)
        self.assertIn(tracks[5]['id'], self.tracks)
