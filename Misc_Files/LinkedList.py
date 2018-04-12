class Node:
     
     def __init__(self,name=None,age=None,next_node=None):
         self.data=(name,age)
         self.next_node=next_node
         
     def get_data(self):
         return self.data

     def get_next(self):
         return self.next_node

     def set_next(self,new_next):
         self.next_node=new_next



class LinkedList(object):

    def __init__(self,head=None,name=None,age=None):
        self.head.get_data()=(name,age)
        self.head=head
        
    def insert(self,name,age):
        data=(name,age)
        new_node=Node(data)
        new_node.set_next(self.head)
        self.head=new_node

    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count

    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        return current         

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    def display(self):
        current = self.head
        elems = []
        while current:
            if current.get_data() != student():
                elems.append(current.get_data())
                current = current.get_next()
            else:
                elems.append(current.get_data())
        print "The elements are:" 
        for e in reversed(elems):
            print e

class student:
    def __init__(self,name=None,age=None):
        self.name=name
        self.age=age




s1=student("charan",21)

l1=LinkedList("charan",21)
l1.insert("charan",21)
l1.display()
