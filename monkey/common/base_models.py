import json
from typing import Sequence

from pydantic import BaseModel, Extra, ValidationError


class InfectionMonkeyModelConfig:
    allow_mutation = False
    underscore_attrs_are_private = True
    extra = Extra.forbid


class MutableInfectionMonkeyModelConfig(InfectionMonkeyModelConfig):
    allow_mutation = True
    validate_assignment = True


class InfectionMonkeyBaseModel(BaseModel):
    class Config(InfectionMonkeyModelConfig):
        pass

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
        except ValidationError as err:
            # TLDR: This exception handler allows users of this class to be decoupled from pydantic.
            #
            # When validation of a pydantic object fails, pydantic raises a `ValidationError`, which
            # is a `ValueError`, even if the real cause was a `TypeError`. Furthermore, allowing
            # `pydantic.ValueError` to be raised would couple other modules to pydantic, which is
            # undesirable. This exception handler re-raises the first validation error that pydantic
            # encountered. This allows users of these models to `except` `TypeError` or `ValueError`
            # and handle them. Pydantic-specific errors are still raised, but they inherit from
            # `TypeError` or `ValueError`.
            e = err.raw_errors[0]
            while isinstance(e, Sequence):
                e = e[0]
            error = e.exc
            if hasattr(e, "_loc"):
                error.args = (f"{e._loc} {error}",)
            raise error

    # We need to be able to convert our models to fully simplified dictionaries. The
    # `BaseModel.dict()` does not support this. There is a proposal to add a `simplify` keyword
    # argument to `dict()` to support this. See
    # https://github.com/pydantic/pydantic/issues/951#issuecomment-552463606. The hope is that we
    # can override `dict()` with an implementation of `simplify` and remove it when the feature gets
    # merged. If the feature doesn't get merged, or the interface is changed, this function can
    # continue to serve as a wrapper until we can update all references to it.
    def dict(self, simplify=False, **kwargs):
        if simplify:
            # Allow keyword arguments to be passed to `json()`
            # We can pass kwargs to `json()` because the parameters of BaseModel.json() are a
            # superset of those of BaseModel.dict().
            return json.loads(self.json(**kwargs))
        return BaseModel.dict(self, **kwargs)


class MutableInfectionMonkeyBaseModel(InfectionMonkeyBaseModel):
    class Config(MutableInfectionMonkeyModelConfig):
        pass
