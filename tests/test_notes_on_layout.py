from pathlib import Path

import pytest

from pyabc2 import Tune

from concertina_helper.notes_on_layout import NotesOnLayout
from concertina_helper.note_generators import notes_from_tune
from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name

paths = list(Path(__file__).parent.glob('*.abc'))
layout = load_bisonoric_layout_by_name('30_wheatstone_cg')


@pytest.mark.parametrize("path", paths)
def test_get_all_fingerings(path):
    tune = Tune(path.read_text())
    notes = notes_from_tune(tune)
    n_l = NotesOnLayout(notes, layout)
    all_fingerings = n_l.get_all_fingerings()
    assert len(all_fingerings) >= 8
    annotation, f_set = all_fingerings[0]
    assert len(f_set) >= 2
    assert "Annotation(pitch=Pitch(name=" in str(annotation)
    # TODO: Add a stronger assertion when we can get pitches from fingering.
    # https://github.com/mccalluc/concertina-helper/issues/44


@pytest.mark.parametrize("path", paths)
def test_get_best_fingerings(path):
    tune = Tune(path.read_text())
    notes = notes_from_tune(tune)
    n_l = NotesOnLayout(notes, layout)
    best_fingerings = n_l.get_best_fingerings([])
    assert len(best_fingerings) >= 8
    # TODO: Add a stronger assertion when we can get pitches from fingering.
    # https://github.com/mccalluc/concertina-helper/issues/44
