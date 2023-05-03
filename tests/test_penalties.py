from concertina_helper.layouts.bisonoric import (
    AnnotatedBisonoricFingering,
    BisonoricFingering,
    UnisonoricFingering,
    Direction)
from concertina_helper.type_defs import Mask
from concertina_helper.layouts.layout_loader import (
    load_bisonoric_layout_by_name)
from concertina_helper.penalties import (
    penalize_bellows_change, penalize_finger_in_same_column,
    penalize_pull_at_start_of_measure)


layout = load_bisonoric_layout_by_name('30_wheatstone_cg')


def make_mask(half_shape: list[int], row: int, column: int) -> Mask:
    return Mask(
        tuple(
            tuple(
                # For debugging:
                # f'{x},{y}'
                row == y and column == x
                for x
                in range(row_len)
            )
            for y, row_len
            in enumerate(half_shape)
        )
    )


def test_make_mask():
    assert make_mask([1, 2], 1, 1).bool_matrix == ((False,), (False, True))
    assert make_mask([1, 2], 1, 0).bool_matrix == ((False,), (True, False))
    assert make_mask([1, 2], 0, 0).bool_matrix == ((True,), (False, False))

c_left = AnnotatedBisonoricFingering(
    fingering=BisonoricFingering(Direction.PUSH, UnisonoricFingering(
        layout.push_layout, make_mask(layout.shape[0], 1, 2), make_mask(layout.shape[1], -1, -1) 
    )),
    measure=1
)
a_left = AnnotatedBisonoricFingering(
    fingering=BisonoricFingering(Direction.PULL, UnisonoricFingering(
        layout.pull_layout, make_mask(layout.shape[0], 2, 2), make_mask(layout.shape[1], -1, -1)
    )),
    measure=2
)

def test_fixture_values():
    assert str(c_left) == \
        '''Measure 1
PUSH:
--- --- --- --- ---    --- --- --- --- ---
--- --- C4  --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---'''
    assert str(a_left) == \
        '''Measure 2
PULL:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---
--- --- A4  --- ---    --- --- --- --- ---'''

def test_penalize_bellows_change():
    assert penalize_bellows_change(42)(c_left, c_left) == 0
    assert penalize_bellows_change(42)(c_left, a_left) == 42


def test_penalize_finger_in_same_column():
    assert penalize_finger_in_same_column(42)(c_left, c_left) == 42
    assert penalize_finger_in_same_column(42)(c_left, a_left) == 42


def test_penalize_pull_at_start_of_measure():
    assert penalize_pull_at_start_of_measure(42)(c_left, c_left) == 0
    assert penalize_pull_at_start_of_measure(42)(c_left, a_left) == 42
