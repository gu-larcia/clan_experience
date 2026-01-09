#!/usr/bin/env python3
"""Test WOM API endpoints to verify correct configuration.

Usage:
    python test_wom_api.py [GROUP_ID]
    
Defaults to group ID 11625 if not specified.
"""

import sys
import requests

BASE_URL = "https://api.wiseoldman.net/v2"
USER_AGENT = "OSRS-Clan-Tracker-Debug/1.0"


def test_endpoint(name: str, url: str) -> bool:
    """Test a single endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Result: List with {len(data)} items")
                if data:
                    print(f"First item keys: {list(data[0].keys())[:5]}...")
            elif isinstance(data, dict):
                print(f"Result: Dict with keys: {list(data.keys())[:5]}...")
            return True
        elif response.status_code == 404:
            print("ERROR: 404 - Not Found")
            print("This endpoint does not exist or the resource was not found.")
            return False
        else:
            print(f"ERROR: Unexpected status code")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False


def main():
    group_id = int(sys.argv[1]) if len(sys.argv) > 1 else 11625
    
    print(f"Testing WOM API v2 for group ID: {group_id}")
    print(f"Base URL: {BASE_URL}")
    
    results = {}
    
    # Test group details
    results["Group Details"] = test_endpoint(
        "Group Details",
        f"{BASE_URL}/groups/{group_id}"
    )
    
    # Test hiscores (correct endpoint for members)
    results["Group Hiscores (members)"] = test_endpoint(
        "Group Hiscores (returns all members)",
        f"{BASE_URL}/groups/{group_id}/hiscores?metric=overall"
    )
    
    # Test the WRONG endpoint to confirm it doesn't exist
    results["Group Members (WRONG)"] = test_endpoint(
        "Group Members (this endpoint does NOT exist)",
        f"{BASE_URL}/groups/{group_id}/members"
    )
    
    # Test gains
    results["Group Gains"] = test_endpoint(
        "Group Gains",
        f"{BASE_URL}/groups/{group_id}/gained?metric=overall&period=week"
    )
    
    # Test achievements
    results["Group Achievements"] = test_endpoint(
        "Group Achievements",
        f"{BASE_URL}/groups/{group_id}/achievements?limit=10"
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} - {name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if not results.get("Group Details"):
        print("\n⚠️  WARNING: Group details failed!")
        print(f"    The group ID {group_id} may not exist.")
        print("    Check: https://wiseoldman.net/groups to find your group ID.")
    
    if results.get("Group Members (WRONG)"):
        print("\n⚠️  UNEXPECTED: /members endpoint returned success")
        print("    This is unusual - the API may have changed.")
    else:
        print("\n✓ Confirmed: /members endpoint does NOT exist (expected)")
        print("  Your code should use /hiscores instead.")


if __name__ == "__main__":
    main()
