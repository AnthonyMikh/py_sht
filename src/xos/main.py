import random
from enum import Enum, unique

@unique
class Mark(Enum):
    EMPTY = 0
    X = 1
    O = 2
    
    def opposite(self) -> 'Mark':
        if self is Mark.X:
            return Mark.O
        else:
            return Mark.X
    
    @classmethod
    def from_figure(fig: 'Figure', own: 'Mark') -> 'Mark':
        if fig is Figure.EMPTY:
            return Mark.EMPTY
        elif fig is Figure.OWN:
            return own
        else:
            return own.opposite()
    
    def __str__(self) -> str:
        if self is Mark.EMPTY:
            return ' '
        elif self is Mark.X:
            return 'X'
        else:
            return 'O'

@unique
class Figure(Enum):
    EMPTY = 0
    OWN = 1
    ENEMY = 2
    
    @classmethod
    def from_mark(mark: Mark, own: Mark) -> 'Figure':
        if mark is Mark.EMPTY:
            return Figure.EMPTY
        elif mark is own:
            return Figure.Own
        else:
            return Figure.Enemy

class Field():
    idx_err = "Field is indexable by single and a pair of integers only"
    
    def __init__(self):
        self.field = [Mark.EMPTY] * 9
    
    @classmethod
    def from_raw_field(cls, field: list) -> 'Field':
        field_ = cls()
        field_.field = field
        return field_
    
    def to_field_repr(self, own: 'Mark') -> 'FieldRepr':
        field = map(lambda m: Figure.from_mark(m, own), self.field)
        return FieldRepr.from_raw_field(field)
    
    def __str__(self):
        bot = "|".join(map(str, self.field[6:9]))
        mid = "|".join(map(str, self.field[3:6]))
        top = "|".join(map(str, self.field[0:3]))
        return '\n-----\n'.join([bot, mid, top])
    
    def __getitem__(self, index) -> Mark:
        if isinstance(index, int):
            return self.field[index]
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(Field.idx_err)
            row, col = index
            return self.field[row * 3 + col]
        else:
            raise IndexError(Field.idx_err)
    
    def __setitem__(self, index, mark: Mark):
        if isinstance(index, int):
            self.field[index] = mark
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(Field.idx_err)
            row, col = index
            self.field[row * 3 + col] = mark
        else:
            raise IndexError(Field.idx_err)

class FieldRepr():
    idx_err = "FieldRepr is indexable by single and a pair of integers only"
    
    def __init__(self):
        self.field = [Figure.Empty] * 9
    
    @classmethod
    def from_raw_field(cls, field: list) -> 'FieldRepr':
        field_repr = cls()
        field_repr.field = field
        return field_repr
    
    def __getitem__(self, index) -> Figure:
        if isinstance(index, int):
            return self.field[index]
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(Field.idx_err)
            row, col = index
            return self.field[row * 3 + col]
        else:
            raise IndexError(Field.idx_err)
    
    def __setitem__(self, index, fig: Figure):
        if isinstance(index, int):
            self.field[index] = fig
        elif isinstance(index, tuple):
            if len(index) != 2:
                raise IndexError(Field.idx_err)
            row, col = index
            self.field[row * 3 + col] = fig
        else:
            raise IndexError(Field.idx_err)

if __name__ == "__main__":
    print("it works")
