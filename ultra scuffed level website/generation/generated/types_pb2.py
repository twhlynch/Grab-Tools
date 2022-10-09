# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: types.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='types.proto',
  package='COD.Types',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0btypes.proto\x12\tCOD.Types\")\n\x06Vector\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"8\n\nQuaternion\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\t\n\x01w\x18\x04 \x01(\x02\"3\n\x05\x43olor\x12\t\n\x01r\x18\x01 \x01(\x02\x12\t\n\x01g\x18\x02 \x01(\x02\x12\t\n\x01\x62\x18\x03 \x01(\x02\x12\t\n\x01\x61\x18\x04 \x01(\x02\"\xb6\x01\n\x10\x41mbienceSettings\x12(\n\x0eskyZenithColor\x18\x01 \x01(\x0b\x32\x10.COD.Types.Color\x12)\n\x0fskyHorizonColor\x18\x02 \x01(\x0b\x32\x10.COD.Types.Color\x12\x13\n\x0bsunAltitude\x18\x03 \x01(\x02\x12\x12\n\nsunAzimuth\x18\x04 \x01(\x02\x12\x0f\n\x07sunSize\x18\x05 \x01(\x02\x12\x13\n\x0b\x66ogDDensity\x18\x06 \x01(\x02\"n\n\x0eLevelNodeStart\x12#\n\x08position\x18\x01 \x01(\x0b\x32\x11.COD.Types.Vector\x12\'\n\x08rotation\x18\x02 \x01(\x0b\x32\x15.COD.Types.Quaternion\x12\x0e\n\x06radius\x18\x03 \x01(\x02\"F\n\x0fLevelNodeFinish\x12#\n\x08position\x18\x01 \x01(\x0b\x32\x11.COD.Types.Vector\x12\x0e\n\x06radius\x18\x02 \x01(\x02\"\xfc\x01\n\x0fLevelNodeStatic\x12(\n\x05shape\x18\x01 \x01(\x0e\x32\x19.COD.Types.LevelNodeShape\x12.\n\x08material\x18\x02 \x01(\x0e\x32\x1c.COD.Types.LevelNodeMaterial\x12#\n\x08position\x18\x03 \x01(\x0b\x32\x11.COD.Types.Vector\x12 \n\x05scale\x18\x04 \x01(\x0b\x32\x11.COD.Types.Vector\x12\'\n\x08rotation\x18\x05 \x01(\x0b\x32\x15.COD.Types.Quaternion\x12\x1f\n\x05\x63olor\x18\x06 \x01(\x0b\x32\x10.COD.Types.Color\"\x87\x02\n\x12LevelNodeCrumbling\x12(\n\x05shape\x18\x01 \x01(\x0e\x32\x19.COD.Types.LevelNodeShape\x12.\n\x08material\x18\x02 \x01(\x0e\x32\x1c.COD.Types.LevelNodeMaterial\x12#\n\x08position\x18\x03 \x01(\x0b\x32\x11.COD.Types.Vector\x12 \n\x05scale\x18\x04 \x01(\x0b\x32\x11.COD.Types.Vector\x12\'\n\x08rotation\x18\x05 \x01(\x0b\x32\x15.COD.Types.Quaternion\x12\x12\n\nstableTime\x18\x06 \x01(\x02\x12\x13\n\x0brespawnTime\x18\x07 \x01(\x02\"k\n\rLevelNodeSign\x12#\n\x08position\x18\x01 \x01(\x0b\x32\x11.COD.Types.Vector\x12\'\n\x08rotation\x18\x02 \x01(\x0b\x32\x15.COD.Types.Quaternion\x12\x0c\n\x04text\x18\x03 \x01(\t\"\xa9\x02\n\tLevelNode\x12\x33\n\x0elevelNodeStart\x18\x01 \x01(\x0b\x32\x19.COD.Types.LevelNodeStartH\x00\x12\x35\n\x0flevelNodeFinish\x18\x02 \x01(\x0b\x32\x1a.COD.Types.LevelNodeFinishH\x00\x12\x35\n\x0flevelNodeStatic\x18\x03 \x01(\x0b\x32\x1a.COD.Types.LevelNodeStaticH\x00\x12\x31\n\rlevelNodeSign\x18\x04 \x01(\x0b\x32\x18.COD.Types.LevelNodeSignH\x00\x12;\n\x12levelNodeCrumbling\x18\x05 \x01(\x0b\x32\x1d.COD.Types.LevelNodeCrumblingH\x00\x42\t\n\x07\x63ontent*\x90\x01\n\x0eLevelNodeShape\x12\t\n\x05START\x10\x00\x12\n\n\x06\x46INISH\x10\x01\x12\x08\n\x04SIGN\x10\x02\x12\x1c\n\x18__END_OF_SPECIAL_PARTS__\x10\x03\x12\t\n\x04\x43UBE\x10\xe8\x07\x12\x0b\n\x06SPHERE\x10\xe9\x07\x12\r\n\x08\x43YLINDER\x10\xea\x07\x12\x0c\n\x07PYRAMID\x10\xeb\x07\x12\n\n\x05PRISM\x10\xec\x07*\x9f\x01\n\x11LevelNodeMaterial\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\r\n\tGRABBABLE\x10\x01\x12\x07\n\x03ICE\x10\x02\x12\x08\n\x04LAVA\x10\x03\x12\x08\n\x04WOOD\x10\x04\x12\x0e\n\nGRAPPLABLE\x10\x05\x12\x13\n\x0fGRAPPLABLE_LAVA\x10\x06\x12\x17\n\x13GRABBABLE_CRUMBLING\x10\x07\x12\x13\n\x0f\x44\x45\x46\x41ULT_COLORED\x10\x08\x62\x06proto3'
)

