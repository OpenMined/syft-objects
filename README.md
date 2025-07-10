# Syft-Objects in 5 Minutes

Syft-objects are best understood in the context of the problem it solves **for OpenMined community members prototyping apps** (and maybe someday for SyftBox dev-users and data scientists)

**Problem:** Unless its a dataset, syftbox users cannot discover or address syftbox files they don't have READ access to. 

**Cost:** Consequently, we waste enormous time building complex RPC/RDS apps to keep track of private intermediate/final variables in use-case specific settings. 

**Solution:** Syft-objects exists to enable users to discover and address (i.e. get a url for) non-dataset objects, reducing the burden on RPC/RDS to mold around following the state of hidden variables.

**Benefit:** I believe this could greatly reduce the complexity of use-case specific builds, and I believe is part of a broader set of tools capable of enabling OpenMined staff to build prototypes in 1 day instead of multiple months. Due to its possible benefits, I believe that syft-objects could have a material impact on the likelihood that the OpenMined community is successful in its mission.

## Part 1: What is syft-objects

(multiple answers in increasing order of complexity)

- it's syft-datasets for all files in SyftBox
- it's a python library for writing .config files which point to mock and real assets
- it's a means of enabling files you can't READ to have an address and schema you can write code against
- it's a way to discover and address non-dataset objects across the syftbox network you don't have READ access to — such as intermediate or final variables in an RDS/NSAI information flow (or any other federated software application)

Syft-objects centers around a permissioned list of objects that a user is able to see.

```python
import syft_objects as so 
so.objects
```

The clever part about this view is that **it is permissioned**. This means that **what you see != what others see**. 
- **Discoverability:** If your email is included in discover_read, then objects will show up *for you*.
- **Mock Visibility:** If you have mock_read permissions, then the "mock" button will be clickable and you can look at the mock file.
- **Private Visibility:** If you have private_read permissions, then the "Private" button will be clickable and you can look at the private data (e.g. if the syft-object refers to your data).

It's this decoupling of read/write permissions from discoverability that makes syft-objects special. It accomplishes this by creating syftobject.yaml files which look like this:

```yaml
created_at: '2025-07-09T03:51:19.701371+00:00'
description: Object 'Sales Data' with explicit mock and private files
metadata:
  _file_operations:
    created_files: []
    files_moved_to_syftbox:
    - "test_real.csv → syft://liamtrask@gmail.com/private/objects/test_real.csv"
    - "test_mock.csv → syft://liamtrask@gmail.com/public/objects/test_real.csv"
    syftbox_available: true
    syftobject_yaml_path: null
mock_permissions:
- public
mock_url: syft://liamtrask@gmail.com/public/objects/test_real.csv
mock_write_permissions: []
name: Sales Data
object_type: file
private_permissions:
- liamtrask@gmail.com
private_url: syft://liamtrask@gmail.com/private/objects/test_real.csv
private_write_permissions:
- liamtrask@gmail.com
syftobject: syft://liamtrask@gmail.com/public/objects/sales_data_d3f96747.syftobject.yaml
syftobject_permissions:
- public
uid: d3f96747-3b27-4e80-b4f4-f3ba2c2ee468
updated_at: '2025-07-09T03:51:19.701375+00:00'
```

In another way, **syft-objects is just a fancy python library for CRUD of these config files** (and the mock/private files this yaml file points to).

## Part 2: How do I use syft-objects?

To use syft-objects, you follow four steps:

1. Import the library
2. Find a syft-object
3. Use the syft-object to create new syft-objects
4. Repeat until you have created your final outputs (and request READ access for them)

### Step 1: Import the library as "so"

```bash
pip install syft-objects
```

```python
import syft_objects as so
```

### Step 2: Find an object

