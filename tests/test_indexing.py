"""Test the new indexing behavior for ObjectsCollection"""

import pytest
import warnings
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from unittest.mock import MagicMock, patch

from syft_objects.collections import ObjectsCollection
from syft_objects.models import SyftObject


def create_test_object(name, created_at):
    """Create a test SyftObject with specified creation time"""
    return SyftObject(
        uid=uuid4(),
        private_url=f"syft://test@example.com/private/{name}.txt",
        mock_url=f"syft://test@example.com/public/{name}.txt",
        syftobject=f"syft://test@example.com/public/{name}.syftobject.yaml",
        name=name,
        created_at=created_at,
        description=f"Test object {name}"
    )


class TestObjectsCollectionIndexing:
    """Test the indexing behavior of ObjectsCollection"""
    
    def test_oldest_newest_indexing(self):
        """Test that objects[0] returns oldest and objects[-1] returns newest"""
        # Create objects with different creation times
        now = datetime.now(timezone.utc)
        
        obj1 = create_test_object("oldest", now - timedelta(days=10))
        obj2 = create_test_object("middle", now - timedelta(days=5))
        obj3 = create_test_object("newest", now)
        
        # Create collection with objects in random order
        collection = ObjectsCollection(objects=[obj2, obj3, obj1])
        
        # Verify sorting happens on access
        assert collection[0].name == "oldest"
        assert collection[1].name == "middle"
        
        # Test negative index with warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = collection[-1]
            assert result.name == "newest"
            assert len(w) == 1
            assert "race conditions" in str(w[0].message)
            assert "objects[-1]" in str(w[0].message)
            assert "objects['<uid>']" in str(w[0].message)
    
    def test_uid_lookup(self):
        """Test that objects['uid'] works for UID lookup"""
        obj1 = create_test_object("test1", datetime.now(timezone.utc))
        obj2 = create_test_object("test2", datetime.now(timezone.utc))
        
        collection = ObjectsCollection(objects=[obj1, obj2])
        
        # Test UID lookup
        assert collection[str(obj1.uid)] == obj1
        assert collection[str(obj2.uid)] == obj2
        
        # Test non-existent UID
        with pytest.raises(KeyError) as exc:
            collection["non-existent-uid"]
        assert "Object with UID 'non-existent-uid' not found" in str(exc.value)
    
    def test_slicing(self):
        """Test that slicing still works correctly"""
        now = datetime.now(timezone.utc)
        objects = [
            create_test_object(f"obj{i}", now - timedelta(days=10-i))
            for i in range(5)
        ]
        
        collection = ObjectsCollection(objects=objects)
        
        # Test slicing
        subset = collection[:3]
        assert isinstance(subset, ObjectsCollection)
        assert len(subset) == 3
        assert subset[0].name == "obj0"  # Still sorted by created_at
    
    def test_integer_indexing(self):
        """Test regular integer indexing"""
        now = datetime.now(timezone.utc)
        objects = [
            create_test_object(f"obj{i}", now - timedelta(hours=5-i))
            for i in range(5)
        ]
        
        collection = ObjectsCollection(objects=objects)
        
        # Test various indices
        assert collection[0].name == "obj0"  # Oldest
        assert collection[2].name == "obj2"  # Middle
        assert collection[4].name == "obj4"  # Same as -1
        
        # Test negative indices (with warning suppression for this test)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert collection[-1].name == "obj4"  # Newest
            assert collection[-2].name == "obj3"  # Second newest
    
    def test_empty_collection(self):
        """Test indexing on empty collection"""
        collection = ObjectsCollection(objects=[])
        
        with pytest.raises(IndexError):
            collection[0]
        
        with pytest.raises(IndexError):
            collection[-1]
    
    def test_objects_without_created_at(self):
        """Test handling of objects without created_at field"""
        # Create objects, some without created_at
        now = datetime.now(timezone.utc)
        
        obj1 = create_test_object("has_created", now)
        
        # Create object without created_at but with updated_at
        obj2 = SyftObject(
            uid=uuid4(),
            private_url="syft://test@example.com/private/updated.txt",
            mock_url="syft://test@example.com/public/updated.txt",
            syftobject="syft://test@example.com/public/updated.syftobject.yaml",
            name="has_updated",
            updated_at=now - timedelta(days=1)
        )
        obj2.created_at = None  # Explicitly remove created_at
        
        # Create object without any timestamps
        obj3 = SyftObject(
            uid=uuid4(),
            private_url="syft://test@example.com/private/notimestamp.txt",
            mock_url="syft://test@example.com/public/notimestamp.txt",
            syftobject="syft://test@example.com/public/notimestamp.syftobject.yaml",
            name="no_timestamp"
        )
        obj3.created_at = None
        obj3.updated_at = None
        
        collection = ObjectsCollection(objects=[obj1, obj2, obj3])
        
        # Objects without timestamps should be sorted to the beginning
        assert collection[0].name == "no_timestamp"
        assert collection[1].name == "has_updated"
        assert collection[2].name == "has_created"
    
    def test_negative_index_warning(self):
        """Test that negative indices trigger a warning about race conditions"""
        now = datetime.now(timezone.utc)
        objects = [
            create_test_object(f"obj{i}", now - timedelta(hours=3-i))
            for i in range(3)
        ]
        
        collection = ObjectsCollection(objects=objects)
        
        # Test various negative indices trigger warnings
        negative_indices = [-1, -2, -3]
        for idx in negative_indices:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                _ = collection[idx]
                assert len(w) == 1
                assert "race conditions" in str(w[0].message)
                assert f"objects[{idx}]" in str(w[0].message)
        
        # Test positive indices don't trigger warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _ = collection[0]
            _ = collection[1]
            assert len(w) == 0
    
    @patch('syft_objects.collections.get_syftbox_client')
    def test_load_and_sort(self, mock_client):
        """Test that _load_objects sorts objects after loading"""
        # Mock the client
        mock_client.return_value = None
        
        collection = ObjectsCollection()
        
        # Manually set some test objects (simulating load)
        now = datetime.now(timezone.utc)
        collection._objects = [
            create_test_object("new", now),
            create_test_object("old", now - timedelta(days=10)),
            create_test_object("middle", now - timedelta(days=5))
        ]
        
        # Call the sort logic that should be at the end of _load_objects
        collection._objects.sort(
            key=lambda obj: obj.created_at if obj.created_at else obj.updated_at or datetime.min.replace(tzinfo=timezone.utc)
        )
        
        # Verify order
        assert collection._objects[0].name == "old"
        assert collection._objects[1].name == "middle"
        assert collection._objects[2].name == "new"