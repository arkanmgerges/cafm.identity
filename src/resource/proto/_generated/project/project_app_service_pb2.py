# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: project/project_app_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from project import project_pb2 as project_dot_project__pb2
import order_pb2 as order__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='project/project_app_service.proto',
  package='cafm.project.project',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!project/project_app_service.proto\x12\x14\x63\x61\x66m.project.project\x1a\x15project/project.proto\x1a\x0border.proto\"6\n&ProjectAppService_projectByNameRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"Y\n\'ProjectAppService_projectByNameResponse\x12.\n\x07project\x18\x01 \x01(\x0b\x32\x1d.cafm.project.project.Project\"2\n$ProjectAppService_projectByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"W\n%ProjectAppService_projectByIdResponse\x12.\n\x07project\x18\x01 \x01(\x0b\x32\x1d.cafm.project.project.Project\"t\n!ProjectAppService_projectsRequest\x12\x12\n\nresultFrom\x18\x01 \x01(\x05\x12\x12\n\nresultSize\x18\x02 \x01(\x05\x12\'\n\x05order\x18\x03 \x03(\x0b\x32\x18.cafm.common.order.Order\"m\n\"ProjectAppService_projectsResponse\x12/\n\x08projects\x18\x01 \x03(\x0b\x32\x1d.cafm.project.project.Project\x12\x16\n\x0etotalItemCount\x18\x02 \x01(\x05\x32\xb0\x03\n\x11ProjectAppService\x12\x8e\x01\n\rprojectByName\x12<.cafm.project.project.ProjectAppService_projectByNameRequest\x1a=.cafm.project.project.ProjectAppService_projectByNameResponse\"\x00\x12\x88\x01\n\x0bprojectById\x12:.cafm.project.project.ProjectAppService_projectByIdRequest\x1a;.cafm.project.project.ProjectAppService_projectByIdResponse\"\x00\x12\x7f\n\x08projects\x12\x37.cafm.project.project.ProjectAppService_projectsRequest\x1a\x38.cafm.project.project.ProjectAppService_projectsResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[project_dot_project__pb2.DESCRIPTOR,order__pb2.DESCRIPTOR,])




_PROJECTAPPSERVICE_PROJECTBYNAMEREQUEST = _descriptor.Descriptor(
  name='ProjectAppService_projectByNameRequest',
  full_name='cafm.project.project.ProjectAppService_projectByNameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='cafm.project.project.ProjectAppService_projectByNameRequest.name', index=0,
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
  serialized_start=95,
  serialized_end=149,
)


_PROJECTAPPSERVICE_PROJECTBYNAMERESPONSE = _descriptor.Descriptor(
  name='ProjectAppService_projectByNameResponse',
  full_name='cafm.project.project.ProjectAppService_projectByNameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='cafm.project.project.ProjectAppService_projectByNameResponse.project', index=0,
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
  serialized_end=240,
)


_PROJECTAPPSERVICE_PROJECTBYIDREQUEST = _descriptor.Descriptor(
  name='ProjectAppService_projectByIdRequest',
  full_name='cafm.project.project.ProjectAppService_projectByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cafm.project.project.ProjectAppService_projectByIdRequest.id', index=0,
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
  serialized_start=242,
  serialized_end=292,
)


_PROJECTAPPSERVICE_PROJECTBYIDRESPONSE = _descriptor.Descriptor(
  name='ProjectAppService_projectByIdResponse',
  full_name='cafm.project.project.ProjectAppService_projectByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='cafm.project.project.ProjectAppService_projectByIdResponse.project', index=0,
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
  serialized_start=294,
  serialized_end=381,
)


_PROJECTAPPSERVICE_PROJECTSREQUEST = _descriptor.Descriptor(
  name='ProjectAppService_projectsRequest',
  full_name='cafm.project.project.ProjectAppService_projectsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultFrom', full_name='cafm.project.project.ProjectAppService_projectsRequest.resultFrom', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resultSize', full_name='cafm.project.project.ProjectAppService_projectsRequest.resultSize', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='cafm.project.project.ProjectAppService_projectsRequest.order', index=2,
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
  serialized_start=383,
  serialized_end=499,
)


_PROJECTAPPSERVICE_PROJECTSRESPONSE = _descriptor.Descriptor(
  name='ProjectAppService_projectsResponse',
  full_name='cafm.project.project.ProjectAppService_projectsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='projects', full_name='cafm.project.project.ProjectAppService_projectsResponse.projects', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='totalItemCount', full_name='cafm.project.project.ProjectAppService_projectsResponse.totalItemCount', index=1,
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
  serialized_start=501,
  serialized_end=610,
)