_LEVELNODESHAPE = _descriptor.EnumDescriptor(
  name='LevelNodeShape',
  full_name='COD.Types.LevelNodeShape',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='START', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FINISH', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIGN', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='__END_OF_SPECIAL_PARTS__', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUBE', index=4, number=1000,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SPHERE', index=5, number=1001,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CYLINDER', index=6, number=1002,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PYRAMID', index=7, number=1003,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PRISM', index=8, number=1004,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1480,
  serialized_end=1624,
)
_sym_db.RegisterEnumDescriptor(_LEVELNODESHAPE)

LevelNodeShape = enum_type_wrapper.EnumTypeWrapper(_LEVELNODESHAPE)
_LEVELNODEMATERIAL = _descriptor.EnumDescriptor(
  name='LevelNodeMaterial',
  full_name='COD.Types.LevelNodeMaterial',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DEFAULT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GRABBABLE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ICE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LAVA', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WOOD', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GRAPPLABLE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GRAPPLABLE_LAVA', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GRABBABLE_CRUMBLING', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEFAULT_COLORED', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1627,
  serialized_end=1786,
)
_sym_db.RegisterEnumDescriptor(_LEVELNODEMATERIAL)

LevelNodeMaterial = enum_type_wrapper.EnumTypeWrapper(_LEVELNODEMATERIAL)
START = 0
FINISH = 1
SIGN = 2
__END_OF_SPECIAL_PARTS__ = 3
CUBE = 1000
SPHERE = 1001
CYLINDER = 1002
PYRAMID = 1003
PRISM = 1004
DEFAULT = 0
GRABBABLE = 1
ICE = 2
LAVA = 3
WOOD = 4
GRAPPLABLE = 5
GRAPPLABLE_LAVA = 6
GRABBABLE_CRUMBLING = 7
DEFAULT_COLORED = 8



_VECTOR = _descriptor.Descriptor(
  name='Vector',
  full_name='COD.Types.Vector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='COD.Types.Vector.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='COD.Types.Vector.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='z', full_name='COD.Types.Vector.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=26,
  serialized_end=67,
)


