# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: resource_type_app_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import resource_type_pb2 as resource__type__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='resource_type_app_service.proto',
  package='cafm.identity.resource_type',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fresource_type_app_service.proto\x12\x1b\x63\x61\x66m.identity.resource_type\x1a\x13resource_type.proto\"@\n0ResourceTypeAppService_resourceTypeByNameRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"t\n1ResourceTypeAppService_resourceTypeByNameResponse\x12?\n\x0cresourceType\x18\x01 \x01(\x0b\x32).cafm.identity.resource_type.ResourceType\"<\n.ResourceTypeAppService_resourceTypeByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"r\n/ResourceTypeAppService_resourceTypeByIdResponse\x12?\n\x0cresourceType\x18\x01 \x01(\x0b\x32).cafm.identity.resource_type.ResourceType\"U\n+ResourceTypeAppService_resourceTypesRequest\x12\x12\n\nresultFrom\x18\x01 \x01(\x05\x12\x12\n\nresultSize\x18\x02 \x01(\x05\"p\n,ResourceTypeAppService_resourceTypesResponse\x12@\n\rresourceTypes\x18\x01 \x03(\x0b\x32).cafm.identity.resource_type.ResourceType2\xab\x04\n\x16ResourceTypeAppService\x12\xb5\x01\n\x12resourceTypeByName\x12M.cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameRequest\x1aN.cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameResponse\"\x00\x12\xaf\x01\n\x10resourceTypeById\x12K.cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdRequest\x1aL.cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdResponse\"\x00\x12\xa6\x01\n\rresourceTypes\x12H.cafm.identity.resource_type.ResourceTypeAppService_resourceTypesRequest\x1aI.cafm.identity.resource_type.ResourceTypeAppService_resourceTypesResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[resource__type__pb2.DESCRIPTOR,])




_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMEREQUEST = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypeByNameRequest',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameRequest.name', index=0,
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
  serialized_start=85,
  serialized_end=149,
)


_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMERESPONSE = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypeByNameResponse',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resourceType', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameResponse.resourceType', index=0,
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
  serialized_start=151,
  serialized_end=267,
)


_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDREQUEST = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypeByIdRequest',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdRequest.id', index=0,
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
  serialized_start=269,
  serialized_end=329,
)


_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDRESPONSE = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypeByIdResponse',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resourceType', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdResponse.resourceType', index=0,
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
  serialized_start=331,
  serialized_end=445,
)


_RESOURCETYPEAPPSERVICE_RESOURCETYPESREQUEST = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypesRequest',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultFrom', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypesRequest.resultFrom', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resultSize', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypesRequest.resultSize', index=1,
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
  serialized_start=447,
  serialized_end=532,
)


_RESOURCETYPEAPPSERVICE_RESOURCETYPESRESPONSE = _descriptor.Descriptor(
  name='ResourceTypeAppService_resourceTypesResponse',
  full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resourceTypes', full_name='cafm.identity.resource_type.ResourceTypeAppService_resourceTypesResponse.resourceTypes', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=534,
  serialized_end=646,
)

_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMERESPONSE.fields_by_name['resourceType'].message_type = resource__type__pb2._RESOURCETYPE
_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDRESPONSE.fields_by_name['resourceType'].message_type = resource__type__pb2._RESOURCETYPE
_RESOURCETYPEAPPSERVICE_RESOURCETYPESRESPONSE.fields_by_name['resourceTypes'].message_type = resource__type__pb2._RESOURCETYPE
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypeByNameRequest'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMEREQUEST
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypeByNameResponse'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMERESPONSE
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypeByIdRequest'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDREQUEST
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypeByIdResponse'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDRESPONSE
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypesRequest'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPESREQUEST
DESCRIPTOR.message_types_by_name['ResourceTypeAppService_resourceTypesResponse'] = _RESOURCETYPEAPPSERVICE_RESOURCETYPESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResourceTypeAppService_resourceTypeByNameRequest = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypeByNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMEREQUEST,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameRequest)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypeByNameRequest)

ResourceTypeAppService_resourceTypeByNameResponse = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypeByNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMERESPONSE,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByNameResponse)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypeByNameResponse)

ResourceTypeAppService_resourceTypeByIdRequest = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypeByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDREQUEST,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdRequest)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypeByIdRequest)

ResourceTypeAppService_resourceTypeByIdResponse = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypeByIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDRESPONSE,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypeByIdResponse)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypeByIdResponse)

ResourceTypeAppService_resourceTypesRequest = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypesRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPESREQUEST,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypesRequest)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypesRequest)

ResourceTypeAppService_resourceTypesResponse = _reflection.GeneratedProtocolMessageType('ResourceTypeAppService_resourceTypesResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCETYPEAPPSERVICE_RESOURCETYPESRESPONSE,
  '__module__' : 'resource_type_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.identity.resource_type.ResourceTypeAppService_resourceTypesResponse)
  })
_sym_db.RegisterMessage(ResourceTypeAppService_resourceTypesResponse)



_RESOURCETYPEAPPSERVICE = _descriptor.ServiceDescriptor(
  name='ResourceTypeAppService',
  full_name='cafm.identity.resource_type.ResourceTypeAppService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=649,
  serialized_end=1204,
  methods=[
  _descriptor.MethodDescriptor(
    name='resourceTypeByName',
    full_name='cafm.identity.resource_type.ResourceTypeAppService.resourceTypeByName',
    index=0,
    containing_service=None,
    input_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMEREQUEST,
    output_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYNAMERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='resourceTypeById',
    full_name='cafm.identity.resource_type.ResourceTypeAppService.resourceTypeById',
    index=1,
    containing_service=None,
    input_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDREQUEST,
    output_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPEBYIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='resourceTypes',
    full_name='cafm.identity.resource_type.ResourceTypeAppService.resourceTypes',
    index=2,
    containing_service=None,
    input_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPESREQUEST,
    output_type=_RESOURCETYPEAPPSERVICE_RESOURCETYPESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RESOURCETYPEAPPSERVICE)

DESCRIPTOR.services_by_name['ResourceTypeAppService'] = _RESOURCETYPEAPPSERVICE

# @@protoc_insertion_point(module_scope)
