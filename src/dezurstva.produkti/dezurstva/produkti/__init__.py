"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory

produktiMessageFactory = MessageFactory('dezurstva.produkti')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
