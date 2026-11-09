# Budget tiers: $15k to $50k

**R0.4 draft · 2026-11-04 · Owner: Faisal Farouq**
Status: **PLANNING ONLY**. Only the items marked *listing* are priced from today's web listings. Everything else is an estimate, not a quote. Nothing is ordered.

## The short version

- **The core walking robot costs about $19,550 if you pay for everything except the test space** (range $13,968–$25,139). So $15k works only if your contacts lend the gantry, the test space, the reviews and the tools.
- **Recommended target: $25k.** That's the core robot, paid for, plus the spares and sensors that keep walking tests going when something breaks, with a 12% reserve.
- **Above $25k, money mostly buys personality and comfort, not a higher chance of walking.** Arms, a moving head and a nicer shell come at $35k; motion capture and a spare leg at $50k.
- **R0.1 under-budgeted the frame.** It allowed $650 for structure; a realistic figure is $1,500–3,000.
- **Money you need in the next 60 days: about $2,698–$5,149** (bench actuator, CAN adapters, power supply, stop chain, bench rig, one-leg rig, computer, IMU, wiring, care-demo hardware, tools).
- **Availability risk:** one seller lists the RobStride 04 as sold out. Ask for a written quote for 11 units (17 at $50k) now.

## Tiers at a glance

Totals use the middle of each estimate range; the reserve is what's left of the tier. Each tier includes everything in the tiers above it.

| Tier | What you get | Mid cost | Reserve | Must come from your contacts |
|---|---|---:|---:|---|
| **$15k · Minimum walker** | Core robot that can take tethered steps on cable power. No battery, arms pinned, printed shell. Only works if your contacts cover the items on the right. | $13,878 | $1,122 (7%) | Overhead gantry or an approved beam, test space, reviews, tools, 3D-printer access |
| **$20k · Core, paid for** | Everything in $15k, plus paid reviews, your own tools, and a battery with safe charging. | $17,554 | $2,446 (12%) | Gantry or approved beam, test space, 3D-printer access |
| **$25k · Reliable core (recommended)** | Adds your own gantry, a second spare actuator, a calibrated IMU, a second power supply and a CAN analyser. **The cheapest level where one broken part or a noisy sensor doesn't stop walking.** | $21,960 | $3,040 (12%) | Test space, 3D-printer access |
| **$35k · Expressive ASTRO** | Adds moving arms (2 joints each) and a head that turns, machined gear stages, a shop-made shell, a second battery, a wireless e-stop and more review time. It starts to *feel* like ASTRO. | $30,004 | $4,996 (14%) | Test space, 3D-printer access |
| **$50k · Research grade** | Adds motion capture (true body position for tuning the gait), a complete spare leg, a machined frame and a rented test space. | $42,849 | $7,151 (14%) | 3D-printer access |
| Beyond $50k | Foot force/torque sensors, 4-joint arms, composite shell, full independent safety review, a bigger computer, a brand-name gantry. | ≈$68,644 | — | — |

**If a contact can't provide something, add it from the next tier:** gantry $1,500–2,500, paid reviews $1,500–3,000, tools $300–700, test space $1,000–2,500 (all estimates).

## Parts by tier

### $15k · Minimum walker

