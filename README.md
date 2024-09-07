# Similar Buffers detector

This is a library to detect similarities between buffers.

Given two buffers, `a` and `b`, the library will return a list of statistics about the similarity between the two buffers.

# Running it

## Getting started - Local python

```bash
make virtualenvironment
source venv/bin/activate
make virtualenvironment-finish
make install
make test
```

## Getting started - Docker

```bash
make up
make bash
# continue the steps for the local installation
make down
```
