import heapq

__author__ = 'Derek'

class heap:
    def __init__(self, L=list([])):
        self.L = list(L)
        self.heapify()
        self.__repr__ = L.__repr__

    def __len__(self):
        return len(self.L)

    def __getitem__(self, item):
        return self.L[item]

    def __setitem__(self, key, value):
        if key >= len(self): self.L.append(None)
        self.L[key] = value

    def __delitem__(self, key):
        del self.L[key]

    def __iter__(self):
        return iter(self.L)

    def __contains__(self, item):
        return item in self.L

    def __add__(self, other):
        self.L += other
        return self

    def heapify(self):
        for i in range(len(self)-1, -1, -1):
            self.down_heapify(i)

    @classmethod
    def parent(cls, i): return (i - 1)/2

    @classmethod
    def left_child(cls, i): return 2 * i + 1

    @classmethod
    def right_child(cls, i): return 2 * i + 2

    def is_leaf(self, i):
        return heap.left_child(i) >= len(self) and heap.right_child(i) >= len(self)

    def one_child(self, i):
        return heap.left_child(i) < len(self) <= heap.right_child(i)

    def smallest(self):
        return self[0]

    def remove_min(self):
        min = self[0]
        last = self.L.pop()
        if min != last: self[0] = last
        self.down_heapify(0)
        return min

    def down_heapify(self, i):
        left_i, right_i = self.left_child(i), self.right_child(i)
        if self.is_leaf(i): return

        left_child = self[left_i]
        if self.one_child(i):
            if self[i] > left_child:
                self[i], self[left_i] = left_child, self[i]
            return

        right_child = self[right_i]
        if min(left_child, right_child) >= self[i]: return

        swap_i = left_i if left_child < right_child else right_i
        self[i], self[swap_i] = self[swap_i], self[i]
        self.down_heapify(swap_i)

        return

    def up_heapify(self, i):
        if i == 0: return
        parent = self.parent(i)

        if self[parent] > self[i]:
            self[i], self[parent] = self[parent], self[i]
            self.up_heapify(parent)

class priority_dict(dict):
    def __init__(self, initial_dict=None, **kwargs):
        self.__heap = []
        dict.__init__(self)
        d = {}
        d.update(kwargs)
        if initial_dict: d.update(initial_dict)
        for (key, value) in d.iteritems(): self.__setitem__(key, value)

    def __setitem__(self, key, value):
        '''Change value stored in dictionary and add corresponding
pair to heap.'''
        dict.__setitem__(self, key, value)

        pair = (value, key)
        heapq.heappush(self.__heap, pair)


    def __iter__(self):
        '''Create destructive sorted iterator of priority_dict.'''
        while len(self):
            (value, key) = heapq.heappop(self.__heap)
            yield (key, value)
            del self[key]