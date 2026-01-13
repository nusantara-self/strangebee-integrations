#!/usr/bin/env python3
"""
Shared utilities for integration manifest generation.

This module contains common functions used by both catalog and documentation
generation scripts.
"""

import os
import json
import yaml
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union


def get_current_branch() -> str:
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() or 'main'
    except Exception:
        return 'main'


# Configuration - dynamically use current branch
CURRENT_BRANCH = get_current_branch()
BASE_URL = f"https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/{CURRENT_BRANCH}"
GITHUB_BASE_URL = f"https://github.com/nusantara-self/strangebee-integrations/blob/{CURRENT_BRANCH}"


def build_url(relative_path: str) -> str:
    """Build full raw URL from relative path."""
    # Remove leading ./ if present (but keep other dots like .upstream)
    if relative_path.startswith('./'):
        path = relative_path[2:]
    else:
        path = relative_path
    return f"{BASE_URL}/{path}"


def build_github_url(relative_path: str) -> str:
    """Build GitHub web UI URL from relative path."""
    # Remove leading ./ if present (but keep other dots like .upstream)
    if relative_path.startswith('./'):
        path = relative_path[2:]
    else:
        path = relative_path
    return f"{GITHUB_BASE_URL}/{path}"


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
                'author': content.get('author'),
                'license': content.get('license'),
                'description': content.get('description'),
                'dataTypes': content.get('dataTypeList', []),
                'file': relative_path,
                'url': build_url(relative_path),
                'github_url': build_github_url(relative_path),
                'integration_type': content.get('integration_type')
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
                'author': content.get('author'),
                'license': content.get('license'),
                'description': content.get('description'),
                'dataTypes': content.get('dataTypeList', []),
                'file': relative_path,
                'url': build_url(relative_path),
                'github_url': build_github_url(relative_path),
                'integration_type': content.get('integration_type')
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

        # Use the actual file name to ensure .js extension is included
        file_name = file_path.name
        relative_path = f"integrations/vendors/{vendor}/thehive/functions/{file_name}"

        functions.append({
            'name': metadata.get('name'),
            'version': metadata.get('version'),
            'description': metadata.get('description'),
            'kind': metadata.get('kind'),
            'mode': metadata.get('mode'),
            'file': relative_path,
            'url': build_url(relative_path),
            'github_url': build_github_url(relative_path)
        })

    return functions


def discover_use_cases_from_markdown(vendor: str) -> List[Dict]:
    """Auto-discover use cases from markdown files in vendor root and use-cases directory."""
    vendor_path = Path('integrations') / 'vendors' / vendor
    if not vendor_path.exists():
        return []

    use_cases = []

    # Find all markdown files in vendor root and use-cases folder, excluding special files
    md_files = list(vendor_path.glob('*.md')) + list(vendor_path.glob('use-cases/*.md'))

    for md_file in md_files:
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

        # Build relative path and URL (check if file is in use-cases subdirectory)
        if md_file.parent.name == 'use-cases':
            relative_doc_path = f"integrations/vendors/{vendor}/use-cases/{md_file.name}"
        else:
            relative_doc_path = f"integrations/vendors/{vendor}/{md_file.name}"

        use_case = {
            'name': title,
            'description': description,
            'documentation': {
                'file': relative_doc_path,
                'url': build_url(relative_doc_path),
                'github_url': build_github_url(relative_doc_path)
            }
        }

        # Add optional fields if present
        if 'tags' in frontmatter:
            use_case['tags'] = frontmatter['tags']
        if 'difficulty' in frontmatter:
            use_case['difficulty'] = frontmatter['difficulty']

        use_cases.append(use_case)

    return use_cases


def auto_detect_logo(vendor: str) -> Dict:
    """Auto-detect logo file from vendor assets directory.

    Priority: SVG > PNG > JPG > JPEG > ICO
    Looks for: logo.*, icon.*, or vendor-name.*
    """
    vendor_dir = Path('integrations') / 'vendors' / vendor
    assets_dir = vendor_dir / 'assets'

    if not assets_dir.exists():
        return {}

    # Priority order for file extensions
    extensions = ['.svg', '.png', '.jpg', '.jpeg', '.ico']

    # Priority order for filenames
    filename_patterns = ['logo', 'icon', vendor.lower()]

    for pattern in filename_patterns:
        for ext in extensions:
            logo_file = assets_dir / f"{pattern}{ext}"
            if logo_file.exists():
                relative_path = f"integrations/vendors/{vendor}/assets/{pattern}{ext}"
                return {
                    'file': relative_path,
                    'url': build_url(relative_path),
                    'github_url': build_github_url(relative_path)
                }

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
        'useCases': [],
        'externalIntegrations': []
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

        # Auto-detect logo from assets directory
        logo_data = auto_detect_logo(vendor)

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
            'useCases': use_cases,
            'externalIntegrations': data.get('externalIntegrations', [])
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

    return sorted(list(vendors), key=str.lower)


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

    # Count external integrations from vendor metadata
    external_integrations_count = len(vendor_metadata.get('externalIntegrations', []))

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
            'totalExternalIntegrations': external_integrations_count,
            'total': len(analyzers) + len(responders) + len(functions) + external_integrations_count
        }
    }

    return manifest
