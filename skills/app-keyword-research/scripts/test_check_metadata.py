#!/usr/bin/env python3
"""Offline checks for the metadata checker:  python3 -I scripts/test_check_metadata.py"""
import os, runpy

check = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_metadata.py"))["check"]

# 7 Minute Math's live v1.0 metadata (October 2026) passes cleanly
assert check("7 Minute Math: Mental Math", "Arithmetic Workout for Adults",
             "brain,training,times,tables,practice,drill,quiz,trainer,speed,daily,percentage,multiplication,games") == ([], [])

fails, warns = check("Calorie Tracker for Apple Watch", "x" * 31, "calorie, diet,diet,meals,meal")
assert any("Apple product" in f for f in fails) and any("31/30" in f for f in fails)
assert any("spaces" in w for w in warns)
assert any("'calorie' is already" in w for w in warns)
assert any("'diet' appears twice" in w for w in warns)
assert any("'meals' is a plural" in w for w in warns)
assert check("Macro Tracker", "", "")[0] == []  # "mac" only matches as a whole word
print("ok")
