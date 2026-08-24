# Lab 4 hand-assembly answer key — instructor-only

Completed translation of the lab manual's Table `tab:lab4-handasm` (all 4
lines), cross-checked mechanically against `hack_interpreter.py`'s own
`assemble()` function in `test_asm.py` (see the "Hand-assembly cross-check"
test — `python test_asm.py` must show it passing).

| Line | Instruction type & fields | 16-bit binary |
|---|---|---|
| `@2` | A-instruction: opcode `0` + value `2` | `0000000000000010` |
| `D=A` | C-instruction: `comp=A` (`110000`), `dest=D` (`010`), no jump (`000`) | `1110110000010000` |
| `@3` | A-instruction: opcode `0` + value `3` | `0000000000000011` |
| `D=D+A` | C-instruction: `comp=D+A` (`000010`), `dest=D` (`010`), no jump (`000`) | `1110000010010000` |

## Derivation for the two rows students complete themselves

**`@3`** — an A-instruction is always opcode bit `0` followed by the
15-bit binary value of the constant. `3` in 15 bits is
`000000000000011`, so the full word is `0` + `000000000000011` =
`0000000000000011`.

**`D=D+A`** — a C-instruction is `111` + `a` + `cccccc` (comp) + `ddd`
(dest) + `jjj` (jump).
- `comp = D+A` uses the A-register directly (not `M`), so `a=0`; its
  6-bit code from the standard Hack comp table is `000010`.
- `dest = D` only → `010` (the three dest bits are A, D, M in that
  order; only the D bit is set).
- No jump → `000`.
- Assembled: `111` + `0` + `000010` + `010` + `000` = `1110000010010000`.

Both derivations are mechanically reproduced by `hack_interpreter.py`'s
`COMP_TABLE`/`DEST_TABLE`/`JUMP_TABLE` and `assemble()` — run
`python test_asm.py` to see the automated cross-check.
