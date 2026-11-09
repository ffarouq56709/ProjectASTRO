# Day 6 · The first working configuration

**R0.3 · 2026-10-28 · Owner: Faisal Farouq**
Day 6 result: **PASS** (configuration document). Owner accepted the recommendations on 2026-10-28. D-03 and D-04 are the modelling basis; they stay provisional until the G2 review.
Nothing here has been built, simulated or tested. Every number is a target, a listing or a hand calculation, and is labelled that way.

## The short version

| Part | R0.2 proposal | R0.3 recommendation | Why |
|---|---|---|---|
| Legs | 5 joints per leg, no hip yaw, both ankle axes | **Keep. 10 joints.** | Flat-foot side-to-side weight shift needs a roll joint at both hip and ankle. Yaw is not needed for straight-line steps. |
| Hip width | Not set (feet 0.34 m apart) | **Hip-roll axes 0.30 m apart, inside wide thigh shells** | Hip roll carries the biggest load: 80.9 N m static at 0.30 m, 97.1 N m at the photo's apparent 0.36 m. Wide shells keep the photo's stance. |
| Drives | Not selected | **Screen a 120 N m-peak module class, with a 3:1 stage on hip roll and 2:1 on knee** | Direct drives fail the rated-torque screen at hip roll and knee. These stages pass it at up to 0.36 m spacing. |
| Head | Fixed | **Keep fixed** | No powered axis is needed for a fixed camera, speaker and face. |
| Arms and hands | Passive | **Arms pinned during walking; hands sculpted and fixed** | A free-swinging arm is an unmodelled pendulum. The photo's fingered hands become later scope. |
| Handling | One-axis carriage on two guides, custom drive | **Keep one axis. Use a bought guided linear actuator with a datasheet holding force, on its own stand.** | It is cheaper, has a known load rating, and moves 2.5 kg off the walking robot. |
| Axes | 10 + 1 = 11 | **10 + 1 = 11 (unchanged)** | |
| Mass | ≤55 kg target, 47.8 kg allocated | **Projection 48.5 kg + 6.5 kg reserve; shell is a risk** | Drives add 3.3 kg; the handling stand removes 2.6 kg. The photo's bulky shell may add about 1.6 kg more. |
| Cash | $10,000 cap; $15,000 scenario | **Actuator line now screens at $2,841–3,481 against a $3,000 pool** | Current listings are far below the R0.1 reference. They are not quotes. |

## Inputs I used

- `requirements/day_006_D03_D04_configuration.md` R0.2 (archived in `revision_history/day_006_revised_proposal_R0_2.zip`)
- `cad_specifications/parameters.json` and `candidate_joints.csv` (R0.1)
- `budget/mass_budget.csv`, `budget/financial_budget.csv` (R0.1)
- `requirements/day_005_D01_budget_options.md` (R0.2, PASS for arithmetic)
- `release_archive/R0_1/Project_ASTRO_Engineering_Baseline_R0_1.pdf` pp. 6–8 (load, mass and handling screens)
- New calculation: `architecture/day_006_joint_load_screen.py` → `day_006_joint_load_screen.csv`, `day_006_actuator_screen.csv`

## Appearance reference

Reference: `cad_specifications/reference/astro-rigid-panel-concept-v1.png` (concept render supplied 2026-10-28; not a drawing). Scale estimate: 1.829 m ≈ 663 px, so ≈ 2.8 mm per px. The render is in perspective, so read every dimension as ±20%.

| Feature in the photo | Engineering consequence |
|---|---|
| Small egg-shaped head on a charcoal collar, two eyes joined by a line | Fixed head; face can be printed or a small display. Speaker and microphone fit in the collar. |
| Very wide shoulders and torso | Shell area likely 3–4 m², above the 2.5 m² assumption. At 1.5 mm and 1,050 kg/m³: 3.5 m² → 5.5 kg + 1.26 kg mounts = **6.8 kg vs 5.2 kg allocated**. |
| Legs set wide, about 0.30–0.38 m between centres | Drives hip-roll torque (table below). Wide thigh shells can hide hip axes set slightly inboard. |
| Chest window with two lenses and a teal light | Fits a stereo/depth camera and a status light. Keep the window clear of the handling tray. |
| Fingered hands | Year one: sculpted, fixed hands with no motors. |
| Charcoal knee pads and exposed ankle joints | Matches the protected charcoal joint gaps in ASTRO-R-010. Check pinch gaps on Day 97. |
| Vents on the thighs and hips | Good places for actuator cooling air. Confirm on Day 124. |
| Broad flat shoes with dark soles | Matches the 0.32 × 0.22 m feet. Sole material is a friction question (Day 117). |

## D-03 · Legs: keep ten joints, no hip yaw

