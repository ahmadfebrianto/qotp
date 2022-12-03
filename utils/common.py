import plyer
import pyotp


def show_notification(message):
    plyer.notification.notify(
        title="OTPY",
        message=message,
        app_name="OTPY",
        timeout=1,
    )



def parse_uri(data):
    parsed_uri = pyotp.parse_uri(data)
    return parsed_uri
