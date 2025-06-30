# syft-objects collections - ObjectsCollection class for managing multiple objects

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .models import SyftObject

from .client import get_syftbox_client, SYFTBOX_AVAILABLE


class ObjectsCollection:
    """Collection of syft objects that can be indexed and displayed as a table"""

    def __init__(self, objects=None, search_info=None):
        if objects is None:
            self._objects = []
            self._search_info = None
            self._cached = False
        else:
            self._objects = objects
            self._search_info = search_info
            self._cached = True

    def _get_object_email(self, syft_obj: 'SyftObject'):
        """Extract email from syft:// URL"""
        try:
            private_url = syft_obj.private
            if private_url.startswith("syft://"):
                parts = private_url.split("/")
                if len(parts) >= 3:
                    return parts[2]
        except:
            pass
        return "unknown@example.com"

    def _load_objects(self):
        """Load all available syft objects from connected datasites"""
        self._objects = []
        
        try:
            if not SYFTBOX_AVAILABLE:
                return

            syftbox_client = get_syftbox_client()
            if not syftbox_client:
                return

            try:
                datasites = list(map(lambda x: x.name, syftbox_client.datasites.iterdir()))
            except Exception:
                return

            for email in datasites:
                try:
                    public_objects_dir = syftbox_client.datasites / email / "public" / "objects"
                    if public_objects_dir.exists():
                        for syftobj_file in public_objects_dir.glob("*.syftobject.yaml"):
                            try:
                                from .models import SyftObject
                                syft_obj = SyftObject.load_yaml(syftobj_file)
                                self._objects.append(syft_obj)
                            except Exception:
                                continue
                    
                    private_objects_dir = syftbox_client.datasites / email / "private" / "objects"
                    if private_objects_dir.exists():
                        for syftobj_file in private_objects_dir.glob("*.syftobject.yaml"):
                            try:
                                from .models import SyftObject
                                syft_obj = SyftObject.load_yaml(syftobj_file)
                                self._objects.append(syft_obj)
                            except Exception:
                                continue
                                
                except Exception:
                    continue

        except Exception:
            pass

    def refresh(self):
        """Manually refresh the objects collection"""
        self._load_objects()
        return self

    def _ensure_loaded(self):
        """Ensure objects are loaded"""
        self._load_objects()

    def search(self, keyword):
        """Search for objects containing the keyword"""
        self._ensure_loaded()
        keyword = keyword.lower()
        filtered_objects = []

        for syft_obj in self._objects:
            email = self._get_object_email(syft_obj)
            name = syft_obj.name or ""
            desc = syft_obj.description or ""
            created_str = syft_obj.created_at.strftime("%Y-%m-%d %H:%M") if getattr(syft_obj, 'created_at', None) else ""
            updated_str = syft_obj.updated_at.strftime("%Y-%m-%d %H:%M") if getattr(syft_obj, 'updated_at', None) else ""
            system_keys = {"_file_operations"}
            meta_values = [str(v).lower() for k, v in syft_obj.metadata.items() if k not in system_keys]
            if (
                keyword in name.lower()
                or keyword in email.lower()
                or keyword in desc.lower()
                or keyword in created_str.lower()
                or keyword in updated_str.lower()
                or any(keyword in v for v in meta_values)
            ):
                filtered_objects.append(syft_obj)

        search_info = f"Search results for '{keyword}'"
        return ObjectsCollection(objects=filtered_objects, search_info=search_info)

    def filter_by_email(self, email_pattern):
        """Filter objects by email pattern"""
        self._ensure_loaded()
        pattern = email_pattern.lower()
        filtered_objects = []

        for syft_obj in self._objects:
            email = self._get_object_email(syft_obj)
            if pattern in email.lower():
                filtered_objects.append(syft_obj)

        search_info = f"Filtered by email containing '{email_pattern}'"
        return ObjectsCollection(objects=filtered_objects, search_info=search_info)

    def list_unique_emails(self):
        """Get list of unique email addresses"""
        self._ensure_loaded()
        emails = set(self._get_object_email(syft_obj) for syft_obj in self._objects)
        return sorted(list(emails))

    def list_unique_names(self):
        """Get list of unique object names"""
        self._ensure_loaded()
        names = set(syft_obj.name for syft_obj in self._objects if syft_obj.name)
        return sorted(list(names))

    def to_list(self):
        """Convert to a simple list of objects"""
        self._ensure_loaded()
        return list(self._objects)

    def get_by_indices(self, indices):
        """Get objects by list of indices"""
        self._ensure_loaded()
        return [self._objects[i] for i in indices if 0 <= i < len(self._objects)]

    def __getitem__(self, index):
        """Allow indexing like objects[0] or slicing like objects[:3]"""
        self._ensure_loaded()
        if isinstance(index, slice):
            slice_info = f"{self._search_info} (slice {index})" if self._search_info else None
            return ObjectsCollection(objects=self._objects[index], search_info=slice_info)
        return self._objects[index]

    def __len__(self):
        self._ensure_loaded()
        return len(self._objects)

    def __iter__(self):
        self._ensure_loaded()
        return iter(self._objects)

    def __str__(self):
        """Display objects as a nice table"""
        self._ensure_loaded()
        if not self._objects:
            return "No syft objects available"

        try:
            from tabulate import tabulate
            table_data = []
            for i, syft_obj in enumerate(self._objects):
                email = self._get_object_email(syft_obj)
                name = syft_obj.name or "Unnamed Object"
                table_data.append([i, email, name, syft_obj.private, syft_obj.mock])

            headers = ["Index", "Email", "Object Name", "Private URL", "Mock URL"]
            return tabulate(table_data, headers=headers, tablefmt="grid")
        except ImportError:
            lines = ["Available Syft Objects:" if self._objects else "No syft objects available"]
            for i, syft_obj in enumerate(self._objects):
                email = self._get_object_email(syft_obj)
                name = syft_obj.name or "Unnamed Object"
                lines.append(f"{i}: {name} ({email})")
            return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def help(self):
        """Show help and examples for using the objects collection"""
        help_text = """
🔐 Syft Objects Collection Help

Import Convention:
  import syft_objects as syo

Interactive UI:
  syo.objects              # Show interactive table with search & selection
  • Use search box to filter in real-time
  • Check boxes to select objects  
  • Click "Generate Code" for copy-paste Python code

Programmatic Usage:
  syo.objects[0]           # Get first object
  syo.objects[:3]          # Get first 3 objects
  len(syo.objects)         # Count objects

Search & Filter:
  syo.objects.search("financial")        # Search for 'financial' in names/emails
  syo.objects.filter_by_email("andrew")  # Filter by email containing 'andrew'
  syo.objects.get_by_indices([0,1,5])    # Get specific objects by index
  
Utility Methods:
  syo.objects.list_unique_emails()       # List all unique emails
  syo.objects.list_unique_names()        # List all unique object names
  syo.objects.refresh()                  # Manually refresh the collection
  
Example Usage:
  import syft_objects as syo
  
  # Browse and select objects interactively
  syo.objects
  
  # Selected objects:
  objects = [syo.objects[i] for i in [0, 1, 16, 20, 23]]
  
  # Access object properties:
  obj = syo.objects[0]
  print(obj.name)           # Object name
  print(obj.private)        # Private syft:// URL
  print(obj.mock)           # Mock syft:// URL
  print(obj.description)    # Object description
  
  # Refresh after creating new objects:
  syo.objects.refresh()
        """
        print(help_text)

    def _repr_html_(self):
        """HTML representation for Jupyter notebooks"""
        self._ensure_loaded()
        if not self._objects:
            return "<p><em>No syft objects available</em></p>"

        title = self._search_info if self._search_info else "Available Syft Objects"
        count = len(self._objects)
        search_indicator = (
            f"<p style='color: #28a745; font-style: italic;'>🔍 {self._search_info}</p>"
            if self._search_info
            else ""
        )

        container_id = f"syft-objects-container-{hash(str(self._objects)) % 10000}"

        # Generate table HTML with interactive features
        return self._generate_interactive_table_html(title, count, search_indicator, container_id)

    def _generate_interactive_table_html(self, title, count, search_indicator, container_id):
        """Generate the interactive HTML table"""
        # This is a simplified version - the full implementation would include
        # all the CSS styling and JavaScript functionality from the original
        html = f"""
        <div style="border: 1px solid #ddd; border-radius: 6px; font-family: sans-serif;">
            <div style="background: #f8f9fa; padding: 10px; border-bottom: 1px solid #ddd;">
                <strong>🔐 {title} ({count} total)</strong>
                {search_indicator}
            </div>
            <div style="padding: 10px;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">#</th>
                            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Email</th>
                            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Name</th>
                            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Private URL</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for i, syft_obj in enumerate(self._objects):
            email = self._get_object_email(syft_obj)
            name = syft_obj.name or "Unnamed Object"
            html += f"""
                        <tr>
                            <td style="padding: 6px; border-bottom: 1px solid #eee;">{i}</td>
                            <td style="padding: 6px; border-bottom: 1px solid #eee; color: #0066cc;">{email}</td>
                            <td style="padding: 6px; border-bottom: 1px solid #eee; color: #28a745;">{name}</td>
                            <td style="padding: 6px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 11px;">{syft_obj.private}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html 