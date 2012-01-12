from zope import schema
from zope.interface import Interface
from plone.app.users.userdataschema import IUserDataSchema
from plone.theme.interfaces import IDefaultPloneLayer
from collective.geo.usermap import _


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IUsersMapView(Interface):
    """Marker interface for UsersMapView
    """


class IUserMapPreferences(Interface):
    """Users Map settings for plone.app.registry
    """
    title = schema.TextLine(title=_(u"Map Title"))
    description = schema.Text(title=_(u"Map Description"))


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    coordinates = schema.TextLine(
        title=_(u'coordinates'),
        required=False,
        )
