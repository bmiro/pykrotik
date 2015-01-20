import socket
import select

from apiros import ApiRos

class MikrotikApi:
    def __init__(self, host, username, password='', port=8728, timeout=10):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__apiros = ApiRos(self.__socket)
        self.__apiros.login(username, password)

        self._timeout = timeout

    def __attr_to_key_value(self, attr):
        elem = attr[1:] # Remove first =
        idx = elem.find('=')
        # from begin to first = is the key, from equal to end is the value
        return { elem[:idx]: elem[idx+1:] }

    def __dictify_response(self, raw_response):
        response = []
        for attrs in raw_response:
            element = {}
            # skip first element
            for attr in attrs[1:]:
                element.update(self.__attr_to_key_value(attr))
            response.append(element)
        return response

    def exec_command(self, command, query_word=None, raw_response=False,
                     timeout=None):
        """ Execute command to device.
        " @return the response as a dict by default
        " if you whant the response as set the raw_response param
        " to True
        " Pass a list of query words to filter if needed i.e.
        " ['?name=CLIEXXX', '?service=pppoe']
        """
        response = []
        if not query_word:
            query_word = []

        timeout = timeout or self._timeout

        print 'Start'

        self.__apiros.writeSentence([command] + query_word)
        finished = False
        while not finished:
            # Select wait for i/o in socket
            print 'Helo'
            r = select.select([self.__socket], [], [], timeout)
            print r
            if self.__socket in r[0]:
                resp = self.__apiros.readSentence()
                if '!done' in resp:
                    finished = True
                else:
                    response.append(resp)

        if raw_response:
            return response
        else:
            return self.__dictify_response(response)
