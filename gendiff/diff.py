def generate_diff(file1_data, file2_data):
    all_keys = sorted(set(file1_data.keys()) | set(file2_data.keys()))
    result = []
    
    for key in all_keys:
        if key not in file1_data:
            result.append(f"  + {key}: {file2_data[key]}")
        elif key not in file2_data:
            result.append(f"  - {key}: {file1_data[key]}")
        elif file1_data[key] != file2_data[key]:
            result.append(f"  - {key}: {file1_data[key]}")
            result.append(f"  + {key}: {file2_data[key]}")
        else:
            result.append(f"    {key}: {file1_data[key]}")
    
    return "{\n" + "\n".join(result) + "\n}" 