#!/usr/bin/env python3
"""
Generate integration documentation (Markdown only).

This script generates human-readable documentation files.
For catalog generation, see generate-catalogs.py.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List

# Import shared utilities
from manifest_utils import (
    CURRENT_BRANCH,
    BASE_URL,
    find_vendors,
    generate_vendor_manifest,
    parse_function_metadata
)


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


def read_function_code(file_path: str) -> str:
    """Read function code from file, excluding metadata frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove the metadata frontmatter (/*---...---*/)
        import re
        cleaned = re.sub(r'/\*---\n.*?\n---\*/', '', content, flags=re.DOTALL)

        # Remove leading/trailing whitespace
        return cleaned.strip()
    except Exception as e:
        return f"// Error reading function code: {e}"


def generate_individual_function_page(func: Dict, vendor_name: str = None) -> str:
    """Generate individual function documentation page with full code."""
    lines = []

    name = func.get('name', 'Unknown')
    version = func.get('version', 'N/A')
    description = func.get('description', 'No description available')
    func_type = func.get('type', 'N/A')
    kind = func.get('kind', 'function')
    mode = func.get('mode', 'N/A')
    code = func.get('code', '')
    file_path = func.get('file', '')

    # Header
    lines.append(f"# {name}")
    lines.append("")

    # Metadata
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- **Version:** `{version}`")
    if vendor_name:
        lines.append(f"- **Vendor:** {vendor_name}")
    else:
        lines.append(f"- **Type:** Generic Function")
    if func_type and func_type != 'N/A':
        lines.append(f"- **Function Type:** `{func_type}`")
    if kind:
        lines.append(f"- **Kind:** `{kind}`")
    if mode and mode != 'N/A':
        lines.append(f"- **Mode:** `{mode}`")
    if file_path:
        lines.append(f"- **Source File:** `{file_path}`")
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(description)
    lines.append("")

    # Code
    if code:
        lines.append("## Code")
        lines.append("")
        lines.append("```javascript")
        lines.append(code)
        lines.append("```")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This documentation is auto-generated. Do not edit manually.*")
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
                    'file': str(func_file),
                    'code': read_function_code(str(func_file))
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

            # Create a safe filename for the function
            safe_name = name.replace(' ', '-').replace('/', '-').lower()
            func_page = f"functions/{safe_name}.md"

            lines.append(f"### [{name}]({func_page}) `v{version}`")
            lines.append("")
            if func_type and func_type != 'N/A':
                lines.append(f"**Type:** {func_type}")
            if mode and mode != 'N/A':
                lines.append(f"**Mode:** {mode}")
            lines.append("")
            lines.append(description)
            lines.append("")
            lines.append(f"📄 [View full documentation]({func_page})")
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

                # Create a safe filename for the function
                safe_name = f"{vendor_name.lower().replace(' ', '-')}-{name.replace(' ', '-').replace('/', '-').lower()}"
                func_page = f"functions/{safe_name}.md"

                lines.append(f"#### [{name}]({func_page}) `v{version}`")
                if kind:
                    lines.append(f"**Kind:** `{kind}`")
                lines.append("")
                lines.append(description)
                lines.append("")
                lines.append(f"📄 [View full documentation]({func_page})")
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


