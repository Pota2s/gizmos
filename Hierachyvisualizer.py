from pathlib import Path
from enum import Enum

class HierarchyError(Exception):
    pass

class Node:
    name : str
    node_type : str
    depth : int
    children : list["Node"]
    parent : "Node | None"

    def __init__(self,name : str, node_type : str, depth : int = 0, parent : "Node | None" = None) -> None:
        self.name = name
        self.node_type = node_type
        self.depth = depth
        self.parent = parent
        self.children = []

    def reparent(self,other : "Node"):
        
        cursor = other
        while cursor:
            if cursor == self:
                raise HierarchyError(f"Parenting {self.name} to {other.name} creates a cycle.")
            cursor = cursor.parent 
            
        parent = self.parent
        if parent is not None:
            parent.children.remove(self)
        
        other.children.append(self)
        self.parent = other
        self.recalculate_depth()

    def addChild(self, name : str , node_type : str) -> "Node":
        node = Node(name,node_type,self.depth + 1,self)
        self.children.append(node)
        return node

    def recalculate_depth(self):
        new_depth = self.parent.depth + 1 if self.parent is not None else 0
        if self.depth == new_depth:
            return
        self.depth = new_depth
        for child in self.children:
            child.recalculate_depth()

    def _pprint(self, origin : int, last : list[bool]):
        
        string = ""
        for boolean in last[:-1]:
            string += ("│ " if not boolean else "  ")
        string += "├─" if not last[-1] else "└─"
        string += f"{self.name:<{32 - (self.depth * 2)}} ({self.node_type})"

        print(string)
        length = len(self.children)
        for index,child in enumerate(self.children,1):
            newLast = last.copy()
            newLast.append(index == length)
            child._pprint(origin,newLast)

    def pprint(self):
        print(f"{self.name:<{32 - (self.depth * 2)}} ({self.node_type})")
        length = len(self.children)
        for index,child in enumerate(self.children,1):
            child._pprint(self.depth + 1,[index == length])

class Modes(Enum):
    DECLARE = 0
    PARENT = 1
    EXIT = 2

def parse(path : Path | str):
    if type(path) == str:
        path = Path(path)

    with open(path,"r") as f:
        mode : Modes = Modes.DECLARE
        first : str | None = None
        nodes : dict[str,Node] = {}
        while(True):
            line = f.readline().strip()

            if not line:
                mode = Modes.EXIT

            match(line):
                case "DECLARE":
                    mode = Modes.DECLARE
                    continue
                case "PARENT":
                    mode = Modes.PARENT
                    continue
                case "EXIT":
                    mode = Modes.EXIT
                    continue

            if mode == Modes.DECLARE:
                node_name, node_type = line.split(",")
                if first is None:
                    first = node_name
                nodes.update({node_name : Node(node_name,node_type)})

            if mode == Modes.PARENT:
                parent_name, child_name = line.split("->")
                parent_node = nodes.get(parent_name)
                child_node = nodes.get(child_name)
                if (parent_node is None or child_node is None):
                    continue
                child_node.reparent(parent_node)

            if mode == Modes.EXIT:
                assert first is not None
                return nodes[first]


def main():
    root = parse(input("Path:") or "./tree.txt")
    root.pprint()

if __name__ == "__main__":
    main()