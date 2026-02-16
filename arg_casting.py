"""Helpers for converting CLI argument strings into typed values."""
from argparse import Namespace
from typing import Type, Union, get_args, get_origin


def replace_hypens_with_underscore(args: Namespace) -> None:
	"""Copy hyphenated arg names to underscore variants on the namespace."""
	attributess_with_hyphens = [attr for attr in vars(args) if '-' in attr]
	for name in attributess_with_hyphens:
		new_name = name.replace('-', '_')
		setattr(args, new_name, getattr(args, name))


def cast(value, target_type: Type):
	"""Cast a value to the provided target_type using supported helpers."""
	for parser in [
			_union_caster,
			_dict_caster,
			_list_caster,
			_generic_caster,
	]:
		try:
			return parser(value, target_type)
		except:
			pass
	raise TypeError(f"Could not cast {value} to {target_type}")


def _generic_caster(value, target_type: Type):
	"""Cast using the target type constructor."""
	return target_type(value)


def _dict_caster(value, target_type: Type) -> dict:
	"""Cast a comma-separated string or list of entries into a dict."""
	if not target_type == dict:
		raise TypeError()

	if isinstance(value, list):
		return _list_to_dict_caster(value)

	data = {}
	if value is None:
		return data
	for part in value.split(","):
		key, value = part.split("=")
		data[key.strip()] = value.strip()
	return data


def _list_to_dict_caster(value: list) -> dict:
	"""Convert a list of key=value strings into a dict."""
	result = {}
	for part in value:
		parts = part.split("=", 1)
		if not len(parts) == 2:
			raise ValueError(f"Got invalid dict entry {part}!")
		result[parts[0]] = parts[1]
	return result


def _union_caster(value, target_type: Type):
	"""Attempt to cast by trying each Union member type in order."""
	if not get_origin(target_type) is Union:
		raise TypeError()

	for potential_type in get_args(target_type):
		try:
			return cast(value, potential_type)
		except:
			pass

def _list_caster(value, target_type: Type):
	if not get_origin(target_type) is list:
		raise TypeError()
	return value.split(",")