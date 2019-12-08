class Edge(object):
    
    def __init__(self, tail, head):
        self._label = None
        self._tail = tail
        self._head = head
        self._attrs = {}

    def get_tail(self):
        return self._tail

    def get_head(self):
        return self._head

