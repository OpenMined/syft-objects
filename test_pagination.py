#!/usr/bin/env python3
"""Test pagination in the static widget"""

import syft_objects as so

# Create many test objects to test pagination
for i in range(120):
    so.create_object(f"Test Object {i+1}", private_contents=f"This is test object number {i+1}")

# Refresh and display
so.objects.refresh()
print(f"Total objects: {len(so.objects)}")

# Save the HTML to a file to inspect
html = so.objects._generate_fallback_widget()
with open("test_widget.html", "w") as f:
    f.write(html)
print("Widget HTML saved to test_widget.html")