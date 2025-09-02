import time
import sys


def main() -> None:
    print("[worker] starting background worker...", flush=True)
    # Minimal idle loop. Replace with actual queue consumption.
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("[worker] stopping...", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()