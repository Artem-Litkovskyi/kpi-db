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
    def __init__(self, key_hash_provider=hash, order=2):
        self.key_hash_provider = key_hash_provider
        self.order = order
        self.root = BTreeNode(True, [], [])

    def __str__(self):
        return BTree._node_to_str(self.root)

    def search(self, key):
        return self._search_in_node(self.root, self.key_hash_provider(key))

    def search_less(self, value):
        result = []
        for values in self._search_in_node_less(self.root, self.key_hash_provider(value)):
            result.extend(values)
        return result

    def search_greater(self, value):
        result = []
        for values in self._search_in_node_greater(self.root, self.key_hash_provider(value)):
            result.extend(values)
        return result

    def _search_in_node(self, node: BTreeNode, key_hash: int):
        if node.leaf:
            for i, k in enumerate(node.keys):
                if k != key_hash:
                    continue
                return node.children[i]
            return []

        child_index = self._get_child_index_by_key(node, key_hash)
        return self._search_in_node(node.children[child_index], key_hash)

    def _search_in_node_less(self, node: BTreeNode, key_hash: int):
        if node.leaf:
            results = []
            for i, k in enumerate(node.keys):
                if k >= key_hash:
                    continue
                results.extend(node.children[i])
            yield results
            return

        child_indexes = self._get_child_indexes_by_key_less(node, key_hash)
        for i in child_indexes:
            results = self._search_in_node_less(node.children[i], key_hash)
            yield from results

    def _search_in_node_greater(self, node: BTreeNode, key_hash: int):
        if node.leaf:
            results = []
            for i, k in enumerate(node.keys):
                if k <= key_hash:
                    continue
                results.extend(node.children[i])
            yield results
            return

        child_indexes = self._get_child_indexes_by_key_greater(node, key_hash)
        for i in child_indexes:
            results = self._search_in_node_greater(node.children[i], key_hash)
            yield from results

    def insert(self, key, value):
        new_things = self._insert_into_node(self.root, self.key_hash_provider(key), value)

        # If nothing was split, return
        if not new_things:
            return

        # Otherwise insert a new root node
        middle_key, new_child = new_things
        self.root = BTreeNode(
            leaf=False,
            keys=[middle_key],
            children=[self.root, new_child]
        )

    def _insert_into_node(self, node: BTreeNode, key_hash: int, value):
        if node.leaf:
            self._insert_into_leaf(node, key_hash, value)

            if len(node.keys) <= self.order * 2:
                return None

            return self._split_the_leaf(node)
        else:
            child_index = self._get_child_index_by_key(node, key_hash)
            new_things = self._insert_into_node(node.children[child_index], key_hash, value)

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

    def _insert_into_leaf(self, leaf: BTreeNode, key_hash: int, value):
        for i, k in enumerate(leaf.keys):
            if k < key_hash:
                continue
            elif k == key_hash:
                leaf.children[i].append(value)
                return
            leaf.keys.insert(i, key_hash)
            leaf.children.insert(i, [value])
            return
        leaf.keys.append(key_hash)
        leaf.children.append([value])

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
        middle_key = node.keys[self.order]
        right_half = BTreeNode(
            leaf=False,
            keys=node.keys[self.order+1:],
            children=node.children[self.order+1:]
        )
        node.keys = node.keys[:self.order]
        node.children = node.children[:self.order+1]
        return middle_key, right_half

    @staticmethod
    def _get_child_index_by_key(node: BTreeNode, key_hash: int):
        for i, k in enumerate(node.keys):
            if k <= key_hash:
                continue
            return i
        return len(node.keys)

    @staticmethod
    def _get_child_indexes_by_key_less(node: BTreeNode, key_hash: int):
        indexes = []
        for i, k in enumerate(node.keys):
            if k <= key_hash:
                indexes.append(i)
                continue
            indexes.append(i)
            return indexes
        return indexes

    @staticmethod
    def _get_child_indexes_by_key_greater(node: BTreeNode, key_hash: int):
        indexes = []
        for i, k in enumerate(node.keys):
            if k <= key_hash:
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