# File Carving Benchmark

## Description

File carving is the task of identifying files in a byte stream, such as one read from a corrupted HDD. It is useful for recovering files and metdata in a file system that is corrupted or deleted. This benchmark recognizes complex file header and footer patterns for zip, mpeg-2 and mpeg-4 files. We also include patterns to identify sensitive data such as e-mail addresses and social security numbers.

## Benchmark

This benchmark contains two automata files and inputs.