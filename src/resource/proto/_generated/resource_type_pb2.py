# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: resource_type.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='resource_type.proto',
  package='cafm.identity.resource_type',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13resource_type.proto\x12\x1b\x63\x61\x66m.identity.resource_type\"(\n\x0cResourceType\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\tb\x06proto3'
)




_RESOURCETYPE = _descriptor.Descriptor(
  name='ResourceType',
  full_name='cafm.identity.resource_type.ResourceType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.resource_type.ResourceType.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.identity.resource_type.ResourceType.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=92,
)

DESCRIPTOR.message_types_by_name['ResourceType'] = _RESOURCETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResourceType = _reflection.GeneratedProtocolMessageType('ResourceType', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPE,
  '__module__' : 'resource_type_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceType)
  })
_sym_db.RegisterMessage(ResourceType)


# @@protoc_insertion_point(module_scope)
