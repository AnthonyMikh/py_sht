import random
from enum import Enum, unique
from abc import ABC, abstractmethod
from typing import Union, Optional, TypeVar, List, Dict, Tuple
from itertools import islice

T = TypeVar('T')
Line = Dict[int, T]

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

PutResult = Tuple[bool, Optional[Mark]]
MarkLine = Line[Mark]

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

FigLine = Line[Figure]

def occupied_or(fig: Mark, alt: T) -> Union[Figure, T]:
    if fig is Mark.EMPTY:
        return alt
    return fig

def slice_indexed(l: List[T], s: slice) -> Line[T]:
    return dict(islice(enumerate(l), *s.indices(len(l))))

def slice_row(l: List[T], index: int, err_msg: str) -> Line[T]:
    if index in [0, 1, 2]: return slice_indexed(l, slice(0, 3))    
    if index in [3, 4, 5]: return slice_indexed(l, slice(3, 6))    
    if index in [6, 7, 8]: return slice_indexed(l, slice(6, 9))
    
    raise IndexError(err_msg)

def slice_col(l: List[T], index: int, err_msg: str) -> Line[T]:
    if index in [0, 3, 6]: return slice_indexed(l, slice(0, None, 3))
    if index in [1, 4, 7]: return slice_indexed(l, slice(1, None, 3))
    if index in [2, 5, 8]: return slice_indexed(l, slice(2, None, 3))
    
    raise IndexError(err_msg)

def slice_diags(l: List[T], index: int, err_msg: str) -> List[Line[T]]:
    if index < 0 or index > 8:
        raise IndexError(err_msg)

    segments = []
    
    if index in [0, 4, 8]:
        segments.append(slice_indexed(l, slice(0, 9, 4)))
    if index in [2, 4, 6]:
        segments.append(slice_indexed(l, slice(2, 8, 2)))
    
    return segments

def is_filled_with(seg: Line[T], elem: T) -> bool:
    return all(x is elem for x in seg.values())

class Board():
    IDX_ERR = "Board is indexable by integers in range [0, 8] only"
    
    numpad = [
        7, 8, 9,
        4, 5, 6,
        1, 2, 3,
    ]
    
    def __init__(self):
        self.board = [Mark.EMPTY] * 9
        self.count = 0
    
    @classmethod
    def from_raw_board(cls, board: list) -> 'Board':
        assert(len(board) == 9)
        board_ = cls()
        board_.board = board
        return board_
    
    @classmethod
    def check(cls, index: int):
        if index < 0 or index > 8:
            raise IndexError(cls.IDX_ERR)
    
    def to_board_repr(self, own: 'Mark') -> 'BoardRepr':
        board = [Figure.from_mark(m, own) for m in self.board]
        return BoardRepr.from_raw_board(board)
    
    def __str__(self):
        indexed = list(map(
            lambda fig_i: str(occupied_or(fig_i[0], fig_i[1])),
            zip(self.board, Board.numpad)))
        
        return "\n-----\n".join([
            "|".join(indexed[0:3]),
            "|".join(indexed[3:6]),
            "|".join(indexed[6:9]),
        ])
    
    def __getitem__(self, index: int) -> Mark:
        Board.check(index)
        return self.board[index]
    
    def __setitem__(self, index: int, mark: Mark):
        Board.check(index)
        self.board[index] = mark
    
    def row(self, index: int) -> MarkLine:
        return slice_row(self.board, index, Board.IDX_ERR)
    
    def col(self, index: int) -> MarkLine:
        return slice_col(self.board, index, Board.IDX_ERR)
    
    def diags(self, index: int) -> List[MarkLine]:
        return slice_diags(self.board, index, Board.IDX_ERR)
    
    def dirs(self, index: int) -> List[MarkLine]:
        return [self.row(index), self.col(index), *self.diags(index)]
    
    def put_mark(self, index: int, mark: Mark) -> PutResult:
        if self[index] is Mark.EMPTY:
            self.count += 1
        
        self[index] = mark
        stuck = self.count == 9
        winner = None
        if any(is_filled_with(line, mark) for line in self.dirs(index)):
            winner = Mark
        
        return (stuck, winner)


