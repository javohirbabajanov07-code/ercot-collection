"""SMOKE TEST ONLY -- one single day, should finish in seconds.
Run this FIRST after setting up VPN/GitHub Actions, before ever running the
full multi-year collect_ercot_only.py again. If this fails with 403, don't
bother running the full script -- the block is still active."""
import gridstatus

ercot = gridstatus.Ercot()
print("Testing ERCOT access with a single day (2024-06-01)...")
try:
    spp = ercot.get_spp(date="2024-06-01", end="2024-06-02", market="REAL_TIME_15_MIN")
    print(f"SUCCESS: got {len(spp)} rows. Geo-block is NOT active from this connection -- "
          f"safe to run the full collect_ercot_only.py now.")
except Exception as e:
    print(f"STILL BLOCKED: {e}")
    print("Do not run the full script yet -- fix access first.")
