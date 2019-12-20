class Edge(object):
    
    def __init__(self, tail, head, **attrs):
        """ Initialises the edge. 

        Args:
            tail(Vertex): the tail vertex
            head(Vertex): the head vertex
            **attrs: additional atttributes that define the edge
        """
        
        self._label = None
        self._tail = tail
        self._head = head
        self._attrs = attrs

    def get_tail(self):
        return self._tail

    def get_head(self):
        return self._head

    def set_attr(self, attr, value):
        self._attrs[attr] = value

    def get_attr(self, attr):
        return self._attrs.get(attr)
