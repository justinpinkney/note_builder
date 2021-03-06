from .context import note_builder
from .fixtures import datadir

import os


def test_find_notes(datadir):
    note_files = note_builder.find_notes(datadir)

    assert note_files[0] == datadir.join('note_1.md')
    assert note_files[1] == datadir.join('note_2.md')


def test_load_single_note(datadir):
    note_path = datadir.join('note_1.md')

    note = note_builder.make_note(note_path)

    assert note.name == 'note_1'
    assert note.content == '# Note 1\n\ncontent\n'
    assert note.title == 'Note 1'


def test_load_multiple_notes(datadir):
    note_files = note_builder.find_notes(datadir)
    expected_names = ['note_1', 'note_2']

    notes = note_builder.load_notes(note_files)

    assert len(list(notes)) == 2
    for note, name in zip(notes, expected_names):
        assert note.name == name


def test_html_renderer_filename(datadir):
    note = note_builder.Note(name='note_1', content='# Note 1\n\ncontent\n')
    expected_name = note.name + '.html'
    expected_filename = datadir.join(expected_name)

    renderer = note_builder.HtmlRenderer()
    renderer.render(datadir, [note])

    assert os.path.isfile(expected_filename)


def test_html_content_no_style(datadir):
    note_path = datadir.join('note_1.md')
    note = note_builder.make_note(note_path)
    expected_name = note.name + '.html'
    expected_filename = datadir.join(expected_name)

    renderer = note_builder.HtmlRenderer()
    renderer.render(datadir, [note])

    with open(expected_filename) as output_file:
        with open(datadir.join('note_1_ref.html')) as reference_file:
            for output, reference in zip(output_file, reference_file):
                assert output == reference


def test_html_content_custom_style(datadir):
    note_path = datadir.join('note_1.md')
    note = note_builder.make_note(note_path)
    expected_name = note.name + '.html'
    expected_filename = datadir.join(expected_name)

    renderer = note_builder.HtmlRenderer(css='custom.css')
    renderer.render(datadir, [note])


def test_html_renderer_note_iterable(datadir):
    note_files = note_builder.find_notes(datadir)
    notes = note_builder.load_notes(note_files)
    renderer = note_builder.HtmlRenderer()

    renderer.render(datadir.join('build'), notes)

    assert os.path.isdir(datadir.join('build'))


def test_move_assets(datadir):
    renderer = note_builder.HtmlRenderer(assets=datadir.join('assets'))

    renderer.render(datadir.join('build'), [])

    assert os.path.isfile(datadir.join('build').join('assets').join('asset'))
