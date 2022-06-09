# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bakdata/trade/v1/trade.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bakdata/trade/v1/trade.proto',
  package='bakdata.trade.v1',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1c\x62\x61kdata/trade/v1/trade.proto\x12\x10\x62\x61kdata.trade.v1\"\xd9\x02\n\x05Trade\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08personid\x18\x02 \x01(\t\x12\x10\n\x08issuerid\x18\x03 \x01(\t\x12\x11\n\tcompanyid\x18\x04 \x01(\t\x12\x10\n\x08position\x18\x05 \x01(\t\x12\x12\n\nasset_type\x18\x06 \x01(\t\x12\x12\n\ntrade_type\x18\x07 \x01(\t\x12\x11\n\tavg_price\x18\x08 \x01(\x01\x12\x1a\n\x12\x61vg_price_currency\x18\t \x01(\t\x12\x18\n\x10\x61ggregate_volume\x18\n \x01(\x01\x12!\n\x19\x61ggregate_volume_currency\x18\x0b \x01(\t\x12\x1c\n\x14\x64\x61te_of_notification\x18\x0c \x01(\t\x12\x15\n\rdate_of_trade\x18\r \x01(\t\x12\x16\n\x0eplace_of_trade\x18\x0e \x01(\t\x12\x1a\n\x12\x64\x61te_of_activation\x18\x0f \x01(\tb\x06proto3')
)




_TRADE = _descriptor.Descriptor(
  name='Trade',
  full_name='bakdata.trade.v1.Trade',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='bakdata.trade.v1.Trade.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='personid', full_name='bakdata.trade.v1.Trade.personid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuerid', full_name='bakdata.trade.v1.Trade.issuerid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='companyid', full_name='bakdata.trade.v1.Trade.companyid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position', full_name='bakdata.trade.v1.Trade.position', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='asset_type', full_name='bakdata.trade.v1.Trade.asset_type', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trade_type', full_name='bakdata.trade.v1.Trade.trade_type', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='avg_price', full_name='bakdata.trade.v1.Trade.avg_price', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='avg_price_currency', full_name='bakdata.trade.v1.Trade.avg_price_currency', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aggregate_volume', full_name='bakdata.trade.v1.Trade.aggregate_volume', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aggregate_volume_currency', full_name='bakdata.trade.v1.Trade.aggregate_volume_currency', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_of_notification', full_name='bakdata.trade.v1.Trade.date_of_notification', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_of_trade', full_name='bakdata.trade.v1.Trade.date_of_trade', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='place_of_trade', full_name='bakdata.trade.v1.Trade.place_of_trade', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_of_activation', full_name='bakdata.trade.v1.Trade.date_of_activation', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=51,
  serialized_end=396,
)

DESCRIPTOR.message_types_by_name['Trade'] = _TRADE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Trade = _reflection.GeneratedProtocolMessageType('Trade', (_message.Message,), dict(
  DESCRIPTOR = _TRADE,
  __module__ = 'bakdata.trade.v1.trade_pb2'
  # @@protoc_insertion_point(class_scope:bakdata.trade.v1.Trade)
  ))
_sym_db.RegisterMessage(Trade)


# @@protoc_insertion_point(module_scope)