To find an object, use so.objects:
  1. Searchbar / Filter by Admin: type key terms related to your search.
  2. Browse: scroll through the search results and look for things that interest you.
  3. Inspect: When you see interesting datasets, click "Mock" and "Info" to see if the dataset has everything you want.
  4. Select: When things interest you, click the "checkbox" next to each row
  5. Copy: Click the "Python" button at the top, which copies python code to your clipboard
  6. Paste: Paste the python code into the next cell. You now have syft-object variables you can do things with.

```python
# Try the following:

# SEARCHBAR / BROWSE / INSPECT / SELECT
# 1. enter "Netflix" in the search bar 
# 2. click the "Mock" and "Info" tabs in interesting rows
# 3. click the checkboxes for several entries
# 4. click the "Python" button
# 5: paste code in the cell below

so.objects
```

```python
# This is an example of copy-pasted code
results_17 = [so.objects["0b2f982d-6f82-48f3-b32e-3005e186e1cc"]]
```

### Step 3: Use the syft-object to create more syft-objects

The syft-object API serves two purposes: discoverability and use.

- **Discoverability:** 90% of the syft-object API and interface is about providing metadata for discoverability
  1. name
  2. description
  3. admin
  4. permissions:
     - discovery_read
     - mock_read
     - mock_write
     - private_read
     - private_write
  6. uid
  7. created
  8. type
  9. metadata
      
- **Use:** 10% of the API provides the key assets which aid with use:

  1. *Mock:* A pretend version of the object you can use to write code against, so you know your code will compile and run against the real asset on someone else's computer.
  2. *Private Filepath:* The path of the object on someone else's computer
  3. *so.create_object()* A method used to create new syft-objects while in a computation.

Step 3 leverages these three API endpoints to use a syft-object to create more syft-objects

```python
# Select the mock and understand its contents
mock_obj = results_17[0].mock
type(mock_obj.obj)  # pandas.core.frame.DataFrame

# Test some code against the mock
my_result = len(mock_obj.obj)  # 137

# Find the address to the real object (on someone else's computer)
mock_obj.path  # '/Users/atrask/SyftBox/datasites/jajif89762@ofacer.com/public/objects/NetflixViewingHistory.csv'

# Get my datasite's email (for permissions of mock outputs)
from syft_core import Client
Client.load().email  # 'liamtrask@gmail.com'

# Create a function which could execute on someone else's computer
def my_data_science_query():

    ## ===== BEGIN SYFT-SPECIFIC INPUT LOADING ===== 
    
    import syft_object as so
    import pandas as pd

    # get the private object (assuming this method is running on someone else's computer)
    path = '/Users/atrask/SyftBox/datasites/jajif89762@ofacer.com/public/objects/NetflixViewingHistory.csv'
    private_obj = pd.DataFrame(path)

    ## ===== END SYFT-SPECIFIC INPUT LOADING ===== 
    
    # compute result
    my_result = len(private_obj)

    ## ===== BEGIN SYFT-SPECIFIC OUTPUT SAVING ===== 
    
    # save the real result
    f = open('intermediate_result.txt', 'w')
    f.write(str(my_result))
    f.close()

    # save a mock result (random but representative)
    f = open('mock_intermediate_result.txt', 'w')
    f.write(str(100))
    f.close()
    
    # write results to new syft-object
    so.create_object(name=my_result, 
                     private_file='intermediate_result.txt', # this is the file we're creating a syft-object around, I won't be able to read it 
                     mock_file='mock_intermediate_result.txt', # this is the file I'll be able to actually read later
                     discovery_read=['liamtrask@gmail.com'], # only I can see this syft object (as opposed to "public")
                     mock_read=['liamtrask@gmail.com']) # only I can see this mock (as opposed to "public")

    ## ===== END SYFT-SPECIFIC OUTPUT SAVING =====
```

### MISSING STEP HERE

