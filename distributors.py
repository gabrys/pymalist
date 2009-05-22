
class TestDistributor(object):
    def distribute(self, list, sender, message, recipients):
        print "List: %s\nSender: %s\nTo: %s\n\n%s" % (list, sender, message, recipients)