These are the parts every tier needs. Running total $10,118–$17,639.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| 10 × Leg actuators | RobStride 04, 120 N m peak / 40 N m rated, 48 V, 1.42 kg | $3,190 | listing |
| Bench + spare actuator | RobStride 04; used on the single-joint bench first, then kept as the spare | $319 | listing |
| 4 × Gear stages | Belt or printed planetary: 3:1 on both hip rolls, 2:1 on both knees | $200–$600 | estimate |
| 2 × USB-CAN adapters | USB to CAN 2.0, 1 Mbit/s (one per leg bus) | $80–$180 | estimate |
| Main computer | Jetson Orin Nano Super 8 GB + NVMe SSD | $249–$330 | listing |
| 2 × IMU | Consumer 9-axis IMU board (BNO085 class), 1 spare | $50–$120 | estimate |
| Foot load cells | 4 load cells per foot + 2 amplifier boards | $80–$200 | estimate |
| Bench / tether power supply | 48 V, ~1 kW enclosed supply (Mean Well RSP-1000-48 class) | $250–$400 | estimate |
| Stop chain | 2 wired e-stops, safety relay, 48 V DC contactor, fuses, breaker | $300–$700 | estimate |
| Wiring and connectors | CAN cable, XT60/XT90, DC-DC converters, enclosures | $300–$600 | estimate |
| Frame parts | Laser-cut / CNC aluminium plates and tubes from an online shop | $1,500–$3,000 | estimate |
| Bearings, shafts, fasteners | — | $300–$600 | estimate |
| Feet | Aluminium plates + rubber soles | $100–$250 | estimate |
| 3D-printing material | PETG / nylon; assumes printer access | $200–$400 | estimate |
| Single-joint bench | Aluminium extrusion frame, lever arm, weights, load cell | $200–$400 | estimate |
| One-leg rig | Extrusion frame, vertical linear guide, hanging support | $500–$1,000 | estimate |
| Trolley, tether, rated connectors | Rigger specifies; includes slack adjuster | $300–$700 | estimate |
| Tether load cell | In-line load cell + amplifier | $100–$300 | estimate |
| Chain hoist | Manual chain hoist on the gantry | $150–$350 | estimate |
| Shell panels | 3D-printed / thermoformed panels and mounts | $600–$1,500 | estimate |
| Handling stand | Guided linear actuator ≥ 98 N holding, controller, limit switches, base (D-04) | $400–$900 | estimate |
| Voice and screen | USB microphone/speaker, 10 in touchscreen | $150–$400 | estimate |
| Shipping, tariffs, tax | ~15% on imported parts (actuators, compute, sensors) | $600–$1,200 | estimate |

### $20k · Core, paid for

Added to the tier above: $2,350–$5,000. Running total $12,468–$22,639.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| Robot battery | 48 V nominal, 15-20 Ah, with BMS | $400–$900 | estimate |
| Charger + fire-safe charging | Matched charger, metal charging container, Class ABC extinguisher | $150–$400 | estimate |
| Tools if not owned | Multimeter, torque wrench, crimpers, USB oscilloscope | $300–$700 | estimate |
| Paid reviews | Limited hours: structural/mechanical, rigging, battery/electrical | $1,500–$3,000 | estimate |

### $25k · Reliable core (recommended)

Added to the tier above: $3,569–$5,244. Running total $16,037–$27,883.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| Overhead gantry | 1-ton adjustable aluminium gantry, ≥ 10 ft under beam (budget brand) | $1,500–$2,500 | estimate |
| Second spare actuator | RobStride 04 | $319 | listing |
| Better IMU | VectorNav VN-100 Rugged development kit | $1,200–$1,525 | listing |
| Second power supply | Same 48 V supply, for parallel or spare | $250–$400 | estimate |
| CAN analyser | PCAN-USB class interface + software | $300–$500 | estimate |

### $35k · Expressive ASTRO

Added to the tier above: $5,594–$10,494. Running total $21,631–$38,377.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| Machined gear stages | Upgrade printed/belt stages to machined planetary (extra cost over tier 1) | $800–$1,800 | estimate |
| Wireless e-stop | Rated wireless stop for the stop operator | $400–$1,000 | estimate |
| Second battery | Same pack as tier 1 | $400–$900 | estimate |
| Extra review hours | More reviewer time before G2 and G4 | $1,000–$2,000 | estimate |
| 4 × Moving arms (2 DoF each) | RobStride 03 (60 N m peak), shoulder pitch + elbow, both arms | $896 | listing |
| Arm brackets and covers | — | $300–$600 | estimate |
| 2 × Head pan/tilt | RobStride 05 (5.5 N m) | $298 | listing |
| Better shell | Shop vacuum-formed panels (extra cost over tier 1) | $1,500–$3,000 | estimate |

### $50k · Research grade

