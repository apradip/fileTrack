import mongoengine


def global_init():
    mongoengine.register_connection(alias='RestAPI',
                                    db='fileTrack',
                                    host='localhost',
                                    port=27017,
                                    username='admin',
                                    password='pixel@123',
                                    authentication_source='admin')
