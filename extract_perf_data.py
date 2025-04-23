import os
import csv
import re

def extract_metrics_from_file(filepath):
    """Extract TMA metrics from a given file."""
    metrics = {}
    pattern = re.compile(r'#\s+([\d\.]+)\s+%\s+(\S+)')
    
    with open(filepath, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                percent, metric = match.groups()
                metrics[metric] = percent
    return metrics

def process_directory(directory):
    all_metrics = {}
    all_keys = set()

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            metrics = extract_metrics_from_file(full_path)
            all_metrics[filename] = metrics
            all_keys.update(metrics.keys())

    return all_metrics, sorted(all_keys)

def write_to_csv(metrics_dict, all_keys, output_file='perf_summary.csv'):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Metric'] + list(metrics_dict.keys())
        writer.writerow(header)

        for key in all_keys:
            row = [key]
            for file in metrics_dict:
                row.append(metrics_dict[file].get(key, ''))
            writer.writerow(row)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Extract TMA metrics from perf output files.")
    parser.add_argument('directory', help='Directory containing perf output files')
    parser.add_argument('--output', default='perf_summary.csv', help='Output CSV file name')
    args = parser.parse_args()

    metrics_dict, all_keys = process_directory(args.directory)
    write_to_csv(metrics_dict, all_keys, args.output)
    print(f"Data written to {args.output}")