def main():
    """Main execution."""
    print(f"=== Documentation Generation ===")
    print(f"Using branch: {CURRENT_BRANCH}")
    print(f"Using base URL: {BASE_URL}\n")

    # Read the generated catalogs
    generated_path = Path('.generated')
    catalogs_path = generated_path / 'catalogs'

    # Load the combined manifest
    manifest_path = generated_path / 'integration-manifest.json'
    if not manifest_path.exists():
        print("Error: integration-manifest.json not found!")
        print("Please run generate-catalogs.py first.")
        exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        all_manifests = json.load(f)

    vendors = list(all_manifests.keys())
    print(f"Loaded manifests for {len(vendors)} vendors\n")

    # Create docs directory structure
    docs_path = generated_path / 'docs'
    docs_path.mkdir(exist_ok=True)

    # Clean up obsolete vendor docs
    vendors_docs_path = docs_path / 'vendors'
    if vendors_docs_path.exists():
        for vendor_dir in vendors_docs_path.iterdir():
            if vendor_dir.is_dir() and vendor_dir.name not in vendors:
                print(f"Cleaning up obsolete docs: {vendor_dir.name}")
                shutil.rmtree(vendor_dir)

    # Generate vendor documentation
    print(f"Generating documentation for {len(vendors)} vendors...")
    for vendor in vendors:
        print(f"  Processing {vendor}...")
        manifest = all_manifests[vendor]

        # Generate human-readable markdown overview
        vendor_docs_path = docs_path / 'vendors' / vendor
        vendor_docs_path.mkdir(parents=True, exist_ok=True)

        overview_content = generate_markdown_overview(vendor, manifest)
        overview_path = vendor_docs_path / 'overview.md'
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(overview_content)

    print(f"✓ Generated {len(vendors)} vendor documentation pages")

    # Generate catalog index
    print("\nGenerating catalog index...")
    catalog_index = generate_catalog_index(all_manifests)
    index_path = generated_path / 'README.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(catalog_index)
    print(f"✓ Catalog index: {index_path}")

    # Generate external integrations documentation
    print("\nGenerating external integrations documentation...")
    external_integrations_path = generated_path / 'external-integrations'
    ext_catalog_path = external_integrations_path / 'catalog.json'

    if ext_catalog_path.exists():
        with open(ext_catalog_path, 'r', encoding='utf-8') as f:
            external_integrations_catalog = json.load(f)

        ext_md_content = generate_external_integrations_markdown(external_integrations_catalog)
        ext_md_path = external_integrations_path / 'README.md'
        with open(ext_md_path, 'w', encoding='utf-8') as f:
            f.write(ext_md_content)
        print(f"✓ External integrations docs: {ext_md_path}")
    else:
        print("  Warning: External integrations catalog not found, skipping docs")

    # Generate functions documentation
    print("\nGenerating functions documentation...")
    functions_catalog = generate_functions_catalog(all_manifests)
    functions_catalog_path = docs_path / 'functions.md'
    with open(functions_catalog_path, 'w', encoding='utf-8') as f:
        f.write(functions_catalog)
    print(f"✓ Functions overview: {functions_catalog_path}")

    # Generate individual function pages
    print("Generating individual function pages...")
    functions_dir = docs_path / 'functions'
    functions_dir.mkdir(exist_ok=True)

    # Collect generic functions
    generic_functions_path = Path('integrations/generic/functions')
    function_count = 0
    if generic_functions_path.exists():
        for func_file in generic_functions_path.glob('function_*.js'):
            metadata = parse_function_metadata(str(func_file))
            if metadata:
                func_data = {
                    'name': metadata.get('name', func_file.stem),
                    'version': metadata.get('version', 'N/A'),
                    'description': metadata.get('description', 'No description available'),
                    'type': metadata.get('type', 'function'),
                    'kind': metadata.get('kind', 'function'),
                    'mode': metadata.get('mode', 'N/A'),
                    'file': str(func_file),
                    'code': read_function_code(str(func_file))
                }

                # Generate page
                safe_name = func_data['name'].replace(' ', '-').replace('/', '-').lower()
                func_page_content = generate_individual_function_page(func_data)
                func_page_path = functions_dir / f"{safe_name}.md"
                with open(func_page_path, 'w', encoding='utf-8') as f:
                    f.write(func_page_content)
                function_count += 1

    # Collect vendor-specific functions
    for vendor_id, manifest in all_manifests.items():
        vendor_name = manifest.get('name', vendor_id)
        functions = manifest.get('integrations', {}).get('functions', [])

        for func in functions:
            # Read the function code
            func_file_path = func.get('file', '')
            if func_file_path and Path(func_file_path).exists():
                func['code'] = read_function_code(func_file_path)
            else:
                func['code'] = ''

            # Generate page
            safe_name = f"{vendor_name.lower().replace(' ', '-')}-{func['name'].replace(' ', '-').replace('/', '-').lower()}"
            func_page_content = generate_individual_function_page(func, vendor_name)
            func_page_path = functions_dir / f"{safe_name}.md"
            with open(func_page_path, 'w', encoding='utf-8') as f:
                f.write(func_page_content)
            function_count += 1

    print(f"✓ Generated {function_count} individual function pages")

    # Generate free/local integrations documentation
    print("\nGenerating free/local integrations documentation...")
    free_local_catalog = generate_free_local_integrations(all_manifests)
    free_local_path = docs_path / 'free-local.md'
    with open(free_local_path, 'w', encoding='utf-8') as f:
        f.write(free_local_catalog)
    print(f"✓ Free/local integrations docs: {free_local_path}")

    print('\n=== Documentation Generation Complete ===')


if __name__ == '__main__':
    main()
