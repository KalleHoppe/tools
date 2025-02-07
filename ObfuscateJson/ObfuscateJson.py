import json
import hashlib
import argparse

# Usage python ObfuscateJson.py input.json output.json key1 key2 key3
# Example Usage:
# If you have a JSON file like:

# {
#     "name": "Alice",
#     "age": 25,
#     "password": "mysecretpassword"
# }
# Running:

# python ObfuscateJson.py input.json output.json name password
# Would produce output.json like:

# {
#     "name": "Alice",
#     "age": "9c1d6c3c1e4d34a7e6b4e1c2b8d6a519",
#     "password": "mysecretpassword"
# }
# Here, "name" and "password" remain unchanged, while "age" is hashed.


def md5_hash(value):
    """Returns the MD5 hash of a given value as a hex string."""
    return hashlib.md5(str(value).encode()).hexdigest()

def process_json(data, exclude_keys):
    """Recursively processes JSON data, hashing all values except those under exclude_keys."""
    if isinstance(data, dict):
        return {k: (v if k in exclude_keys else process_json(v, exclude_keys)) for k, v in data.items()}
    elif isinstance(data, list):
        return [process_json(item, exclude_keys) for item in data]
    elif isinstance(data, (str, int, float, bool)):
        return md5_hash(data)
    return data

def main(input_file, output_file, exclude_keys):
    """Reads JSON from input file, processes it, and writes to output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processed_data = process_json(data, exclude_keys)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=4)
    
    print(f"Processed JSON saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MD5 hash all JSON values except for specific keys.")
    parser.add_argument("input_file", help="Path to input JSON file.")
    parser.add_argument("output_file", help="Path to output JSON file.")
    parser.add_argument("exclude_keys", nargs='+', help="List of keys to exclude from hashing.")
    
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.exclude_keys)