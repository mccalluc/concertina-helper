import pytest

from concertina_helper.type_defs import Mask


def test_mask_union_mixed_types():
    with pytest.raises(TypeError):
        Mask(((True,),)) | 'not a mask!'


def test_mask_union_mixed_shapes():
    with pytest.raises(ValueError):
        Mask(((True,),)) | Mask(((True, False),))