At this point we'd submit our "my_data_science_query()" to be run on someone else's machine. However, that's not the job of syft-objects. It's the job of programs like [syft-data-science](https://github.com/OpenMined/syft-data-science) and [syft-queue](https://github.com/OpenMined/syft-queue). Please see their tutorials for more on this.

### Step 4: Repeat until you have created your final outputs

And with the above process, a data user can run a program which creates intermediate results, and then run followup programs which use those intermediate results. Crucially, intermediate results can be any file type, such as:
- CSV
- SQL Lite databases
- Python Code! (my_code.py)
- Huggingface Models
- ...

Everything file-based is supported by default (note the underlying structures are also language agnostic — although this tutorial happens to be in Python and use a Python library/SDK)

## Part 3: What are basic CRUD operations for Syft-Objects?

Syft-objects support basic CRUD on all their metadata through:
- **UIs:** there are 3 UI options to choose from (so.objects, SyftBox UI -> apps -> syft-objects, or you can click the "Open in Window" button in the so.objects which will open a localhost website). And through this UI you can:
    - **Create:** by drag-and-drop into the UI OR by clicking the "New" button and filing out the form
    - **Read:** by searching/browsing the UI and clicking through its many buttons
    - **Update:** You can update an object's Mock or Private file (if you have WRITE access) by clicking the "Mock" or "Private" buttons on its row in the UI.
    - **Delete:** You can delete a syft-object by clicking the small, red garbage can icon on the right side of that object's row, or by clicking the checkbox on the left side and pushign the "Delete Selected" button.
      
- **Python API:** CRUD operations exist (most comprehensively) on the python API.
    - **Create:** so.create_object()
    - **Read:** You can either return the object in Jupyter notebook (which will render an _html_repr_) or you can use getter methods present on each syft-object: (get_created_at, get_description, get_file_type, get_info, get_metadata, get_name, get_path, get_permissions, get_uid, get_updated_at, get_urls)
    - **Update:** For every getter there is also a setter.
    - **Delete:** Each syft-object has a .delete_obj() method.

### Python API Examples

#### CREATE with Python API

```python
# Basic creation with inline content
obj = so.create_object(
    name="Customer Analysis", 
    mock_contents="Sample: 100 customers, avg age 42, 60% retention rate",
    private_contents="Full: 47,293 customers, avg age 41.7, 58.3% retention, avg LTV $1,247",
    
    # Permission control
    discovery_read=["public"],           # Who knows it exists
    mock_read=["employee@company.com"],  # Who sees demo
    private_read=["cfo@company.com"]     # Who sees real data
)

# File-based creation
dataset = so.create_object(
    name="Dataset Analysis",
    mock_file="sample_100_rows.csv",      # Demo file path
    private_file="full_50k_rows.csv",     # Real file path
    discovery_read=["public"]
)
```

#### READ with Python API

```python
# Display in Jupyter (shows rich HTML widget)
obj

# Access mock data
mock_obj = obj.mock
type(mock_obj.obj)  # Check the type

# Get various properties
obj.get_name()
obj.get_created_at()
obj.get_description()
obj.get_permissions()
obj.get_urls()
obj.get_metadata()
```

#### UPDATE with Python API

```python
# Update name
obj.set_name("Updated Analysis")

# Update permissions
obj.set_permissions(
    mock_read=["new-user@company.com"],
    private_read=["cfo@company.com", "ceo@company.com"]
)

# Update metadata
obj.update_metadata({
    "department": "Finance",
    "version": "2.0"
})
```

#### DELETE with Python API

```python
# Delete the object
obj.delete_obj()
```

## Installation

```bash
pip install syft-objects
```

For SyftBox integration:
```bash
pip install syft-objects[syftbox]
```

### SyftBox Auto-Installation

When you import `syft_objects`, it automatically sets up the SyftBox app if SyftBox is installed:

```python
import syft_objects  # Auto-installs to ~/SyftBox/apps/ if needed
```

## Web Interface

Access your objects through a modern web UI:

```bash
# Start the web server
./run.sh
```

Visit `http://localhost:8004` to:
- Browse all objects in a searchable table
- View detailed object information
- Edit files with syntax highlighting
- Manage permissions interactively

## License

Apache License 2.0