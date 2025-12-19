#!/usr/bin/env python3

import os
import json
import yaml
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union

# Configuration
BASE_URL = "https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/main"

def build_url(relative_path: str) -> str:
    """Build full URL from relative path."""
    # Remove leading ./ if present
    path = relative_path.lstrip('./')
    return f"{BASE_URL}/{path}"

def parse_markdown_frontmatter(file_path: str) -> Optional[Dict]:
    """Parse YAML front matter from markdown files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match YAML front matter (---\n...\n---)
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        
        yaml_content = match.group(1)
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"  Warning: Error parsing front matter from {file_path}: {e}")
        return None

def parse_function_metadata(file_path: str) -> Optional[Dict]:
    """Parse function metadata from JavaScript file comments."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match the YAML front matter in comments
        match = re.search(r'/\*---\n(.*?)\n---\*/', content, re.DOTALL)
        if not match:
            return None
        
        yaml_content = match.group(1)
        metadata = yaml.safe_load(yaml_content)
        return metadata.get('thehive') if metadata else None
    except Exception as e:
        print(f"Error parsing metadata from {file_path}: {e}")
        return None

def scan_analyzers(vendor: str) -> tuple[List[Dict], Dict]:
    """Scan analyzers for a vendor and extract subscription info."""
    analyzers_path = Path('.upstream') / 'cortex' / 'analyzers' / vendor
    if not analyzers_path.exists():
        return [], {}
    
    analyzers = []
    subscription_fields = {
        'registration_required': [],
        'subscription_required': [],
        'free_subscription': []
    }
    
    for file_path in analyzers_path.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            relative_path = f".upstream/cortex/analyzers/{vendor}/{file_path.name}"
            
            analyzers.append({
                'name': content.get('name'),
                'version': content.get('version'),
                'description': content.get('description'),
                'dataTypes': content.get('dataTypeList', []),
                'file': relative_path,
                'url': build_url(relative_path)
            })
            
            # Collect subscription fields
            if 'registration_required' in content:
                subscription_fields['registration_required'].append(content['registration_required'])
            if 'subscription_required' in content:
                subscription_fields['subscription_required'].append(content['subscription_required'])
            if 'free_subscription' in content:
                subscription_fields['free_subscription'].append(content['free_subscription'])
                
        except Exception as e:
            print(f"Error reading analyzer {file_path}: {e}")
    
    return analyzers, subscription_fields

def scan_responders(vendor: str) -> tuple[List[Dict], Dict]:
    """Scan responders for a vendor and extract subscription info."""
    responders_path = Path('.upstream') / 'cortex' / 'responders' / vendor
    if not responders_path.exists():
        return [], {}
    
    responders = []
    subscription_fields = {
        'registration_required': [],
        'subscription_required': [],
        'free_subscription': []
    }
    
    for file_path in responders_path.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            relative_path = f".upstream/cortex/responders/{vendor}/{file_path.name}"
            
            responders.append({
                'name': content.get('name'),
                'version': content.get('version'),
                'description': content.get('description'),
                'dataTypes': content.get('dataTypeList', []),
                'file': relative_path,
                'url': build_url(relative_path)
            })
            
            # Collect subscription fields
            if 'registration_required' in content:
                subscription_fields['registration_required'].append(content['registration_required'])
            if 'subscription_required' in content:
                subscription_fields['subscription_required'].append(content['subscription_required'])
            if 'free_subscription' in content:
                subscription_fields['free_subscription'].append(content['free_subscription'])
                
        except Exception as e:
            print(f"Error reading responder {file_path}: {e}")
    
    return responders, subscription_fields

def consolidate_subscription_fields(analyzer_fields: Dict, responder_fields: Dict) -> Dict:
    """Consolidate subscription fields from analyzers and responders."""
    result = {}
    
    # Combine all fields
    all_fields = {
        'registration_required': [],
        'subscription_required': [],
        'free_subscription': []
    }
    
    for key in all_fields.keys():
        all_fields[key] = analyzer_fields.get(key, []) + responder_fields.get(key, [])
    
    # Process each field
    for key, values in all_fields.items():
        if not values:
            continue
            
        unique_values = list(set(values))
        
        if len(unique_values) == 1:
            # All values are the same, use single value
            result[key] = unique_values[0]
        else:
            # Multiple different values, use array
            result[key] = sorted(unique_values, key=lambda x: (not x, x))  # False first, then True
    
    return result

def scan_functions(vendor: str) -> List[Dict]:
    """Scan functions for a vendor."""
    functions_path = Path('integrations') / 'vendors' / vendor / 'thehive' / 'functions'
    if not functions_path.exists():
        return []

    functions = []
    for file_path in functions_path.glob('*.js'):
        metadata = parse_function_metadata(str(file_path))
        if not metadata:
            continue

        file_name = metadata.get('definition', file_path.name)
        relative_path = f"integrations/vendors/{vendor}/thehive/functions/{file_name}"
        
        functions.append({
            'name': metadata.get('name'),
            'version': metadata.get('version'),
            'description': metadata.get('description'),
            'kind': metadata.get('kind'),
            'mode': metadata.get('mode'),
            'file': relative_path,
            'url': build_url(relative_path)
        })
    
    return functions

