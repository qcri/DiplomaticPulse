
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


config={
  "type": "service_account",
  "project_id": "diplomaticpulse-501c3",
  "private_key_id": "dab36f43b4a785854f333248c3384c0bf0d9d333",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDIwk13VfWeAmB5\nW/eif1Mwc/MPZXQhamRmytXbvmr8RWUi0AixwNx5BPayo+kWPRTWnjKWYPmWgh0z\n1EEZXnaWbkzdeKtn5IX4SwrkHrX8p2ltCN3SN1CZ774surTQONlCcV0DAtcIzDzB\n3+Ncg0NF8HTcKpyxsQuX+2eSlMqmrrv3u+f9C9yDw4fkELk6sUVGWMjI9pjw8QpD\nafAIMfKlnN8wzbHw5KCnuOeZTnNTVHUpTrxGbelVPsi4cuypbNpwYRMjaqiRvCVT\nCEMA7jgGwl6rDrMYdj0FWwMXtlB1mdpgxUVN2xW9Xfgewb0ZNI8mTKOotVEqOMva\n20V1XvrfAgMBAAECggEAALLMWjHuXNJdS47KWcJfo7eDjPYpZURdfQ4PmGgdLyt+\nopRes1+cZL9jrFNtqComPGjofCVyONfTCi8e2tu9ReC0W8Djt8TPwoFgVFLXBz39\n2+c//k869I4k9zrfDipkdxq13CDSZrFvNK12uQer4D5p6aosSWH4TFsPjS7/VX0c\njnYBRngMo7yByhYshsqDEJ7Q0dyS3g/Qdkj+5jtsckTCyRy/4kLvN+n4kSVi4gLH\nwuBB22T4rN3YTUKkcB3wgQWAKjfAd8zm2jgoc7RsAr/HY67Vl/TMKd3WC1yeUy9q\nziFfNtK4DZrYfuPUprc+m+dIvNrl/Pi22yPabxLnAQKBgQDlC1Q0bE+J8QyEJO+z\nXTC3Ok4EHjKwn/PyzPUMyc3iAv7T+RnE8xG71f3EvTBKzm/8qPtVu+Axa3yMnbS/\neSY27cy8j/JD4wRMxUdHtQV2JCQrSLv+VHFfjkDv7+CIxAxu0tGlhfoGLePOOyEB\nwgK2p9pf+fhTPcoErwt2VnnMIQKBgQDgYsrN+wmso2R1mz2HBwC3cTqOAwZ1E5dz\na9ZdX7ZkEYrlLz4JDJ/UJbqYn4nqUZ8c0SWqTP3rvoILtKFSgvCbsbttWS2En7Te\nCCDKDA0BsXNg5pAmZ4J8KIF5G9zeXsEUe8mxhtTZTVhd1cmrAfp2pL3lNeI4dKBg\nCVTHV8fm/wKBgCXN3eMdMW+iIp+4/PtM2VqUvAW/+jve2sPrglLPCDVSqz7Pcapp\nODcZld4gH9VpB2Dbf0hiTxm5FQCckxW7aExOqalB1QnRcYc+VIqIXVNnmbSvN6A9\nzcyozR0NKbFJMogkMcgxOdhFQMFsTwFcRVhikg+fUZZjr3FgdvLcSRQhAoGAdrzQ\nhN9q5ygvaOyVSnayMmCAk9WV/S443qMZ9J9JbPq7fTvan/9GNIUikNEbshsvD5i9\nTbkgRTeyqW8UTw1rNXh/rgWayKuakkPK1iA6YcL9QzG+5hOwQPNOUEAmSKXrlmNK\n/95RlAwRztXquct6Nn5G3pv88dMFasyFSFdzORECgYAnYZTkecZVAN/6ILiuwVdH\nTesJCjE+RGTNf9RWz8WXTzbyO+MGzGxXi7wzvPbVt0rrcCaQQMtpXiiMHH/aHIXt\nT5raeT21BKaTF08Qlcqq0jGvKcdd0d0y72EyuVsD8BrrXRN0Kn/S/vV8yCENY6eJ\ncJSpyNFM3fsb9ZB3SV4Y6Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-pe8t8@diplomaticpulse-501c3.iam.gserviceaccount.com",
  "client_id": "109728927604892847745",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pe8t8%40diplomaticpulse-501c3.iam.gserviceaccount.com"
}


class Firebase_db:
    def connect(self):

        print('start connection to firebase')
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db