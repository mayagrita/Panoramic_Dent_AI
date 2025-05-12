import os

def check_yolo_normalization(labels_dir):
    total_invalid_lines = 0
    affected_files = 0

    for filename in os.listdir(labels_dir):
        if not filename.endswith('.txt'):
            continue
        file_path = os.path.join(labels_dir, filename)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        file_has_invalid = False

        for i, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 5:
                total_invalid_lines += 1
                file_has_invalid = True
                continue
            try:
                class_id = int(parts[0])
                coords = list(map(float, parts[1:]))
                if not all(0 <= val <= 1 for val in coords):
                    total_invalid_lines += 1
                    file_has_invalid = True
            except ValueError:
                total_invalid_lines += 1
                file_has_invalid = True

        if file_has_invalid:
            affected_files += 1

    return affected_files, total_invalid_lines

base_path = r'C:\Users\DELL\Desktop\kaggle-Dental-data set\YOLO\YOLO'
label_dirs = ['train\labels', 'valid\labels', 'test\labels']

total_files = 0
total_lines = 0

for subdir in label_dirs:
    full_path = os.path.join(base_path, subdir)
    print(f"\n فحص المجلد: {full_path}")
    bad_files, bad_lines = check_yolo_normalization(full_path)
    print(f" عدد الملفات غير الصالحة في هذا المجلد: {bad_files}")
    print(f" عدد الأسطر غير الصالحة في هذا المجلد: {bad_lines}")
    total_files += bad_files
    total_lines += bad_lines

print("\n الإحصائيات النهائية:")
print(f" إجمالي عدد الملفات التي تحتوي أسطرًا غير صالحة: {total_files}")
print(f"إجمالي عدد الأسطر غير الصالحة: {total_lines}")

def check_and_fix_yolo_labels(labels_dir, fix_invalid=True):
    total_invalid_lines = 0
    affected_files = 0
    fixed_files = 0

    for filename in os.listdir(labels_dir):
        if not filename.endswith('.txt'):
            continue
        file_path = os.path.join(labels_dir, filename)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        file_has_invalid = False

        for i, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 5:
                total_invalid_lines += 1
                file_has_invalid = True
                continue
            try:
                class_id = int(parts[0])
                coords = list(map(float, parts[1:]))
                if not all(0 <= val <= 1 for val in coords):
                    total_invalid_lines += 1
                    file_has_invalid = True
                    if fix_invalid:
                        coords = [max(0, min(1, val)) for val in coords]
                        new_line = f"{class_id} " + " ".join(map(str, coords)) + "\n"
                        new_lines.append(new_line)
                        continue
            except ValueError:
                total_invalid_lines += 1
                file_has_invalid = True
                continue

            new_lines.append(line)

        if file_has_invalid:
            affected_files += 1
            with open(file_path, 'w') as f:
                f.writelines(new_lines)
            if fix_invalid:
                fixed_files += 1

    return affected_files, total_invalid_lines, fixed_files

base_path = r'C:\Users\DELL\Desktop\kaggle-Dental-data set\YOLO\YOLO'
label_dirs = ['train\labels', 'valid\labels', 'test\labels']

grand_total_invalid_lines = 0
grand_total_affected_files = 0
grand_total_fixed_files = 0

for subdir in label_dirs:
    full_path = os.path.join(base_path, subdir)
    print(f"\n فحص وإصلاح المجلد: {full_path}")
    affected, invalid_lines, fixed = check_and_fix_yolo_labels(full_path, fix_invalid=True)
    print(f" عدد الملفات التي تحتوي أسطرًا غير صالحة: {affected}")
    print(f" عدد الأسطر غير الصالحة: {invalid_lines}")
    print(f" عدد الملفات التي تم تصحيحها: {fixed}")

    grand_total_invalid_lines += invalid_lines
    grand_total_affected_files += affected
    grand_total_fixed_files += fixed

print("\n الإحصائيات الإجمالية:")
print(f" إجمالي الملفات المتأثرة: {grand_total_affected_files}")
print(f" إجمالي الأسطر غير الصالحة: {grand_total_invalid_lines}")
print(f" إجمالي الملفات التي تم تصحيحها: {grand_total_fixed_files}")