# run
```bash
uv run main.py --help
```

## examples

```bash
# all raphael + figure '.de' domains
uv run main.py "raphael[0-9]\.de" 

# letter,vowel,letter,vowel '.de' domains
uv run main.py "[a-z][aeiouy][a-z][aeiouy]\.de"

# random 4 letters '.de' domains
uv run main.py "[a-z]{4}\.de" -r
```