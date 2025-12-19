#!/usr/bin/env python3
"""
Validate vendor.yml files against schema and taxonomy.

Usage:
    python validate-vendor-metadata.py [--vendor VENDOR_NAME]

    Without --vendor: validates all vendor.yml files
    With --vendor: validates specific vendor only
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
import yaml

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema package not found")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


def load_schema() -> Dict:
    """Load the vendor schema."""
    schema_path = Path('scripts') / 'schemas' / 'vendor-schema.yml'
    if not schema_path.exists():
        print(f"{Colors.RED}Error: scripts/schemas/vendor-schema.yml not found{Colors.NC}")
        sys.exit(1)

    with open(schema_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_taxonomy() -> Dict:
    """Load the taxonomy."""
    taxonomy_path = Path('scripts') / 'schemas' / 'taxonomy.yml'
    if not taxonomy_path.exists():
        print(f"{Colors.YELLOW}Warning: scripts/schemas/taxonomy.yml not found, skipping taxonomy validation{Colors.NC}")
        return {'categories': [], 'tags': []}

    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_valid_categories(taxonomy: Dict) -> List[str]:
    """Extract valid category names from taxonomy."""
    return [cat['name'] for cat in taxonomy.get('categories', [])]


def get_valid_tags(taxonomy: Dict) -> List[str]:
    """Extract valid tag names from taxonomy."""
    return [tag['name'] for tag in taxonomy.get('tags', [])]


def validate_vendor_file(vendor_name: str, schema: Dict, taxonomy: Dict) -> Tuple[str, List[str]]:
    """
    Validate a single vendor.yml file.

    Returns:
        (status, warnings) where status is 'valid', 'missing', or 'invalid'
    """
    vendor_yml_path = Path('docs') / 'vendors' / vendor_name / 'vendor.yml'

    if not vendor_yml_path.exists():
        return 'missing', [
            "vendor.yml not found - manifest will be generated with empty defaults",
            "Create vendor.yml with at minimum: description, category, tags, homepage"
        ]

    errors = []

    try:
        with open(vendor_yml_path, 'r', encoding='utf-8') as f:
            vendor_data = yaml.safe_load(f)

        if not vendor_data:
            return False, ["vendor.yml is empty"]

        # Schema validation
        try:
            validator = Draft7Validator(schema)
            schema_errors = list(validator.iter_errors(vendor_data))

            if schema_errors:
                for error in schema_errors:
                    if error.path:
                        field_path = '.'.join(str(p) for p in error.path)
                        errors.append(f"Schema error at '{field_path}': {error.message}")
                    else:
                        errors.append(f"Schema error: {error.message}")
        except Exception as e:
            errors.append(f"Schema validation failed: {str(e)}")

        # Taxonomy validation
        valid_categories = get_valid_categories(taxonomy)
        valid_tags = get_valid_tags(taxonomy)

        # Check category
        if 'category' in vendor_data:
            category = vendor_data['category']
            if category and valid_categories and category not in valid_categories:
                errors.append(
                    f"Invalid category '{category}'. Valid categories: {', '.join(valid_categories)}"
                )

        # Check tags
        if 'tags' in vendor_data:
            tags = vendor_data['tags']
            if tags and valid_tags:
                invalid_tags = [tag for tag in tags if tag not in valid_tags]
                if invalid_tags:
                    errors.append(
                        f"Invalid tags: {', '.join(invalid_tags)}. "
                        f"See taxonomy.yml for valid tags."
                    )

        # Check ID matches directory name
        if 'id' in vendor_data and vendor_data['id'] != vendor_name:
            errors.append(
                f"ID mismatch: vendor.yml has id '{vendor_data['id']}' "
                f"but directory is '{vendor_name}'"
            )

        status = 'valid' if len(errors) == 0 else 'invalid'
        return status, errors

    except yaml.YAMLError as e:
        return 'invalid', [f"YAML parsing error: {str(e)}"]
    except Exception as e:
        return 'invalid', [f"Unexpected error: {str(e)}"]


def find_all_vendors() -> List[str]:
    """Find all vendor directories."""
    vendors = []
    vendors_path = Path('docs') / 'vendors'

    if not vendors_path.exists():
        return []

    for vendor_dir in vendors_path.iterdir():
        if vendor_dir.is_dir():
            vendors.append(vendor_dir.name)

    return sorted(vendors)


def validate_all_vendors(schema: Dict, taxonomy: Dict, specific_vendor: str = None) -> bool:
    """
    Validate all vendor.yml files or a specific vendor.

    Returns:
        True if all validations pass (no invalid), False otherwise
    """

    if specific_vendor:
        vendors = [specific_vendor]
        print(f"{Colors.BLUE}Validating vendor: {specific_vendor}{Colors.NC}\n")
    else:
        vendors = find_all_vendors()
        print(f"{Colors.BLUE}Validating {len(vendors)} vendors...{Colors.NC}\n")

    results = []
    valid_count = 0
    missing_count = 0
    invalid_count = 0

    for vendor in vendors:
        status, messages = validate_vendor_file(vendor, schema, taxonomy)

        if status == 'valid':
            print(f"{Colors.GREEN}✅ {vendor}{Colors.NC}")
            valid_count += 1
        elif status == 'missing':
            print(f"{Colors.YELLOW}⚠️  {vendor}{Colors.NC}")
            for message in messages:
                print(f"   {Colors.YELLOW}→{Colors.NC} {message}")
            missing_count += 1
        else:  # invalid
            print(f"{Colors.RED}❌ {vendor}{Colors.NC}")
            for message in messages:
                print(f"   {Colors.RED}→{Colors.NC} {message}")
            invalid_count += 1

        results.append((vendor, status, messages))

    # Summary
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.CYAN}Summary{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"Total vendors: {len(vendors)}")
    print(f"{Colors.GREEN}Valid: {valid_count}{Colors.NC}")
    print(f"{Colors.YELLOW}Missing vendor.yml: {missing_count}{Colors.NC}")
    print(f"{Colors.RED}Invalid: {invalid_count}{Colors.NC}")

    if missing_count > 0 or invalid_count > 0:
        complete_count = valid_count
        coverage = (complete_count / len(vendors) * 100) if vendors else 0
        print(f"Complete coverage: {coverage:.1f}%")

    if missing_count > 0:
        print(f"\n{Colors.YELLOW}Note: {missing_count} vendor(s) missing vendor.yml will use empty defaults{Colors.NC}")

    # Only fail on invalid, not on missing
    return invalid_count == 0


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Validate vendor.yml files against schema and taxonomy'
    )
    parser.add_argument(
        '--vendor',
        type=str,
        help='Validate specific vendor only'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with error code if any validation fails'
    )

    args = parser.parse_args()

    # Load schema and taxonomy
    print(f"{Colors.CYAN}Loading schema and taxonomy...{Colors.NC}")
    schema = load_schema()
    taxonomy = load_taxonomy()
    print()

    # Validate
    all_valid = validate_all_vendors(schema, taxonomy, args.vendor)

    # Exit code
    if args.strict and not all_valid:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
