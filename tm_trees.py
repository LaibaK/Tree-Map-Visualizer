"""
Assignment 2: Trees for Treemap

=== CSC148 Summer 2022 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        #     self._expanded = False
        self._expanded = False

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        if len(self._subtrees) == 0:
            self.data_size = data_size
        else:
            s = 0
            for subtree in self._subtrees:
                s += subtree.data_size
                subtree._parent_tree = self
            self.data_size = s

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        x, y, width, height = rect
        self.rect = rect
        og_x = x
        og_y = y

        i = 0
        total_w = 0
        total_h = 0

        for subtree in self._subtrees:
            n = len(self._subtrees) - 1
            if subtree.data_size > 0:
                if width > height and self.data_size > 0 and i != n:
                    new_wid = math.floor((subtree.data_size / self.data_size)
                                         * width)
                    subtree.update_rectangles((og_x, y, new_wid, height))
                    total_w += new_wid
                    og_x += new_wid
                    i += 1

                elif width > height and self.data_size > 0 and i == n:
                    subtree.update_rectangles((og_x, y,
                                               width - total_w, height))

                elif height >= width and self.data_size > 0 and i != n:
                    new_hig = math.floor((subtree.data_size / self.data_size)
                                         * height)
                    subtree.update_rectangles((x, og_y, width, new_hig))
                    og_y += new_hig
                    total_h += new_hig
                    i += 1

                elif height >= width and self.data_size > 0 and i == n:
                    subtree.update_rectangles((x, og_y, width,
                                               height - total_h))
            else:
                if width > height and self.data_size > 0 and i != n:
                    subtree.update_rectangles((og_x, y, 0, 0))
                    i += 1

                elif width > height and self.data_size > 0 and i == n:
                    subtree.update_rectangles((og_x, y, 0, 0))

                elif height >= width and self.data_size > 0 and i != n:
                    subtree.update_rectangles((x, og_y, 0, 0))
                    i += 1

                elif height >= width and self.data_size > 0 and i == n:
                    subtree.update_rectangles((x, og_y, 0, 0))

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0:
            return []
        if not self._expanded:
            tup = (self.rect, self._colour)
            return [tup]
        else:
            if not self._subtrees:
                tup = (self.rect, self._colour)
                return [tup]
            lst = []
            for subtree in self._subtrees:
                lst.extend(subtree.get_rectangles())
            return lst

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        x, y, width, height = self.rect
        if self._expanded:
            lst = []
            for subtree in self._subtrees:
                if subtree.get_tree_at_position(pos):
                    lst.append(subtree.get_tree_at_position(pos))
            r = None
            s = -1
            for tree in lst:
                val = (tree.rect[0] * tree.rect[0]) + \
                      (tree.rect[1] * tree.rect[1])
                dist = math.sqrt(val)
                if dist < s or s == -1:
                    s = dist
                    r = tree
            return r
        else:
            m = pos
            if (y <= m[1] <= y + height) and (x <= m[0] <= x + width):
                return self
            else:
                return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if len(self._subtrees) == 0:
            return self.data_size
        else:
            s = 0
            for subtree in self._subtrees:
                s += subtree.update_data_sizes()
            self.data_size = s
            return s

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if not self._subtrees and destination._subtrees:
            item = self
            if self._parent_tree:
                self._parent_tree._subtrees.remove(item)

                if not self._parent_tree._subtrees:
                    self._parent_tree.data_size = 0
                self._parent_tree.update_data_sizes()

            destination._subtrees.append(item)
            item._parent_tree = destination
            destination.update_data_sizes()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees:
            c = factor * self.data_size

            if c > 0:
                self.data_size += math.ceil(c)
            else:
                val = self.data_size + math.floor(c)
                if val <= 1:
                    self.data_size = 1
                else:
                    self.data_size += math.floor(c)

            if self._parent_tree:
                self._parent_tree.update_data_sizes()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        if self._parent_tree is not None:
            if self._subtrees == []:
                self.data_size = 0
                self.rect = (0, 0, 0, 0)
                self.update_data_sizes()
                self.update_rectangles((0, 0, 0, 0))
            else:
                for trees in self._subtrees:
                    trees.delete_self()
            self._parent_tree.data_size = 0
            self._parent_tree.rect = (0, 0, 0, 0)
            self._parent_tree.update_data_sizes()
            self._parent_tree.update_rectangles()

    def expand(self) -> None:
        """Expand the tree. If tree is a leaf, do nothing."""
        if len(self._subtrees) != 0:
            self._expanded = True

    def expand_all(self) -> None:
        """Expand the whole tree. If tree is a leaf, do nothing."""
        if len(self._subtrees) != 0:
            self.expand()
            for subtree in self._subtrees:
                subtree.expand_all()

    def _collapse_helper(self) -> None:
        """Collapse all the subtrees except their leaf."""
        for subtree in self._subtrees:
            subtree._expanded = False
            subtree._collapse_helper()

    def collapse(self) -> None:
        """Collapse the tree. If self._parent_tree is None, do nothing."""
        if self._parent_tree is not None:
            self._parent_tree._expanded = False
            self._parent_tree._collapse_helper()

    def collapse_all(self) -> None:
        """Collapse the whole tree. If self._parent_tree is None, do nothing."""
        if self._parent_tree is not None and \
                self._parent_tree._parent_tree is None:
            self.collapse()
        elif self._parent_tree is not None:
            parent_node = self._parent_tree
            parent_node.collapse_all()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        name = os.path.basename(path)

        if os.path.isdir(path):
            subtree = []
            dirs = os.listdir(path)
            for filename in dirs:
                item = os.path.join(path, filename)
                subtree.append(FileSystemTree(item))
            TMTree.__init__(self, name, subtree)
        else:
            s = os.path.getsize(path)
            TMTree.__init__(self, name, [], s)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
