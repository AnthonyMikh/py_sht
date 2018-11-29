import random
from enum import Enum, unique
from abc import ABC, abstractmethod
from typing import Union, Optional, TypeVar

T = TypeVar('T')

@unique
class Mark(Enum):
    EMPTY = 0
    X = 1
    O = 2
    
    
    def opposite(self) -> 'Mark':
        return {
         Mark.EMPTY: Mark.EMPTY,
         Mark.X: Mark.O,
         Mark.O: Mark.X,
        }[self]
    
    @classmethod
    def from_figure(fig: 'Figure', own: 'Mark') -> 'Mark':
        if fig is Figure.EMPTY:
            return Mark.EMPTY
        
        if fig is Figure.OWN:
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
    
    @staticmethod
    def from_mark(mark: Mark, own: Mark) -> 'Figure':
        if mark is Mark.EMPTY:
            return Figure.EMPTY
        elif mark is own:
            return Figure.OWN
        else:
            return Figure.ENEMY

def occupied_or(fig: Mark, alt: T) -> Union[Figure, T]:
    if fig is Mark.EMPTY:
        return alt
    return fig

numpad = [
    7, 8, 9,
    4, 5, 6,
    1, 2, 3,
]

class Field():
    def __init__(self):
        self.field = [Mark.EMPTY] * 9
    
    @classmethod
    def from_raw_field(cls, field: list) -> 'Field':
        field_ = cls()
        field_.field = field
        return field_
    
    def to_field_repr(self, own: 'Mark') -> 'FieldRepr':
        field = [Figure.from_mark(m, own) for m in self.field]
        return FieldRepr.from_raw_field(field)
    
    def __str__(self):
        indexed = list(map(
            lambda fig_i: str(occupied_or(fig_i[0], fig_i[1])),
            zip(self.field, numpad)))
        
        return "\n-----\n".join([
            "|".join(indexed[0:3]),
            "|".join(indexed[3:6]),
            "|".join(indexed[6:9]),
        ])
    
    def __getitem__(self, index: int) -> Mark:
        return self.field[index]
    
    def __setitem__(self, index: int, mark: Mark):
        self.field[index] = mark
            

class FieldRepr():
    def __init__(self):
        self.field = [Figure.EMPTY] * 9
    
    @classmethod
    def from_raw_field(cls, field: list) -> 'FieldRepr':
        field_repr = cls()
        field_repr.field = field
        return field_repr
    
    def __getitem__(self, index: int) -> Figure:
        return self.field[index]
    
    def __setitem__(self, index: int, fig: Figure):
        self.field[index] = fig

class Turner(ABC):
    @abstractmethod
    def choose_turn(self, field: FieldRepr) -> int:
        pass

class Crazy(Turner):
    def choose_turn(self, field: FieldRepr) -> int:
        return random.choice([i for (i, fig) in enumerate(field) if fig is Figure.EMPTY])

numpad_to_coord = {
    7: 0, 8: 1, 9: 2,
    4: 3, 5: 4, 6: 5,
    1: 6, 2: 7, 3: 8,
}

def input_turn(promt: str, int_err: str, bound_err: str) -> int:
    while True:
        try:
            cell = int(input(promt))
        except:
            print(int_err)
            continue
        try:
            coord = numpad_to_coord[cell]
        except:
            print(bound_err)
            continue
        return coord

def unwrap_or(x, alt):
    if x is None:
        return alt
    return x

def unwrap_or_else(x, f):
    if x is None:
        return f()
    return x

class Player(Turner):
    PROMT = "Enter number of cell to make turn: "
    INT_ERR = "You input was not number"
    BOUND_ERR = "Your input was out of border of field"
    OCCUPIED_ERR = "This cell is already occupied"
    
    def __init__(self, *,
            promt:        Optional[str] = None, 
            int_err:      Optional[str] = None, 
            bound_err:    Optional[str] = None, 
            occupied_err: Optional[str] = None):
        self.promt        = unwrap_or(promt,        Player.PROMT)
        self.int_err      = unwrap_or(int_err,      Player.INT_ERR)
        self.bound_err    = unwrap_or(bound_err,    Player.BOUND_ERR)
        self.occupied_err = unwrap_or(occupied_err, Player.OCCUPIED_ERR)
    
    def choose_turn(self, field: FieldRepr) -> int:
        while True:
            coord = input_turn(Player.PROMT, Player.INT_ERR, Player.BOUND_ERR)
            if field[coord] is not Figure.EMPTY:
                print(self.occupied_err)
            else:
                return coord

class Game:
    def __init__(self, *,
        ai = Crazy(),
        player_mark = Mark.X,
        player_is_first = True
    ):
        self.field = Field()
        self.ai = ai
        self.player = Player()
        self.current = int(not player_is_first)
        
        if self.current == 0: #if player's turn is first
            self.marks = [player_mark, player_mark.opposite()]
        else:
            self.marks = [player_mark.opposite(), player_mark]
    
    def draw_board(self):
        print(self.field)
    
    def advance(self) -> bool:
        current = self.current
        turner = [self.player, self.ai][current]
        current_mark = self.marks[current]
        
        # FIXME: check if turn is correct
        field = self.field.to_field_repr(current_mark)
        coord = turner.choose_turn(field)
        self.field[coord] = current_mark
        
        if self.current != 0: #if it is not player's turn
            self.draw_board()

        self.current = 1 - current
        
        # FIXME: check if turn ends the game
        return False
    
if __name__ == "__main__":
    game = Game()
    game.draw_board()
    
    # FIXME: handle gracefully end of game
    while True:
        game.advance()
