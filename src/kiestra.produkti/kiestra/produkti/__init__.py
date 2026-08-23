"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory

produktiMessageFactory = MessageFactory('kiestra.produkti')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
