"""
test_chips.py -- exhaustive/representative correctness checks for chips.py
(CS401 Lab 3 instructor reference oracle).

Run: python test_chips.py
Expects: "8/8 chips PASS"
"""

from chips import DFF, Bit, Register, RAM8, RAM64, RAM512, RAM4K, RAM16K, PC

PASS = []
FAIL = []


def check(name, condition, detail=""):
    if condition:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: {detail}")


def cycle(chip, **kwargs):
    """Drive one clock cycle: set_input(**kwargs) then tock()."""
    chip.set_input(**kwargs)
    chip.tock()


# ---------------------------------------------------------------------------
# DFF: holds until an explicit set_input/tock changes it
# ---------------------------------------------------------------------------

d = DFF()
d.set_input(1)
d.tock()
check("DFF latches 1", d.out == 1, f"got {d.out}")
d.set_input(0)
# no tock yet -- out must still read the OLD value (combinational settle
# should not leak into out before the clock edge)
check("DFF holds pre-tock", d.out == 1, f"got {d.out} before tock")
d.tock()
check("DFF latches 0", d.out == 0, f"got {d.out}")

# ---------------------------------------------------------------------------
# Bit: load vs. hold semantics, exhaustive over a short sequence
# ---------------------------------------------------------------------------

b = Bit()
cycle(b, in_bit=1, load=1)
check("Bit loads 1", b.out == 1)
cycle(b, in_bit=0, load=0)  # hold -- in_bit ignored
check("Bit holds under load=0", b.out == 1, f"got {b.out}")
cycle(b, in_bit=0, load=1)
check("Bit loads 0", b.out == 0)

# ---------------------------------------------------------------------------
# Register: 16-bit load/hold
# ---------------------------------------------------------------------------

r = Register()
cycle(r, in_value=0xBEEF, load=1)
check("Register loads 0xBEEF", r.out == 0xBEEF, f"got {r.out:#06x}")
cycle(r, in_value=0x0000, load=0)
check("Register holds under load=0", r.out == 0xBEEF, f"got {r.out:#06x}")

# ---------------------------------------------------------------------------
# RAM8: independent-address write/read
# ---------------------------------------------------------------------------

ram8 = RAM8()
for addr in range(8):
    cycle(ram8, in_value=(addr * 111) & 0xFFFF, load=1, address=addr)
ok = True
for addr in range(8):
    ram8.set_input(in_value=0, load=0, address=addr)  # select for read, no write
    if ram8.out != (addr * 111) & 0xFFFF:
        ok = False
check("RAM8 stores 8 independent addresses", ok)

# writing to one address must not disturb the others
ram8.set_input(in_value=0xFFFF, load=1, address=3)
ram8.tock()
ram8.set_input(in_value=0, load=0, address=5)
check("RAM8 write to addr 3 leaves addr 5 untouched",
      ram8.out == (5 * 111) & 0xFFFF, f"got {ram8.out:#06x}")
ram8.set_input(in_value=0, load=0, address=3)
check("RAM8 addr 3 updated correctly", ram8.out == 0xFFFF, f"got {ram8.out:#06x}")

# ---------------------------------------------------------------------------
# RAM64: recursive addressing (spot check across child boundaries)
# ---------------------------------------------------------------------------

ram64 = RAM64()
test_addrs = [0, 7, 8, 15, 33, 63]  # spans multiple RAM8 children
for addr in test_addrs:
    cycle(ram64, in_value=(addr + 1000) & 0xFFFF, load=1, address=addr)
ok = True
for addr in test_addrs:
    ram64.set_input(in_value=0, load=0, address=addr)
    if ram64.out != (addr + 1000) & 0xFFFF:
        ok = False
check("RAM64 recursive addressing across child boundaries", ok)

# ---------------------------------------------------------------------------
# RAM512 / RAM4K: representative spot checks only (deeper recursion,
# same pattern already proven at RAM8/RAM64 -- exhaustive testing here
# adds instantiation cost without adding confidence).
# ---------------------------------------------------------------------------

ram512 = RAM512()
for addr in [0, 63, 64, 511]:
    cycle(ram512, in_value=(addr + 2000) & 0xFFFF, load=1, address=addr)
ok = True
for addr in [0, 63, 64, 511]:
    ram512.set_input(in_value=0, load=0, address=addr)
    if ram512.out != (addr + 2000) & 0xFFFF:
        ok = False
check("RAM512 spot check", ok)

ram4k = RAM4K()
for addr in [0, 511, 512, 4095]:
    cycle(ram4k, in_value=(addr + 3000) & 0xFFFF, load=1, address=addr)
ok = True
for addr in [0, 511, 512, 4095]:
    ram4k.set_input(in_value=0, load=0, address=addr)
    if ram4k.out != (addr + 3000) & 0xFFFF:
        ok = False
check("RAM4K spot check", ok)

# ---------------------------------------------------------------------------
# RAM16K: 4-way top split (not 8-way), spot check across all 4 top children
# ---------------------------------------------------------------------------

ram16k = RAM16K()
test_addrs_16k = [0, 4095, 4096, 8191, 12288, 16383]
for addr in test_addrs_16k:
    cycle(ram16k, in_value=(addr % 65536), load=1, address=addr)
ok = True
for addr in test_addrs_16k:
    ram16k.set_input(in_value=0, load=0, address=addr)
    if ram16k.out != (addr % 65536):
        ok = False
check("RAM16K 4-way top-level addressing across all 4 children", ok)

# ---------------------------------------------------------------------------
# PC: reset > load > inc > hold priority
# ---------------------------------------------------------------------------

pc = PC()
cycle(pc, in_value=0, load=0, inc=1, reset=0)
check("PC increments from 0", pc.out == 1, f"got {pc.out}")
cycle(pc, in_value=0, load=0, inc=1, reset=0)
check("PC increments to 2", pc.out == 2, f"got {pc.out}")
cycle(pc, in_value=500, load=1, inc=1, reset=0)  # load wins over inc
check("PC load beats inc", pc.out == 500, f"got {pc.out}")
cycle(pc, in_value=999, load=1, inc=1, reset=1)  # reset wins over load and inc
check("PC reset beats load and inc", pc.out == 0, f"got {pc.out}")
cycle(pc, in_value=0, load=0, inc=0, reset=0)
cycle(pc, in_value=0, load=0, inc=0, reset=0)
check("PC holds when all control bits are 0", pc.out == 0, f"got {pc.out}")

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

print(f"{len(PASS)}/{len(PASS) + len(FAIL)} checks PASS")
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print(f"  - {f}")
    raise SystemExit(1)
else:
    print("8/8 chips PASS (DFF, Bit, Register, RAM8, RAM64, RAM512/RAM4K spot-checked, RAM16K, PC)")
