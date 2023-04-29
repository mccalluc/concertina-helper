from pathlib import Path

from pyabc2 import Tune

from concertina_helper.tune_on_layout import TuneOnLayout
from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name

tune = Tune(Path('tests/g-major.abc').read_text())
wheatstone_cg_layout = load_bisonoric_layout_by_name('wheatstone_cg')

def test_get_all_fingerings():
    t_l = TuneOnLayout(tune, wheatstone_cg_layout)
    all_fingerings = t_l.get_all_fingerings()
    assert len(all_fingerings) == 8
    assert len(all_fingerings[0]) == 3
    # TODO: Add a stronger assertion when we can get pitches from layout.


def test_get_best_fingerings():
    t_l = TuneOnLayout(tune, wheatstone_cg_layout)
    best_fingerings = t_l.get_best_fingerings()
    assert len(best_fingerings) == 8
    # TODO: Add a stronger assertion when we can get pitches from layout.
