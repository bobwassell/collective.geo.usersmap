# from persistent import Persistent
from persistent.mapping import PersistentMapping
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree

from zope.interface import implements

from collective.geo.geographer.interfaces import IGeoCoder
from collective.geo.usermap.interfaces import IUserCoordinates


class UserData(PersistentMapping):
    """User Data persistent mapping

    This object stores the user's properties used to create
    the kml file which contains the coordinates of users
    """

    def __init__(self, userid, fullname, location, coordinates):
        super(UserData, self).__init__()
        self.update({'userid': userid,
                'fullname': fullname,
                'location': location,
                'coordinates': coordinates,
            })


class UserCoordinates(SimpleItem):
    implements(IUserCoordinates)

    def __init__(self, id, title=None):
        super(UserCoordinates, self).__init__()
        self.id = id
        self.title = title
        self._records = OOBTree()

    @property
    def records(self):
        return self._records

    def __getitem__(self, name):
        return self.records[name]

    def __setitem__(self, name, value):
        if not isinstance(value, UserData):
            raise TypeError
        self.records[name].value = value

    def __contains__(self, name):
        return name in self.records

    def __iter__(self):
        return self.records.__iter__()

    def items(self):
        return self.records.items()

    def iteritems(self):
        return self.records.iteritems()

    def keys(self):
        return self.records.keys()

    def get(self, name, default=None):
        return self.records.get(name, default)

    def add(self, userid, fullname, location):
        if userid in self.records:
            raise ValueError

        coordinates = self.get_coordinates(location)
        usr_data = UserData(userid, fullname, location, coordinates)
        self.records[userid] = usr_data

    def update(self, userid, fullname, location):
        if userid in self.records:
            usr_data = self.get(userid)
            usr_data['fullname'] = fullname
            if usr_data['location'] != location:
                usr_data['location'] = location
                usr_data['coordinates'] = self.get_coordinates(location)

    def delete(self, userid):
        self.records.pop(userid)

    @property
    def geocoder(self):
        return IGeoCoder(None)

    def get_coordinates(self, location):
        """get coordinates with IGeoCoder and return
        the first coordinates retrieved
        """
        geo_data = self.geocoder.retrieve(location)
        if not geo_data:
            return (0.0, 0.0)
        return geo_data[0][1]