**Frontal-plane check.** To shift weight sideways with both feet flat, each leg tilts by the same angle φ. The hip must roll by −φ and the ankle by +φ. Without ankle roll the sole tips onto its edge. Option C (yaw instead of ankle roll) therefore cannot do a flat-foot weight shift. Robots without ankle roll walk dynamically on a narrow contact instead. Unitree's H1 lists five leg joints with one ankle joint; its successor H1-2 lists two ankle joints per leg ([Unitree H1 page](https://www.unitree.com/h1), checked 2026-10-28). That is a design data point, not proof for this robot.

**Yaw check.** Without hip yaw the feet keep the pelvis heading. Straight-line steps do not need yaw. The stance foot resists the swing leg's yaw reaction by friction. Screen: μ = 0.5 (assumed, unmeasured) × 539.55 N × 0.104 m mean contact radius = **28.2 N m** of yaw capacity. The swing reaction must be checked in simulation (Day 159, Day 171). Turning stays out of year one (ASTRO-R-055).

**Alternatives, costed.**

| Option | Joints | Lower-body actuator cost (listing, unquoted) | Mass effect | Verdict |
|---|---:|---|---|---|
| A · roll/pitch hip, knee, pitch/roll ankle | 10 | $2,841–3,481 (below) | +3.3 kg vs allocation | **Recommend** |
| B · add hip yaw | 12 | +2 small modules ≈ +$448–638 | +1.8–2.8 kg | Breaks ASTRO-R-005. Needed only for turning. |
| C · yaw replaces ankle roll | 10 | same as A | same as A | Loses flat-foot lateral shift. Reject for year one. |

**Gait method.** Plan a ZMP preview-control gait (Kajita et al., 2003). Reaching 0.10–0.15 m/s needs steps of about 1.2 s, which is too fast for a purely static gait. Linear-inverted-pendulum screen: centre-of-mass height 1.0 m (assumed), sway frequency 2.62 rad/s, gain 1.70. A lateral sway of **0.100 m** puts the ZMP at the foot centre (0.17 m). Step length at 1.2 s: **0.120 m** for 0.10 m/s, **0.180 m** for 0.15 m/s. Three steps covering 0.45 m take **3.0–4.5 s**.

## Loads: where the torque goes

Hand screen, single support, 55 kg robot, 10 kg per leg, 35 kg above the hips. Dynamic multiplier 1.5 is the R0.1 illustrative value, not a design factor.

| Joint | Case | Static N m | ×1.5 N m |
|---|---|---:|---:|
| Hip roll | hip spacing 0.36 m (photo) | **97.1** | 145.7 |
| Hip roll | hip spacing 0.34 m (R0.1 feet) | **91.7** | 137.6 |
| Hip roll | hip spacing 0.30 m (recommended) | **80.9** | 121.4 |
| Hip roll | hip spacing 0.24 m (narrow) | **64.7** | 97.1 |
| Knee pitch | knee bent 0.5 rad | 51.7 | 77.5 |
| Knee pitch | knee bent 0.7 rad | 71.6 | 107.4 |
| Hip pitch | torso held 0.05 m forward | 17.2 | 25.8 |
| Ankle pitch | ZMP 0.06 m from ankle | 32.4 | 48.6 |
| Ankle roll | ZMP 0.04 m from ankle | 21.6 | 32.4 |

Formula for hip roll: τ = g(m_upper × s/2 + m_leg × s), where s is hip spacing. The R0.1 screen (35 kg × 0.15 m = 51.5 N m) left out the swing leg and **underestimates hip roll by 13–46 N m**. Ankle torque cannot usefully exceed weight × distance to the sole edge: 107.9 N m (toe), 64.7 N m (heel), 59.4 N m (side).

## Drives and cost

