# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: identity/unhashed_key.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="identity/unhashed_key.proto",
    package="cafm.identity.authz",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x1bidentity/unhashed_key.proto\x12\x13\x63\x61\x66m.identity.authz"\x1a\n\x0bUnhashedKey\x12\x0b\n\x03key\x18\x01 \x01(\tb\x06proto3',
)


_UNHASHEDKEY = _descriptor.Descriptor(
    name="UnhashedKey",
    full_name="cafm.identity.authz.UnhashedKey",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="key",
            full_name="cafm.identity.authz.UnhashedKey.key",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=52,
    serialized_end=78,
)

DESCRIPTOR.message_types_by_name["UnhashedKey"] = _UNHASHEDKEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UnhashedKey = _reflection.GeneratedProtocolMessageType(
    "UnhashedKey",
    (_message.Message,),
    {
        "DESCRIPTOR": _UNHASHEDKEY,
        "__module__": "identity.unhashed_key_pb2"
        # @@protoc_insertion_point(class_scope:cafm.identity.authz.UnhashedKey)
    },
)
_sym_db.RegisterMessage(UnhashedKey)


# @@protoc_insertion_point(module_scope)
