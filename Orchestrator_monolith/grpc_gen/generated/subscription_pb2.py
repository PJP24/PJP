# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: subscription.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'subscription.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12subscription.proto\x12\x14subscription_service\"&\n\x13SubscriptionRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"R\n\x14SubscriptionResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x19\n\x11subscription_type\x18\x02 \x01(\t\x12\x0e\n\x06period\x18\x03 \x01(\t2\x86\x01\n\x13SubscriptionService\x12o\n\x16GetSubscriptionDetails\x12).subscription_service.SubscriptionRequest\x1a*.subscription_service.SubscriptionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'subscription_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUBSCRIPTIONREQUEST']._serialized_start=44
  _globals['_SUBSCRIPTIONREQUEST']._serialized_end=82
  _globals['_SUBSCRIPTIONRESPONSE']._serialized_start=84
  _globals['_SUBSCRIPTIONRESPONSE']._serialized_end=166
  _globals['_SUBSCRIPTIONSERVICE']._serialized_start=169
  _globals['_SUBSCRIPTIONSERVICE']._serialized_end=303
# @@protoc_insertion_point(module_scope)