Added to the tier above: $10,595–$15,095. Running total $32,226–$53,472.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| Machined frame upgrade | Shop-machined joints and brackets (extra cost over tier 1) | $2,000–$4,000 | estimate |
| Test-space rental | If no free space is approved | $1,000–$2,500 | estimate |
| Motion capture | OptiTrack Flex 3, 6-camera bundle | $6,000–$7,000 | listing |
| 5 × Spare leg set | 5 x RobStride 04 | $1,595 | listing |

### Beyond $50k

Added to the tier above: $17,595–$33,995. Running total $49,821–$87,467.

| Part | Specification | Cost | Price basis |
|---|---|---:|---|
| Rated brand-name gantry | RAZE 1-ton, 12 ft span, 8-12 ft (replaces budget gantry; extra cost) | $2,700–$3,700 | listing |
| Bigger computer | Jetson AGX Orin 64 GB developer kit | $1,999–$5,399 | listing |
| 2 × Foot force/torque sensors | 6-axis F/T sensor per foot (Bota SensONE class) | $6,000–$12,000 | quote needed |
| 4 × Full arms (4 DoF each) | +2 RobStride 03 per arm (shoulder roll, wrist) | $896 | listing |
| Composite shell | Professional fibreglass / composite panels (extra cost over tier 3) | $3,000–$6,000 | estimate |
| Full independent safety review | Documented review of the complete walking setup | $3,000–$6,000 | estimate |

## Things to know before ordering

- **Mass:** the $35k and $50k tiers add arm and head actuators. Re-run the mass budget before ordering them; the 55 kg cap still applies.
- **Arms are for gestures only.** They never lift, catch or hold a person (ASTRO-R-059).
- **Battery waits:** Year 1 walking is tethered, so the $15k tier runs on cable power. Buy the battery only after the power tests (about Day 220).
- **Tariffs and shipping:** about 15% is included for imported parts. Check the rate when you order.
- **Funding timing:** you said you can raise money when parts are ordered. The first actuator, power supply and stop chain are needed around Day 20. Raise that first $2,700–5,100 now (the 60-day list above).

## For comparison: buying a walking robot

Unitree's H2 (182 cm) base model is $29,900 from Unitree or $40,900 from a US store, but the base model has no developer access. The programmable EDU version starts at $66,800. A full-size walker you can program yourself costs more than this whole $50k range, so building is the cheaper path.

## Sources (checked 2026-11-04)

- RobStride listings: [rcdrone.top RobStride collection](https://rcdrone.top/collections/robstride); [openelab RobStride 04](https://openelab.io/a/s/products/robstride04-qdd-120n-m-integrated-joint-motor-module) (EUR 254.75, sold out; specs 40/120 N m, 1.42 kg, 48 V)
- [Jetson Orin Nano Super, USD 249](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-launches-new-usd249-ai-development-board-that-does-67-tops)
- [VectorNav VN-100 Rugged Development Kit](https://vectornav.com/store/products/imu-ahrs/p/vn-100-rugged-development-kit), USD 1,200–1,525
- [OptiTrack Flex 3](https://www.optitrack.com/cameras/flex-3): 6-camera bundle under USD 7,000
- [Crane Depot RAZE 1-ton gantry, 12 ft span](https://cranedepot.com/1-ton-raze-ag-series-aluminum-gantry-crane-1/), USD 5,200
- [Jetson AGX Orin 64 GB listing](https://rcdrone.top/products/nvidia-jetson-agx-orin-64gb-developer-kit), USD 5,399 (sold out); NVIDIA launch list USD 1,999
- [Humanoid prices, roboticscenter.ai](https://www.roboticscenter.ai/learn/research-humanoid-cost), updated 2026-10-18
- [CubeMars AK10-9 V3.0](https://openelab.com/products/cubemars-ak10-9-v3-0), USD 922.99 (18/53 N m): checked as an alternative; the RobStride 04 gives more torque for a third of the price
- R0.1 `budget/financial_budget.csv` for the old allowances

Full line list: `budget/budget_tiers_R0_4.csv`.