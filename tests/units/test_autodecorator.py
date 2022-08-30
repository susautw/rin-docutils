import pytest
from sphinx.ext.autodoc import FunctionDocumenter, ClassDocumenter

from rin.docutils import markers
from rin.docutils.autodecorator import PatchedFunctionDocumenter, PatchedClassDocumenter, \
    PatchedSphinxToolboxClassDocumenter, PatchedDecoratorDocumenter


@markers.decorator
def decorated_function(fn):
    return fn


def normal_function():
    pass


class NormalClass:
    pass


@pytest.mark.parametrize("obj, result", [
    (pytest.lazy_fixture('method_descriptor'), True),
    (NormalClass, False),
    (decorated_function, True),
    (normal_function, False)
])
def test_decorator_documenter__can_document_member(obj, result):
    assert PatchedDecoratorDocumenter.can_document_member(obj, "", False, None) is result


@pytest.mark.parametrize("cls, base_cls, decorated, normal", [
    (PatchedFunctionDocumenter, FunctionDocumenter, decorated_function, normal_function),
    (PatchedClassDocumenter, ClassDocumenter, pytest.lazy_fixture("method_descriptor"), NormalClass),
    (PatchedSphinxToolboxClassDocumenter, ClassDocumenter, pytest.lazy_fixture("method_descriptor"), NormalClass)
])
def test_other_documenter__can_document_member(mocker, cls, base_cls, decorated, normal):
    original_can_document_member = mocker.patch.object(base_cls, 'can_document_member')
    original_can_document_member.return_value = True

    assert not cls.can_document_member(decorated, "", False, None)
    assert cls.can_document_member(normal, "", False, None)

    original_can_document_member.return_value = False
    assert not cls.can_document_member(decorated, "", False, None)
    assert not cls.can_document_member(normal, "", False, None)
