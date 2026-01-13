#!/bin/bash
# check-vendor-logos.sh
# Checks which vendors have logos and which are missing

set -e

echo "=========================================="
echo "Vendor Logo Availability Report"
echo "=========================================="
echo ""

# Supported formats in priority order
FORMATS=("svg" "png" "jpg" "jpeg")

# Arrays to track results
declare -a vendors_with_logos
declare -a vendors_missing_logos
declare -a logo_details

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a logo exists for a vendor
check_vendor_logo() {
    local vendor="$1"
    local vendor_dir="docs/vendors/$vendor"

    if [ ! -d "$vendor_dir" ]; then
        return 1
    fi

    # Check for logo.* files
    for ext in "${FORMATS[@]}"; do
        if [ -f "$vendor_dir/logo.$ext" ]; then
            echo "$vendor_dir/logo.$ext"
            return 0
        fi
    done

    # Check for icon.* files
    for ext in "${FORMATS[@]}"; do
        if [ -f "$vendor_dir/icon.$ext" ]; then
            echo "$vendor_dir/icon.$ext"
            return 0
        fi
    done

    # Check for vendorname.* files (exact match)
    for ext in "${FORMATS[@]}"; do
        if [ -f "$vendor_dir/$vendor.$ext" ]; then
            echo "$vendor_dir/$vendor.$ext"
            return 0
        fi
    done

    # Check for vendorname.* files (lowercase)
    local vendor_lower=$(echo "$vendor" | tr '[:upper:]' '[:lower:]')
    for ext in "${FORMATS[@]}"; do
        if [ -f "$vendor_dir/$vendor_lower.$ext" ]; then
            echo "$vendor_dir/$vendor_lower.$ext"
            return 0
        fi
    done

    return 1
}

# Discover all vendors from cortex directories
echo "Scanning for vendors..."
echo ""

# Collect all unique vendors
vendors=()

# From analyzers
if [ -d "cortex/analyzers" ]; then
    for vendor_dir in cortex/analyzers/*/; do
        if [ -d "$vendor_dir" ]; then
            vendor=$(basename "$vendor_dir")
            if [[ ! " ${vendors[@]} " =~ " ${vendor} " ]]; then
                vendors+=("$vendor")
            fi
        fi
    done
fi

# From responders
if [ -d "cortex/responders" ]; then
    for vendor_dir in cortex/responders/*/; do
        if [ -d "$vendor_dir" ]; then
            vendor=$(basename "$vendor_dir")
            if [[ ! " ${vendors[@]} " =~ " ${vendor} " ]]; then
                vendors+=("$vendor")
            fi
        fi
    done
fi

# Sort vendors alphabetically
IFS=$'\n' vendors=($(sort <<<"${vendors[*]}"))
unset IFS

echo "Found ${#vendors[@]} vendors"
echo ""
echo "Checking logos..."
echo ""

# Check each vendor for logos
for vendor in "${vendors[@]}"; do
    logo_path=$(check_vendor_logo "$vendor")
    if [ $? -eq 0 ]; then
        vendors_with_logos+=("$vendor")
        logo_file=$(basename "$logo_path")
        logo_details+=("$vendor: $logo_file")
    else
        vendors_missing_logos+=("$vendor")
    fi
done

# Print results
echo "=========================================="
echo "Results"
echo "=========================================="
echo ""

# Vendors with logos
echo -e "${GREEN}✅ Vendors with logos (${#vendors_with_logos[@]}):${NC}"
echo ""
if [ ${#logo_details[@]} -gt 0 ]; then
    for detail in "${logo_details[@]}"; do
        echo "  $detail"
    done
else
    echo "  (none)"
fi

echo ""
echo "=========================================="
echo ""

# Missing logos
echo -e "${RED}❌ Vendors missing logos (${#vendors_missing_logos[@]}):${NC}"
echo ""
if [ ${#vendors_missing_logos[@]} -gt 0 ]; then
    for vendor in "${vendors_missing_logos[@]}"; do
        echo "  $vendor"
    done
else
    echo "  (none)"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "Total vendors: ${#vendors[@]}"
echo -e "${GREEN}With logos: ${#vendors_with_logos[@]}${NC}"
echo -e "${RED}Missing logos: ${#vendors_missing_logos[@]}${NC}"

coverage=0
if [ ${#vendors[@]} -gt 0 ]; then
    coverage=$((${#vendors_with_logos[@]} * 100 / ${#vendors[@]}))
fi
echo "Coverage: ${coverage}%"
echo ""

# Exit with error if there are missing logos (for CI)
if [ ${#vendors_missing_logos[@]} -gt 0 ]; then
    exit 1
fi
