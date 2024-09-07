# Similar Buffers detector

This is a library to detect similarities between buffers.

Given two buffers, `a` and `b`, the library will return a list of statistics about the similarity between the two buffers.

## Design

The library is designed to be modular and extensible (following the OCP). The main components are:
* `Statistic`: A statistic is the interface that receives two buffers and computes a single statistic
* `SimilarBufferDetector`: The main class that receives a list of statistics. It is modeled as a Rules Engine.

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
