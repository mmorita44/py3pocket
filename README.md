Python3 package for interacting with Pocket via REST APIs.
=========================

[![licence badge]][licence]

# Install

```bash
git clone https://github.com/mmorita44/py3pocket.git
cd py3pocket
python setup.py install
```

# Usage

```python
import py3pocket

py3pocket.Client('consumer key', 'username', 'password')
print(pocket.retrieve()) # {'complete': 1, 'search_meta': {'search_type': 'normal'}, 'error': None, ...

```

# Caution

Logging in Pocket and getting access token methods are informal, they may are changed in future.

[licence]: <LICENSE>
[licence badge]: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
