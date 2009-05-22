
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
            list, sender, message, recipients = processor.process(mail)
        except Exception, e:
            react(reactor, 'processor', e)
        else:
            try:
                distributor.distribute(list, sender, message, recipients)
            except Exception, e:
                react(reactor, 'distributor', e)

