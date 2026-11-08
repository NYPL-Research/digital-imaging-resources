#!/usr/bin/env python3

import os
import glob
import shutil
import json
import argparse
import bagit

def unpackage(barcode_dir):
    """
    Acts like a vacuum: finds all asset/JSON files anywhere in the directory tree,
    moves them to the root level, and deletes all subdirectories and bagit files.
    """
    print(f"Unpackaging everything in {barcode_dir} to root...")
    
    # 1. Find ALL files anywhere in the directory tree
    all_files = []
    for root, dirs, files in os.walk(barcode_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
            
    # 2. Move target files (images, jsons) to the root directory
    for file_path in all_files:
        filename = os.path.basename(file_path)
        # Check if it's one of our data files
        if "_" in filename and (filename.endswith('.jpg') or filename.endswith('.tif') or filename.endswith('.json')):
            dst = os.path.join(barcode_dir, filename)
            if file_path != dst:
                shutil.move(file_path, dst)
                
    # 3. Delete all bag metadata files at any level
    for root, dirs, files in os.walk(barcode_dir):
        for file in files:
            if file in ['bagit.txt', 'bag-info.txt', 'fetch.txt'] or file.startswith('manifest-') or file.startswith('tagmanifest-'):
                try:
                    os.remove(os.path.join(root, file))
                except FileNotFoundError:
                    pass
                
    # 4. Remove all subdirectories (like 'u001', 'data', etc.)
    # Walk bottom-up so we can safely delete directories after emptying them
    for root, dirs, files in os.walk(barcode_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                shutil.rmtree(dir_path)
            except Exception:
                pass
                
    print("Unpackaging complete. Root directory is clean.\n")

def update_json_sequences(barcode_dir):
    """
    Finds all JSON files in the root directory, extracts the sequence number 
    from the filename, and updates the sequenceNumber and sequenceLabel in the JSON.
    """
    print("Updating JSON sequence numbers...")
    json_files = glob.glob(os.path.join(barcode_dir, "*.json"))
    
    updated_count = 0
    for json_file in json_files:
        filename = os.path.basename(json_file)
        parts = filename.split('_')
        
        if len(parts) >= 2 and parts[1].isdigit():
            seq_num = int(parts[1])
            
            with open(json_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    continue
            
            # Ensure the nested structure exists before trying to update it
            if 'source' not in data:
                data['source'] = {}
            if 'sequence' not in data['source']:
                data['source']['sequence'] = {}
                
            # Update the specific fields
            data['source']['sequence']['sequenceNumber'] = seq_num
            data['source']['sequence']['sequenceLabel'] = f"Frame {seq_num}"
            
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            updated_count += 1
            
    print(f"Updated sequence data in {updated_count} JSON files.\n")

def repackage(barcode_dir):
    """
    Groups files by prefix, reads their JSON to determine the unit index,
    moves them into corresponding uXXX folders, and bags the entire barcode dir.
    """
    print(f"Repackaging {barcode_dir}...")
    
    files = [f for f in os.listdir(barcode_dir) if os.path.isfile(os.path.join(barcode_dir, f))]
    
    prefixes = set()
    for f in files:
        if "_" in f:
            parts = f.split('_')
            if len(parts) >= 2:
                prefixes.add(f"{parts[0]}_{parts[1]}")
                
    for prefix in prefixes:
        json_files = glob.glob(os.path.join(barcode_dir, f"{prefix}*.json"))
        if not json_files:
            continue
            
        with open(json_files[0], 'r') as jf:
            data = json.load(jf)
            
            # Safely navigate the JSON tree: source -> sequence -> unitIndex
            unit_val = data.get('source', {}).get('sequence', {}).get('unitIndex')
            
        if unit_val is None:
            print(f"  Warning: 'unitIndex' not found for {prefix}. Skipping...")
            continue
            
        # Format the directory name (e.g., 1 -> "u001")
        if isinstance(unit_val, int) or (isinstance(unit_val, str) and unit_val.isdigit()):
            unit_dir_name = f"u{int(unit_val):03d}"
        else:
            unit_dir_name = str(unit_val)
            
        unit_path = os.path.join(barcode_dir, unit_dir_name)
        os.makedirs(unit_path, exist_ok=True)
        
        for matching_file in glob.glob(os.path.join(barcode_dir, f"{prefix}*")):
            shutil.move(matching_file, os.path.join(unit_path, os.path.basename(matching_file)))
            
    print("Files separated into unit directories.")
    
    print("Creating top-level bag...")
    bagit.make_bag(barcode_dir, checksums=['md5'])
    print(f"Success! {barcode_dir} is now a single bag.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Path to the top-level barcode directory")
    parser.add_argument("--mode", choices=["unpackage", "repackage", "both"], default="both", 
                        help="Action to perform (default: both)")
    parser.add_argument("--update-json", action="store_true", 
                        help="Update JSON sequence numbers based on filenames before repackaging")
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.dir)
    
    if args.mode in ["unpackage", "both"]:
        unpackage(target_dir)
        
    if args.mode in ["repackage", "both"]:
        if args.update_json:
            update_json_sequences(target_dir)
        repackage(target_dir)