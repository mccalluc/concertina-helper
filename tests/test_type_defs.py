import pytest

from concertina_helper.type_defs import Mask, Pitch


def test_mask_union_mixed_types():
    with pytest.raises(TypeError):
        Mask(((True,),)) | 'not a mask!'


def test_mask_union_mixed_shapes():
    with pytest.raises(ValueError):
        Mask(((True,),)) | Mask(((True, False),))


def test_enharmonic():
    assert Pitch('A#3') == Pitch('Bb3')


def test_compare_pitch_to_other():
    with pytest.raises(TypeError, match=r'mixed operand types'):
        assert Pitch('C') != 'not a pitch'
