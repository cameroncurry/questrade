#
# Copyright Cameron Curry (c) 2017
#


def qt_str(klass):
    return '{}[{}]'.format(klass.__class__.__name__, ', '.join('%s=%s' % (k[1:], v) for k, v in vars(klass).items()))