_QUATERNION = _descriptor.Descriptor(
  name='Quaternion',
  full_name='COD.Types.Quaternion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='COD.Types.Quaternion.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='COD.Types.Quaternion.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='z', full_name='COD.Types.Quaternion.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='w', full_name='COD.Types.Quaternion.w', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=69,
  serialized_end=125,
)


_COLOR = _descriptor.Descriptor(
  name='Color',
  full_name='COD.Types.Color',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='r', full_name='COD.Types.Color.r', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='g', full_name='COD.Types.Color.g', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b', full_name='COD.Types.Color.b', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='a', full_name='COD.Types.Color.a', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=127,
  serialized_end=178,
)


_AMBIENCESETTINGS = _descriptor.Descriptor(
  name='AmbienceSettings',
  full_name='COD.Types.AmbienceSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='skyZenithColor', full_name='COD.Types.AmbienceSettings.skyZenithColor', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skyHorizonColor', full_name='COD.Types.AmbienceSettings.skyHorizonColor', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sunAltitude', full_name='COD.Types.AmbienceSettings.sunAltitude', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sunAzimuth', full_name='COD.Types.AmbienceSettings.sunAzimuth', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sunSize', full_name='COD.Types.AmbienceSettings.sunSize', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fogDDensity', full_name='COD.Types.AmbienceSettings.fogDDensity', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=181,
  serialized_end=363,
)


_LEVELNODESTART = _descriptor.Descriptor(
  name='LevelNodeStart',
  full_name='COD.Types.LevelNodeStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='COD.Types.LevelNodeStart.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='COD.Types.LevelNodeStart.rotation', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='COD.Types.LevelNodeStart.radius', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=365,
  serialized_end=475,
)


_LEVELNODEFINISH = _descriptor.Descriptor(
  name='LevelNodeFinish',
  full_name='COD.Types.LevelNodeFinish',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='COD.Types.LevelNodeFinish.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='COD.Types.LevelNodeFinish.radius', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=477,
  serialized_end=547,
)


_LEVELNODESTATIC = _descriptor.Descriptor(
  name='LevelNodeStatic',
  full_name='COD.Types.LevelNodeStatic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='COD.Types.LevelNodeStatic.shape', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='material', full_name='COD.Types.LevelNodeStatic.material', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position', full_name='COD.Types.LevelNodeStatic.position', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scale', full_name='COD.Types.LevelNodeStatic.scale', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='COD.Types.LevelNodeStatic.rotation', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='color', full_name='COD.Types.LevelNodeStatic.color', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=550,
  serialized_end=802,
)


_LEVELNODECRUMBLING = _descriptor.Descriptor(
  name='LevelNodeCrumbling',
  full_name='COD.Types.LevelNodeCrumbling',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='COD.Types.LevelNodeCrumbling.shape', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='material', full_name='COD.Types.LevelNodeCrumbling.material', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position', full_name='COD.Types.LevelNodeCrumbling.position', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scale', full_name='COD.Types.LevelNodeCrumbling.scale', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='COD.Types.LevelNodeCrumbling.rotation', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stableTime', full_name='COD.Types.LevelNodeCrumbling.stableTime', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='respawnTime', full_name='COD.Types.LevelNodeCrumbling.respawnTime', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=805,
  serialized_end=1068,
)


_LEVELNODESIGN = _descriptor.Descriptor(
  name='LevelNodeSign',
  full_name='COD.Types.LevelNodeSign',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='COD.Types.LevelNodeSign.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='COD.Types.LevelNodeSign.rotation', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='COD.Types.LevelNodeSign.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=1070,
  serialized_end=1177,
)


