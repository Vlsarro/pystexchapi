import traceback
import requests
import warnings


__all__ = ('APIResponseParsingException', 'APIDataException')


class APIBaseException(requests.exceptions.RequestException):

    msg = None
    error_code = None

    def __init__(self, msg=None, exc=None, *args, **kwargs):
        super(APIBaseException, self).__init__(msg, *args, **kwargs)
        self.exc = exc
        if msg is not None:
            self.msg = msg
        elif not self.msg:
            warnings.warn('{} must implement attribute `msg`'.format(self.__class__.__name__),
                          stacklevel=2)

        try:
            self.error_code = kwargs['error_code']
        except KeyError:
            pass

        self.kw = kwargs

    def __repr__(self):
        args = list([repr(a) for a in self.args])
        try:
            args.extend(['%s=%s' % (k, repr(v)) for k, v in self.kw.items()])
        except Exception as e:
            traceback.print_exc()
            return '{INTERNAL EXCEPTION %s}' % e.__class__.__name__

        return u'{}({})'.format(self.__class__.__name__, u', '.join(args))

    def __call__(self):
        return str(self)


class APIResponseParsingException(APIBaseException):
    msg = 'Parsing error'
    error_code = '04'


class APIDataException(APIBaseException):
    error_code = '05'