_PROJECTAPPSERVICE_PROJECTBYNAMERESPONSE.fields_by_name['project'].message_type = project_dot_project__pb2._PROJECT
_PROJECTAPPSERVICE_PROJECTBYIDRESPONSE.fields_by_name['project'].message_type = project_dot_project__pb2._PROJECT
_PROJECTAPPSERVICE_PROJECTSREQUEST.fields_by_name['order'].message_type = order__pb2._ORDER
_PROJECTAPPSERVICE_PROJECTSRESPONSE.fields_by_name['projects'].message_type = project_dot_project__pb2._PROJECT
DESCRIPTOR.message_types_by_name['ProjectAppService_projectByNameRequest'] = _PROJECTAPPSERVICE_PROJECTBYNAMEREQUEST
DESCRIPTOR.message_types_by_name['ProjectAppService_projectByNameResponse'] = _PROJECTAPPSERVICE_PROJECTBYNAMERESPONSE
DESCRIPTOR.message_types_by_name['ProjectAppService_projectByIdRequest'] = _PROJECTAPPSERVICE_PROJECTBYIDREQUEST
DESCRIPTOR.message_types_by_name['ProjectAppService_projectByIdResponse'] = _PROJECTAPPSERVICE_PROJECTBYIDRESPONSE
DESCRIPTOR.message_types_by_name['ProjectAppService_projectsRequest'] = _PROJECTAPPSERVICE_PROJECTSREQUEST
DESCRIPTOR.message_types_by_name['ProjectAppService_projectsResponse'] = _PROJECTAPPSERVICE_PROJECTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProjectAppService_projectByNameRequest = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectByNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTBYNAMEREQUEST,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectByNameRequest)
  })
_sym_db.RegisterMessage(ProjectAppService_projectByNameRequest)

ProjectAppService_projectByNameResponse = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectByNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTBYNAMERESPONSE,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectByNameResponse)
  })
_sym_db.RegisterMessage(ProjectAppService_projectByNameResponse)

ProjectAppService_projectByIdRequest = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTBYIDREQUEST,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectByIdRequest)
  })
_sym_db.RegisterMessage(ProjectAppService_projectByIdRequest)

ProjectAppService_projectByIdResponse = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectByIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTBYIDRESPONSE,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectByIdResponse)
  })
_sym_db.RegisterMessage(ProjectAppService_projectByIdResponse)

ProjectAppService_projectsRequest = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectsRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTSREQUEST,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectsRequest)
  })
_sym_db.RegisterMessage(ProjectAppService_projectsRequest)

ProjectAppService_projectsResponse = _reflection.GeneratedProtocolMessageType('ProjectAppService_projectsResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTAPPSERVICE_PROJECTSRESPONSE,
  '__module__' : 'project.project_app_service_pb2'
  # @@protoc_insertion_point(class_scope:cafm.project.project.ProjectAppService_projectsResponse)
  })
_sym_db.RegisterMessage(ProjectAppService_projectsResponse)



_PROJECTAPPSERVICE = _descriptor.ServiceDescriptor(
  name='ProjectAppService',
  full_name='cafm.project.project.ProjectAppService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=613,
  serialized_end=1045,
  methods=[
  _descriptor.MethodDescriptor(
    name='projectByName',
    full_name='cafm.project.project.ProjectAppService.projectByName',
    index=0,
    containing_service=None,
    input_type=_PROJECTAPPSERVICE_PROJECTBYNAMEREQUEST,
    output_type=_PROJECTAPPSERVICE_PROJECTBYNAMERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='projectById',
    full_name='cafm.project.project.ProjectAppService.projectById',
    index=1,
    containing_service=None,
    input_type=_PROJECTAPPSERVICE_PROJECTBYIDREQUEST,
    output_type=_PROJECTAPPSERVICE_PROJECTBYIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='projects',
    full_name='cafm.project.project.ProjectAppService.projects',
    index=2,
    containing_service=None,
    input_type=_PROJECTAPPSERVICE_PROJECTSREQUEST,
    output_type=_PROJECTAPPSERVICE_PROJECTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROJECTAPPSERVICE)

DESCRIPTOR.services_by_name['ProjectAppService'] = _PROJECTAPPSERVICE

# @@protoc_insertion_point(module_scope)
