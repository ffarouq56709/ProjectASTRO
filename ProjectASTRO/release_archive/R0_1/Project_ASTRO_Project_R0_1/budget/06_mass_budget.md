# Mass budget and engineering screens

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-06

**Objective:** Allocate onboard mass and expose sizing conflicts before selecting actuators.

**Required inputs:** Provisional geometry and material densities; component datasheets and CAD masses later.

**Known values and provisional assumptions:** 47.8 kg allocated components plus 7.2 kg growth reserve =55.0 kg target; payload and external fixtures accounted separately.

**Unknowns:** Actual masses, COM, inertias, structural stresses, full duty cycle, foot friction and arrest loads.

**Calculations:** All calculation examples below and workbook Engineering/Mass tabs; none is a validated selection or physical result.

**Output file:** budget/06_mass_budget.md

**Implementation steps:** 1. Replace allowances with datasheet/CAD values. 2. Compute COM/inertias by configuration. 3. Run inverse dynamics and thermal duty analysis. 4. Weigh assemblies. 5. Reconcile remaining reserve at every gate.

**Acceptance test:** ASTRO-V-02/03; no duplicated/omitted components, all onboard parts counted, measured <=55 kg target, independent engineering sizing review.

**Stop conditions:** Projected >55 kg requires rework; >65 kg major review; missing load cases or peak-only actuator selection blocks procurement.

**Result:** REWORK - allocation and screening calculations only

**Next dependency:** G2 CAD mass/inertia model and load cases

**Physical authorization and supervision:** No fabrication or loading authorized; calculations require independent review.

**Budget effect:** Mass growth requires a cost revision; no monetary change accepted.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The component allocations are in budget/mass_budget.csv. They are design ceilings, not a prediction of the as-built robot. The 14 kg lower-body actuation allocation includes ten modules, transmissions and dedicated actuation mounts. Generic structural brackets belong to the structure line; the later BOM must prevent double counting. External robot arrest, test fixture, floor hardware and the inert payload are outside operating robot mass, but are separately listed and rated. A stationary configuration with the 2 kg object has 57 kg moving/retained robot-plus-object mass at the 55 kg robot target. Walking with that payload is prohibited. Removing a module requires a separately weighed and versioned configuration.

Mass growth: 47.8 x 1.20 =57.36 kg before any unused reserve is counted. This exceeds the 55 kg target by 2.36 kg. At 40 percent growth, 47.8 x 1.40 =66.92 kg, exceeding the 65 kg major-review threshold by 1.92 kg. Growth reserve is headroom, not extra hardware and must not be added again to these grown component sums.

Panels: for assumed area A=2.5 m2, thickness t=0.0015 m and density rho=1050 kg/m3, m=A*t*rho=3.9375 kg. Adding 1.2625 kg for panel supports/overlap gives 5.2 kg. Doubling to 0.003 m produces 9.1375 kg, a 3.9375 kg increase. Area, plastic density, process thickness and required impact/fire performance need material selection and actual CAD; large solid-printed shells can exceed this budget.

Gravity screen with g=9.81 m/s2 and m=55 kg: W=539.55 N. A horizontal COM offset e=0.10 m from a loaded ankle gives tau=W*e=53.96 N m. At e=0.15 m, tau=80.93 N m. Multiplying by an illustrative dynamic screening factor of 1.5 yields 80.93 and 121.40 N m. This is not a final factor of safety or joint load envelope. It omits link inertia, impacts, compliance and load sharing. A full-body inverse-dynamics trajectory and fault-load cases are required.

For illustration, a 35 kg effective upper load at a 0.15 m hip lever gives 35*9.81*0.15=51.50 N m static; a 0.20 m knee lever gives 68.67 N m. The same 1.5 screen gives 77.25 and 103.01 N m. The effective mass and lever arms are assumptions. The manufacturer's AK80-64 reference lists 48 N m rated and 120 N m peak (SRC-02). Even the 0.10 m ankle static example exceeds that rated value. Low walking speed does not remove sustained gravitational torque or winding heating. The 120 N m peak value is not a continuous holding rating.

Foot screen: a 0.32 x 0.22 m rectangle has 0.0704 m2 area. A 55 kg single-support load uniformly spread over it gives 7.66 kPa, but real contact area and local pressure differ. The ideal lateral half-width is 0.11 m; an illustrative 0.025 m edge allowance leaves 0.085 m at the same coordinate origin. Dynamic ZMP, friction and contact uncertainties still require simulation and tests; this is no stability proof. Estimated COM height from provisional component centers is computed as sum(m_i*z_i)/sum(m_i); the reserve has no physical location and is excluded until assigned.

Handling screen: a 2 kg object at horizontal reach 0.30 m contributes 2*9.81*0.30=5.886 N m; at 5 kg it contributes 14.715 N m, 2.5 times as much, before module self-weight, motion, friction and safety factors. A counterbalance or independent supported module reduces the biped integration burden. It does not remove the need for structural/retention review.

Energy screen: assume ten joints each average 40 N m at 0.50 rad/s simultaneously. P_mech=10*40*0.50=200 W. At illustrative efficiency 0.60 plus 60 W electronics, P_bus=200/0.60+60=393.33 W. A 48 V, 8 Ah nominal pack stores 384 Wh=1.3824 MJ. At 80 percent usable energy, ideal runtime is 307.2/393.33=0.781 h=2812 s. This is not a runtime prediction; holding losses, peak loads, temperature, converters, aging and duty cycle are unresolved. Average bus current for this example is 8.19 A. Manufacturer ADC/phase current must not be summed as battery DC current. Peak bus, fuse, conductor, regen and contactor sizing require a reviewed electrical model.

Thermal work remains open: compute tau_RMS=sqrt(sum(tau_i^2*dt_i)/sum(dt_i)), convert motor-side torque to current using vendor gearbox efficiency and torque constant conventions, calculate copper/driver loss, and model temperature with measured thermal parameters. No winding resistance convention or peak-duration limit has been assumed sufficient for purchase. Robot arrest sizing likewise cannot use W alone: a simple energy screen F_avg approximately m*g*(1+h/d) excludes peak amplification and rig geometry and is intentionally not used to select rated equipment.
