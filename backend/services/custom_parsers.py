from typing import Any, Dict, cast, Set

from django.core.exceptions import ValidationError
from django.http import QueryDict
from formencode.variabledecode import variable_decode
from rest_framework import parsers


class CustomMultiParser(parsers.MultiPartParser):
    def parse(self, stream: Any, media_type: Any = None, parser_context: Any = None) -> Dict[str, Any]:
        result = cast(parsers.DataAndFiles, super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        ))

        _data_keys: Set[str] = set(result.data.keys())
        _file_keys: Set[str] = set(result.files.keys())

        _intersect = _file_keys.intersection(_data_keys)
        if len(_intersect) > 0:
            raise ValidationError('files and data had intersection on keys: ' + str(_intersect))

        # merge everything together
        merged = QueryDict(mutable=True)
        merged.update(result.data)
        merged.update(result.files)  # type: ignore
        # decode it together
        decoded_merged = variable_decode(merged)
        parser_context['__JSON_AS_STRING__'] = True
        decoded_merged = self.decode_nested(decoded_merged)
        if len(result.files) > 0:
            # if we had at least one file put everything into files so we
            # later know we had at least one file by running len(request.FILES)
            parser_context['request'].META['REQUEST_HAD_FILES'] = True
            return parsers.DataAndFiles(decoded_merged, {})  # type: ignore
        else:
            # just put it into data, doesnt matter really otherwise
            return parsers.DataAndFiles(decoded_merged, {})  # type: ignore

    @staticmethod
    def decode_nested(decoded_data: dict) -> dict:
        return decoded_data
