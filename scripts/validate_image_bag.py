#!/usr/bin/env python3

import os
import json
import argparse
import urllib.request
import jsonschema
import bagit

SCHEMA_URL = "https://raw.githubusercontent.com/NYPL-Research/digital-imaging-resources/main/static/schemas/digitized_image_schema.json"

def load_schema(schema_path=None):
    """Loads the schema locally if provided, otherwise attempts to fetch from URL."""
    if schema_path:
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"  [ERROR] Failed to load local schema from {schema_path}: {e}")
            return None
            
    print("Attempting to fetch JSON schema from URL...")
    try:
        with urllib.request.urlopen(SCHEMA_URL) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [WARNING] Failed to fetch schema: {e}")
        print("  [WARNING] Proceeding without schema validation (Use --schema-path to provide a local copy).")
        return None

def validate_single_bag(bag_dir, schema, skip_checksums):
    print(f"\n================ Validating Bag: {os.path.basename(bag_dir)} ================")
    errors = []
    
    # 1. Check BagIt Structure
    if not os.path.exists(os.path.join(bag_dir, 'bagit.txt')):
        errors.append(f"Not a valid Bag (missing bagit.txt): {bag_dir}")
        return errors
        
    for root, dirs, files in os.walk(bag_dir):
        if root != bag_dir and 'bagit.txt' in files:
            errors.append(f"Found nested bag at: {root}")
            
    if skip_checksums:
        print("  [SKIP] BagIt checksum validation skipped.")
    else:
        print("  [RUN] Validating BagIt checksums...")
        try:
            bag = bagit.Bag(bag_dir)
            bag.validate()
            print("  [PASS] BagIt checksums and manifests are valid.")
        except bagit.BagValidationError as e:
            errors.append(f"Bag validation failed: {e}")
        except Exception as e:
            errors.append(f"Bag validation error: {e}")

    # 2. Validate Payload
    data_dir = os.path.join(bag_dir, 'data')
    if not os.path.exists(data_dir):
        errors.append(f"Payload directory 'data' not found in {bag_dir}")
        return errors

    file_groups = {}
    for root, _, files in os.walk(data_dir):
        for f in files:
            if f.startswith('.'):
                continue
            parts = f.split('_')
            if len(parts) >= 2:
                prefix = f"{parts[0]}_{parts[1]}"
                if prefix not in file_groups:
                    file_groups[prefix] = []
                file_groups[prefix].append({
                    'filename': f,
                    'path': os.path.join(root, f),
                    'rel_dir': os.path.relpath(root, data_dir)
                })

    sequence_tracker = {}
    
    # Create the validator instance once if schema exists
    validator = None
    if schema:
        validator_class = jsonschema.validators.validator_for(schema)
        validator = validator_class(schema)

    for prefix, files in file_groups.items():
        roles_found = {'pres': {}, 'serv': {}, 'access': {}}
        for file_info in files:
            fname = file_info['filename']
            for role in roles_found.keys():
                if f"_{role}." in fname:
                    if fname.endswith('.json'):
                        roles_found[role]['json'] = file_info
                    elif fname.endswith(('.jpg', '.tif', '.jp2')):
                        roles_found[role]['image'] = file_info

        # Check for completeness (Image + JSON for all 3 roles)
        for role, pairs in roles_found.items():
            if 'image' in pairs and 'json' not in pairs:
                errors.append(f"{prefix}: Missing JSON for {role} image.")
            elif 'json' in pairs and 'image' not in pairs:
                errors.append(f"{prefix}: Missing image for {role} JSON.")
            elif 'image' not in pairs and 'json' not in pairs:
                errors.append(f"{prefix}: Missing entire {role} set (image + JSON).")
                
        # Deep JSON checks
        for role, pairs in roles_found.items():
            if 'json' in pairs:
                json_info = pairs['json']
                try:
                    with open(json_info['path'], 'r') as jf:
                        data = json.load(jf)
                        
                    # Strict schema validation - catch ALL errors
                    if validator:
                        for schema_err in validator.iter_errors(data):
                            # Construct the path to where the error occurred (e.g. source.sequence.unitIndex)
                            path = ".".join([str(p) for p in schema_err.path]) if schema_err.path else "root"
                            errors.append(f"{json_info['filename']} schema error [{path}]: {schema_err.message}")

                    # Ensure referenceFilename matches actual image file
                    if 'image' in pairs:
                        img_fname = pairs['image']['filename']
                        ref_fname = data.get('asset', {}).get('referenceFilename')
                        if ref_fname != img_fname:
                            errors.append(f"{json_info['filename']}: referenceFilename '{ref_fname}' does not match image '{img_fname}'.")

                    seq_data = data.get('source', {}).get('sequence', {})
                    seq_num = seq_data.get('sequenceNumber')
                    unit_index = seq_data.get('unitIndex')
                    
                    if seq_num is not None:
                        sequence_tracker[prefix] = seq_num
                        
                    rel_dir = json_info['rel_dir']
                    if unit_index is not None:
                        expected_dir = f"u{int(unit_index):03d}"
                        if rel_dir != expected_dir:
                            errors.append(f"{json_info['filename']}: JSON specifies unitIndex {unit_index}, but file is physically in '{rel_dir}' (expected '{expected_dir}').")
                    else:
                        if rel_dir != '.':
                            errors.append(f"{json_info['filename']}: No unitIndex in JSON, but file is inside a subfolder '{rel_dir}'.")

                except json.JSONDecodeError:
                    errors.append(f"{json_info['filename']} is not a valid JSON file.")

    # 3. Check Chronological Sequence across the entire bag
    if sequence_tracker:
        sorted_seqs = sorted(sequence_tracker.items(), key=lambda x: x[1])
        expected_seq = 1
        for prefix, seq_num in sorted_seqs:
            if seq_num != expected_seq:
                errors.append(f"Sequence gap/mismatch detected at {prefix}: Expected {expected_seq}, found {seq_num}")
                expected_seq = seq_num 
            expected_seq += 1

    if not errors:
        print("  [PASS] All internal structural and JSON checks passed.")
        
    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate digitized image BagIt packages.")
    parser.add_argument("target", help="Path to a single bag OR a directory containing multiple bags.")
    parser.add_argument("--skip-checksums", action="store_true", help="Skip the slow BagIt checksum validation.")
    parser.add_argument("--schema-path", help="Path to a local JSON schema file (to avoid 404 errors on download).")
    args = parser.parse_args()
    
    target = os.path.abspath(args.target)
    schema = load_schema(args.schema_path)
    
    bags_to_process = []
    
    # Check if target is a bag itself, or a parent directory of bags
    if os.path.exists(os.path.join(target, 'bagit.txt')):
        bags_to_process.append(target)
    else:
        for item in os.listdir(target):
            item_path = os.path.join(target, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'bagit.txt')):
                bags_to_process.append(item_path)
                
    if not bags_to_process:
        print(f"Error: No bags found at {target}")
        exit(1)
        
    print(f"\nFound {len(bags_to_process)} bag(s) to validate.")
    
    all_results = {}
    for bag in bags_to_process:
        errors = validate_single_bag(bag, schema, args.skip_checksums)
        all_results[bag] = errors
        
    print("\n================ FINAL SUMMARY ================")
    total_failed = 0
    for bag, errors in all_results.items():
        bag_name = os.path.basename(bag)
        if not errors:
            print(f"✅ [OK] {bag_name}")
        else:
            print(f"❌ [FAILED] {bag_name} ({len(errors)} errors)")
            for e in errors:
                print(f"    - {e}")
            total_failed += 1
            
    if total_failed > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()