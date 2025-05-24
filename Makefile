
update:
	uv pip compile pyproject.toml > requirements.txt
	uv sync