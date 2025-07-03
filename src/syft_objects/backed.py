"""
SyftBox-backed file-based object system.

This module provides generic file-based object classes that store attributes
in syft-object files, providing automatic mock/private value separation.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
from uuid import UUID, uuid4

from .models import SyftObject, utcnow
from .factory import syobj, detect_user_email


class SingleSyftObjBacked:
    """
    A generic file-based object backed by a single syft-object file.
    
    This class doesn't retain any internal state - all data is stored in a single
    syft-object file that provides automatic mock/private value separation.
    
    Most methods are private to hide implementation details from subclasses.
    """
    
    def __init__(self, object_path: Union[str, Path], object_name: str = None, owner_email: str = None, create_if_missing: bool = True):
        """
        Initialize a SyftBox-backed object.
        
        Args:
            object_path: Path to the object's directory
            object_name: Name for the object (used in syft-object naming)
            owner_email: Email of the owner (auto-detected if not provided)
            create_if_missing: Whether to create the object if it doesn't exist
        """
        self._object_path = Path(object_path)
        self._object_name = object_name or self._object_path.name
        self._owner_email = owner_email or detect_user_email()
        self._syft_object = None
        self._fallback_file = self._object_path / "data.json"
        
        if create_if_missing:
            self._object_path.mkdir(parents=True, exist_ok=True)
            if not self._has_backing_file():
                self._initialize_backing_file()
    
    @property
    def object_path(self) -> Path:
        """Get the path to this object's directory."""
        return self._object_path
    
    def _has_backing_file(self) -> bool:
        """Check if the backing file exists."""
        syft_object_file = self._object_path / f"{self._object_name}.syftobject.yaml"
        return syft_object_file.exists() or self._fallback_file.exists()
    
    def _initialize_backing_file(self) -> None:
        """Initialize the backing file with empty data."""
        initial_data = {
            "created_at": datetime.now().isoformat(),
            "object_name": self._object_name,
            "owner_email": self._owner_email,
            "attributes": {}
        }
        
        try:
            # Create syft-object with initial data
            private_content = json.dumps(initial_data, indent=2)
            mock_content = json.dumps({
                "object_name": self._object_name,
                "created_at": initial_data["created_at"],
                "type": "SingleSyftObjBacked",
                "attributes": "[Private - contact owner for access]"
            }, indent=2)
            
            self._syft_object = syobj(
                name=self._object_name,
                private_contents=private_content,
                mock_contents=mock_content,
                private_read=[self._owner_email],
                private_write=[self._owner_email],
                mock_read=["public"],
                mock_write=[],
                metadata={
                    "object_type": "SingleSyftObjBacked",
                    "object_name": self._object_name,
                    "owner_email": self._owner_email,
                    "save_to": str(self._object_path / f"{self._object_name}.syftobject.yaml")
                }
            )
        except Exception as e:
            print(f"Warning: Could not create syft-object, using fallback JSON: {e}")
            # Fallback to JSON file
            with open(self._fallback_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def _load_backing_file(self) -> Dict[str, Any]:
        """Load data from the backing file."""
        syft_object_file = self._object_path / f"{self._object_name}.syftobject.yaml"
        if syft_object_file.exists():
            try:
                if self._syft_object is None:
                    self._syft_object = SyftObject.load_yaml(syft_object_file)
                
                # Get private content - check if it has proper structure
                if hasattr(self._syft_object, 'private') and hasattr(self._syft_object.private, 'file'):
                    if hasattr(self._syft_object.private.file, 'read_text'):
                        # It's a Path object
                        private_content = self._syft_object.private.file.read_text()
                    else:
                        # It's a file handle, use regular read
                        private_content = self._syft_object.private.file.read()
                    
                    return json.loads(private_content)
                else:
                    raise Exception("Syft-object structure not as expected")
                    
            except Exception as e:
                print(f"Error loading syft-object: {e}")
                return {"attributes": {}}
        
        # Fallback to JSON file
        if self._fallback_file.exists():
            try:
                with open(self._fallback_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {"attributes": {}}
    
    def _save_backing_file(self, data: Dict[str, Any]) -> None:
        """Save data to the backing file."""
        if self._syft_object is not None:
            try:
                # Update private content
                private_content = json.dumps(data, indent=2)
                
                # Create mock content (sanitized version)
                mock_data = {
                    "object_name": self._object_name,
                    "created_at": data.get("created_at", datetime.now().isoformat()),
                    "type": "SingleSyftObjBacked",
                    "last_updated": datetime.now().isoformat(),
                    "attributes": {
                        "count": len(data.get("attributes", {})),
                        "keys": list(data.get("attributes", {}).keys())[:5]  # Show first 5 keys
                    }
                }
                mock_content = json.dumps(mock_data, indent=2)
                
                # Update syft-object - check if it has proper structure
                if hasattr(self._syft_object, 'private') and hasattr(self._syft_object.private, 'file'):
                    if hasattr(self._syft_object.private.file, 'write_text'):
                        # It's a Path object
                        self._syft_object.private.file.write_text(private_content)
                        self._syft_object.mock.file.write_text(mock_content)
                    else:
                        # It's a file handle, use regular write
                        self._syft_object.private.file.write(private_content)
                        self._syft_object.mock.file.write(mock_content)
                    
                    # Update metadata if possible
                    if hasattr(self._syft_object, 'updated_at'):
                        self._syft_object.updated_at = datetime.now()
                    
                    # Save syft-object metadata if possible
                    if hasattr(self._syft_object, 'save_yaml'):
                        syft_object_file = self._object_path / f"{self._object_name}.syftobject.yaml"
                        self._syft_object.save_yaml(syft_object_file)
                else:
                    # Fallback if syft-object structure is unexpected
                    raise Exception("Syft-object structure not as expected")
                
            except Exception as e:
                print(f"Error saving syft-object: {e}")
                # Fallback to JSON
                with open(self._fallback_file, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            # Fallback to JSON file
            with open(self._fallback_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def _set_attribute(self, name: str, value: Any) -> None:
        """
        Set an attribute value in the backing file.
        
        Args:
            name: Name of the attribute
            value: Value to store (must be JSON-serializable)
        """
        data = self._load_backing_file()
        if "attributes" not in data:
            data["attributes"] = {}
        
        # Serialize complex types
        data["attributes"][name] = self._serialize_value(value)
        data["last_updated"] = datetime.now().isoformat()
        
        self._save_backing_file(data)
    
    def _get_attribute(self, name: str, default: Any = None) -> Any:
        """
        Get an attribute value from the backing file.
        
        Args:
            name: Name of the attribute
            default: Default value if attribute doesn't exist
            
        Returns:
            The attribute value, or default if not found
        """
        data = self._load_backing_file()
        attributes = data.get("attributes", {})
        
        if name not in attributes:
            return default
        
        return self._deserialize_value(attributes[name])
    
    def _has_attribute(self, name: str) -> bool:
        """Check if an attribute exists."""
        data = self._load_backing_file()
        attributes = data.get("attributes", {})
        return name in attributes
    
    def _delete_attribute(self, name: str) -> bool:
        """
        Delete an attribute.
        
        Args:
            name: Name of the attribute to delete
            
        Returns:
            True if the attribute was deleted, False if it didn't exist
        """
        data = self._load_backing_file()
        attributes = data.get("attributes", {})
        
        if name in attributes:
            del attributes[name]
            data["last_updated"] = datetime.now().isoformat()
            self._save_backing_file(data)
            return True
        return False
    
    def _list_attributes(self) -> List[str]:
        """List all available attributes."""
        data = self._load_backing_file()
        attributes = data.get("attributes", {})
        return list(attributes.keys())
    
    def _set_folder_attribute(self, name: str, create: bool = True) -> Path:
        """
        Set up a folder attribute and return its path.
        
        Args:
            name: Name of the folder attribute
            create: Whether to create the folder if it doesn't exist
            
        Returns:
            Path to the folder
        """
        folder_path = self._object_path / name
        
        if create:
            folder_path.mkdir(parents=True, exist_ok=True)
        
        # Store folder reference in attributes
        self._set_attribute(f"_folder_{name}", str(folder_path))
        
        return folder_path
    
    def _get_folder_attribute(self, name: str) -> Optional[Path]:
        """
        Get a folder attribute path.
        
        Args:
            name: Name of the folder attribute
            
        Returns:
            Path to the folder if it exists, None otherwise
        """
        folder_path = self._object_path / name
        return folder_path if folder_path.exists() else None
    
    def _set_text_file(self, name: str, content: str) -> None:
        """
        Set a text file attribute.
        
        Args:
            name: Name of the text file (without extension)
            content: Text content to write
        """
        # Store in attributes instead of separate file
        self._set_attribute(f"_text_{name}", content)
    
    def _get_text_file(self, name: str, default: str = "") -> str:
        """
        Get content from a text file attribute.
        
        Args:
            name: Name of the text file (without extension)
            default: Default content if file doesn't exist
            
        Returns:
            File content or default
        """
        return self._get_attribute(f"_text_{name}", default)
    
    def _create_syft_pub_yaml(self, folder_name: str, read_permissions: List[str] = None, write_permissions: List[str] = None) -> None:
        """
        Create a syft.pub.yaml file in a folder attribute.
        
        Args:
            folder_name: Name of the folder attribute
            read_permissions: List of emails/patterns that can read (default: ['*'])
            write_permissions: List of emails/patterns that can write (default: [])
        """
        folder_path = self._set_folder_attribute(folder_name, create=True)
        syft_pub_file = folder_path / "syft.pub.yaml"
        
        if read_permissions is None:
            read_permissions = ['*']
        if write_permissions is None:
            write_permissions = []
        
        content = "rules:\n- pattern: '**'\n  access:\n    read:\n"
        for perm in read_permissions:
            content += f"    - '{perm}'\n"
        
        if write_permissions:
            content += "    write:\n"
            for perm in write_permissions:
                content += f"    - '{perm}'\n"
        
        with open(syft_pub_file, 'w') as f:
            f.write(content)
    
    def _serialize_value(self, value: Any) -> Any:
        """Convert a value to JSON-serializable format."""
        if isinstance(value, Path):
            return {"__type__": "Path", "value": str(value)}
        elif isinstance(value, UUID):
            return {"__type__": "UUID", "value": str(value)}
        elif isinstance(value, datetime):
            return {"__type__": "datetime", "value": value.isoformat()}
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        else:
            return value
    
    def _deserialize_value(self, value: Any) -> Any:
        """Convert a JSON value back to its original type."""
        if isinstance(value, dict) and "__type__" in value:
            type_name = value["__type__"]
            if type_name == "Path":
                return Path(value["value"])
            elif type_name == "UUID":
                return UUID(value["value"])
            elif type_name == "datetime":
                return datetime.fromisoformat(value["value"])
        elif isinstance(value, list):
            return [self._deserialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: self._deserialize_value(v) for k, v in value.items()}
        else:
            return value
    
    def _get_all_attributes(self) -> Dict[str, Any]:
        """Get all attributes as a dictionary."""
        data = self._load_backing_file()
        attributes = data.get("attributes", {})
        return {k: self._deserialize_value(v) for k, v in attributes.items()}
    
    def _set_multiple_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set multiple attributes at once."""
        data = self._load_backing_file()
        if "attributes" not in data:
            data["attributes"] = {}
        
        for name, value in attributes.items():
            data["attributes"][name] = self._serialize_value(value)
        
        data["last_updated"] = datetime.now().isoformat()
        self._save_backing_file(data)
    
    def _get_mock_data(self) -> Dict[str, Any]:
        """Get the mock/public version of the data."""
        if self._syft_object is not None:
            try:
                # Check if it has proper structure
                if hasattr(self._syft_object, 'mock') and hasattr(self._syft_object.mock, 'file'):
                    if hasattr(self._syft_object.mock.file, 'read_text'):
                        # It's a Path object
                        mock_content = self._syft_object.mock.file.read_text()
                    else:
                        # It's a file handle, use regular read
                        mock_content = self._syft_object.mock.file.read()
                    
                    return json.loads(mock_content)
                else:
                    raise Exception("Syft-object mock structure not as expected")
                    
            except Exception as e:
                print(f"Error loading mock data: {e}")
        
        # Fallback mock data
        return {
            "object_name": self._object_name,
            "type": "SingleSyftObjBacked",
            "attributes": "[Private - contact owner for access]"
        }
    
    # Public API - minimal interface for object lifecycle
    
    def exists(self) -> bool:
        """Check if this object exists."""
        return self._has_backing_file()
    
    def copy_to(self, destination_path: Union[str, Path]) -> 'SingleSyftObjBacked':
        """
        Copy this object to a new location.
        
        Args:
            destination_path: Path where to copy the object
            
        Returns:
            New SingleSyftObjBacked at the destination
        """
        import shutil
        
        dest_path = Path(destination_path)
        
        # Copy the entire directory structure
        if self._object_path.exists():
            shutil.copytree(self._object_path, dest_path, dirs_exist_ok=True)
        
        return SingleSyftObjBacked(dest_path, self._object_name, self._owner_email, create_if_missing=False)
    
    def move_to(self, destination_path: Union[str, Path]) -> 'SingleSyftObjBacked':
        """
        Move this object to a new location.
        
        Args:
            destination_path: Path where to move the object
            
        Returns:
            New SingleSyftObjBacked at the destination
        """
        import shutil
        
        dest_path = Path(destination_path)
        
        # Move the entire directory structure
        if self._object_path.exists():
            shutil.move(str(self._object_path), str(dest_path))
        
        # Update our own path reference
        self._object_path = dest_path
        
        return self
    
    def delete(self) -> bool:
        """
        Delete this object and all its files.
        
        Returns:
            True if the object was deleted, False if it didn't exist
        """
        import shutil
        
        if self._object_path.exists():
            shutil.rmtree(self._object_path)
            return True
        return False
    
    def __str__(self) -> str:
        """String representation of the object."""
        return f"SingleSyftObjBacked(name={self._object_name}, path={self._object_path})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        attrs = self._list_attributes()
        return f"SingleSyftObjBacked(name={self._object_name}, path={self._object_path}, attributes={attrs})"


class MultiSyftObjBacked:
    """
    A generic file-based object backed by multiple syft-object files.
    
    This class manages multiple syft-objects for different concerns (e.g., config, 
    credentials, cache, logs). Each syft-object provides automatic mock/private 
    value separation.
    
    Most methods are private to hide implementation details from subclasses.
    """
    
    def __init__(self, object_path: Union[str, Path], object_name: str = None, owner_email: str = None, create_if_missing: bool = True):
        """
        Initialize a multi-syft-object backed object.
        
        Args:
            object_path: Path to the object's directory
            object_name: Name for the object (used as prefix for syft-object naming)
            owner_email: Email of the owner (auto-detected if not provided)
            create_if_missing: Whether to create the object if it doesn't exist
        """
        self._object_path = Path(object_path)
        self._object_name = object_name or self._object_path.name
        self._owner_email = owner_email or detect_user_email()
        self._syft_objects: Dict[str, Any] = {}
        self._fallback_files: Dict[str, Path] = {}
        
        if create_if_missing:
            self._object_path.mkdir(parents=True, exist_ok=True)
            # Create a main index file to track all syft-objects
            self._create_index_file()
    
    @property
    def object_path(self) -> Path:
        """Get the path to this object's directory."""
        return self._object_path
    
    def _create_index_file(self) -> None:
        """Create an index file to track all syft-objects."""
        index_file = self._object_path / "index.json"
        if not index_file.exists():
            index_data = {
                "object_name": self._object_name,
                "owner_email": self._owner_email,
                "created_at": datetime.now().isoformat(),
                "syft_objects": {},
                "type": "MultiSyftObjBacked"
            }
            with open(index_file, 'w') as f:
                json.dump(index_data, f, indent=2)
    
    def _load_index_file(self) -> Dict[str, Any]:
        """Load the index file."""
        index_file = self._object_path / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {
            "object_name": self._object_name,
            "owner_email": self._owner_email,
            "syft_objects": {},
            "type": "MultiSyftObjBacked"
        }
    
    def _save_index_file(self, index_data: Dict[str, Any]) -> None:
        """Save the index file."""
        index_file = self._object_path / "index.json"
        index_data["last_updated"] = datetime.now().isoformat()
        
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
    
    def _create_syft_object(self, name: str, initial_data: Dict[str, Any] = None, 
                           private_read: List[str] = None, private_write: List[str] = None,
                           mock_read: List[str] = None, mock_write: List[str] = None) -> Any:
        """
        Create a new syft-object for this multi-object.
        
        Args:
            name: Name for this syft-object (will be prefixed with object_name)
            initial_data: Initial data to store in the syft-object
            private_read: Who can read private data (defaults to owner)
            private_write: Who can write private data (defaults to owner)
            mock_read: Who can read mock data (defaults to public)
            mock_write: Who can write mock data (defaults to nobody)
            
        Returns:
            The created syft-object
        """
        if initial_data is None:
            initial_data = {}
        
        if private_read is None:
            private_read = [self._owner_email]
        if private_write is None:
            private_write = [self._owner_email]
        if mock_read is None:
            mock_read = ["public"]
        if mock_write is None:
            mock_write = []
        
        syft_obj_name = f"{self._object_name}_{name}"
        
        try:
            # Create syft-object with initial data
            private_content = json.dumps(initial_data, indent=2)
            mock_content = json.dumps({
                "object_name": syft_obj_name,
                "parent_object": self._object_name,
                "type": f"MultiSyftObjBacked_{name}",
                "created_at": datetime.now().isoformat(),
                "data": "[Private - contact owner for access]"
            }, indent=2)
            
            syft_obj = syobj(
                name=syft_obj_name,
                private_contents=private_content,
                mock_contents=mock_content,
                private_read=private_read,
                private_write=private_write,
                mock_read=mock_read,
                mock_write=mock_write,
                metadata={
                    "object_type": "MultiSyftObjBacked",
                    "sub_object_name": name,
                    "parent_object": self._object_name,
                    "owner_email": self._owner_email,
                    "save_to": str(self._object_path / f"{syft_obj_name}.syftobject.yaml")
                }
            )
            
            self._syft_objects[name] = syft_obj
        except Exception as e:
            print(f"Warning: Could not create syft-object {name}, using fallback JSON: {e}")
            # Fallback to JSON file
            fallback_file = self._object_path / f"{name}.json"
            with open(fallback_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
            self._fallback_files[name] = fallback_file
        
        # Update index
        index_data = self._load_index_file()
        index_data["syft_objects"][name] = {
            "created_at": datetime.now().isoformat(),
            "syft_object_name": syft_obj_name
        }
        self._save_index_file(index_data)
        
        return self._syft_objects.get(name) or self._fallback_files.get(name)
    
    def _get_syft_object(self, name: str) -> Optional[Any]:
        """Get an existing syft-object by name."""
        if name in self._syft_objects:
            return self._syft_objects[name]
        
        # Try to load from file
        syft_obj_name = f"{self._object_name}_{name}"
        syft_obj_file = self._object_path / f"{syft_obj_name}.syftobject.yaml"
        
        if syft_obj_file.exists():
            try:
                syft_obj = SyftObject.load_yaml(syft_obj_file)
                self._syft_objects[name] = syft_obj
                return syft_obj
            except Exception as e:
                print(f"Error loading syft-object {name}: {e}")
        
        # Fallback to JSON file
        fallback_file = self._object_path / f"{name}.json"
        if fallback_file.exists():
            self._fallback_files[name] = fallback_file
            return fallback_file
        
        return None
    
    def _set_syft_object_data(self, name: str, data: Dict[str, Any]) -> None:
        """Set data in a specific syft-object."""
        syft_obj = self._get_syft_object(name)
        
        if not syft_obj:
            # Create new syft-object if it doesn't exist
            self._create_syft_object(name, data)
            return
        
        if hasattr(syft_obj, 'private'):
            try:
                # Update private content
                private_content = json.dumps(data, indent=2)
                
                # Check if it has proper structure
                if hasattr(syft_obj.private, 'file'):
                    if hasattr(syft_obj.private.file, 'write_text'):
                        # It's a Path object
                        syft_obj.private.file.write_text(private_content)
                    else:
                        # It's a file handle, use regular write
                        syft_obj.private.file.write(private_content)
                
                # Update mock content
                mock_data = {
                    "object_name": f"{self._object_name}_{name}",
                    "parent_object": self._object_name,
                    "type": f"MultiSyftObjBacked_{name}",
                    "last_updated": datetime.now().isoformat(),
                    "data": f"[Private - {len(data)} keys available to authorized users]"
                }
                mock_content = json.dumps(mock_data, indent=2)
                
                if hasattr(syft_obj.mock, 'file'):
                    if hasattr(syft_obj.mock.file, 'write_text'):
                        # It's a Path object
                        syft_obj.mock.file.write_text(mock_content)
                    else:
                        # It's a file handle, use regular write
                        syft_obj.mock.file.write(mock_content)
                
                # Update metadata if possible
                if hasattr(syft_obj, 'updated_at'):
                    syft_obj.updated_at = datetime.now()
                
                # Save syft-object metadata if possible
                if hasattr(syft_obj, 'save_yaml'):
                    syft_obj_name = f"{self._object_name}_{name}"
                    syft_obj_file = self._object_path / f"{syft_obj_name}.syftobject.yaml"
                    syft_obj.save_yaml(syft_obj_file)
                
            except Exception as e:
                print(f"Error updating syft-object {name}: {e}")
                # Fallback to JSON
                fallback_file = self._object_path / f"{name}.json"
                with open(fallback_file, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            # Fallback to JSON file
            with open(syft_obj, 'w') as f:
                json.dump(data, f, indent=2)
    
    def _get_syft_object_data(self, name: str) -> Dict[str, Any]:
        """Get data from a specific syft-object."""
        syft_obj = self._get_syft_object(name)
        
        if not syft_obj:
            return {}
        
        if hasattr(syft_obj, 'private'):
            try:
                # Check if it has proper structure
                if hasattr(syft_obj.private, 'file'):
                    if hasattr(syft_obj.private.file, 'read_text'):
                        # It's a Path object
                        private_content = syft_obj.private.file.read_text()
                    else:
                        # It's a file handle, use regular read
                        private_content = syft_obj.private.file.read()
                    
                    return json.loads(private_content)
                else:
                    raise Exception("Syft-object private structure not as expected")
                    
            except Exception as e:
                print(f"Error reading syft-object {name}: {e}")
                return {}
        else:
            # Fallback to JSON file
            try:
                with open(syft_obj, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
    
    def _list_syft_objects(self) -> List[str]:
        """List all syft-object names in this multi-object."""
        index_data = self._load_index_file()
        return list(index_data.get("syft_objects", {}).keys())
    
    def _delete_syft_object(self, name: str) -> bool:
        """Delete a syft-object."""
        syft_obj_name = f"{self._object_name}_{name}"
        syft_obj_file = self._object_path / f"{syft_obj_name}.syftobject.yaml"
        fallback_file = self._object_path / f"{name}.json"
        
        deleted = False
        
        # Remove syft-object file
        if syft_obj_file.exists():
            syft_obj_file.unlink()
            deleted = True
        
        # Remove fallback file
        if fallback_file.exists():
            fallback_file.unlink()
            deleted = True
        
        # Remove from memory
        if name in self._syft_objects:
            del self._syft_objects[name]
            deleted = True
        
        if name in self._fallback_files:
            del self._fallback_files[name]
            deleted = True
        
        # Update index
        if deleted:
            index_data = self._load_index_file()
            if name in index_data.get("syft_objects", {}):
                del index_data["syft_objects"][name]
                self._save_index_file(index_data)
        
        return deleted
    
    # Public API - minimal interface for object lifecycle
    
    def exists(self) -> bool:
        """Check if this object exists."""
        index_file = self._object_path / "index.json"
        return index_file.exists()
    
    def copy_to(self, destination_path: Union[str, Path]) -> 'MultiSyftObjBacked':
        """
        Copy this object to a new location.
        
        Args:
            destination_path: Path where to copy the object
            
        Returns:
            New MultiSyftObjBacked at the destination
        """
        import shutil
        
        dest_path = Path(destination_path)
        
        # Copy the entire directory structure
        if self._object_path.exists():
            shutil.copytree(self._object_path, dest_path, dirs_exist_ok=True)
        
        return MultiSyftObjBacked(dest_path, self._object_name, self._owner_email, create_if_missing=False)
    
    def move_to(self, destination_path: Union[str, Path]) -> 'MultiSyftObjBacked':
        """
        Move this object to a new location.
        
        Args:
            destination_path: Path where to move the object
            
        Returns:
            New MultiSyftObjBacked at the destination
        """
        import shutil
        
        dest_path = Path(destination_path)
        
        # Move the entire directory structure
        if self._object_path.exists():
            shutil.move(str(self._object_path), str(dest_path))
        
        # Update our own path reference
        self._object_path = dest_path
        
        return self
    
    def delete(self) -> bool:
        """
        Delete this object and all its files.
        
        Returns:
            True if the object was deleted, False if it didn't exist
        """
        import shutil
        
        if self._object_path.exists():
            shutil.rmtree(self._object_path)
            return True
        return False
    
    def __str__(self) -> str:
        """String representation of the object."""
        return f"MultiSyftObjBacked(name={self._object_name}, path={self._object_path})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        syft_objs = self._list_syft_objects()
        return f"MultiSyftObjBacked(name={self._object_name}, path={self._object_path}, syft_objects={syft_objs})" 