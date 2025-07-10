# 🎯 Syft Objects

[![PyPI version](https://badge.fury.io/py/syft-objects.svg)](https://badge.fury.io/py/syft-objects)

**Discover and use files you can't read.** Syft Objects enables federated data science by letting you write code against mock data that runs on real data elsewhere.

## Why Syft Objects?

In federated computing, you often need to:
- 🔍 **Discover** files that exist on other machines
- 📍 **Address** those files in your code
- 🧪 **Test** your code locally before running remotely
- 🔐 **Control** who can see what

Syft Objects solves this by providing a simple mock/private pattern for any file type.

## Installation

```bash
pip install syft-objects
```

## Quick Start

```python
import syft_objects as so

# Create an object with mock (public) and private versions
analysis = so.create_object(
    name="Q4 Sales Analysis",
    mock_contents="Revenue up 10% to $2.5M",         # What others see
    private_contents="Revenue: $2,547,891.23",       # What you see
    discovery_read=["public"],                       # Who can discover it
    mock_read=["team@customer_company.com"],         # Who can see mock
    private_read=["cfo@our_company.com"]             # Who can see real data
)

# Browse available objects
so.objects  # Interactive table with search, filter, and permissions
```

## Core Concepts

### 1. Every Object Has Two Versions
- **Mock**: Sample/demo data anyone can code against
- **Private**: Real data only authorized users can access

### 2. Permissioned Discovery
```python
# Others can discover your object exists, even if they can't read it
so.objects  # Shows objects YOU can discover (not everyone sees the same list)
```

### 3. Write Once, Run Anywhere
```python
# Test locally with mock data
netflix_data = so.objects["0b2f982d-6f82-48f3-b32e-3005e186e1cc"]
result = len(netflix_data.mock.obj)  # Works with mock

# Same code runs on private data elsewhere
def analyze_netflix_data():
    data = pd.read_csv(netflix_data.private.path)  # Runs on real data
    return len(data)
```

## Common Workflows

### Creating Objects from Files
```python
# From existing files
dataset = so.create_object(
    name="Customer Dataset",
    mock_file="sample_100.csv",
    private_file="customers_full.csv"
)

# From folders
model = so.create_object(
    name="ML Model",
    mock_folder="model_demo/",
    private_folder="model_prod/"
)
```

### Finding and Using Objects
```python
# 1. Browse available objects
so.objects

# 2. Search and select (checkbox) objects of interest
# 3. Click "Python" button to copy code
# 4. Paste and use:
results = [so.objects["uid-here"]]
mock_data = results[0].mock.obj
```

### Creating Derivative Objects
```python
# Your analysis creates new syft objects
def my_analysis():
    # Load input
    input_data = pd.read_csv(input_path)
    
    # Process
    result = len(input_data)
    
    # Save as new syft object
    so.create_object(
        name=f"Row count: {result}",
        private_file="result.txt",
        mock_file="result_mock.txt",
        discovery_read=["researcher@university.edu"]
    )
```

## CRUD Operations

### Create
```python
obj = so.create_object(name="My Object", mock_contents="demo", private_contents="real")
```

### Read
```python
obj.get_name()
obj.get_permissions() 
obj.mock.obj  # Access mock data
```

### Update
```python
obj.set_name("Updated Name")
obj.set_permissions(mock_read=["new@user.com"])
```

### Delete
```python
obj.delete_obj()
```

## Web Interface

```bash
./run.sh  # Starts web UI at http://localhost:8004
```

Features:
- Search and filter objects
- Drag-and-drop file upload
- Edit permissions
- View/edit mock and private files

## How It Works

Syft Objects creates YAML config files that point to mock and private versions of your data:

```yaml
name: Sales Data
mock_url: syft://user@email.com/public/objects/sales_mock.csv
private_url: syft://user@email.com/private/objects/sales_real.csv
mock_permissions: [public]
private_permissions: [cfo@company.com]
```

The library handles all the complexity of:
- File management and syft:// URLs
- Permission checking
- Mock/private switching
- Cross-datasite discovery

## Use Cases

- **Federated Data Science**: Write analysis code against mock data, run on real data elsewhere
- **Privacy-Preserving ML**: Train models on distributed data without seeing it
- **Secure Collaboration**: Share data structure without revealing contents
- **Intermediate Results**: Track outputs from multi-step federated computations

## Learn More

- **Tutorial**: See `5mins.ipynb` for hands-on examples
- **Federated Execution**: Use with [syft-queue](https://github.com/OpenMined/syft-queue) or [syft-data-science](https://github.com/OpenMined/syft-data-science)
- **Issues**: https://github.com/OpenMined/syft-objects/issues

## License

Apache License 2.0