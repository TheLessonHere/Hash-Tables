# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash = 5381
        for letter in key:
            hash = (( hash << 5) + hash) + ord(letter)
        return hash % self.capacity


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        # Create hash index to fit in the table
        idx = self._hash_mod(key)
        # Identify the target slot for storage
        target_slot = self.storage[idx]
        # Identify and store the item hashed at that slot if any
        # this gives us a mutable variable to iterate over later when going
        # down the linked list
        node = target_slot
        # Create a new list node out of the key and value so that we can chain as necessary
        new_node = LinkedPair(key, value)
        # If our target slot already has a node in it...
        if target_slot is not None:
            # and if that node has the same key as our new node...
            if target_slot.key == new_node.key:
                # override that node with the new node
                new_node.next = target_slot.next
                self.storage[idx] = new_node
            # otherwise if they do not share a key...
            else:
                # iterate down the linked list
                while node is not None:
                    # check to see if there is another node after the current one
                    if node.next is None:
                        # if not link the new node onto the tail of the list
                        node.next = new_node
                        break
                    # If there is another node linked, and that node shares a key
                    elif node.next.key == new_node.key:
                        # Override that node with the new node
                        new_node.next = node.next.next
                        node.next = new_node
                        break
                    # If neither condiditon is met, test all conditions again,
                    # starting with the next node on the list until you find a place for the new node
                    else:
                        node = node.next
        # If the target slot does not have a node in it, the new node is simply inserted there.
        else:
            self.storage[idx] = new_node


    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        # Get the index for where the key would be hashed
        idx = self._hash_mod(key)
        # Check if there is anything hashed there
        if self.storage[idx] is not None:
            # If so, declare a starting node to search from
            node = self.storage[idx]
            # Iterate down the list until you hit the end
            while node is not None:
                # If the node you are currently checking has a matching key
                if node.key == key:
                    # Set that slot equal to the next node or None
                    self.storage[idx] = node.next
                    break
                # Otherwise if the key doesn't match
                elif node.key != key:
                    # continue down the list until you hit the end, at which point return warning
                    if node.next is not None:
                        node = node.next
                    else:
                        return print("Key not found")
        # If nothing is hashed there, print a notification
        else:
            return print("No values at the hashed index")


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        # Get the hashed index
        idx = self._hash_mod(key)
        # Check if there is anything hashed there
        if self.storage[idx]:
            # Declare a starting node
            node = self.storage[idx]
            # Iterate down the list until you find a key that matches and return its value
            while node is not None:
                if node.key == key:
                    return node.value
                else:
                    node = node.next
        # If you don't find anything return None
        return None


    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        # Double the capacity
        new_capacity = self.capacity * 2
        # Create a new table with the new capacity
        new_table = HashTable(new_capacity)
        # For each node currently in storage
        for node in self.storage:
            # Iterate over the nodes and insert them into the new table
            while node is not None:
                new_table.insert(node.key, node.value)
                node = node.next
        # Once finished, reset the capacity and storage with the new values
        self.capacity = new_capacity
        self.storage = new_table.storage



if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test djb2
    print(ht._hash_djb2("line_1"))
    print(ht._hash_djb2("line_2"))
    print(ht._hash_djb2("line_3"))

    print("")
