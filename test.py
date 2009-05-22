
from pymalist import play
from fetchers import *
from processors import *
from distributors import *
from reactors import *

play(
    fetcher=Pop3Fetcher(
        host='pop3.mail.com',
        user='user',
        password='hackyou',
        ssl=True,
    ),

    distributor=ChainDistributor(
        TestDistributor(),
        SmtpDistributor(
            host='smtp.mail.com',
            user='user',
            password='hackyou',
            tls=True,
        ),
    ),

    processor=DummyProcessor(),
    reactor=StdErrLogger(),
)

