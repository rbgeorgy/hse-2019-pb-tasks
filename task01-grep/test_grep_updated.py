#!/usr/bin/env python3
import io
import sys
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_stdin_regex_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', '-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '4\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_file_regex_grep_count(
        tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '2\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:needle suf\n'


def test_integrate_files_regex_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:the needl\nb.txt:pref needle suf\na.txt:needle suf\n'


def test_integrate_files_regex_grep_count(
        tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', '-E', 'needle?', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:2\na.txt:2\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_format_lines(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.format_lines(
        '', 'needle', sys.stdin, True, False, False, False, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_format_lines_ignore(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nnEedle suf\nthe Needl\npref neEdle suf'))
    grep.format_lines(
        '', 'NeEdLe', sys.stdin, True, False, True, False, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_format_lines_inverse(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.format_lines(
        '', 'needle', sys.stdin, True, False, False, True, False, False, True)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_unit_files_output(capsys):
    str_list = ['needle']
    grep.files_output('temp.txt', str_list, False, True, False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'temp.txt:needle\n'


def test_unit_files_count_output():
    str_list = ['needle']
    assert grep.files_output('temp.txt', str_list, True, True, False) == ['1']
