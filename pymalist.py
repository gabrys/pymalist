
from fetchers import NothingMore

def react(reactor, type, exception):
    try:
        reactor.react(type, exception)
    except:
        pass

def play(fetcher, processor, distributor, reactor):
    while True:
        try:
            mail = fetcher.fetch()
        except NothingMore:
            return
        except Exception, e:
            react(reactor, 'fetcher', e)
            return

        try:
            mail = processor.process(mail)
        except Exception, e:
            react(reactor, 'processor', e)
        else:
            try:
                distributor.distribute(mail)
            except Exception, e:
                react(reactor, 'distributor', e)

