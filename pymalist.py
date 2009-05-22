#!/usr/bin/env python
# encoding: utf-8

from exceptions import NothingMore

def play(fetcher, processor, distributor, reactor):
    while True:
        try:
            mail = fetcher.fetch()
        except NothingMore:
            return
        except Exception, e:
            reactor.react('fetcher', e)
            return

        try:
            addresses, message = processor.process(mail)
        except Exception, e:
            reactor.react('processor', e)
        else:
            try:
                distributor.distribute(addresses, message)
            except Exception, e:
                reactor.react('distributor', e)

