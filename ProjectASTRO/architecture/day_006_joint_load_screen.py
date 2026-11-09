"""Day 6 joint-load, gait and actuator screen for Project ASTRO (R0.3, 2026-10-28).

Static and simplified-dynamic hand calculations only. Every input is an
assumption listed in ASSUMPTIONS. Nothing here is a simulation result, an
approved load case or an actuator selection.

Run:  python3 day_006_joint_load_screen.py
Writes: day_006_joint_load_screen.csv and day_006_actuator_screen.csv next to this file.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
G = 9.81

ASSUMPTIONS = {
    # id: (value, unit, basis)
    "A6-01 robot mass": (55.0, "kg", "Year-one target ASTRO-R-003"),
    "A6-02 mass per leg incl. 5 actuators, structure, foot": (10.0, "kg", "Assumed; 5 x 1.42 kg listed module + 2.5 kg structure + 1.25 kg foot ~ 10.9 kg, rounded"),
    "A6-03 thigh = shank length": (0.43, "m", "parameters.json R0.1"),
    "A6-04 foot length x width": ((0.32, 0.22), "m", "parameters.json R0.1"),
    "A6-05 ankle axis to toe / to heel": ((0.20, 0.12), "m", "Assumed ankle placement on 0.32 m foot"),
    "A6-06 hip-joint lateral spacing cases": ((0.24, 0.30, 0.34, 0.36), "m", "0.34 = R0.1 foot spacing; 0.30-0.38 m estimated from the reference concept image (perspective, +/-20%); 0.24 = narrow-hip option"),
    "A6-07 knee flexion in stance cases": ((0.3, 0.5, 0.7), "rad", "Bent-knee walking range typical of ZMP gaits; assumed"),
    "A6-08 torso CoM forward of hip axis": (0.05, "m", "Assumed"),
    "A6-09 swing-leg CoM distance from hip": (0.25, "m", "Assumed"),
    "A6-10 swing-leg peak sagittal angle": (0.35, "rad", "Assumed"),
    "A6-11 dynamic screening multiplier": (1.5, "-", "R0.1 illustrative screen; not a design factor"),
    "A6-12 CoM height": (1.0, "m", "Assumed for a 1.829 m robot with heavy torso"),
    "A6-13 step period": (1.2, "s", "Assumed; gives 0.12 m/s at 0.144 m steps"),
    "A6-14 sole friction coefficient": (0.5, "-", "Assumed; unmeasured (Day 117 plan)"),
    "A6-15 optional external reduction": (2.0, "-", "Belt/gear stage option; efficiency 0.95 assumed"),
    "A6-16 planned ZMP offset from ankle (sagittal, lateral)": ((0.06, 0.04), "m", "Assumed planner margin inside the 0.32 x 0.22 m sole"),
}


def a(key):
    return ASSUMPTIONS[key][0]


def joint_rows():
    m = a("A6-01 robot mass")
    m_leg = a("A6-02 mass per leg incl. 5 actuators, structure, foot")
    m_up = m - 2 * m_leg  # pelvis, torso, head, arms, battery, electronics
    L = a("A6-03 thigh = shank length")
    k = a("A6-11 dynamic screening multiplier")
    toe, heel = a("A6-05 ankle axis to toe / to heel")
    half_w = a("A6-04 foot length x width")[1] / 2
    rows = []

    # Hip roll, single support: pelvis+torso cantilevered medially from the stance hip,
    # swing leg hangs one hip-spacing further out. Static moment about stance hip roll axis.
    for spacing in a("A6-06 hip-joint lateral spacing cases"):
        h = spacing / 2
        tau = G * (m_up * h + m_leg * spacing)
        rows.append(("hip_roll", f"single support, hip spacing {spacing:.2f} m",
                     tau, tau * k, f"g*(m_up*{h:.2f} + m_leg*{spacing:.2f}); m_up={m_up:.1f} kg"))

    # Knee pitch, stance: mass above stance shank acts along the hip-ankle line;
    # knee sits L*sin(theta/2) off that line.
    m_above_knee = m - (m_leg * 0.55)  # shank+foot+ankle actuators ~55% of leg mass (assumed)
    for th in a("A6-07 knee flexion in stance cases"):
        e = L * math.sin(th / 2)
        tau = m_above_knee * G * e
        rows.append(("knee_pitch", f"single support, knee flexion {th:.1f} rad",
                     tau, tau * k, f"{m_above_knee:.1f} kg * g * {e:.3f} m"))

    # Hip pitch, stance + swing contributions.
    tau_stance = m_up * G * a("A6-08 torso CoM forward of hip axis")
    tau_swing = m_leg * G * a("A6-09 swing-leg CoM distance from hip") * math.sin(a("A6-10 swing-leg peak sagittal angle"))
    rows.append(("hip_pitch", "torso hold (stance)", tau_stance, tau_stance * k, "m_up*g*0.05 m"))
    rows.append(("hip_pitch", "swing leg at 0.35 rad", tau_swing, tau_swing * k, "m_leg*g*0.25*sin(0.35)"))

    # Ankle: torque = weight x (planned ZMP offset from the ankle axis). A gait planner keeps
    # the ZMP well inside the sole; the sole edge sets the most torque that can ever be useful.
    W = m * G
    zx, zy = a("A6-16 planned ZMP offset from ankle (sagittal, lateral)")
    rows.append(("ankle_pitch", f"planned ZMP {zx:.2f} m from ankle", W * zx, W * zx * k, f"m*g*{zx:.2f} m"))
    rows.append(("ankle_roll", f"planned ZMP {zy:.2f} m from ankle", W * zy, W * zy * k, f"m*g*{zy:.2f} m"))
    rows.append(("ankle_pitch", "BOUND: CoP at toe", W * toe, W * toe, "m*g*0.20 m; more torque is useless (foot tips)"))
    rows.append(("ankle_pitch", "BOUND: CoP at heel", W * heel, W * heel, "m*g*0.12 m"))
    rows.append(("ankle_roll", "BOUND: CoP at sole edge", W * half_w, W * half_w, "m*g*0.11 m"))
    return rows, m_up


def gait_rows():
    zc = a("A6-12 CoM height")
    T = a("A6-13 step period")
    w = 2 * math.pi / (2 * T)  # lateral sway frequency: one sway cycle per two steps
    gain = 1 + zc * w ** 2 / G  # LIPM: p = y - (zc/g) y'' for y = A sin(wt)
    foot_offset = 0.34 / 2
    A_sway = foot_offset / gain
    v_lo, v_hi = 0.10, 0.15
    mu = a("A6-14 sole friction coefficient")
    lx, ly = a("A6-04 foot length x width")
    # Mean distance of a uniformly loaded rectangle from its centroid (numerical).
    n = 200
    s = 0.0
    for i in range(n):
        for j in range(n):
            x = (i + 0.5) / n * lx - lx / 2
            y = (j + 0.5) / n * ly - ly / 2
            s += math.hypot(x, y)
    r_mean = s / n ** 2
    M_yaw = mu * a("A6-01 robot mass") * G * r_mean
    return [
        ("lateral sway amplitude for ZMP at foot centre", A_sway, "m", f"0.17/(1+zc*w^2/g), w={w:.3f} rad/s, gain={gain:.3f}"),
        ("step length for 0.10 m/s", v_lo * T, "m", f"v*T, T={T} s"),
        ("step length for 0.15 m/s", v_hi * T, "m", f"v*T, T={T} s"),
        ("three-step interval at 0.10-0.15 m/s for 0.45 m", 0.45 / v_hi, "s (fast end)", "R0.1 example 3 x 0.15 m"),
        ("three-step interval at 0.10 m/s for 0.45 m", 0.45 / v_lo, "s (slow end)", ""),
        ("stance-foot yaw friction capacity", M_yaw, "N m", f"mu*m*g*r_mean, r_mean={r_mean:.4f} m, mu assumed {mu}"),
    ]


ACTUATORS = [
    # name, rated Nm, peak Nm, mass kg, listed price USD (low, high), source note
    ("RobStride 04 (listing)", 40.0, 120.0, 1.42, (255.0, 319.0),
     "aifitlab.com USD 255 (USD 240 at 5+); rcdrone.top 'from USD 319'; rated 40 N m with 345 x 345 mm heat sink, 35 N m with 220 x 200 mm (openelab.io guide). Checked 2026-10-28. UNQUOTED."),
    ("RobStride 04 + 2:1 stage (concept)", 76.0, 228.0, 1.77, (305.0, 369.0),
     "Concept only: 0.95 efficiency, +0.35 kg and +USD 50 per stage are ASSUMPTIONS."),
    ("RobStride 04 + 3:1 stage (concept)", 114.0, 342.0, 1.87, (305.0, 369.0),
     "Concept only: 0.95 efficiency, +0.45 kg and +USD 50 per stage are ASSUMPTIONS; stage peak rating must be checked."),
    ("CubeMars AK80-64 (listing)", 48.0, 120.0, 0.85, (1150.76, 1150.76),
     "robotshop.com USD 1,150.76 checked 2026-10-28; R0.1 SRC-02 showed USD 889.90 on 2026-10-23. UNQUOTED."),
    ("RobStride 03 (listing)", 20.0, 60.0, 0.88, (224.0, 224.0),
     "rcdrone.top 'from USD 224'; pakronics.com.au AUD 509.15 inc. GST; 20 N m rated / 60 N m peak. UNQUOTED."),
]


def main():
    rows, m_up = joint_rows()
    with open(HERE / "day_006_joint_load_screen.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Joint", "Case", "Static torque N m", "Screened torque N m (x1.5 or bound)", "Formula / basis", "Status"])
        for j, case, tau, scr, basis in rows:
            w.writerow([j, case, f"{tau:.1f}", f"{scr:.1f}", basis, "HAND SCREEN - NOT SIMULATED - NOT REVIEWED"])
        w.writerow([])
        w.writerow(["Gait screen", "Value", "Unit", "Basis", "", ""])
        for name, val, unit, basis in gait_rows():
            w.writerow([name, f"{val:.3f}", unit, basis, "", ""])
        w.writerow([])
        w.writerow(["Assumption", "Value", "Unit", "Basis", "", ""])
        for k, (v, u, b) in ASSUMPTIONS.items():
            w.writerow([k, v, u, b, "", ""])

    need = {}
    for j, case, tau, scr, basis in rows:
        if case.startswith("BOUND"):
            continue
        need.setdefault(j, [0, 0])
        need[j][0] = max(need[j][0], tau)
        need[j][1] = max(need[j][1], scr)
    with open(HERE / "day_006_actuator_screen.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Actuator", "Rated N m", "Peak N m", "Mass kg", "Joint", "Worst static N m", "Worst screened N m",
                    "Rated >= static?", "Peak >= screened?", "Set of 10 USD (low-high)", "Set of 10 kg", "Source / status"])
        for name, rated, peak, mass, (plo, phi), note in ACTUATORS:
            for j, (st, sc) in need.items():
                w.writerow([name, rated, peak, mass, j, f"{st:.1f}", f"{sc:.1f}",
                            "yes" if rated >= st else "NO", "yes" if peak >= sc else "NO",
                            f"{10*plo:,.0f}-{10*phi:,.0f}", f"{10*mass:.1f}", note])
    print(f"upper-body mass used: {m_up:.1f} kg")
    for j, (st, sc) in need.items():
        print(f"{j:12s} worst static {st:6.1f} N m  screened {sc:6.1f} N m")
    for name, val, unit, basis in gait_rows():
        print(f"{name}: {val:.3f} {unit}")


if __name__ == "__main__":
    main()
