# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: identity/user_app_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from identity import user_pb2 as identity_dot_user__pb2
import order_pb2 as order__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='identity/user_app_service.proto',
  package='cafm.identity.user',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fidentity/user_app_service.proto\x12\x12\x63\x61\x66m.identity.user\x1a\x13identity/user.proto\x1a\x0border.proto\"O\n,UserAppService_userByEmailAndPasswordRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"W\n-UserAppService_userByEmailAndPasswordResponse\x12&\n\x04user\x18\x01 \x01(\x0b\x32\x18.cafm.identity.user.User\",\n\x1eUserAppService_userByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"I\n\x1fUserAppService_userByIdResponse\x12&\n\x04user\x18\x01 \x01(\x0b\x32\x18.cafm.identity.user.User\"q\n\x1bUserAppService_usersRequest\x12\x13\n\x0bresult_from\x18\x01 \x01(\x05\x12\x13\n\x0bresult_size\x18\x02 \x01(\x05\x12(\n\x06orders\x18\x03 \x03(\x0b\x32\x18.cafm.common.order.Order\"a\n\x1cUserAppService_usersResponse\x12\'\n\x05users\x18\x01 \x03(\x0b\x32\x18.cafm.identity.user.User\x12\x18\n\x10total_item_count\x18\x02 \x01(\x05\"\x1d\n\x1bUserAppService_newIdRequest\"*\n\x1cUserAppService_newIdResponse\x12\n\n\x02id\x18\x01 \x01(\t\"?\n,UserAppService_userHasOneTimePasswordRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"N\n-UserAppService_userHasOneTimePasswordResponse\x12\x1d\n\x15has_one_time_password\x18\x01 \x01(\x08\x32\xb2\x05\n\x0eUserAppService\x12\xa3\x01\n\x1auser_by_email_and_password\x12@.cafm.identity.user.UserAppService_userByEmailAndPasswordRequest\x1a\x41.cafm.identity.user.UserAppService_userByEmailAndPasswordResponse\"\x00\x12w\n\nuser_by_id\x12\x32.cafm.identity.user.UserAppService_userByIdRequest\x1a\x33.cafm.identity.user.UserAppService_userByIdResponse\"\x00\x12l\n\x05users\x12/.cafm.identity.user.UserAppService_usersRequest\x1a\x30.cafm.identity.user.UserAppService_usersResponse\"\x00\x12m\n\x06new_id\x12/.cafm.identity.user.UserAppService_newIdRequest\x1a\x30.cafm.identity.user.UserAppService_newIdResponse\"\x00\x12\xa3\x01\n\x1auser_has_one_time_password\x12@.cafm.identity.user.UserAppService_userHasOneTimePasswordRequest\x1a\x41.cafm.identity.user.UserAppService_userHasOneTimePasswordResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[identity_dot_user__pb2.DESCRIPTOR,order__pb2.DESCRIPTOR,])




_USERAPPSERVICE_USERBYEMAILANDPASSWORDREQUEST = _descriptor.Descriptor(
  name='UserAppService_userByEmailAndPasswordRequest',
  full_name='cafm.identity.user.UserAppService_userByEmailAndPasswordRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='cafm.identity.user.UserAppService_userByEmailAndPasswordRequest.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='cafm.identity.user.UserAppService_userByEmailAndPasswordRequest.password', index=1,
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
  serialized_start=89,
  serialized_end=168,
)


_USERAPPSERVICE_USERBYEMAILANDPASSWORDRESPONSE = _descriptor.Descriptor(
  name='UserAppService_userByEmailAndPasswordResponse',
  full_name='cafm.identity.user.UserAppService_userByEmailAndPasswordResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user', full_name='cafm.identity.user.UserAppService_userByEmailAndPasswordResponse.user', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=170,
  serialized_end=257,
)


_USERAPPSERVICE_USERBYIDREQUEST = _descriptor.Descriptor(
  name='UserAppService_userByIdRequest',
  full_name='cafm.identity.user.UserAppService_userByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.user.UserAppService_userByIdRequest.id', index=0,
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
  serialized_start=259,
  serialized_end=303,
)


_USERAPPSERVICE_USERBYIDRESPONSE = _descriptor.Descriptor(
  name='UserAppService_userByIdResponse',
  full_name='cafm.identity.user.UserAppService_userByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user', full_name='cafm.identity.user.UserAppService_userByIdResponse.user', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=305,
  serialized_end=378,
)


_USERAPPSERVICE_USERSREQUEST = _descriptor.Descriptor(
  name='UserAppService_usersRequest',
  full_name='cafm.identity.user.UserAppService_usersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result_from', full_name='cafm.identity.user.UserAppService_usersRequest.result_from', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result_size', full_name='cafm.identity.user.UserAppService_usersRequest.result_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='orders', full_name='cafm.identity.user.UserAppService_usersRequest.orders', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=380,
  serialized_end=493,
)


_USERAPPSERVICE_USERSRESPONSE = _descriptor.Descriptor(
  name='UserAppService_usersResponse',
  full_name='cafm.identity.user.UserAppService_usersResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='users', full_name='cafm.identity.user.UserAppService_usersResponse.users', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_item_count', full_name='cafm.identity.user.UserAppService_usersResponse.total_item_count', index=1,
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
  serialized_start=495,
  serialized_end=592,
)


_USERAPPSERVICE_NEWIDREQUEST = _descriptor.Descriptor(
  name='UserAppService_newIdRequest',
  full_name='cafm.identity.user.UserAppService_newIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=594,
  serialized_end=623,
)


_USERAPPSERVICE_NEWIDRESPONSE = _descriptor.Descriptor(
  name='UserAppService_newIdResponse',
  full_name='cafm.identity.user.UserAppService_newIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.user.UserAppService_newIdResponse.id', index=0,
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
  serialized_start=625,
  serialized_end=667,
)


_USERAPPSERVICE_USERHASONETIMEPASSWORDREQUEST = _descriptor.Descriptor(
  name='UserAppService_userHasOneTimePasswordRequest',
  full_name='cafm.identity.user.UserAppService_userHasOneTimePasswordRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='cafm.identity.user.UserAppService_userHasOneTimePasswordRequest.user_id', index=0,
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
  serialized_start=669,
  serialized_end=732,
)


_USERAPPSERVICE_USERHASONETIMEPASSWORDRESPONSE = _descriptor.Descriptor(
  name='UserAppService_userHasOneTimePasswordResponse',
  full_name='cafm.identity.user.UserAppService_userHasOneTimePasswordResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='has_one_time_password', full_name='cafm.identity.user.UserAppService_userHasOneTimePasswordResponse.has_one_time_password', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=734,
  serialized_end=812,
)

_USERAPPSERVICE_USERBYEMAILANDPASSWORDRESPONSE.fields_by_name['user'].message_type = identity_dot_user__pb2._USER
_USERAPPSERVICE_USERBYIDRESPONSE.fields_by_name['user'].message_type = identity_dot_user__pb2._USER
_USERAPPSERVICE_USERSREQUEST.fields_by_name['orders'].message_type = order__pb2._ORDER
_USERAPPSERVICE_USERSRESPONSE.fields_by_name['users'].message_type = identity_dot_user__pb2._USER
DESCRIPTOR.message_types_by_name['UserAppService_userByEmailAndPasswordRequest'] = _USERAPPSERVICE_USERBYEMAILANDPASSWORDREQUEST
DESCRIPTOR.message_types_by_name['UserAppService_userByEmailAndPasswordResponse'] = _USERAPPSERVICE_USERBYEMAILANDPASSWORDRESPONSE
DESCRIPTOR.message_types_by_name['UserAppService_userByIdRequest'] = _USERAPPSERVICE_USERBYIDREQUEST
DESCRIPTOR.message_types_by_name['UserAppService_userByIdResponse'] = _USERAPPSERVICE_USERBYIDRESPONSE
DESCRIPTOR.message_types_by_name['UserAppService_usersRequest'] = _USERAPPSERVICE_USERSREQUEST
DESCRIPTOR.message_types_by_name['UserAppService_usersResponse'] = _USERAPPSERVICE_USERSRESPONSE
DESCRIPTOR.message_types_by_name['UserAppService_newIdRequest'] = _USERAPPSERVICE_NEWIDREQUEST
DESCRIPTOR.message_types_by_name['UserAppService_newIdResponse'] = _USERAPPSERVICE_NEWIDRESPONSE
DESCRIPTOR.message_types_by_name['UserAppService_userHasOneTimePasswordRequest'] = _USERAPPSERVICE_USERHASONETIMEPASSWORDREQUEST
DESCRIPTOR.message_types_by_name['UserAppService_userHasOneTimePasswordResponse'] = _USERAPPSERVICE_USERHASONETIMEPASSWORDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserAppService_userByEmailAndPasswordRequest = _reflection.GeneratedProtocolMessageType('UserAppService_userByEmailAndPasswordRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERBYEMAILANDPASSWORDREQUEST,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userByEmailAndPasswordRequest)
  })
_sym_db.RegisterMessage(UserAppService_userByEmailAndPasswordRequest)

UserAppService_userByEmailAndPasswordResponse = _reflection.GeneratedProtocolMessageType('UserAppService_userByEmailAndPasswordResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERBYEMAILANDPASSWORDRESPONSE,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userByEmailAndPasswordResponse)
  })
_sym_db.RegisterMessage(UserAppService_userByEmailAndPasswordResponse)

UserAppService_userByIdRequest = _reflection.GeneratedProtocolMessageType('UserAppService_userByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERBYIDREQUEST,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userByIdRequest)
  })
