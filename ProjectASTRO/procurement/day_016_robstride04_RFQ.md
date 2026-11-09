# Day 16 — RobStride 04 request for quote

Revision: R0.3  
Actual work date: 2026-11-05  
Baseline target date: 2026-11-08  
Accountable owner: Faisal Farouq  
Owner time recorded: 2.0 hours  
Document result: **PASS — identical RFQ package complete; dispatch not claimed**

## Outcome

One vendor-neutral request was prepared for **11 identical RobStride 04 integrated actuator modules: 10 robot units plus 1 bench/spare unit**. Three real sales routes were identified. Every route remains **UNSENT — OWNER TO SEND** because the owner said he will perform outreach and no sent message, vendor receipt or reply is recorded.

This document is a request for information and quotation. It is not an order, seller selection, technical qualification, purchase authorization or powered-test release. Day 20 remains blocked until a revision-specific landed quote, an acceptable Day 19 bench permit and the owner's written authorization for the exact order line exist.

## Dispatch register

| Candidate vendor | Verified sales route | Product/listing reference checked 2026-11-05 | Dispatch status | Exact blocker / next action |
|---|---|---|---|---|
| RobStride Dynamics Co., Ltd. | `zhaoyuan@robstride.com`; `https://robstride.com/about-us` | Official RobStride 04 page: `https://www.robstride.com/products/robStride04`; retail display USD 255 | **UNSENT — OWNER TO SEND** | Owner must send the identical RFQ and retain the sent message or form receipt |
| OpenELAB Technology Ltd. | `info@openelab.io`; product-page Request for Quote form | `https://openelab.io/products/robstride04-qdd-120n-m-integrated-joint-motor-module`; displayed EUR 267.49 for the motor variant and a bulk-RFQ route | **UNSENT — OWNER TO SEND** | Owner must send the identical RFQ and retain the sent message or form receipt |
| RCDrone / Shenzhen Baichen Trading Co., Ltd. | `https://rcdrone.top/pages/contact` | `https://rcdrone.top/products/robstride-04-qdd-120n-m-integrated-actuator-module-48v-9-1-ratio-dual-magnetic-encoder-ip52-700w-output`; displayed from USD 319 | **UNSENT — OWNER TO SEND** | Owner must send the identical RFQ through the contact route and retain its receipt |

The displayed prices are **LISTINGS — UNQUOTED**. They do not establish availability, the included variant, quantity pricing, landed cost or purchase authority. The plan's arithmetic reference remains:

`11 × USD 319 = USD 3,509 before freight, tax, tariff, cables, interfaces and spares.`

The delivery destination is only known at city level as Berkeley, California, USA. The owner must provide the exact delivery address privately to each vendor before treating a response as a landed quote; payment credentials and the private address do not belong in this repository.

## Identical RFQ text

**Subject:** RFQ — 11 identical RobStride 04 actuator modules for university robotics prototype

Hello,

Please provide a formal quotation and technical package for **11 identical RobStride 04 integrated actuator modules** for a research robot project: **10 intended robot units plus 1 bench/spare unit**.

This is a request for quotation and technical information only. It is not an order. Please do not substitute a different model, hardware revision, firmware revision or accessory without identifying the difference in writing.

### Commercial response requested

1. Exact manufacturer name, model, orderable SKU and module configuration.
2. Hardware revision and firmware version that would ship for all 11 units.
3. Quantity available now, whether all 11 can be revision-matched and any lot/batch information.
4. Unit price, 11-unit price, currency, quotation validity date and payment terms.
5. Freight, insurance, tax, tariff/duty and other charges needed for delivery to Berkeley, California, USA. The owner will provide the private postal address directly.
6. Incoterm, ship-from location, estimated dispatch date and delivery lead time.
7. Warranty duration and coverage, return terms, restocking terms, RMA process and who pays return freight.
8. Whether university/research pricing, volume pricing or evaluation-unit pricing is available.
9. Confirmation that no revision or model substitution will occur without written approval.

### Included hardware and interface response requested

10. Confirm whether each unit includes the integrated driver, motor, planetary reducer and both encoders.
11. List included power and CAN cables, mating connectors, connector part numbers, pinout and recommended wire sizes.
12. Quote the compatible official USB-to-CAN or debugging interface, termination hardware and any required hub separately.
13. Identify the supported host operating systems, configuration/debug software, SDK, example code and licence terms.
14. Provide the exact CAN protocol/manual for the quoted firmware, default bitrate, identifier configuration method and termination requirements.
15. Provide firmware update and recovery procedures and state whether the shipped units require calibration or commissioning.

### Engineering evidence requested