def is_completing_line(line: Line[T], idx: int, elem: T, empty: T) -> bool:
    return all(x is elem for (i, x) in line.items() if i != idx) and\
        line[idx] is empty

def is_winning_line(seg: FigLine, idx: int) -> bool:
    return is_completing_line(seg, idx, Figure.OWN,   Figure.EMPTY)

def is_losing_line(seg: FigLine, idx: int) -> bool:
    return is_completing_line(seg, idx, Figure.ENEMY, Figure.EMPTY)

class BoardRepr():
    IDX_ERR = "BoardRepr is indexable by integers in range [0, 8] only"
    
    def __init__(self):
        self.board = [Figure.EMPTY] * 9
    
    @classmethod
    def from_raw_board(cls, board: list) -> 'BoardRepr':
        assert(len(board) == 9)
        board_repr = cls()
        board_repr.board = board
        return board_repr
    
    @classmethod
    def check(cls, index: int):
        if index < 0 or index > 8:
            raise IndexError(cls.IDX_ERR)
    
    def __getitem__(self, index: int) -> Figure:
        BoardRepr.check(index)
        return self.board[index]
    
    def __setitem__(self, index: int, fig: Figure):
        BoardRepr.check(index)
        self.board[index] = fig
    
    def row(self, index: int) -> MarkLine:
        return slice_row(self.board, index, Board.IDX_ERR)

    def col(self, index: int) -> MarkLine:
        return slice_col(self.board, index, Board.IDX_ERR)    

    def diags(self, index: int) -> List[MarkLine]:
        return slice_diags(self.board, index, Board.IDX_ERR)
    
    def dirs(self, index: int) -> List[FigLine]:
        return [self.row(index), self.col(index), *self.diags(index)]

class Turner(ABC):
    @abstractmethod
    def choose_turn(self, board: BoardRepr) -> int:
        pass

class Crazy(Turner):
    def choose_turn(self, board: BoardRepr) -> int:
        return random.choice([i for (i, fig) in enumerate(board) if fig is Figure.EMPTY])

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
            print(int_err, end = "")
            continue
        try:
            coord = numpad_to_coord[cell]
        except:
            print(bound_err, end = "")
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
    BOUND_ERR = "Your input was out of border of board"
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
    
    def choose_turn(self, board: BoardRepr) -> int:
        while True:
            coord = input_turn(Player.PROMT, Player.INT_ERR, Player.BOUND_ERR)
            if board[coord] is not Figure.EMPTY:
                print(self.occupied_err, end = "")
            else:
                return coord

class Game:
    def __init__(self, *,
        player0: Turner = Player(),
        player1: Turner = Crazy(),
        player0_mark: Mark = Mark.X,
        player0_is_first: bool = True
    ):
        self.board = Board()
        self.players = [(player0, player0_mark),
                        (player1, player0_mark.opposite())]
        self.current = 0 if player0_is_first else 1
    
    def draw_board(self):
        print()
        print(self.board, end = "")
        print()
    
    def advance(self, draw_board: bool) -> Tuple[bool, Optional[int]]:
        current = self.current
        turner, current_mark = self.players[current]
        
        # FIXME: check if turn is correct
        board = self.board.to_board_repr(current_mark)
        coord = turner.choose_turn(board)
        stuck, completed = self.board.put_mark(coord, current_mark)
        
        if draw_board:
            self.draw_board()
        
        winner = current if completed is not None else None
        self.current = 1 - current
        
        return (stuck, winner)

if __name__ == "__main__":
    game = Game()
    game.draw_board()
    
    while True:
        redraw = game.current == 1
        stuck, winner = game.advance(draw_board = redraw)
        if winner == 0:
            if not redraw:
                game.draw_board()
            print("You won!")
            break
        if winner == 1:
            if not redraw:
                game.draw_board()            
            print("You lost")
            break
        if stuck:
            if not redraw:
                game.draw_board()            
            game.draw_board()
            print("Draw")
            break