_sym_db.RegisterMessage(UserAppService_userByIdRequest)

UserAppService_userByIdResponse = _reflection.GeneratedProtocolMessageType('UserAppService_userByIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERBYIDRESPONSE,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userByIdResponse)
  })
_sym_db.RegisterMessage(UserAppService_userByIdResponse)

UserAppService_usersRequest = _reflection.GeneratedProtocolMessageType('UserAppService_usersRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERSREQUEST,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_usersRequest)
  })
_sym_db.RegisterMessage(UserAppService_usersRequest)

UserAppService_usersResponse = _reflection.GeneratedProtocolMessageType('UserAppService_usersResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERSRESPONSE,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_usersResponse)
  })
_sym_db.RegisterMessage(UserAppService_usersResponse)

UserAppService_newIdRequest = _reflection.GeneratedProtocolMessageType('UserAppService_newIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_NEWIDREQUEST,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_newIdRequest)
  })
_sym_db.RegisterMessage(UserAppService_newIdRequest)

UserAppService_newIdResponse = _reflection.GeneratedProtocolMessageType('UserAppService_newIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_NEWIDRESPONSE,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_newIdResponse)
  })
_sym_db.RegisterMessage(UserAppService_newIdResponse)

UserAppService_userHasOneTimePasswordRequest = _reflection.GeneratedProtocolMessageType('UserAppService_userHasOneTimePasswordRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERHASONETIMEPASSWORDREQUEST,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userHasOneTimePasswordRequest)
  })
