# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: identity/project_includes_realms_include_users_include_roles.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from identity import realm_includes_users_include_roles_pb2 as identity_dot_realm__includes__users__include__roles__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='identity/project_includes_realms_include_users_include_roles.proto',
  package='cafm.identity.policy',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nBidentity/project_includes_realms_include_users_include_roles.proto\x12\x14\x63\x61\x66m.identity.policy\x1a\x31identity/realm_includes_users_include_roles.proto\"\xab\x01\n-ProjectIncludesRealmsIncludeUsersIncludeRoles\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12`\n\"realm_includes_users_include_roles\x18\x04 \x03(\x0b\x32\x34.cafm.identity.policy.RealmIncludesUsersIncludeRolesb\x06proto3'
  ,
  dependencies=[identity_dot_realm__includes__users__include__roles__pb2.DESCRIPTOR,])




_PROJECTINCLUDESREALMSINCLUDEUSERSINCLUDEROLES = _descriptor.Descriptor(
  name='ProjectIncludesRealmsIncludeUsersIncludeRoles',
  full_name='cafm.identity.policy.ProjectIncludesRealmsIncludeUsersIncludeRoles',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.policy.ProjectIncludesRealmsIncludeUsersIncludeRoles.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.identity.policy.ProjectIncludesRealmsIncludeUsersIncludeRoles.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='realm_includes_users_include_roles', full_name='cafm.identity.policy.ProjectIncludesRealmsIncludeUsersIncludeRoles.realm_includes_users_include_roles', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=144,
  serialized_end=315,
)

_PROJECTINCLUDESREALMSINCLUDEUSERSINCLUDEROLES.fields_by_name['realm_includes_users_include_roles'].message_type = identity_dot_realm__includes__users__include__roles__pb2._REALMINCLUDESUSERSINCLUDEROLES
DESCRIPTOR.message_types_by_name['ProjectIncludesRealmsIncludeUsersIncludeRoles'] = _PROJECTINCLUDESREALMSINCLUDEUSERSINCLUDEROLES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProjectIncludesRealmsIncludeUsersIncludeRoles = _reflection.GeneratedProtocolMessageType('ProjectIncludesRealmsIncludeUsersIncludeRoles', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTINCLUDESREALMSINCLUDEUSERSINCLUDEROLES,
  '__module__' : 'identity.project_includes_realms_include_users_include_roles_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.policy.ProjectIncludesRealmsIncludeUsersIncludeRoles)
  })
_sym_db.RegisterMessage(ProjectIncludesRealmsIncludeUsersIncludeRoles)


# @@protoc_insertion_point(module_scope)
