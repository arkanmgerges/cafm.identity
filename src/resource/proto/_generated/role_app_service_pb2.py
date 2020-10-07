# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: role_app_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='role_app_service.proto',
  package='cafm.identity.role',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16role_app_service.proto\x12\x12\x63\x61\x66m.identity.role\"0\n RoleAppService_roleByNameRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"=\n!RoleAppService_roleByNameResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"E\n\x1bRoleAppService_rolesRequest\x12\x12\n\nresultFrom\x18\x01 \x01(\x05\x12\x12\n\nresultSize\x18\x02 \x01(\x05\"0\n\x1cRoleAppService_rolesResponse\x12\x10\n\x08response\x18\x01 \x01(\t2\xfb\x01\n\x0eRoleAppService\x12{\n\nroleByName\x12\x34.cafm.identity.role.RoleAppService_roleByNameRequest\x1a\x35.cafm.identity.role.RoleAppService_roleByNameResponse\"\x00\x12l\n\x05roles\x12/.cafm.identity.role.RoleAppService_rolesRequest\x1a\x30.cafm.identity.role.RoleAppService_rolesResponse\"\x00\x62\x06proto3'
)




_ROLEAPPSERVICE_ROLEBYNAMEREQUEST = _descriptor.Descriptor(
  name='RoleAppService_roleByNameRequest',
  full_name='cafm.identity.role.RoleAppService_roleByNameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.identity.role.RoleAppService_roleByNameRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=46,
  serialized_end=94,
)


_ROLEAPPSERVICE_ROLEBYNAMERESPONSE = _descriptor.Descriptor(
  name='RoleAppService_roleByNameResponse',
  full_name='cafm.identity.role.RoleAppService_roleByNameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.role.RoleAppService_roleByNameResponse.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.identity.role.RoleAppService_roleByNameResponse.name', index=1,
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
  serialized_start=96,
  serialized_end=157,
)


_ROLEAPPSERVICE_ROLESREQUEST = _descriptor.Descriptor(
  name='RoleAppService_rolesRequest',
  full_name='cafm.identity.role.RoleAppService_rolesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultFrom', full_name='cafm.identity.role.RoleAppService_rolesRequest.resultFrom', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resultSize', full_name='cafm.identity.role.RoleAppService_rolesRequest.resultSize', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=159,
  serialized_end=228,
)


_ROLEAPPSERVICE_ROLESRESPONSE = _descriptor.Descriptor(
  name='RoleAppService_rolesResponse',
  full_name='cafm.identity.role.RoleAppService_rolesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='cafm.identity.role.RoleAppService_rolesResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=230,
  serialized_end=278,
)

DESCRIPTOR.message_types_by_name['RoleAppService_roleByNameRequest'] = _ROLEAPPSERVICE_ROLEBYNAMEREQUEST
DESCRIPTOR.message_types_by_name['RoleAppService_roleByNameResponse'] = _ROLEAPPSERVICE_ROLEBYNAMERESPONSE
DESCRIPTOR.message_types_by_name['RoleAppService_rolesRequest'] = _ROLEAPPSERVICE_ROLESREQUEST
DESCRIPTOR.message_types_by_name['RoleAppService_rolesResponse'] = _ROLEAPPSERVICE_ROLESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RoleAppService_roleByNameRequest = _reflection.GeneratedProtocolMessageType('RoleAppService_roleByNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _ROLEAPPSERVICE_ROLEBYNAMEREQUEST,
  '__module__' : 'role_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.role.RoleAppService_roleByNameRequest)
  })
_sym_db.RegisterMessage(RoleAppService_roleByNameRequest)

RoleAppService_roleByNameResponse = _reflection.GeneratedProtocolMessageType('RoleAppService_roleByNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLEAPPSERVICE_ROLEBYNAMERESPONSE,
  '__module__' : 'role_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.role.RoleAppService_roleByNameResponse)
  })
_sym_db.RegisterMessage(RoleAppService_roleByNameResponse)

RoleAppService_rolesRequest = _reflection.GeneratedProtocolMessageType('RoleAppService_rolesRequest', (_message.Message,), {
  'DESCRIPTOR' : _ROLEAPPSERVICE_ROLESREQUEST,
  '__module__' : 'role_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.role.RoleAppService_rolesRequest)
  })
_sym_db.RegisterMessage(RoleAppService_rolesRequest)

RoleAppService_rolesResponse = _reflection.GeneratedProtocolMessageType('RoleAppService_rolesResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLEAPPSERVICE_ROLESRESPONSE,
  '__module__' : 'role_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.role.RoleAppService_rolesResponse)
  })
_sym_db.RegisterMessage(RoleAppService_rolesResponse)



_ROLEAPPSERVICE = _descriptor.ServiceDescriptor(
  name='RoleAppService',
  full_name='cafm.identity.role.RoleAppService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=281,
  serialized_end=532,
  methods=[
  _descriptor.MethodDescriptor(
    name='roleByName',
    full_name='cafm.identity.role.RoleAppService.roleByName',
    index=0,
    containing_service=None,
    input_type=_ROLEAPPSERVICE_ROLEBYNAMEREQUEST,
    output_type=_ROLEAPPSERVICE_ROLEBYNAMERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='roles',
    full_name='cafm.identity.role.RoleAppService.roles',
    index=1,
    containing_service=None,
    input_type=_ROLEAPPSERVICE_ROLESREQUEST,
    output_type=_ROLEAPPSERVICE_ROLESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ROLEAPPSERVICE)

DESCRIPTOR.services_by_name['RoleAppService'] = _ROLEAPPSERVICE

# @@protoc_insertion_point(module_scope)
