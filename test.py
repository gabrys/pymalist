from pymalist import play
from fetchers import *
from processors import *
from distributors import *
from reactors import *

pop3 = Pop3Fetcher(
    host='pop3.host.com',
    user='user',
    password='pass',
    ssl=True,
)

smtp = SmtpDistributor(
    host='smtp.host.com',
    user='user',
    password='pass',
    tls=True,
)

play(
    fetcher = pop3,
    distributor = ChainDistributor(
        smtp,
        DistributeToDistributor(['archive@host.com'], smtp),
    ),
    processor=SingleListProcessor(
        list_mail = 'list@host.com',
        subject_prefix = '[MY LIST] ',
        subscribers = ['you@host.com', 'your.friend@other.host.com']
    ),
    reactor=StdErrLogger(),
)

