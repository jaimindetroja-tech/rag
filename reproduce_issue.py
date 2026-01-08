
import sys
import os

# Add root to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from indexing import create_vector_index
from models import setup_global_settings

print("Setting up models...")
setup_global_settings()
print("Creating vector index...")
index = create_vector_index()
print("Vector index created:", index)
if index:
    print("Success!")
else:
    print("Failed to create index.")
