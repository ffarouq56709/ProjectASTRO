# Day 10 · Joint and payload hazards

**R0.3 · 2026-11-02 · Owner: Faisal Farouq**
Day 10 result: **PASS** (desk work: hazard list and control ideas). Severity, likelihood and residual risk stay **UNASSESSED** for a qualified reviewer.

Full table: `day_010_motion_payload_hazards.csv` (15 hazards, MP-01 to MP-15). On Day 13 they get permanent IDs (JB-H-21 onward).

## The short version

- **The drives are strong enough to crush a hand.** A knee at its rated torque pushes about 760 N at 10 cm from the joint, and a hip-roll joint about 1,140 N. Force limits can't make that safe, so the controls are **guards, gaps and distance**.
- **A runaway joint is fast.** At no-load speed a hip-roll joint turns 7 rad/s, so the leg tip could move about 6 m/s. That's why speed limits, a watchdog and an independent e-stop come before any motion, and why first tests use a restraint.
- **The handling stand is low-energy but still pinches.** The object weighs 19.6 N, but the actuator's push force can be hundreds of newtons, so the gap and the actuator choice matter more than the object.
- **People will want to touch it.** The pinned arms and tray look like handles. Briefings, barrier signs and the keep-out zone deal with that.

## The 15 hazards

| ID | Where | Hazard | Key number | Control idea | Check |
|---|---|---|---|---|---|
| MP-01 | Knee | Finger or hand in the knee-pad gap | 760 N rated, 2,280 N peak at 0.10 m | Guard or bellows; else gap ≥ 25 mm (fingers) | Days 97, 317 |
| MP-02 | Ankle | Finger between shin and foot cover | 400 N rated, 1,200 N peak at 0.10 m | Same as knee | Days 95, 97, 317 |
| MP-03 | Hip | Hand between thighs or thigh and pelvis | 1,140 N rated, 3,420 N peak at 0.10 m | Guard; else gap ≥ 100 mm (hand) | Days 93, 97, 317 |
| MP-04 | Foot | Person's foot stepped on | up to 539.55 N through one foot | Keep-out zone, barrier | Days 136, 261 |
| MP-05 | Swinging leg | Leg strikes a person | ≈0.45 m/s planned foot speed | Keep-out zone; speed limits | Days 131, 136 |
| MP-06 | Any joint | Runaway joint | 20.9 / 10.5 / 7.0 rad/s no-load; leg tip ≈6 m/s | Firmware + file speed limits, watchdog, independent e-stop, end stops, restraint | Days 131, 221, 233 |
| MP-07 | Shoulder pin | Pinch when posing; arm drops if pin lost | arm ≈1 kg (assumed) | Captive pin with clip; preflight check | Days 87, 261 |
| MP-08 | Shell seams | Panels collide, crack or pinch skin | — | Swept-clearance study; rounded edges | Days 97, 309, 317 |
| MP-09 | Cables | Cable snag cuts a sensor or power line | detect sensor loss ≤ 100 ms | Service loops; bend check; stale-sensor detection | Days 97, 216 |
| MP-10 | Tray | Dropped object | 21.6 J to the floor from 1.1 m; 2.9 J onto a catch tray 0.15 m below | Lip + pin; catch tray; unbreakable object | Days 201, 298 |
| MP-11 | Handling actuator | Hand pinched by the tray | push force = datasheet (often 100s of N) vs 24.5 N held | Lowest push force that still holds ≥ 98 N; guard or ≥ 100 mm gap; limit switches | Days 187, 201, 299 |
| MP-12 | Stand | Stand tips over | 7.35 N m; 10 kg stand needs base half-width > 0.075 m | Wide base or bolted | Day 201 |
| MP-13 | Handling power loss | Tray drops when power cut | 24.5 N held; ≥ 98 N holding screen | Holding force or brake; power-off test | Days 296, 299 |
| MP-14 | Arms, tray, stand | Used as a handhold | not designed to hold a person | Briefing, sign, no contact | Days 139, 333 |
| MP-15 | Mode | Walking with the object or docked to the stand | — | Payload and support interlocks block walking | Days 237, 299 |

Gap values come from ISO 13854 (minimum gaps to avoid crushing parts of the body: fingers 25 mm, hand 100 mm). Treat them as starting values; the mechanical reviewer confirms them.

## How the numbers were worked out

- **Pinch force** = joint torque ÷ distance from the joint axis. Example: 76 N m ÷ 0.10 m = 760 N. Rated values from Day 6: 40 N m direct, 76 N m at 2:1, 114 N m at 3:1. Peak values: 120, 228, 342 N m.
- **Runaway speed**: RobStride 04 no-load 200 rpm = 20.9 rad/s; ÷2 = 10.5; ÷3 = 7.0 rad/s. Leg tip at 0.86 m: 7.0 × 0.86 ≈ 6.0 m/s.
- **Planned swing**: 0.144 m in 0.6 s with a smooth profile peaks at 1.875 × the average speed: 1.875 × 0.24 = 0.45 m/s.
- **Drop energy** = m g h: 2 × 9.81 × 1.1 = 21.6 J; 2 × 9.81 × 0.15 = 2.9 J.

## How this links to the existing register

| Existing hazard | New detail added |
|---|---|
| JB-H-02 pinch / shell | MP-01, 02, 03, 07, 08, 11 |
| JB-H-03 runaway | MP-06, 09 |
| JB-H-05 payload / misuse | MP-10 to 15 |
| JB-H-17 power loss | MP-13 |
| JB-H-20 people get close | MP-04, 05, 14 |

## Outside help

A mechanical reviewer confirms the gap sizes and guard designs (Days 97 and 199) and the handling holding force (Day 296). A controls or safety reviewer confirms the runaway protections (Day 129). No one is named yet (D-02).

## Checks

| Check | Result |
|---|---|
| Every hazard has a control idea, a test ID and a reviewer role | PASS |
| No gap size, force limit or residual risk presented as approved | PASS |
| Person lifting and walking with cargo listed as excluded uses | PASS (MP-14, MP-15) |

Sources: R0.1 hazard register JB-H-02, 03, 05, 17, 20; R0.1 verification register; Day 6 R0.3 drive data; Day 9 keep-out sketch; ISO 13854 (minimum gaps to avoid crushing; values to be confirmed by the reviewer).
