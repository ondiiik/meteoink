from micropython import const
from heap        import refresh

_SINGLE_QUOTE = const(39)  # ord("'")
_DOUBLE_QUOTE = const(34)  # ord('"')
_BACKSLASH    = const(92)  # ord('\\')
_OBJECT_BEGIN = const(123) # ord('{')
_OBJECT_END   = const(125) # ord('}')
_LIST_BEGIN   = const(91)  # ord('[')
_LIST_END     = const(93)  # ord(']')
_ASIGNATOR    = const(58)  # ord(':')
_SEPARATOR    = const(44)  # ord(',')

_PARSE_KEY    = const(0)
_PARSE_VAL    = const(1)
_PARSE_STRING = const(2)
_PARSE_OBJECT = const(3)

class JsonRead:
    class _Reader:
        def __init__(self, stream, size):
            __slots__   = ('stream', 'idx', 'len', 'data')
            self.stream = stream
            self.idx    = size
            self.len    = size
            self.data   = bytearray(size)
        
        def read(self):
            # Reread buffer?
            if self.len == self.idx:
#                 self.data = self.stream.recv(len(self.data))
#                 self.len  = len(self.data)
                self.len = self.stream.readinto(self.data)
                self.idx = 0
                print('.', end='')
                
                # EOF?
                if 0 == self.len:
                    return None
                    
            # Return next character
            c         = self.data[self.idx]
            self.idx += 1
            return c
    
    
    def __init__(self, stream, buffer_size = 512):
        __slots__ = 'data'
        _reader   = self._Reader(stream, buffer_size)
        
        if _OBJECT_BEGIN == _reader.read():
            self.data = self._parse(_reader, {}, _OBJECT_END)
            refresh()
        else:
            raise ValueError('JSON does not start with "{"')
    
    
    def _parse(self, _reader, obj, esc):
        name  = bytearray(0)
        val   = bytearray(0)
        parse = _PARSE_KEY
        
        for i in range(100000):
            c = _reader.read()
            
            if (esc == c) or (c is None):
                self._append(obj, name, val, parse, esc)
                return obj
            
            # Drop quotes from strings
            if (_DOUBLE_QUOTE == c):
                if not (_PARSE_KEY == parse):
                    parse = _PARSE_STRING
                continue
            # Switch from parsing key to parsing value
            if   _ASIGNATOR == c:
                parse = _PARSE_VAL
            # Store value and start new item
            elif _SEPARATOR == c:
                self._append(obj, name, val, parse, esc)
                name  = bytearray(0)
                val   = bytearray(0)
                parse = _PARSE_KEY
            # Start parsing of inherited object
            elif _OBJECT_BEGIN == c:
                val   = self.data = self._parse(_reader, {}, _OBJECT_END)
                parse = _PARSE_OBJECT
                refresh()
            # Start parsing of inherited object
            elif _LIST_BEGIN == c:
                val   = self.data = self._parse(_reader, [], _LIST_END)
                parse = _PARSE_OBJECT
                refresh()
            # Append new character to key
            elif parse == _PARSE_KEY:
                name.append(c)
                refresh()
            # Append new character to value
            else:
                val.append(c)
                refresh()
    
    
    @staticmethod
    def _append(obj, name, val, parse, esc):
        if esc == _LIST_END:
            obj.append(val)
            return
        
        name = name.decode()
        
        if parse == _PARSE_OBJECT:
            obj[name] = val
            return
        
        val = val.decode()
        
        if parse == _PARSE_VAL:
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
            
        obj[name] = val