| Module (listing, checked 2026-10-28) | Rated / peak N m | Mass | Price seen | Passes hip roll at 0.30 m (80.9 static)? |
|---|---|---:|---|---|
| RobStride 04 | 40 / 120 | 1.42 kg | $255 ([aifitlab](https://aifitlab.com/products/robstride-04-motor)); from $319 ([rcdrone](https://rcdrone.top/collections/robstride)) | Peak yes; **rated no** |
| RobStride 04 + 2:1 stage (concept) | 76 / 228 | 1.77 kg | +$50 per stage (assumed) | No (passes knee) |
| RobStride 04 + 3:1 stage (concept) | 114 / 342 | 1.87 kg | +$50 per stage (assumed) | **Yes, up to 0.36 m** |
| CubeMars AK80-64 | 48 / 120 | 0.85 kg | $1,150.76 ([RobotShop](https://www.robotshop.com/products/cubemars-ak80-64-kv80-ak-series-robotic-actuator)) | Peak yes; rated no |
| RobStride 03 | 20 / 60 | 0.88 kg | from $224 | No |

RobStride 04 rated torque is 40 N m with a 345 × 345 mm heat sink and 35 N m with a smaller one ([openelab guide](https://openelab.io/blogs/learn/what-is-robstride04-120nm-qdd-high-torque-robot-joints)). A leg gives it far less cooling, so the thermal check on Days 110 and 124 matters.

**Actuator line, R0.3 screen (unquoted):**

```text
10 x $255 + 4 x $50 stage + $91.25 USB-CAN hub = $2,841
10 x $319 + 4 x $50 stage + $91.25 USB-CAN hub = $3,481
R0.1 pool under the $10,000 cap                 = $3,000
Project total with R0.1 non-actuator lines     = $9,841 – $10,481
```

This replaces the R0.1 reference total of $15,899. It does **not** prove the cap works. The $7,000 of non-actuator allowances are still unquoted and look thin: $650 for structure and fabrication, $1,000 for rated robot fall protection, $600 for engineering review. Shipping, tax and import duty are unknown.

## Mass projection

| Line | R0.1 kg | R0.3 kg | Change |
|---|---:|---:|---|
| M-02 ten drives, transmissions, mounts | 14.0 | 17.3 | 10 × 1.42 + 2 × 0.45 (3:1) + 2 × 0.35 (2:1) + 10 × 0.15 mount (stage and mount masses assumed) |
| M-09 handling module | 3.0 | 0.4 | Docking plate only; the stand and actuator move off the robot (assumed) |
| Other lines | 30.8 | 30.8 | unchanged |
| **Components** | **47.8** | **48.5** | +0.7 |
| Reserve to 55 kg | 7.2 | **6.5** | |
| Risk not yet in the projection: bulky shell | | +1.6 | Reserve would fall to 4.9 kg |

The handling configuration still counts everything attached to the robot. The stand, actuator, tray and 2 kg object are listed separately (ASTRO-R-003 note in `budget/06_mass_budget.md`).

## Head and arms

- **Head:** fixed. It holds the connected-eye face, speaker, microphone with a hardware privacy switch, and a camera. No powered head axis in year one.
- **Arms:** unpowered and **pinned** at the shoulder during every gait trial. A removable pin lets you pose them for photos. The 2.0 kg M-10 allocation is unchanged.
- **Hands:** sculpted and fixed. The photo's fingers are cosmetic in year one.

## D-04 · Handling: one axis, bought, on its own stand

Keep the R0.2 idea: one vertical axis, retained tray, robot secured and stationary. Change how it is built.

| Item | Recommendation | Evidence to collect |
|---|---|---|
| Drive | Commercial guided linear actuator or screw stage, ≥100 mm stroke, with a **datasheet static holding force** or integral brake | Datasheet page showing holding force, duty cycle and limit switches |
| Load to hold | Object 19.62 N + tray and carriage (≈0.5 kg assumed, 4.91 N) = **24.5 N** | Weighed tray and carriage |
| Screen | Datasheet holding force ≥ 4 × 24.5 N = **98 N** (screening ratio assumed, for a reviewer to confirm) | Reviewer's written ratio |
| Moment at 0.30 m reach | 2 × 9.81 × 0.30 = **5.886 N m** object only | Bracket check by a mechanical reviewer |
| Stand | Separate floor stand, positioned so the tray sits in front of the robot's chest | Stand drawing; tip-over check |
| Robot | Secured to its support frame, walking disabled | Interlock test (Day 299) |

Power-loss behaviour: a lead screw is **not** assumed self-locking. Use the datasheet holding rating or a brake. B-08 stays at $350 unquoted.

## Sensing (unchanged from R0.2)

10 output-side joint encoders · 1 pelvis IMU · 8 foot load channels (4 per foot) · 1 tether load cell · 2 reference cameras (side, front) · handling position, current, temperature and retained-object switch. These are analysis quantities. Nothing is selected or owned.

## What changed from R0.2, and what it costs

| Change | Joints | Mass | Scope | Cash |
|---|---|---|---|---|
| Hip axes 0.30 m apart under wide shells | none | none | CAD task added to Days 86, 93 | none |
| 3:1 stage on hip roll, 2:1 on knee | none | +1.6 kg | adds 4 stage assemblies to fabricate | +$200 assumed |
| Listing-based drive class | none | +1.7 kg vs allocation | | actuator line $2,841–3,481 vs R0.1 $8,899 |
| Fixed sculpted hands | none | inside M-10 | articulated hands moved to later scope | none |
| Arms pinned for gait | none | none | pin detail on Day 87 | ≈$0 |
| Bought handling actuator on a stand | handling axis still 1 | −2.6 kg on robot | stand added to Day 201 drawings | within B-08 $350 (unquoted) |

## Decisions for Day 7

1. **D-03:** accept Option A (10 joints, no yaw) for further modelling. Yes / change.
2. **Hip spacing and drives:** (a) hip axes 0.30 m apart under wide shells, 3:1 on hip roll, 2:1 on knee — keeps the photo's look (recommended); or (b) 0.24 m with 2:1 on both — lighter load, visibly narrower stance.
3. **D-04:** accept the bought guided actuator on its own stand as the primary handling concept. Yes / change.
4. **D-01:** keep $10,000 as the working cap until quotes arrive (Days 188–193), with $15,000 as the fallback scenario. Or set the ceiling now.

## When you need outside help

| Topic | When | Ask for | Evidence to keep |
|---|---|---|---|
| Joint loads and drive choice | Day 112 | A mechanical or robotics engineer to check `day_110_joint_duty_summary.csv` | Written comments with name, date and file revision |
| Hip and knee 2:1 stage | Day 199 | Structural check of belt or gear stage brackets | Marked-up drawing or calculation sign-off |
| Handling stand and holding force | Day 296 | Mechanical reviewer to confirm the holding ratio and stand stability | Signed note with ratio and drawing revision |

No reviewer is named yet. Day 4 lists all six specialist roles as UNASSIGNED.

## Checks and result

| Check | Observation | Result |
|---|---|---|
| Lower-body count | 5 + 5 = 10 named joints, both ankle axes, no yaw | PASS |
| Screen reproducible | `python3 day_006_joint_load_screen.py` reproduces every number in the load and gait tables | PASS |
| Cost arithmetic | 2,550 + 200 + 91.25 = 2,841.25; 3,190 + 200 + 91.25 = 3,481.25 | PASS |
| Mass arithmetic | 47.8 − 14.0 + 17.3 − 3.0 + 0.4 = 48.5; 55 − 48.5 = 6.5 | PASS |
| Appearance | Reference photo received; proportions estimated ±20% | PASS (estimate only) |
| Prices labelled | All prices are listings dated 2026-10-28, not quotes | PASS |
| Owner acceptance | Accepted 2026-10-28: Option A, 0.30 m hip axes with 3:1 / 2:1 stages, handling stand, USD 10,000 working cap | PASS |
| Day 1 scope differences | Height tolerance, lift height, message timing, real-data wording, lower funding case | OPEN |

**Day 6: PASS** for the configuration document. You accepted all four decisions on 2026-10-28. This does not release G2 or approve any purchase. The R0.2 owner time entry (2 h) is kept in the R0.2 evidence record. No gate is released. No money is committed.

## Sources

Local (paths relative to `ProjectASTRO/`): S01 mission PDF R0.1; S02 engineering baseline R0.1 pp. 6–8; S05 `requirements/requirements.csv`; S07–S08 `cad_specifications/candidate_joints.csv`, `parameters.json`; S22 `budget/mass_budget.csv`; `budget/financial_budget.csv`; `requirements/day_005_D01_budget_options.md`; R0.2 Day 6 records in `revision_history/day_006_revised_proposal_R0_2.zip`; original Day 6 records in `revision_history/day_006_initial_proposal_R0_2.zip`.

Primary engineering references:

- Kajita, S. et al. "Biped walking pattern generation by using preview control of zero-moment point." IEEE ICRA 2003, pp. 1620–1626. doi:10.1109/ROBOT.2003.1241826.
- Vukobratović, M. and Borovac, B. "Zero-moment point — thirty five years of its life." International Journal of Humanoid Robotics 1(1), 2004, pp. 157–173. doi:10.1142/S0219843604000083.
- MuJoCo Modeling documentation, kinematic tree and actuator force limits: https://mujoco.readthedocs.io/en/stable/modeling.html (version to pin on Day 141).
- ISO 13482:2014 Robots and robotic devices — Safety requirements for personal care robots (scope reference, full text not reviewed).
- ISO 13850:2015 Safety of machinery — Emergency stop function (scope reference).
- ISO 13849-1:2023 Safety of machinery — Safety-related parts of control systems (for the Day 129 reviewer).

Manufacturer and listing data (checked 2026-10-28, live pages, not quotes): Unitree H1/H1-2 specification page; RobStride 04 listings at aifitlab.com and rcdrone.top; RobStride 04 specification guide at openelab.io; CubeMars AK80-64 listing at robotshop.com; RobStride 03 listing at pakronics.com.au.

Reference image: `cad_specifications/reference/astro-rigid-panel-concept-v1.png`, supplied by the owner 2026-10-28.

Revision history: R0.1 baseline 2026-10-23. R0.2 initial proposal and R0.2 revised proposal 2026-10-28, both archived unchanged. R0.3 2026-10-28: added load, gait, drive, cost and mass screens; changed arms to pinned for gait and hands to fixed; added appearance analysis from the reference photo; recommended 0.30 m hip axes with 3:1 hip-roll and 2:1 knee stages; changed handling drive to a bought guided actuator on a separate stand.
