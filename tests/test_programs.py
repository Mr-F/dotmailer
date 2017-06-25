import pytest
from dotmailer.programs import Program


def test_get_all(connection):
    response = Program.get_all()
    assert type(response) is list
    if len(response) > 0:
        assert response[0].id is not None


def test_get_id(connection):
    response = Program.get_all()
    if len(response) < 1:
        assert False, 'Unable to test as no programs exists'
    id = response[0].id
    program = Program.get_by_id(id)
    assert type(program) is Program
    assert program.name == response[0].name
    assert program.status == response[0].status
    assert program.date_created == response[0].date_created


def test_invalid_get_id(connection):
    with pytest.raises(Exception):
        Program.get_multiple(0)
