"""Sphinx plugin for Django documentation.

 Copied from the
`Django repo <https://github.com/django/django/blob/main/docs/_ext/djangodocs.py>`_.
"""

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata


def setup(app: Sphinx) -> ExtensionMetadata:
    """Set up Sphinx with the Django crossref types.

    Adds the types `setting`, `ttag`, `tfilter`, `lookup`, and `djadmin` for references.

    Parameters
    ----------
    app : Sphinx
        The Sphinx application.

    Returns
    -------
    ExtensionMetadata
        Metadata from this extension.
    """
    app.add_crossref_type(
        directivename="setting", rolename="setting", indextemplate="pair: %s; setting"
    )
    app.add_crossref_type(
        directivename="templatetag",
        rolename="ttag",
        indextemplate="pair: %s; template tag",
    )
    app.add_crossref_type(
        directivename="templatefilter",
        rolename="tfilter",
        indextemplate="pair: %s; template filter",
    )
    app.add_crossref_type(
        directivename="fieldlookup",
        rolename="lookup",
        indextemplate="pair: %s; field lookup type",
    )
    app.add_object_type(
        directivename="django-admin",
        rolename="djadmin",
        indextemplate="pair: %s; django-admin command",
    )
    return {"parallel_read_safe": True, "parallel_write_safe": True}
