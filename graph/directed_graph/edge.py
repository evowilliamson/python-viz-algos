class Edge(object):
    
    def __init__(self, head, tail):
        self._label = None
        self._head = head
        self._tail = tail

    def get_tail(self):
        return self._tail

    def get_head(self):
        return self._head

