# CSS Analysis Tools

A set of Python tools for analyzing CSS class usage in React/TSX projects.

## Setup

1. Activate the virtual environment:

```bash
source css-analyzer-env/bin/activate
```

## Tools

### 1. scan_tsx_classes.py

Scans TSX files and extracts all CSS classes in use.

**Usage:**

```bash
python scan_tsx_classes.py -p ../src -v
python scan_tsx_classes.py -p ../src -o used_classes.txt
```

**Options:**

- `-p, --path`: Path to scan for TSX files (default: current directory)
- `-o, --output`: Output file to write results
- `-v, --verbose`: Verbose output

### 2. scan_css_classes.py

Scans CSS files and extracts all class definitions.

**Usage:**

```bash
python scan_css_classes.py -f ../src/index.css -v
python scan_css_classes.py -f ../src/index.css -o css_classes.txt
```

**Options:**

- `-f, --file`: CSS file to scan (required)
- `-o, --output`: Output file to write results
- `-v, --verbose`: Verbose output

### 3. extract_used_css.py

Extracts only the CSS rules for classes that are actually used in TSX files.

**Usage:**

```bash
python extract_used_css.py -c ../src/index.css -t ../src -o used_styles.css -v
```

**Options:**

- `-c, --css-file`: CSS file to extract from (required)
- `-t, --tsx-path`: Path to scan for TSX files (required)
- `-o, --output`: Output CSS file (required)
- `-v, --verbose`: Verbose output

## Example Workflow

1. **Analyze current usage:**

```bash
# See what classes are being used
python scan_tsx_classes.py -p ../src -v

# See what classes are defined in CSS
python scan_css_classes.py -f ../src/index.css -v
```

2. **Extract only used styles:**

```bash
# Create a minimal CSS file with only used classes
python extract_used_css.py \
  -c ../src/index.css \
  -t ../src \
  -o minimal_styles.css \
  -v
```

This will help identify unused CSS and create optimized stylesheets.