16. Continuous output torque versus speed across supported voltage, ambient temperature and cooling conditions.
17. Peak torque duration, recovery/cool-down requirement, allowable duty cycle and the conditions behind each rating.
18. Required heat sink or mounting thermal path for the stated 40 N·m rated torque and any derating without it.
19. Motor, driver and gearbox temperature limits, temperature measurement location, thermal protection behaviour and available telemetry.
20. Efficiency data, torque constant, line/winding resistance, phase-current definition, DC-bus current limits and current-measurement accuracy.
21. Supported DC voltage range, absolute limits, inrush/pre-charge requirements and regenerative-energy behaviour at normal and full bus voltage.
22. Required external protection, including fuse, over-voltage handling, braking/bleeder hardware and safe power-down sequence.
23. Rotor and output inertia, backlash, torsional compliance and repeatability.
24. Permitted radial, axial and overturning-moment loads, bearing-life basis and mechanical-life evidence.
25. Power-off/backdrive behaviour, holding behaviour, brake availability and behaviour after communications loss, watchdog timeout or internal fault.
26. Encoder resolution and accuracy, absolute-position persistence, multi-turn behaviour and reboot/zero-reference behaviour.
27. Fault, enable, disable and emergency-stop-related interfaces; fault codes; reset conditions; and whether torque disable is independently verifiable.
28. STEP model, 2D dimensioned/toleranced drawing, mass tolerance, connector envelope and mounting/fastener requirements.
29. Official user manual, protocol document, datasheet, declaration/certification documents and their revision dates.
30. Any exclusions, prohibited applications or conditions that affect use in a restrained humanoid-robot actuator test bench.

Please answer each numbered item or mark it **not available**. Please attach or link the controlled documents that support each technical answer.

Thank you,

Faisal Farouq  
Project owner  
Jacobs Caregiver Research Robot / Project ASTRO internal codename

## Response acceptance table

| Group | Mandatory fields before comparison | Missing-data rule |
|---|---|---|
| Identity | Manufacturer, model, SKU, hardware revision, firmware revision, driver inclusion | Leave response incomplete; do not infer from a listing |
| Quantity and timing | Matched quantity 11, stock, lot/revision match, ship date, lead time | No delivery assumption |
| Landed commercial terms | Currency, unit and 11-unit price, freight, tax/duty, Incoterm, validity, payment, warranty and returns | No landed total and no seller selection |
| Electrical/interface | Voltage range, current definitions, CAN protocol/revision, connectors, cables, debug interface and termination | Bench integration remains blocked |
| Duty and thermal | Continuous torque-speed evidence, peak duration/recovery, cooling, derating and temperature limits | Actuator remains technically unqualified |
| Mechanical | STEP/2D drawing, mass, inertia, backlash/compliance, bearing/load limits and life | CAD and one-leg release remain blocked |
| Fault and regeneration | Disable/fault behaviour, watchdog, power-off behaviour, regen, over-voltage and external protection | Powered permit remains blocked |

## Internal procurement boundary

- RFQs prepared: 3 identical copies/routes.
- RFQs actually sent: 0.
- Vendor replies received: 0.
- Formal quotations received: 0.
- Seller selected: no.
- Purchase authorized: no.
- Order placed: no.
- Payment information recorded: no.
- Hardware, powered motion and reviewer approval claimed: none.

The owner should send the identical request without removing the engineering questions. If a vendor requires a shorter web form, send the commercial summary in the form and attach or link this full numbered list. Save the sent timestamp and the vendor's receipt for Day 17.

## Day 16 completion checks

- PASS: quantity 11 and the exact RobStride 04 model appear in the request.
- PASS: the same commercial, landed-cost and technical questions apply to every candidate vendor.
- PASS: contact routes and listing references are dated and source-linked.
- PASS: the USD 319 value and every displayed price remain labelled LISTING — UNQUOTED.
- PASS: no order, seller selection, purchase authorization or powered-work release is claimed.
- PASS: every unsent route has the exact blocker and next owner action.

## Sources

- RobStride 04 official product page: `https://www.robstride.com/products/robStride04` (checked 2026-11-05)
- RobStride official contact page: `https://robstride.com/about-us` (checked 2026-11-05)
- RobStride 04 official manual: `https://www.robstride.com/assets/product_manual_robStride04-37549d59.pdf` (checked 2026-11-05)
- OpenELAB RobStride 04 product/RFQ page: `https://openelab.io/products/robstride04-qdd-120n-m-integrated-joint-motor-module` (checked 2026-11-05)
- RCDrone RobStride 04 product page: `https://rcdrone.top/products/robstride-04-qdd-120n-m-integrated-actuator-module-48v-9-1-ratio-dual-magnetic-encoder-ip52-700w-output` (checked 2026-11-05)
- `procurement/11_make_versus_buy.md`
- `requirements/day_006_D03_D04_configuration.md`
- `revision_history/decision_log_R0_3.csv` (D-15)

