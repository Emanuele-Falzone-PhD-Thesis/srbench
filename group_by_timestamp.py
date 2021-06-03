import os
import csv
import sys

def get_csv_files(folder):
    csv_files = []
    for root, dirs, files in os.walk(folder, topdown = False):
        for filename in files:
            name, extension = os.path.splitext(filename)
            if extension == ".csv":
                csv_files.append(os.path.join(root, filename))
    return csv_files

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_csv(path, fieldnames):
    if not os.path.isfile(path):
        csv_file = open(path, "w")
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        csv_file.close()

if __name__ == "__main__":
    
    print("Number of arguments:", len(sys.argv), "arguments.")
    print("Argument List:", str(sys.argv))

    if len(sys.argv) != 3:
        print("Please specify input and output folders.")
        exit(1)

    input_folder = sys.argv[1]
    output_base_folder = sys.argv[2]

    print("Input folder: {}".format(input_folder))
    print("Output folder: {}".format(output_base_folder))

    ensure_dir(output_base_folder)

    csv_files = get_csv_files(input_folder)

    fieldnames = ["timestamp","sensorId","property","value","unit"]

    print("Progress: {:.2%}".format(0), end="\r", flush=True)

    for i, csv_file in enumerate(csv_files):
        
        input_file = open(csv_file, "r")
        reader = csv.DictReader(input_file)
        
        for row in reader:
            
            output_folder = os.path.join(output_base_folder, row["timestamp"])
            ensure_dir(output_folder)

            output_filename = os.path.join(output_folder, "{}.csv".format(row["sensorId"]))
            ensure_csv(output_filename, fieldnames)

            output_file = open(output_filename, "a")
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writerow(row)
            output_file.close()

        input_file.close()

        print("Progress: {:.2%}".format(i / len(csv_files)), end="\r", flush=True)
    
    print("Progress: {:.2%}".format(1), flush=True)

    print("Done!")
    
    