_LEVELNODE = _descriptor.Descriptor(
  name='LevelNode',
  full_name='COD.Types.LevelNode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='levelNodeStart', full_name='COD.Types.LevelNode.levelNodeStart', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='levelNodeFinish', full_name='COD.Types.LevelNode.levelNodeFinish', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='levelNodeStatic', full_name='COD.Types.LevelNode.levelNodeStatic', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='levelNodeSign', full_name='COD.Types.LevelNode.levelNodeSign', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='levelNodeCrumbling', full_name='COD.Types.LevelNode.levelNodeCrumbling', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='content', full_name='COD.Types.LevelNode.content',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1180,
  serialized_end=1477,
)

_AMBIENCESETTINGS.fields_by_name['skyZenithColor'].message_type = _COLOR
_AMBIENCESETTINGS.fields_by_name['skyHorizonColor'].message_type = _COLOR
_LEVELNODESTART.fields_by_name['position'].message_type = _VECTOR
_LEVELNODESTART.fields_by_name['rotation'].message_type = _QUATERNION
_LEVELNODEFINISH.fields_by_name['position'].message_type = _VECTOR
_LEVELNODESTATIC.fields_by_name['shape'].enum_type = _LEVELNODESHAPE
_LEVELNODESTATIC.fields_by_name['material'].enum_type = _LEVELNODEMATERIAL
_LEVELNODESTATIC.fields_by_name['position'].message_type = _VECTOR
_LEVELNODESTATIC.fields_by_name['scale'].message_type = _VECTOR
_LEVELNODESTATIC.fields_by_name['rotation'].message_type = _QUATERNION
_LEVELNODESTATIC.fields_by_name['color'].message_type = _COLOR
_LEVELNODECRUMBLING.fields_by_name['shape'].enum_type = _LEVELNODESHAPE
_LEVELNODECRUMBLING.fields_by_name['material'].enum_type = _LEVELNODEMATERIAL
_LEVELNODECRUMBLING.fields_by_name['position'].message_type = _VECTOR
_LEVELNODECRUMBLING.fields_by_name['scale'].message_type = _VECTOR
_LEVELNODECRUMBLING.fields_by_name['rotation'].message_type = _QUATERNION
_LEVELNODESIGN.fields_by_name['position'].message_type = _VECTOR
_LEVELNODESIGN.fields_by_name['rotation'].message_type = _QUATERNION
_LEVELNODE.fields_by_name['levelNodeStart'].message_type = _LEVELNODESTART
_LEVELNODE.fields_by_name['levelNodeFinish'].message_type = _LEVELNODEFINISH
_LEVELNODE.fields_by_name['levelNodeStatic'].message_type = _LEVELNODESTATIC
_LEVELNODE.fields_by_name['levelNodeSign'].message_type = _LEVELNODESIGN
_LEVELNODE.fields_by_name['levelNodeCrumbling'].message_type = _LEVELNODECRUMBLING
_LEVELNODE.oneofs_by_name['content'].fields.append(
  _LEVELNODE.fields_by_name['levelNodeStart'])
_LEVELNODE.fields_by_name['levelNodeStart'].containing_oneof = _LEVELNODE.oneofs_by_name['content']
_LEVELNODE.oneofs_by_name['content'].fields.append(
  _LEVELNODE.fields_by_name['levelNodeFinish'])
_LEVELNODE.fields_by_name['levelNodeFinish'].containing_oneof = _LEVELNODE.oneofs_by_name['content']
_LEVELNODE.oneofs_by_name['content'].fields.append(
  _LEVELNODE.fields_by_name['levelNodeStatic'])
_LEVELNODE.fields_by_name['levelNodeStatic'].containing_oneof = _LEVELNODE.oneofs_by_name['content']
_LEVELNODE.oneofs_by_name['content'].fields.append(
  _LEVELNODE.fields_by_name['levelNodeSign'])
_LEVELNODE.fields_by_name['levelNodeSign'].containing_oneof = _LEVELNODE.oneofs_by_name['content']
_LEVELNODE.oneofs_by_name['content'].fields.append(
  _LEVELNODE.fields_by_name['levelNodeCrumbling'])
