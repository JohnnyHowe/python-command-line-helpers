"""Namespace normalization helpers for argparse outputs."""

from argparse import Namespace


def replace_hypens_with_underscore(args: Namespace) -> None:
	"""Copy hyphenated arg names to underscore variants on the namespace."""
	attributess_with_hyphens = [attr for attr in vars(args) if '-' in attr]
	for name in attributess_with_hyphens:
		new_name = name.replace('-', '_')
		setattr(args, new_name, getattr(args, name))
