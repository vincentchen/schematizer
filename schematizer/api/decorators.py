# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime

from pyramid.httpexceptions import exception_response
from pyramid.httpexceptions import HTTPException


def handle_view_exception(exception, status_code, error_message=None):
    def handle_view_exception_decorator(func):
        def handle_exception(request):
            try:
                return func(request)
            except exception as e:
                if not isinstance(e, HTTPException):
                    raise exception_response(
                        status_code,
                        detail=error_message or repr(e)
                    )
                else:
                    raise e
        return handle_exception
    return handle_view_exception_decorator


def _transform_datetime_field(response):
    if isinstance(response, dict):
        for key, value in response.iteritems():
            if isinstance(value, datetime):
                response[key] = value.isoformat()
            elif isinstance(value, dict):
                _transform_datetime_field(value)


def _dict_filter_out_none_values(input_dict):
    """Filters out dict entries whose values are None.
    Views are expected to use this function so that they don't return back
    dict responses with None values, since `null` entries aren't supported by
    the swagger schema.

    See https://jira.yelpcorp.com/browse/PSHIP-4692 for more info.
    """
    if isinstance(input_dict, dict):
        for key in input_dict.keys():
            if input_dict[key] is None:
                del input_dict[key]
            elif isinstance(input_dict[key], dict):
                _dict_filter_out_none_values(input_dict[key])


DEFAULT_TRANSFORMERS = [
    _transform_datetime_field,
    _dict_filter_out_none_values
]


def transform_api_response(transformers=DEFAULT_TRANSFORMERS):
    """ Transform an api response with a given list of transformation
    functions.
    """
    def serialize_response_decorator(func):
        def serialize_response_func(request):
            response = func(request)
            if isinstance(response, list):
                for item in response:
                    for transformer in transformers:
                        transformer(item)
            else:
                for transformer in transformers:
                    transformer(response)
            return response
        return serialize_response_func
    return serialize_response_decorator