_sym_db.RegisterMessage(UserAppService_userHasOneTimePasswordRequest)

UserAppService_userHasOneTimePasswordResponse = _reflection.GeneratedProtocolMessageType('UserAppService_userHasOneTimePasswordResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERAPPSERVICE_USERHASONETIMEPASSWORDRESPONSE,
  '__module__' : 'identity.user_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.user.UserAppService_userHasOneTimePasswordResponse)
  })
_sym_db.RegisterMessage(UserAppService_userHasOneTimePasswordResponse)



_USERAPPSERVICE = _descriptor.ServiceDescriptor(
  name='UserAppService',
  full_name='cafm.identity.user.UserAppService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=815,
  serialized_end=1505,
  methods=[
  _descriptor.MethodDescriptor(
    name='user_by_email_and_password',
    full_name='cafm.identity.user.UserAppService.user_by_email_and_password',
    index=0,
    containing_service=None,
    input_type=_USERAPPSERVICE_USERBYEMAILANDPASSWORDREQUEST,
    output_type=_USERAPPSERVICE_USERBYEMAILANDPASSWORDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='user_by_id',
    full_name='cafm.identity.user.UserAppService.user_by_id',
    index=1,
    containing_service=None,
    input_type=_USERAPPSERVICE_USERBYIDREQUEST,
    output_type=_USERAPPSERVICE_USERBYIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='users',
    full_name='cafm.identity.user.UserAppService.users',
    index=2,
    containing_service=None,
    input_type=_USERAPPSERVICE_USERSREQUEST,
    output_type=_USERAPPSERVICE_USERSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='new_id',
    full_name='cafm.identity.user.UserAppService.new_id',
    index=3,
    containing_service=None,
    input_type=_USERAPPSERVICE_NEWIDREQUEST,
    output_type=_USERAPPSERVICE_NEWIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='user_has_one_time_password',
    full_name='cafm.identity.user.UserAppService.user_has_one_time_password',
    index=4,
    containing_service=None,
    input_type=_USERAPPSERVICE_USERHASONETIMEPASSWORDREQUEST,
    output_type=_USERAPPSERVICE_USERHASONETIMEPASSWORDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERAPPSERVICE)

DESCRIPTOR.services_by_name['UserAppService'] = _USERAPPSERVICE

# @@protoc_insertion_point(module_scope)
