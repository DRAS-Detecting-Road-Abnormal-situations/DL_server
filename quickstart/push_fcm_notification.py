from firebase_admin import messaging

def send_to_firebase_cloud_messaging():
    # This registration token comes from the client FCM SDKs.
    registration_token = 'dEn7h6FyDEw:APA91bFvJa1wBNZyCwd7d5wkwrAuFm_Dh-ryAlSi0UO-f_dntQEK5G2W6vsqIBtz_QVwRdWJlf6__YFk48P6tJuXmx6-LW8vgoEefdhPpDvhQ6qnW12Sz8vLNdG49Fws9JakpSoa0B5u'

    # See documentation on defining a message payload.
    message = messaging.Message(
    data={
        'title':'조심하세요',
        'body':'경로에 교통사고가 났습니다. 주의하세요', 
        'cctv_id' : '1',
        'image_name' : '111101741',
    },
    token=registration_token,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)

def send_to_token():
    #default_app = firebase_admin.initialize_app()
    registration_token = 'cHXdiCBkUFM:APA91bFI01-x0KnqCSSJRCh7iD-50rprDalwsom5nhdcHCDomm9XLc7m9rJAR-OsRJzFLJ-YctQUsfTs6um_wO4yb476s6b_frfVPom94_CwJoo7JwKG1iOdbmBg4MrmV-PwCQOTLUC-'
    message = messaging.Message(
    data={
        'title':'조심하세요',
        'body':'경로에 교통사고가 났습니다. 주의하세요', 
        'cctv_id' : '1',
        'image_name' : '111101741',
    },
    token=registration_token,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)