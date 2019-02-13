from sqlalchemy import Integer, Column


class SurrogatePK(object):
    '''A mixin that adds a surrogate integer 'primary key' column
    named ``id`` to any declarative-mapped class.

    From Mike Bayer's "Building the app" talk
    https://speakerdeck.com/zzzeek/building-the-app
    '''
    __table__args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