_LEVELNODE.fields_by_name['levelNodeCrumbling'].containing_oneof = _LEVELNODE.oneofs_by_name['content']
DESCRIPTOR.message_types_by_name['Vector'] = _VECTOR
DESCRIPTOR.message_types_by_name['Quaternion'] = _QUATERNION
DESCRIPTOR.message_types_by_name['Color'] = _COLOR
DESCRIPTOR.message_types_by_name['AmbienceSettings'] = _AMBIENCESETTINGS
DESCRIPTOR.message_types_by_name['LevelNodeStart'] = _LEVELNODESTART
DESCRIPTOR.message_types_by_name['LevelNodeFinish'] = _LEVELNODEFINISH
DESCRIPTOR.message_types_by_name['LevelNodeStatic'] = _LEVELNODESTATIC
DESCRIPTOR.message_types_by_name['LevelNodeCrumbling'] = _LEVELNODECRUMBLING
DESCRIPTOR.message_types_by_name['LevelNodeSign'] = _LEVELNODESIGN
DESCRIPTOR.message_types_by_name['LevelNode'] = _LEVELNODE
DESCRIPTOR.enum_types_by_name['LevelNodeShape'] = _LEVELNODESHAPE
DESCRIPTOR.enum_types_by_name['LevelNodeMaterial'] = _LEVELNODEMATERIAL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Vector = _reflection.GeneratedProtocolMessageType('Vector', (_message.Message,), {
  'DESCRIPTOR' : _VECTOR,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.Vector)
  })
_sym_db.RegisterMessage(Vector)

Quaternion = _reflection.GeneratedProtocolMessageType('Quaternion', (_message.Message,), {
  'DESCRIPTOR' : _QUATERNION,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.Quaternion)
  })
_sym_db.RegisterMessage(Quaternion)

Color = _reflection.GeneratedProtocolMessageType('Color', (_message.Message,), {
  'DESCRIPTOR' : _COLOR,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.Color)
  })
_sym_db.RegisterMessage(Color)

AmbienceSettings = _reflection.GeneratedProtocolMessageType('AmbienceSettings', (_message.Message,), {
  'DESCRIPTOR' : _AMBIENCESETTINGS,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.AmbienceSettings)
  })
_sym_db.RegisterMessage(AmbienceSettings)

LevelNodeStart = _reflection.GeneratedProtocolMessageType('LevelNodeStart', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODESTART,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNodeStart)
  })
_sym_db.RegisterMessage(LevelNodeStart)

LevelNodeFinish = _reflection.GeneratedProtocolMessageType('LevelNodeFinish', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODEFINISH,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNodeFinish)
  })
_sym_db.RegisterMessage(LevelNodeFinish)

LevelNodeStatic = _reflection.GeneratedProtocolMessageType('LevelNodeStatic', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODESTATIC,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNodeStatic)
  })
_sym_db.RegisterMessage(LevelNodeStatic)

LevelNodeCrumbling = _reflection.GeneratedProtocolMessageType('LevelNodeCrumbling', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODECRUMBLING,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNodeCrumbling)
  })
_sym_db.RegisterMessage(LevelNodeCrumbling)

LevelNodeSign = _reflection.GeneratedProtocolMessageType('LevelNodeSign', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODESIGN,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNodeSign)
  })
_sym_db.RegisterMessage(LevelNodeSign)

LevelNode = _reflection.GeneratedProtocolMessageType('LevelNode', (_message.Message,), {
  'DESCRIPTOR' : _LEVELNODE,
  '__module__' : 'types_pb2'
  # @@protoc_insertion_point(class_scope:COD.Types.LevelNode)
  })
_sym_db.RegisterMessage(LevelNode)


# @@protoc_insertion_point(module_scope)
