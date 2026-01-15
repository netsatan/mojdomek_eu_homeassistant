#!/usr/bin/env python3
"""Simple test script to validate the MójDomek integration structure."""

import asyncio
import json
import os
import sys
from pathlib import Path


def test_structure():
    """Test that all required files exist."""
    base_path = Path(__file__).parent / "custom_components" / "mojdomek"
    
    required_files = [
        "manifest.json",
        "__init__.py",
        "const.py",
        "api.py",
        "coordinator.py",
        "sensor.py",
        "config_flow.py",
        "strings.json",
        "translations/en.json",
        "translations/pl.json",
    ]
    
    print("Checking file structure...")
    all_exist = True
    for file in required_files:
        file_path = base_path / file
        exists = file_path.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist


def test_manifest():
    """Test that manifest.json is valid."""
    manifest_path = Path(__file__).parent / "custom_components" / "mojdomek" / "manifest.json"
    
    print("\nValidating manifest.json...")
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        required_keys = ["domain", "name", "version", "config_flow", "integration_type"]
        for key in required_keys:
            if key in manifest:
                print(f"✓ {key}: {manifest[key]}")
            else:
                print(f"✗ Missing required key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error reading manifest: {e}")
        return False


async def test_api():
    """Test API connection."""
    print("\nTesting API connection...")
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            api_id = os.getenv("MOJDOMEK_API_ID")
            if not api_id:
                print("⚠ MOJDOMEK_API_ID not set - skipping API test")
                return None

            url = f"https://mojdomek.eu/api/api2.php?id={api_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ API accessible")
                    print(f"✓ Account: {data.get('firstname')} {data.get('lastname')}")
                    print(f"✓ Locations found: {len(data.get('locations', []))}")
                    return True
                else:
                    print(f"✗ API returned status {response.status}")
                    return False
    except ImportError:
        print("⚠ aiohttp not installed - skipping API test")
        print("  Install with: pip install aiohttp")
        return None
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MójDomek Home Assistant Integration - Validation Tests")
    print("=" * 60)
    
    structure_ok = test_structure()
    manifest_ok = test_manifest()
    
    # API test
    try:
        api_ok = asyncio.run(test_api())
    except Exception as e:
        print(f"API test error: {e}")
        api_ok = False
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  File structure: {'✓ PASS' if structure_ok else '✗ FAIL'}")
    print(f"  Manifest: {'✓ PASS' if manifest_ok else '✗ FAIL'}")
    if api_ok is None:
        print(f"  API test: ⚠ SKIPPED")
    else:
        print(f"  API test: {'✓ PASS' if api_ok else '✗ FAIL'}")
    print("=" * 60)
    
    if structure_ok and manifest_ok:
        print("\n✓ Integration is ready to install!")
        print("\nNext steps:")
        print("  1. Copy custom_components/mojdomek to your HA config/custom_components/")
        print("  2. Restart Home Assistant")
        print("  3. Go to Settings → Devices & Services → Add Integration")
        print("  4. Search for 'MójDomek' and add your API ID")
        return 0
    else:
        print("\n✗ Integration has errors - please fix before installing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
