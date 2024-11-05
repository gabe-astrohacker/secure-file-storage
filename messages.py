import enum

class MessageAPI(enum.StrEnum):
    DISCONNECT_MESSAGE = "!DISCONNECT"
    LOG_IN_MESSAGE = "!LOG IN"
    SIGN_UP_MESSAGE = "!SIGN UP"
    DOWNLOAD_MESSAGE = "!DOWNLOAD"
    UPLOAD_MESSAGE = "!UPLOAD"
    LOG_IN_SUCCESSFUL_REPLY = "Authentication successful."
    LOG_IN_FAILED_REPLY = "Authentication failed."
