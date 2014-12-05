import socket
import select

from apiros import ApiRos

class MikrotikApi:
    def __init__(self, host, username, password='', port=8728):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__apiros = ApiRos(self.__socket)
        self.__apiros.login(username, password)

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

    def exec_command(self, command, raw_response=False):
        """ Execute command to device.
        " @return the response as a dict by default
        " if you whant the response as set the raw_response param
        " to True
        """
        response = []

        self.__apiros.writeSentence([command])
        finished = False
        while not finished:
            # Select wait for i/o in socket
            r = select.select([self.__socket], [], [], None)
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