def discover_use_cases_from_markdown(vendor: str) -> List[Dict]:
    """Auto-discover use cases from markdown files in vendor docs directory."""
    vendor_docs_path = Path('integrations') / 'vendors' / vendor / 'docs'
    if not vendor_docs_path.exists():
        return []

    use_cases = []

    # Find all markdown files, excluding manifest and vendor files
    for md_file in vendor_docs_path.glob('*.md'):
        # Skip any files that might be auto-generated or metadata files
        if md_file.name in ['manifest.md', 'vendor.md', 'README.md']:
            continue

        frontmatter = parse_markdown_frontmatter(str(md_file))
        if not frontmatter:
            continue

        # Extract metadata from frontmatter
        title = frontmatter.get('title')
        description = frontmatter.get('description')

        # Skip files without title and description (not valid use-cases)
        if not title or not description:
            continue

        # Build relative path and URL
        relative_doc_path = f"integrations/vendors/{vendor}/docs/{md_file.name}"

        use_case = {
            'name': title,
            'description': description,
            'documentation': {
                'file': relative_doc_path,
                'url': build_url(relative_doc_path)
            }
        }

        # Add optional fields if present
        if 'tags' in frontmatter:
            use_case['tags'] = frontmatter['tags']
        if 'difficulty' in frontmatter:
            use_case['difficulty'] = frontmatter['difficulty']

        use_cases.append(use_case)

    return use_cases

def process_logo(vendor: str, logo_data: Union[str, Dict]) -> Dict:
    """Process logo data - supports both simple string and light/dark mode."""
    if not logo_data:
        return {}
    
    # If it's a string, treat as simple logo path
    if isinstance(logo_data, str):
        logo_path = logo_data
        # Check if it starts with integrations/ or .upstream/
        if logo_path.startswith(('integrations/', '.upstream/')):
            relative_logo = logo_path
        else:
            # Assume it's relative to vendor directory
            relative_logo = f"integrations/vendors/{vendor}/{logo_path}"
        
        return {
            'file': relative_logo,
            'url': build_url(relative_logo)
        }
    
    # If it's a dict, handle light/dark modes
    if isinstance(logo_data, dict):
        result = {}
        
        # Handle light mode
        if 'light' in logo_data:
            light_path = logo_data['light']
            if light_path.startswith(('integrations/', '.upstream/')):
                relative_light = light_path
            else:
                relative_light = f"integrations/vendors/{vendor}/{light_path}"
            
            result['light'] = {
                'file': relative_light,
                'url': build_url(relative_light)
            }
        
        # Handle dark mode
        if 'dark' in logo_data:
            dark_path = logo_data['dark']
            if dark_path.startswith(('integrations/', '.upstream/')):
                relative_dark = dark_path
            else:
                relative_dark = f"integrations/vendors/{vendor}/{dark_path}"
            
            result['dark'] = {
                'file': relative_dark,
                'url': build_url(relative_dark)
            }
        
        # If only one mode provided, return simple format
        if 'light' in result and 'dark' not in result:
            return result['light']
        
        return result
    
    return {}

