from pathlib import Path

from pyabc2 import Tune

from concertina_helper.tune_on_layout import TuneOnLayout
from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name

tune = Tune(Path('tests/g-major.abc').read_text())
layout = load_bisonoric_layout_by_name('30_wheatstone_cg')


def test_get_all_fingerings():
    t_l = TuneOnLayout(tune, layout)
    all_fingerings = t_l.get_all_fingerings()
    assert len(all_fingerings) == 8
    annotation, f_set = all_fingerings[0]
    assert len(f_set) == 3
    assert str(annotation) == "Annotation(pitch=Pitch(name='G4'), measure=1)"
    # TODO: Add a stronger assertion when we can get pitches from fingering.
    # https://github.com/mccalluc/concertina-helper/issues/44


def test_get_best_fingerings():
    t_l = TuneOnLayout(tune, layout)
    best_fingerings = t_l.get_best_fingerings([])
    assert len(best_fingerings) == 8
    # TODO: Add a stronger assertion when we can get pitches from fingering.
    # https://github.com/mccalluc/concertina-helper/issues/44
