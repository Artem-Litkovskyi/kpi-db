class BTreeNode:
    def __init__(self, leaf: bool, keys: list, children: list):
        self.leaf = leaf
        self.keys = keys
        self.children = children

    def __str__(self):
        return 'BTreeNode(leaf=%s, keys=%s, children=%s)' % (
            self.leaf,
            self.keys,
            '[%s]' % ', '.join([type(child).__name__ for child in self.children])
        )

# key1 <= x < key2
class BTree:
    def __init__(self, key_provider=hash, order=2):
        self.key_provider = key_provider
        self.order = order
        self.root = BTreeNode(True, [], [])

    def __str__(self):
        return BTree._node_to_str(self.root)

    def search(self, value):
        return self._search_in_node(self.root, self.key_provider(value))

    def search_lower(self, value):
        result = []
        for values in self._search_in_node_lower(self.root, self.key_provider(value)):
            result.extend(values)
        return result

    def search_greater(self, value):
        result = []
        for values in self._search_in_node_greater(self.root, self.key_provider(value)):
            result.extend(values)
        return result

    def _search_in_node(self, node: BTreeNode, key: int):
        if node.leaf:
            results = []
            for i, k in enumerate(node.keys):
                if k != key:
                    continue
                results.append(node.children[i])
            return results

        child_index = self._get_child_index_by_key(node, key)
        return self._search_in_node(node.children[child_index], key)

    def _search_in_node_lower(self, node: BTreeNode, key: int):
        if node.leaf:
            results = []
            for i, k in enumerate(node.keys):
                if k >= key:
                    continue
                results.append(node.children[i])
            yield results
            return

        child_indexes = self._get_child_indexes_by_key_lower(node, key)
        for i in child_indexes:
            results = self._search_in_node_lower(node.children[i], key)
            yield from results

    def _search_in_node_greater(self, node: BTreeNode, key: int):
        if node.leaf:
            results = []
            for i, k in enumerate(node.keys):
                if k <= key:
                    continue
                results.append(node.children[i])
            yield results
            return

        child_indexes = self._get_child_indexes_by_key_greater(node, key)
        for i in child_indexes:
            results = self._search_in_node_greater(node.children[i], key)
            yield from results

    def insert(self, value):
        new_things = self._insert_into_node(self.root, self.key_provider(value), value)

        # If child wasn't split, return
        if not new_things:
            return

        # Otherwise insert a new tree level
        middle_key, new_child = new_things
        self.root = BTreeNode(
            leaf=False,
            keys=[middle_key],
            children=[self.root, new_child]
        )

    def _insert_into_node(self, node: BTreeNode, key: int, value):
        if node.leaf:
            self._insert_into_leaf(node, key, value)

            if len(node.keys) <= self.order * 2:
                return None

            return self._split_the_leaf(node)
        else:
            child_index = self._get_child_index_by_key(node, key)
            new_things = self._insert_into_node(node.children[child_index], key, value)

            # If child wasn't split, return None
            if not new_things:
                return None

            # Otherwise, insert the new child (the right half of the old child)
            middle_key, new_child = new_things
            node.keys.insert(child_index, middle_key)
            node.children.insert(child_index + 1, new_child)

            if len(node.keys) <= self.order * 2:
                return None

            return self._split_the_node(node)

    def _insert_into_leaf(self, leaf: BTreeNode, key: int, value):
        for i, k in enumerate(leaf.keys):
            if k <= key:
                continue
            leaf.keys.insert(i, key)
            leaf.children.insert(i, value)
            return
        leaf.keys.append(key)
        leaf.children.append(value)

    def _split_the_leaf(self, node: BTreeNode):
        right_half = BTreeNode(
            leaf=True,
            keys=node.keys[self.order:],
            children=node.children[self.order:]
        )
        node.keys = node.keys[:self.order]
        node.children = node.children[:self.order]
        return right_half.keys[0], right_half

    def _split_the_node(self, node: BTreeNode):
        middle_key = node.keys[0]
        right_half = BTreeNode(
            leaf=True,
            keys=node.keys[self.order+1:],
            children=node.children[self.order+1:]
        )
        node.keys = node.keys[:self.order]
        node.children = node.children[:self.order]
        return middle_key, right_half

    @staticmethod
    def _get_child_index_by_key(node: BTreeNode, key: int):
        for i, k in enumerate(node.keys):
            if k <= key:
                continue
            return i
        return len(node.keys)

    @staticmethod
    def _get_child_indexes_by_key_lower(node: BTreeNode, key: int):
        indexes = []
        for i, k in enumerate(node.keys):
            if k <= key:
                indexes.append(i)
                continue
            indexes.append(i)
            return indexes
        return indexes

    @staticmethod
    def _get_child_indexes_by_key_greater(node: BTreeNode, key: int):
        indexes = []
        for i, k in enumerate(node.keys):
            if k <= key:
                continue
            indexes.append(i)
        indexes.append(len(node.keys))
        return indexes

    @staticmethod
    def _node_to_str(node, indent_level=0):
        indent = '\t' * indent_level

        string = indent + 'BTreeNode(\n'
        string += indent + '\tleaf: %s\n' % node.leaf
        string += indent + '\tkeys: %s\n' % node.keys
        string += indent + '\tchildren: '

        if node.leaf:
            string += '%s\n' % node.children
        else:
            string += '[\n'
            for child in node.children:
                string += BTree._node_to_str(child, indent_level + 2) + ',\n'
            string += indent + '\t]\n'

        string += indent + ')'

        return string