def read_vendor_metadata(vendor: str) -> Dict:
    """Read vendor metadata from vendor.yml."""
    vendor_yml_path = Path('integrations') / 'vendors' / vendor / 'vendor.yml'

    default_metadata = {
        'id': vendor,
        'name': vendor,
        'description': '',
        'category': '',
        'tags': [],
        'homepage': '',
        'logo': {},
        'useCases': []
    }

    if not vendor_yml_path.exists():
        print(f"  Warning: vendor.yml not found for {vendor}, using defaults")
        return default_metadata

    try:
        with open(vendor_yml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return default_metadata

        # Auto-discover use cases from markdown files
        use_cases = discover_use_cases_from_markdown(vendor)

        # Handle logo path (supports both simple string and light/dark modes)
        logo_data = process_logo(vendor, data.get('logo'))

        # Handle tags
        tags = data.get('tags', [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]

        return {
            'id': data.get('id', vendor),
            'name': data.get('name', vendor),
            'description': data.get('description', ''),
            'category': data.get('category', ''),
            'tags': tags,
            'homepage': data.get('homepage', ''),
            'logo': logo_data,
            'useCases': use_cases
        }
    except Exception as e:
        print(f"  Error reading vendor.yml for {vendor}: {e}")
        return default_metadata

def find_vendors() -> List[str]:
    """Find all vendors from directory structure."""
    vendors = set()

    # Check cortex analyzers
    analyzers_path = Path('.upstream') / 'cortex' / 'analyzers'
    if analyzers_path.exists():
        vendors.update([d.name for d in analyzers_path.iterdir() if d.is_dir()])

    # Check cortex responders
    responders_path = Path('.upstream') / 'cortex' / 'responders'
    if responders_path.exists():
        vendors.update([d.name for d in responders_path.iterdir() if d.is_dir()])
    
    # Check integrations/vendors directory
    vendors_path = Path('integrations') / 'vendors'
    if vendors_path.exists():
        vendors.update([d.name for d in vendors_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    return sorted(list(vendors))

def generate_vendor_manifest(vendor: str) -> Dict:
    """Generate complete manifest for a vendor from external files only."""
    # Read vendor metadata from vendor.yml
    vendor_metadata = read_vendor_metadata(vendor)
    
    # Scan for integrations and collect subscription info
    analyzers, analyzer_subscription = scan_analyzers(vendor)
    responders, responder_subscription = scan_responders(vendor)
    functions = scan_functions(vendor)
    
    # Consolidate subscription fields
    subscription_info = consolidate_subscription_fields(analyzer_subscription, responder_subscription)
    
    manifest = {
        **vendor_metadata,
        **subscription_info,  # Add consolidated subscription fields
        'integrations': {
            'analyzers': analyzers,
            'responders': responders,
            'functions': functions
        },
        'stats': {
            'totalAnalyzers': len(analyzers),
            'totalResponders': len(responders),
            'totalFunctions': len(functions),
            'total': len(analyzers) + len(responders) + len(functions)
        }
    }
    
    return manifest

def main():
    """Main execution."""
    vendors = find_vendors()
    all_manifests = {}

    print(f"Using base URL: {BASE_URL}\n")

    # Create .generated directory
    catalogs_path = Path('.generated')
    catalogs_path.mkdir(exist_ok=True)

    # Clean up obsolete vendor manifests
    if catalogs_path.exists():
        for vendor_dir in catalogs_path.iterdir():
            if vendor_dir.is_dir() and vendor_dir.name not in vendors:
                print(f"Cleaning up obsolete manifest: {vendor_dir.name}")
                shutil.rmtree(vendor_dir)

    for vendor in vendors:
        print(f"Generating manifest for {vendor}...")
        manifest = generate_vendor_manifest(vendor)
        all_manifests[vendor] = manifest

        # Create vendor catalog directory if it doesn't exist
        vendor_catalog_path = catalogs_path / vendor
        vendor_catalog_path.mkdir(parents=True, exist_ok=True)

        # Write individual vendor manifest as YAML
        manifest_yml_path = vendor_catalog_path / 'manifest.yml'
        with open(manifest_yml_path, 'w', encoding='utf-8') as f:
            f.write("# AUTO-GENERATED - DO NOT EDIT\n")
            f.write("# This file is generated by generate-manifest.py\n")
            f.write("# Edit vendor.yml for vendor metadata, then re-run the generator\n\n")
            yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
        print(f"  → {manifest_yml_path}")

        # Write individual vendor manifest as JSON
        manifest_json_path = vendor_catalog_path / 'manifest.json'
        with open(manifest_json_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"  → {manifest_json_path}")

    # Write combined manifest (JSON and YAML) to .generated directory
    output_path = catalogs_path / 'integration-manifest.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_manifests, f, indent=2, ensure_ascii=False)
    print(f"\nCombined manifest generated: {output_path}")

    yaml_output_path = catalogs_path / 'integration-manifest.yml'
    with open(yaml_output_path, 'w', encoding='utf-8') as f:
        yaml.dump(all_manifests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"Combined YAML manifest generated: {yaml_output_path}")
    
    # Print summary
    print('\n=== Summary ===')
    for vendor, data in all_manifests.items():
        print(f"\n{data['name']} ({vendor}):")
        print(f"  Category: {data['category'] or 'N/A'}")
        tags_str = ', '.join(data.get('tags', [])) if data.get('tags') else 'N/A'
        print(f"  Tags: {tags_str}")
        
        # Show subscription info if available
        if data.get('registration_required') is not None:
            print(f"  Registration Required: {data['registration_required']}")
        if data.get('subscription_required') is not None:
            print(f"  Subscription Required: {data['subscription_required']}")
        if data.get('free_subscription') is not None:
            print(f"  Free Subscription: {data['free_subscription']}")
        
        print(f"  Use Cases: {len(data.get('useCases', []))}")
        print(f"  Analyzers: {data['stats']['totalAnalyzers']}")
        print(f"  Responders: {data['stats']['totalResponders']}")
        print(f"  Functions: {data['stats']['totalFunctions']}")
        print(f"  Total: {data['stats']['total']}")

if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Please run: pip install pyyaml")
        exit(1)
    
    main()
