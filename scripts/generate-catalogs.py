#!/usr/bin/env python3
"""
Generate integration catalogs (JSON/YAML only).

This script generates machine-readable catalog files for integrations.
For documentation generation, see generate-docs.py.
"""

import os
import json
import yaml
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


def generate_functions_catalog_data(all_manifests: Dict) -> Dict:
    """Generate functions catalog data structure."""
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
                    'vendor': 'Generic'
                })

    # Collect vendor-specific functions
    vendor_functions = []
    for vendor_id, manifest in all_manifests.items():
        functions = manifest.get('integrations', {}).get('functions', [])
        for func in functions:
            vendor_functions.append({
                **func,
                'vendor': manifest.get('name', vendor_id),
                'vendor_id': vendor_id
            })

    all_functions = generic_functions + vendor_functions

    return {
        'total_functions': len(all_functions),
        'generic_count': len(generic_functions),
        'vendor_count': len(vendor_functions),
        'functions': all_functions
    }


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

    lines.append("# 📊 Catalog Generation Summary")
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

    print(f"=== Catalog Generation ===")
    print(f"Using branch: {CURRENT_BRANCH}")
    print(f"Using base URL: {BASE_URL}\n")

    # Create .generated directory structure
    generated_path = Path('.generated')
    generated_path.mkdir(exist_ok=True)

    catalogs_path = generated_path / 'catalogs'
    catalogs_path.mkdir(exist_ok=True)

    # Create subdirectories for catalogs
    vendors_catalogs_path = catalogs_path / 'vendors'
    vendors_catalogs_path.mkdir(exist_ok=True)

    # Clean up obsolete vendor catalogs
    if vendors_catalogs_path.exists():
        for vendor_dir in vendors_catalogs_path.iterdir():
            if vendor_dir.is_dir() and vendor_dir.name not in vendors:
                print(f"Cleaning up obsolete catalog: {vendor_dir.name}")
                shutil.rmtree(vendor_dir)

    # Generate vendor manifests
    print(f"\nGenerating manifests for {len(vendors)} vendors...")
    for vendor in vendors:
        print(f"  Processing {vendor}...")
        manifest = generate_vendor_manifest(vendor)
        all_manifests[vendor] = manifest

        # Create vendor catalog directory in vendors/ subdirectory
        vendor_catalog_path = vendors_catalogs_path / vendor
        vendor_catalog_path.mkdir(parents=True, exist_ok=True)

        # Write individual vendor manifest as YAML
        manifest_yml_path = vendor_catalog_path / 'manifest.yml'
        with open(manifest_yml_path, 'w', encoding='utf-8') as f:
            f.write("# AUTO-GENERATED - DO NOT EDIT\n")
            f.write("# This file is generated by generate-catalogs.py\n")
            f.write("# Edit vendor.yml for vendor metadata, then re-run the generator\n\n")
            yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

        # Write individual vendor manifest as JSON
        manifest_json_path = vendor_catalog_path / 'manifest.json'
        with open(manifest_json_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Generated {len(vendors)} vendor catalogs in catalogs/vendors/")

    # Write combined manifest (JSON and YAML) to catalogs/ directory
    output_path = catalogs_path / 'integration-manifest.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_manifests, f, indent=2, ensure_ascii=False)
    print(f"✓ Combined manifest (JSON): {output_path}")

    yaml_output_path = catalogs_path / 'integration-manifest.yml'
    with open(yaml_output_path, 'w', encoding='utf-8') as f:
        yaml.dump(all_manifests, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"✓ Combined manifest (YAML): {yaml_output_path}")

    # Generate external integrations catalog
    print("\nGenerating external integrations catalog...")
    external_integrations_catalog = generate_external_integrations_catalog(all_manifests)

    # Create external-integrations directory in catalogs/
    external_integrations_path = catalogs_path / 'external-integrations'
    external_integrations_path.mkdir(exist_ok=True)

    # Write catalog as JSON
    ext_json_path = external_integrations_path / 'catalog.json'
    with open(ext_json_path, 'w', encoding='utf-8') as f:
        json.dump(external_integrations_catalog, f, indent=2, ensure_ascii=False)
    print(f"✓ External integrations catalog (JSON): {ext_json_path}")

    # Write catalog as YAML
    ext_yaml_path = external_integrations_path / 'catalog.yml'
    with open(ext_yaml_path, 'w', encoding='utf-8') as f:
        f.write("# AUTO-GENERATED - DO NOT EDIT\n")
        f.write("# This file is generated by generate-catalogs.py\n\n")
        yaml.dump(external_integrations_catalog, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"✓ External integrations catalog (YAML): {ext_yaml_path}")

    # Generate functions catalog (data only)
    print("\nGenerating functions catalog...")
    functions_catalog = generate_functions_catalog_data(all_manifests)

    # Create functions directory in catalogs/
    functions_catalog_path = catalogs_path / 'functions'
    functions_catalog_path.mkdir(exist_ok=True)

    functions_catalog_json_path = functions_catalog_path / 'catalog.json'
    with open(functions_catalog_json_path, 'w', encoding='utf-8') as f:
        json.dump(functions_catalog, f, indent=2, ensure_ascii=False)
    print(f"✓ Functions catalog (JSON): {functions_catalog_json_path}")

    functions_catalog_yaml_path = functions_catalog_path / 'catalog.yml'
    with open(functions_catalog_yaml_path, 'w', encoding='utf-8') as f:
        f.write("# AUTO-GENERATED - DO NOT EDIT\n")
        f.write("# This file is generated by generate-catalogs.py\n\n")
        yaml.dump(functions_catalog, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(f"✓ Functions catalog (YAML): {functions_catalog_yaml_path}")

    # Load previous manifests for change detection (if exists)
    previous_manifests = None
    previous_manifest_path = catalogs_path / 'integration-manifest.json'
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
    print("\nGenerating GitHub Actions summary...")
    summary = generate_github_summary(all_manifests, previous_manifests)
    github_summary_path = generated_path / 'GITHUB_SUMMARY.md'
    write_github_summary(summary, github_summary_path)
    print(f"✓ GitHub Actions summary: {github_summary_path}")

    # Print summary
    print('\n=== Catalog Generation Complete ===')
    print(f"\nTotal Vendors: {len(all_manifests)}")
    print(f"Total Analyzers: {sum(m['stats']['totalAnalyzers'] for m in all_manifests.values())}")
    print(f"Total Responders: {sum(m['stats']['totalResponders'] for m in all_manifests.values())}")
    print(f"Total Functions: {sum(m['stats']['totalFunctions'] for m in all_manifests.values())}")
    print(f"Total External Integrations: {external_integrations_catalog['totalIntegrations']}")
    print(f"Total Integrations: {sum(m['stats']['total'] for m in all_manifests.values())}")


if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Please run: pip install pyyaml")
        exit(1)

    main()
