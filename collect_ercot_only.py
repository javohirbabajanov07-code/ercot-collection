"""ERCOT-only collection, with retry logic for network flakiness."""
import gridstatus
import time
import sys

ERCOT_START, ERCOT_END = "2019-01-01", "2025-11-30"  # hard cap before RTC+B (5 Dec 2025)


def retry(fn, *args, max_tries=4, **kwargs):
    for attempt in range(1, max_tries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"  attempt {attempt}/{max_tries} failed: {e}", file=sys.stderr)
            if attempt == max_tries:
                print(f"  giving up after {max_tries} attempts, skipping this piece")
                return None
            time.sleep(10 * attempt)


def main():
    ercot = gridstatus.Ercot()

    print(f"ERCOT: real-time SPP, {ERCOT_START} to {ERCOT_END} (hard cap before RTC+B)...")
    spp = retry(ercot.get_spp, date=ERCOT_START, end=ERCOT_END, market="REAL_TIME_15_MIN")
    if spp is not None:
        spp.to_csv("ercot_rt_spp.csv", index=False)
        print(f"  saved ercot_rt_spp.csv ({len(spp)} rows)")

    print("ERCOT: ancillary service clearing prices (incl. ECRS from 2023-06-10)...")
    as_prices = retry(ercot.get_as_prices, date=ERCOT_START, end=ERCOT_END)
    if as_prices is not None:
        as_prices.to_csv("ercot_ancillary_prices.csv", index=False)
        print(f"  saved ercot_ancillary_prices.csv ({len(as_prices)} rows)")

    print("Done with ERCOT.")


if __name__ == "__main__":
    main()
