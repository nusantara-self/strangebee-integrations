#!/usr/bin/env python3

import os
import json
import yaml
import re
import shutil
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
                'github_url': build_github_url(relative_path)
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
                'github_url': build_github_url(relative_path)
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

def generate_markdown_overview(vendor: str, manifest: Dict) -> str:
    """Generate human-readable markdown overview from manifest."""
    lines = []

    # Header
    lines.append(f"# {manifest['name']}")
    lines.append("")

    # Logo (if available)
    logo = manifest.get('logo')
    if logo:
        # Check if it's light/dark mode or simple format
        if isinstance(logo, dict):
            if 'light' in logo and 'dark' in logo:
                # Both light and dark logos - use picture element for theme support
                lines.append("<picture>")
                lines.append(f"  <source media=\"(prefers-color-scheme: dark)\" srcset=\"{logo['dark']['url']}\">")
                lines.append(f"  <source media=\"(prefers-color-scheme: light)\" srcset=\"{logo['light']['url']}\">")
                lines.append(f"  <img alt=\"{manifest['name']} Logo\" src=\"{logo['light']['url']}\" width=\"200\">")
                lines.append("</picture>")
                lines.append("")
            elif 'light' in logo:
                # Only light logo
                lines.append(f"![{manifest['name']} Logo]({logo['light']['url']})")
                lines.append("")
            elif 'dark' in logo:
                # Only dark logo
                lines.append(f"![{manifest['name']} Logo]({logo['dark']['url']})")
                lines.append("")
            elif 'url' in logo:
                # Simple format with url key
                lines.append(f"![{manifest['name']} Logo]({logo['url']})")
                lines.append("")

    # Description
    if manifest.get('description'):
        lines.append(manifest['description'])
        lines.append("")

    # Metadata
    if manifest.get('category'):
        lines.append(f"**Category:** {manifest['category']}  ")
    if manifest.get('homepage'):
        lines.append(f"**Homepage:** {manifest['homepage']}  ")
    if manifest.get('tags'):
        tags_str = ', '.join(manifest['tags'])
        lines.append(f"**Tags:** {tags_str}")
    lines.append("")

    # Subscription Information
    subscription_fields = ['registration_required', 'subscription_required', 'free_subscription']
    has_subscription_info = any(manifest.get(field) is not None for field in subscription_fields)

    if has_subscription_info:
        lines.append("## Subscription Information")
        lines.append("")

        if manifest.get('registration_required') is not None:
            value = "Yes" if manifest['registration_required'] else "No"
            lines.append(f"- **Registration Required:** {value}")
        if manifest.get('subscription_required') is not None:
            value = "Yes" if manifest['subscription_required'] else "No"
            lines.append(f"- **Subscription Required:** {value}")
        if manifest.get('free_subscription') is not None:
            value = "Yes" if manifest['free_subscription'] else "No"
            lines.append(f"- **Free Subscription Available:** {value}")
        lines.append("")

    # Analyzers
    analyzers = manifest.get('integrations', {}).get('analyzers', [])
    if analyzers:
        lines.append(f"## Analyzers ({len(analyzers)})")
        lines.append("")

        for analyzer in analyzers:
            name = analyzer.get('name', 'Unknown')
            version = analyzer.get('version', '')
            lines.append(f"### {name} `v{version}`")

            if analyzer.get('description'):
                lines.append(analyzer['description'])
                lines.append("")

            if analyzer.get('author'):
                lines.append(f"- **Author:** {analyzer['author']}")
            if analyzer.get('license'):
                lines.append(f"- **License:** {analyzer['license']}")
            if analyzer.get('dataTypes'):
                data_types = ', '.join(f"`{dt}`" for dt in analyzer['dataTypes'])
                lines.append(f"- **Data Types:** {data_types}")

            if analyzer.get('file'):
                lines.append(f"- **Configuration:** [{analyzer['file']}]({analyzer['github_url']}) ([raw]({analyzer['url']}))")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Responders
    responders = manifest.get('integrations', {}).get('responders', [])
    if responders:
        lines.append(f"## Responders ({len(responders)})")
        lines.append("")

        for responder in responders:
            name = responder.get('name', 'Unknown')
            version = responder.get('version', '')
            lines.append(f"### {name} `v{version}`")

            if responder.get('description'):
                lines.append(responder['description'])
                lines.append("")

            if responder.get('author'):
                lines.append(f"- **Author:** {responder['author']}")
            if responder.get('license'):
                lines.append(f"- **License:** {responder['license']}")
            if responder.get('dataTypes'):
                data_types = ', '.join(f"`{dt}`" for dt in responder['dataTypes'])
                lines.append(f"- **Data Types:** {data_types}")

            if responder.get('file'):
                lines.append(f"- **Configuration:** [{responder['file']}]({responder['github_url']}) ([raw]({responder['url']}))")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Functions
    functions = manifest.get('integrations', {}).get('functions', [])
    if functions:
        lines.append(f"## Functions ({len(functions)})")
        lines.append("")

        for func in functions:
            name = func.get('name', 'Unknown')
            version = func.get('version', '')
            lines.append(f"### {name} `v{version}`")

            if func.get('description'):
                lines.append(func['description'])
                lines.append("")

            if func.get('kind'):
                lines.append(f"- **Kind:** {func['kind']}")
            if func.get('mode'):
                lines.append(f"- **Mode:** {func['mode']}")
            if func.get('file'):
                lines.append(f"- **File:** [{func['file']}]({func['github_url']}) ([raw]({func['url']}))")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Use Cases
    use_cases = manifest.get('useCases', [])
    if use_cases:
        lines.append(f"## Use Cases ({len(use_cases)})")
        lines.append("")

        for uc in use_cases:
            lines.append(f"### {uc['name']}")
            if uc.get('description'):
                lines.append(uc['description'])
            lines.append("")

            # Optional metadata
            if uc.get('tags'):
                tags_str = ', '.join(uc['tags'])
                lines.append(f"**Tags:** {tags_str}")

            # Documentation link
            if uc.get('documentation', {}).get('github_url'):
                lines.append(f"📄 [Documentation]({uc['documentation']['github_url']}) ([raw]({uc['documentation']['url']}))")

            lines.append("")
            lines.append("---")
            lines.append("")

    # External Integrations (integrations built by the vendor, community, or third parties)
    external_integrations = manifest.get('externalIntegrations', [])
    if external_integrations:
        lines.append(f"## External Integrations ({len(external_integrations)})")
        lines.append("")
        lines.append(f"External integrations that connect {manifest['name']} with TheHive:")
        lines.append("")

        for vi in external_integrations:
            lines.append(f"### {vi['name']}")
            if vi.get('description'):
                lines.append(vi['description'])
            lines.append("")

            if vi.get('type'):
                lines.append(f"**Type:** {vi['type']}")

            if vi.get('documentation'):
                lines.append(f"**Documentation:** [{vi['documentation']}]({vi['documentation']})")

            lines.append("")
            lines.append("---")
            lines.append("")

    # Statistics
    stats = manifest.get('stats', {})
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Total Analyzers:** {stats.get('totalAnalyzers', 0)}")
    lines.append(f"- **Total Responders:** {stats.get('totalResponders', 0)}")
    lines.append(f"- **Total Functions:** {stats.get('totalFunctions', 0)}")
    lines.append(f"- **Total External Integrations:** {stats.get('totalExternalIntegrations', 0)}")
    lines.append(f"- **Total Integrations:** {stats.get('total', 0)}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated from the integration manifest. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_catalog_index(all_manifests: Dict) -> str:
    """Generate main catalog index with all vendors organized by category."""
    lines = []

    # Header
    lines.append("# Integration Catalog")
    lines.append("")
    lines.append("Auto-generated catalog of TheHive and Cortex integrations.")
    lines.append("")

    # Calculate statistics
    total_vendors = len(all_manifests)
    total_analyzers = sum(m['stats']['totalAnalyzers'] for m in all_manifests.values())
    total_responders = sum(m['stats']['totalResponders'] for m in all_manifests.values())
    total_functions = sum(m['stats']['totalFunctions'] for m in all_manifests.values())
    total_external_integrations = sum(m['stats'].get('totalExternalIntegrations', 0) for m in all_manifests.values())
    total_integrations = sum(m['stats']['total'] for m in all_manifests.values())

    # Summary statistics
    lines.append("## 📊 Summary Statistics")
    lines.append("")
    lines.append(f"- **Total Vendors:** {total_vendors}")
    lines.append(f"- **Total Analyzers:** {total_analyzers}")
    lines.append(f"- **Total Responders:** {total_responders}")
    lines.append(f"- **Total Functions:** {total_functions}")
    lines.append(f"- **Total External Integrations:** {total_external_integrations}")
    lines.append(f"- **Total Integrations:** {total_integrations}")
    lines.append("")

    # Group vendors by category
    by_category = {}
    uncategorized = []

    for vendor_id, manifest in all_manifests.items():
        category = manifest.get('category')
        if category:
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((vendor_id, manifest))
        else:
            uncategorized.append((vendor_id, manifest))

    # Vendors by category
    if by_category:
        lines.append("## 📂 Vendors by Category")
        lines.append("")

        for category in sorted(by_category.keys(), key=str.lower):
            lines.append(f"### {category}")
            lines.append("")

            vendors = sorted(by_category[category], key=lambda x: x[1]['name'].lower())
            for vendor_id, manifest in vendors:
                name = manifest['name']
                total = manifest['stats']['total']
                desc = manifest.get('description', '')

                # Truncate long descriptions
                if desc and len(desc) > 100:
                    desc = desc[:97] + "..."

                lines.append(f"**[{name}](docs/vendors/{vendor_id}/overview.md)** ({total} integrations)")
                if desc:
                    lines.append(f"  {desc}")
                lines.append("")

            lines.append("")

    # All vendors alphabetically
    lines.append("## 🔤 All Vendors (A-Z)")
    lines.append("")

    all_vendors = sorted(all_manifests.items(), key=lambda x: x[1]['name'].lower())

    for vendor_id, manifest in all_vendors:
        name = manifest['name']
        stats = manifest['stats']
        category = manifest.get('category') or 'Uncategorized'

        integration_breakdown = []
        if stats['totalAnalyzers'] > 0:
            integration_breakdown.append(f"{stats['totalAnalyzers']} analyzers")
        if stats['totalResponders'] > 0:
            integration_breakdown.append(f"{stats['totalResponders']} responders")
        if stats['totalFunctions'] > 0:
            integration_breakdown.append(f"{stats['totalFunctions']} functions")
        if stats.get('totalExternalIntegrations', 0) > 0:
            integration_breakdown.append(f"{stats['totalExternalIntegrations']} external")

        breakdown_str = ", ".join(integration_breakdown) if integration_breakdown else "No integrations"

        lines.append(f"- **[{name}](docs/vendors/{vendor_id}/overview.md)** - *{category}* - {breakdown_str}")

    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("📖 **[View individual vendor documentation](docs/)** for detailed integration information.")
    lines.append("")
    lines.append("*This catalog is auto-generated. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_external_integrations_catalog(all_manifests: Dict) -> Dict:
    """Generate catalog of all external integrations across vendors."""
    external_integrations = []

    for vendor_id, manifest in all_manifests.items():
        vendor_external = manifest.get('externalIntegrations', [])
        for integration in vendor_external:
            external_integrations.append({
                'name': integration.get('name'),
                'vendor': manifest.get('name'),
                'vendorId': vendor_id,
                'type': integration.get('type'),
                'description': integration.get('description'),
                'documentation': integration.get('documentation'),
                'category': manifest.get('category')
            })

    # Sort by vendor name, then integration name
    external_integrations.sort(key=lambda x: (x['vendor'].lower(), x['name'].lower()))

    return {
        'totalIntegrations': len(external_integrations),
        'integrations': external_integrations,
        'byVendor': _group_by_vendor(external_integrations),
        'byCategory': _group_by_category(external_integrations),
        'byType': _group_by_type(external_integrations)
    }

def _group_by_vendor(integrations: list) -> Dict:
    """Group integrations by vendor."""
    by_vendor = {}
    for integration in integrations:
        vendor = integration['vendor']
        if vendor not in by_vendor:
            by_vendor[vendor] = []
        by_vendor[vendor].append(integration)
    return by_vendor

def _group_by_category(integrations: list) -> Dict:
    """Group integrations by vendor category."""
    by_category = {}
    for integration in integrations:
        category = integration.get('category', 'Other')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(integration)
    return by_category

def _group_by_type(integrations: list) -> Dict:
    """Group integrations by type."""
    by_type = {}
    for integration in integrations:
        int_type = integration.get('type', 'unknown')
        if int_type not in by_type:
            by_type[int_type] = []
        by_type[int_type].append(integration)
    return by_type

def generate_external_integrations_markdown(catalog: Dict) -> str:
    """Generate markdown documentation for external integrations catalog."""
    lines = []

    # Header
    lines.append("# External Integrations Catalog")
    lines.append("")
    lines.append("Community and vendor-built integrations that connect various platforms with TheHive and Cortex.")
    lines.append("")

    # Summary
    lines.append("## 📊 Overview")
    lines.append("")
    lines.append(f"**Total External Integrations:** {catalog['totalIntegrations']}")
    lines.append("")

    # Quick stats by type
    lines.append("### By Type")
    lines.append("")
    for int_type, integrations in sorted(catalog['byType'].items()):
        lines.append(f"- **{int_type}**: {len(integrations)} integration(s)")
    lines.append("")

    # Quick stats by category
    lines.append("### By Vendor Category")
    lines.append("")
    for category, integrations in sorted(catalog['byCategory'].items()):
        lines.append(f"- **{category}**: {len(integrations)} integration(s)")
    lines.append("")

    # All integrations grouped by vendor
    lines.append("## 🔗 All External Integrations")
    lines.append("")

    for vendor, integrations in sorted(catalog['byVendor'].items()):
        lines.append(f"### {vendor}")
        lines.append("")

        for integration in integrations:
            lines.append(f"#### {integration['name']}")
            lines.append("")
            if integration.get('description'):
                lines.append(integration['description'])
                lines.append("")
            if integration.get('type'):
                lines.append(f"**Type:** `{integration['type']}`  ")
            if integration.get('documentation'):
                lines.append(f"**Documentation:** [{integration['documentation']}]({integration['documentation']})")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This catalog is auto-generated. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_external_integrations_catalog(all_manifests: Dict) -> Dict:
    """Generate catalog of all external integrations across vendors."""
    external_integrations = []

    for vendor_id, manifest in all_manifests.items():
        vendor_external = manifest.get('externalIntegrations', [])
        for integration in vendor_external:
            external_integrations.append({
                'name': integration.get('name'),
                'vendor': manifest.get('name'),
                'vendorId': vendor_id,
                'type': integration.get('type'),
                'description': integration.get('description'),
                'documentation': integration.get('documentation'),
                'category': manifest.get('category')
            })

    # Sort by vendor name, then integration name
    external_integrations.sort(key=lambda x: (x['vendor'].lower(), x['name'].lower()))

    return {
        'totalIntegrations': len(external_integrations),
        'integrations': external_integrations,
        'byVendor': _group_by_vendor(external_integrations),
        'byCategory': _group_by_category(external_integrations),
        'byType': _group_by_type(external_integrations)
    }

def _group_by_vendor(integrations: list) -> Dict:
    """Group integrations by vendor."""
    by_vendor = {}
    for integration in integrations:
        vendor = integration['vendor']
        if vendor not in by_vendor:
            by_vendor[vendor] = []
        by_vendor[vendor].append(integration)
    return by_vendor

def _group_by_category(integrations: list) -> Dict:
    """Group integrations by vendor category."""
    by_category = {}
    for integration in integrations:
        category = integration.get('category', 'Other')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(integration)
    return by_category

def _group_by_type(integrations: list) -> Dict:
    """Group integrations by type."""
    by_type = {}
    for integration in integrations:
        int_type = integration.get('type', 'unknown')
        if int_type not in by_type:
            by_type[int_type] = []
        by_type[int_type].append(integration)
    return by_type

def generate_external_integrations_markdown(catalog: Dict) -> str:
    """Generate markdown documentation for external integrations catalog."""
    lines = []

    # Header
    lines.append("# External Integrations Catalog")
    lines.append("")
    lines.append("Community and vendor-built integrations that connect various platforms with TheHive and Cortex.")
    lines.append("")

    # Summary
    lines.append("## 📊 Overview")
    lines.append("")
    lines.append(f"**Total External Integrations:** {catalog['totalIntegrations']}")
    lines.append("")

    # Quick stats by type
    lines.append("### By Type")
    lines.append("")
    for int_type, integrations in sorted(catalog['byType'].items()):
        lines.append(f"- **{int_type}**: {len(integrations)} integration(s)")
    lines.append("")

    # Quick stats by category
    lines.append("### By Vendor Category")
    lines.append("")
    for category, integrations in sorted(catalog['byCategory'].items()):
        lines.append(f"- **{category}**: {len(integrations)} integration(s)")
    lines.append("")

    # All integrations grouped by vendor
    lines.append("## 🔗 All External Integrations")
    lines.append("")

    for vendor, integrations in sorted(catalog['byVendor'].items()):
        lines.append(f"### {vendor}")
        lines.append("")

        for integration in integrations:
            lines.append(f"#### {integration['name']}")
            lines.append("")
            if integration.get('description'):
                lines.append(integration['description'])
                lines.append("")
            if integration.get('type'):
                lines.append(f"**Type:** `{integration['type']}`  ")
            if integration.get('documentation'):
                lines.append(f"**Documentation:** [{integration['documentation']}]({integration['documentation']})")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This catalog is auto-generated. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_functions_catalog(all_manifests: Dict) -> str:
    """Generate markdown catalog of all functions (generic + vendor-specific)."""
    lines = []
    lines.append("# Functions Catalog")
    lines.append("")
    lines.append("Complete list of TheHive functions available for workflow automation.")
    lines.append("")

    # Collect generic functions from integrations/generic/functions/
    generic_functions = []
    generic_functions_path = Path('integrations/generic/functions')
    if generic_functions_path.exists():
        for func_file in generic_functions_path.glob('function_*.js'):
            metadata = parse_function_metadata(str(func_file))
            if metadata:
                generic_functions.append({
                    'name': metadata.get('name', func_file.stem),
                    'version': metadata.get('version', 'N/A'),
                    'description': metadata.get('description', 'No description available'),
                    'type': metadata.get('type', 'function'),
                    'kind': metadata.get('kind', 'function'),
                    'mode': metadata.get('mode', 'N/A'),
                    'file': str(func_file)
                })

    # Collect vendor-specific functions
    vendor_functions = {}
    total_functions = len(generic_functions)

    for vendor_id, manifest in all_manifests.items():
        functions = manifest.get('integrations', {}).get('functions', [])
        if functions:
            vendor_name = manifest.get('name', vendor_id)
            vendor_functions[vendor_name] = {
                'vendor_id': vendor_id,
                'functions': functions
            }
            total_functions += len(functions)

    # Summary
    lines.append(f"## 📊 Summary")
    lines.append("")
    lines.append(f"- **Total Functions:** {total_functions}")
    lines.append(f"- **Generic Functions:** {len(generic_functions)}")
    lines.append(f"- **Vendor-Specific Functions:** {total_functions - len(generic_functions)}")
    lines.append(f"- **Vendors with Functions:** {len(vendor_functions)}")
    lines.append("")

    # Generic Functions Section
    if generic_functions:
        lines.append("## 🔧 Generic Functions")
        lines.append("")
        lines.append("These functions are vendor-agnostic and can be used across all TheHive installations:")
        lines.append("")

        for func in sorted(generic_functions, key=lambda x: x.get('name', '').lower()):
            name = func.get('name', 'Unknown')
            version = func.get('version', 'N/A')
            description = func.get('description', 'No description available')
            func_type = func.get('type', 'N/A')
            mode = func.get('mode', 'N/A')

            lines.append(f"### {name} `v{version}`")
            lines.append("")
            if func_type and func_type != 'N/A':
                lines.append(f"**Type:** {func_type}")
            if mode and mode != 'N/A':
                lines.append(f"**Mode:** {mode}")
            lines.append("")
            lines.append(description)
            lines.append("")
            lines.append("---")
            lines.append("")

    # Vendor-Specific Functions Section
    if vendor_functions:
        lines.append("## 🏢 Vendor-Specific Functions")
        lines.append("")

        for vendor_name in sorted(vendor_functions.keys()):
            vendor_data = vendor_functions[vendor_name]
            vendor_id = vendor_data['vendor_id']
            functions = vendor_data['functions']

            lines.append(f"### {vendor_name}")
            lines.append("")
            lines.append(f"**Vendor:** [{vendor_name}](/vendors/{vendor_id}/overview)")
            lines.append("")

            for func in sorted(functions, key=lambda x: x.get('name', '').lower()):
                name = func.get('name', 'Unknown')
                version = func.get('version', 'N/A')
                description = func.get('description', 'No description available')
                kind = func.get('kind', 'function')

                lines.append(f"#### {name} `v{version}`")
                if kind:
                    lines.append(f"**Kind:** `{kind}`")
                lines.append("")
                lines.append(description)
                lines.append("")

            lines.append("---")
            lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This catalog is auto-generated. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_free_local_integrations(all_manifests: Dict) -> str:
    """Generate markdown catalog of free or local integrations."""
    lines = []
    lines.append("# Free & Local Integrations")
    lines.append("")
    lines.append("Integrations that are either free to use or run locally without external dependencies.")
    lines.append("")

    # Collect free/local integrations
    free_local_integrations = {
        'analyzers': [],
        'responders': []
    }

    for vendor_id, manifest in all_manifests.items():
        vendor_name = manifest.get('name', vendor_id)
        free_subscription = manifest.get('free_subscription', False)

        # Check analyzers
        for analyzer in manifest.get('integrations', {}).get('analyzers', []):
            integration_type = analyzer.get('integration_type', '')
            if free_subscription or integration_type == 'local':
                free_local_integrations['analyzers'].append({
                    'vendor': vendor_name,
                    'vendor_id': vendor_id,
                    'free_subscription': free_subscription,
                    'is_local': integration_type == 'local',
                    **analyzer
                })

        # Check responders
        for responder in manifest.get('integrations', {}).get('responders', []):
            integration_type = responder.get('integration_type', '')
            if free_subscription or integration_type == 'local':
                free_local_integrations['responders'].append({
                    'vendor': vendor_name,
                    'vendor_id': vendor_id,
                    'free_subscription': free_subscription,
                    'is_local': integration_type == 'local',
                    **responder
                })

    total_analyzers = len(free_local_integrations['analyzers'])
    total_responders = len(free_local_integrations['responders'])

    # Summary
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append(f"- **Total Free/Local Analyzers:** {total_analyzers}")
    lines.append(f"- **Total Free/Local Responders:** {total_responders}")
    lines.append(f"- **Total:** {total_analyzers + total_responders}")
    lines.append("")
    lines.append("**Legend:**")
    lines.append("- 🆓 Free subscription available")
    lines.append("- 🏠 Local integration (no external API required)")
    lines.append("")

    # Analyzers Section
    if free_local_integrations['analyzers']:
        lines.append("## 🔍 Analyzers")
        lines.append("")

        for analyzer in sorted(free_local_integrations['analyzers'], key=lambda x: (x['vendor'].lower(), x.get('name', '').lower())):
            name = analyzer.get('name', 'Unknown')
            version = analyzer.get('version', 'N/A')
            description = analyzer.get('description', 'No description available')
            vendor = analyzer['vendor']
            vendor_id = analyzer['vendor_id']
            data_types = analyzer.get('dataTypes', [])

            # Badges
            badges = []
            if analyzer['free_subscription']:
                badges.append("🆓")
            if analyzer['is_local']:
                badges.append("🏠")
            badge_str = " ".join(badges)

            lines.append(f"### {name} `v{version}` {badge_str}")
            lines.append("")
            lines.append(f"**Vendor:** [{vendor}](/vendors/{vendor_id}/overview)")
            if data_types:
                lines.append(f"**Data Types:** {', '.join(f'`{dt}`' for dt in data_types)}")
            lines.append("")
            lines.append(description)
            lines.append("")
            lines.append("---")
            lines.append("")

    # Responders Section
    if free_local_integrations['responders']:
        lines.append("## ⚡ Responders")
        lines.append("")

        for responder in sorted(free_local_integrations['responders'], key=lambda x: (x['vendor'].lower(), x.get('name', '').lower())):
            name = responder.get('name', 'Unknown')
            version = responder.get('version', 'N/A')
            description = responder.get('description', 'No description available')
            vendor = responder['vendor']
            vendor_id = responder['vendor_id']
            data_types = responder.get('dataTypes', [])

            # Badges
            badges = []
            if responder['free_subscription']:
                badges.append("🆓")
            if responder['is_local']:
                badges.append("🏠")
            badge_str = " ".join(badges)

            lines.append(f"### {name} `v{version}` {badge_str}")
            lines.append("")
            lines.append(f"**Vendor:** [{vendor}](/vendors/{vendor_id}/overview)")
            if data_types:
                lines.append(f"**Data Types:** {', '.join(f'`{dt}`' for dt in data_types)}")
            lines.append("")
            lines.append(description)
            lines.append("")
            lines.append("---")
            lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This catalog is auto-generated. Do not edit manually.*")
    lines.append("")

    return '\n'.join(lines)

def generate_github_summary(all_manifests: Dict, previous_manifests: Dict = None) -> Dict:
    """Generate GitHub Actions summary of changes."""
    summary = {
        'total_vendors': len(all_manifests),
        'total_analyzers': sum(m['stats']['totalAnalyzers'] for m in all_manifests.values()),
        'total_responders': sum(m['stats']['totalResponders'] for m in all_manifests.values()),
        'total_functions': sum(m['stats']['totalFunctions'] for m in all_manifests.values()),
        'total_external_integrations': sum(m['stats'].get('totalExternalIntegrations', 0) for m in all_manifests.values()),
        'total_integrations': sum(m['stats']['total'] for m in all_manifests.values()),
        'added': [],
        'updated': [],
        'removed': []
    }

    if previous_manifests:
        current_vendors = set(all_manifests.keys())
        previous_vendors = set(previous_manifests.keys())

        # Find added vendors
        summary['added'] = sorted(current_vendors - previous_vendors, key=str.lower)

        # Find removed vendors
        summary['removed'] = sorted(previous_vendors - current_vendors, key=str.lower)

        # Find updated vendors (compare stats)
        for vendor in current_vendors & previous_vendors:
            current_stats = all_manifests[vendor]['stats']
            previous_stats = previous_manifests[vendor]['stats']

            if current_stats != previous_stats:
                summary['updated'].append({
                    'vendor': vendor,
                    'name': all_manifests[vendor]['name'],
                    'previous': previous_stats['total'],
                    'current': current_stats['total'],
                    'change': current_stats['total'] - previous_stats['total']
                })

    return summary

def write_github_summary(summary: Dict, output_path: Path):
    """Write GitHub Actions summary in markdown format."""
    lines = []

    lines.append("# 📊 Manifest Generation Summary")
    lines.append("")
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Total Vendors:** {summary['total_vendors']}")
    lines.append(f"- **Total Analyzers:** {summary['total_analyzers']}")
    lines.append(f"- **Total Responders:** {summary['total_responders']}")
    lines.append(f"- **Total Functions:** {summary['total_functions']}")
    lines.append(f"- **Total External Integrations:** {summary['total_external_integrations']}")
    lines.append(f"- **Total Integrations:** {summary['total_integrations']}")
    lines.append("")

    # Changes
    has_changes = summary['added'] or summary['removed'] or summary['updated']

    if has_changes:
        lines.append("## Changes")
        lines.append("")

        if summary['added']:
            lines.append(f"### ✅ Added Vendors ({len(summary['added'])})")
            lines.append("")
            for vendor in summary['added']:
                lines.append(f"- `{vendor}`")
            lines.append("")

        if summary['removed']:
            lines.append(f"### ❌ Removed Vendors ({len(summary['removed'])})")
            lines.append("")
            for vendor in summary['removed']:
                lines.append(f"- `{vendor}`")
            lines.append("")

        if summary['updated']:
            lines.append(f"### 🔄 Updated Vendors ({len(summary['updated'])})")
            lines.append("")
            for item in summary['updated']:
                change_indicator = "+" if item['change'] > 0 else ""
                lines.append(f"- **{item['name']}**: {item['previous']} → {item['current']} ({change_indicator}{item['change']})")
            lines.append("")
    else:
        lines.append("## Changes")
        lines.append("")
        lines.append("No changes detected.")
        lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    """Main execution."""
    vendors = find_vendors()
    all_manifests = {}

    print(f"Using branch: {CURRENT_BRANCH}")
    print(f"Using base URL: {BASE_URL}\n")

    # Create .generated directory structure
    generated_path = Path('.generated')
    generated_path.mkdir(exist_ok=True)

    catalogs_path = generated_path / 'catalogs'
    catalogs_path.mkdir(exist_ok=True)

    docs_path = generated_path / 'docs'
    docs_path.mkdir(exist_ok=True)

    # Clean up obsolete vendor catalogs
    if catalogs_path.exists():
        for vendor_dir in catalogs_path.iterdir():
            if vendor_dir.is_dir() and vendor_dir.name not in vendors:
                print(f"Cleaning up obsolete catalog: {vendor_dir.name}")
                shutil.rmtree(vendor_dir)

    # Clean up obsolete vendor docs
    if docs_path.exists():
        for vendor_dir in docs_path.iterdir():
            if vendor_dir.is_dir() and vendor_dir.name not in vendors:
                print(f"Cleaning up obsolete docs: {vendor_dir.name}")
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

        # Generate human-readable markdown overview
        vendor_docs_path = docs_path / 'vendors' / vendor
        vendor_docs_path.mkdir(parents=True, exist_ok=True)

        overview_content = generate_markdown_overview(vendor, manifest)
        overview_path = vendor_docs_path / 'overview.md'
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(overview_content)
        print(f"  → {overview_path}")

    # Write combined manifest (JSON and YAML) to .generated directory root
    output_path = generated_path / 'integration-manifest.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_manifests, f, indent=2, ensure_ascii=False)
    print(f"\nCombined manifest generated: {output_path}")

    yaml_output_path = generated_path / 'integration-manifest.yml'
    with open(yaml_output_path, 'w', encoding='utf-8') as f:
        yaml.dump(all_manifests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"Combined YAML manifest generated: {yaml_output_path}")

    # Generate catalog index
    catalog_index = generate_catalog_index(all_manifests)
    index_path = generated_path / 'README.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(catalog_index)
    print(f"Catalog index generated: {index_path}")

    # Generate external integrations catalog
    external_integrations_catalog = generate_external_integrations_catalog(all_manifests)

    # Create external-integrations directory
    external_integrations_path = generated_path / 'external-integrations'
    external_integrations_path.mkdir(exist_ok=True)

    # Write catalog as JSON
    ext_json_path = external_integrations_path / 'catalog.json'
    with open(ext_json_path, 'w', encoding='utf-8') as f:
        json.dump(external_integrations_catalog, f, indent=2, ensure_ascii=False)
    print(f"External integrations catalog (JSON): {ext_json_path}")

    # Write catalog as YAML
    ext_yaml_path = external_integrations_path / 'catalog.yml'
    with open(ext_yaml_path, 'w', encoding='utf-8') as f:
        f.write("# AUTO-GENERATED - DO NOT EDIT\n")
        f.write("# This file is generated by generate-manifest.py\n\n")
        yaml.dump(external_integrations_catalog, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"External integrations catalog (YAML): {ext_yaml_path}")

    # Write catalog as Markdown
    ext_md_content = generate_external_integrations_markdown(external_integrations_catalog)
    ext_md_path = external_integrations_path / 'README.md'
    with open(ext_md_path, 'w', encoding='utf-8') as f:
        f.write(ext_md_content)
    print(f"External integrations catalog (Markdown): {ext_md_path}")

    # Generate functions catalog
    functions_catalog = generate_functions_catalog(all_manifests)
    functions_catalog_path = docs_path / 'functions.md'
    with open(functions_catalog_path, 'w', encoding='utf-8') as f:
        f.write(functions_catalog)
    print(f"Functions catalog: {functions_catalog_path}")

    # Generate free/local integrations catalog
    free_local_catalog = generate_free_local_integrations(all_manifests)
    free_local_path = docs_path / 'free-local.md'
    with open(free_local_path, 'w', encoding='utf-8') as f:
        f.write(free_local_catalog)
    print(f"Free/local integrations catalog: {free_local_path}")

    # Load previous manifests for change detection (if exists)
    previous_manifests = None
    previous_manifest_path = generated_path / 'integration-manifest.json'
    if previous_manifest_path.exists():
        try:
            # Read from git if available, otherwise use current file
            import subprocess
            result = subprocess.run(
                ['git', 'show', f'HEAD:{previous_manifest_path}'],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode == 0:
                previous_manifests = json.loads(result.stdout)
        except Exception:
            pass  # If git fails or file doesn't exist in git, skip change detection

    # Generate GitHub Actions summary
    summary = generate_github_summary(all_manifests, previous_manifests)
    github_summary_path = generated_path / 'GITHUB_SUMMARY.md'
    write_github_summary(summary, github_summary_path)
    print(f"GitHub Actions summary: {github_summary_path}")

    # Print summary
    print('\n=== Summary ===')
    print(f"\nTotal External Integrations: {external_integrations_catalog['totalIntegrations']}")
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
        print(f"  External Integrations: {data['stats'].get('totalExternalIntegrations', 0)}")
        print(f"  Total: {data['stats']['total']}")

if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Please run: pip install pyyaml")
        exit(1)
    
    main()
