from pathlib import Path
import json,csv,re,io
from plan_content import WEEKS
import plan_engineering,plan_hardware,plan_finish
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'source_baseline.json'
baseline=json.loads(BASE.read_text())
assert len(WEEKS)==52,len(WEEKS)
DEFAULTS={
 'Foundation':('Desk work','Stop if the requested scope introduces real patient data, clinical authority, unapproved spending or powered motion.'),
 'Software':('Software only','Stop and record REWORK for unauthorized capture/send, silent record mutation, clinical or dosing advice, real patient information or corrupted audit evidence.'),
 'Engineering':('Engineering desk work','Stop release decisions if load, rating, material, safety integrity, facility access or operating limits are missing. Provisional calculations authorize no fabrication or motion.'),
 'Simulation':('Simulation only','Stop a success claim if it depends on unrealistic support, unbounded actuators, invalid physics, missing logs or unreviewed assumptions. No simulator result authorizes hardware.'),
 'Procurement':('Conditional procurement','Do not commit funds without the exact written owner/G3 authorization. Stop for over-cap costs, incomplete technical evidence or unconfirmed donated resources.'),
 'Fabrication':('Qualified fabrication only','No physical fabrication before G4 and a named authorized qualified fabricator. Stop for unreleased drawings, substitutions or inspection failures.'),
 'Hardware':('Qualified supervised testing','Do not energize or move anything without the current signed test permit, qualified team, accepted prior stage, approved limits, inspected supports and controlled area. Stop at any approved trip, unexpected motion, barrier entry or missing evidence.'),
 'Handling':('Stationary supported handling','No payload work without the signed permit, secured independent support, captured inert 2 kg object, qualified team and approved limits. Stop for grip loss, interference, heat/current/force/position trips or walking enable.'),
 'Enclosure':('Conditional enclosure work','Keep gravity loads secured and energy isolated for fitting. Powered clearance/thermal work needs its own qualified permit. Stop for interference, exposed hazardous gaps, obstructed stops/vents or mass overrun.'),
 'Integration':('Controlled integration','Do not combine unvalidated hazardous subsystems. Only the current signed permit can authorize live motion; otherwise use a secured disabled setup. Stop for privacy, clinical-boundary or independent-stop failures.'),
 'Closeout':('Evidence and review','Stop any release claim with missing evidence, mismatched configuration, absent qualified review or a failed required criterion. A deadline cannot change the result.'),
 'Buffer':('Dependency and rework','Do not use a buffer day to bypass a gate, invent a pass, increase a payload or add an unreviewed feature. Physical retests still need current authorization.'),
}
fallbacks={
 'Procurement':['Compare the quotation baseline with the unanswered vendor fields for this exact package.','Update the landed-cost/technical comparison using replies already received; leave unavailable evidence unknown.','Save the missing approval, responsible reviewer, requested evidence and next follow-up date; commit no funds.'],
 'Fabrication':['Inspect the named drawing/configuration in CAD and mark every unreleased or substituted interface.','Prepare the exact reviewer questions and inspection hold points for this part or fixture.','Save a drawing-rework packet; perform no fabrication or assembly outside an actual release.'],
 'Hardware':['Open the protocol and existing raw/simulation logs for this named stage; do not energize the robot.','Compare the required signals, calibration, approved limits and support evidence against what is actually available.','Write the exact missing permit/review/equipment items and one next action for the responsible qualified person.'],
 'Handling':['Recalculate the stationary 2 kg load case using the current documented reach and module self-weight assumptions.','Audit retention, fixture, walking-inhibit and force/current/temperature evidence for the named handling configuration.','Save the missing qualified review or test prerequisites; keep the object unloaded and hazardous motion disabled.'],
 'Enclosure':['Use the CAD swept envelope and panel schedule to inspect this named clearance/service issue without powered motion.','Compare panel masses, material documents and prior temperature logs to the accepted configuration.','Save an annotated rework drawing or missing-evidence list; do not improvise a physical clearance or heat test.'],
 'Integration':['Run the corresponding fictional workflow on the laptop or a mechanically secured disabled interface.','Inspect exact-preview consent, record provenance and typed-gateway denials for the named scenario.','Save software-only evidence and explicitly keep the missing physical segment unvalidated.'],
}
days=[]
for wi,w in enumerate(WEEKS,1):
 for di,(title,a,b,test,file) in enumerate(w['entries'],1):
  n=(wi-1)*7+di;mode,stop=DEFAULTS[w['phase']]
  output=f"ProjectASTRO/{w['area']}/day_{n:03d}_{file}"
  gates=list(w['gate']);stages=list(w['stage'])
  if wi==28 and di==7:gates=['G3']
  if wi==30 and di>=3:gates=['G4']
  if wi==44:mode='Qualified stationary handling test'
  if wi==46:mode='Qualified enclosure verification'
  if wi==49:mode='Qualified controlled demonstration'
  duration=120 if di==7 else 150
  times=[10,45,35,20,5,5] if duration==120 else [15,50,40,30,10,5]
  steps=[
   f"Open the required inputs listed below. Check the exact revision and identify unresolved decisions for '{title.lower()}'. Do not assume equipment, approval or test results exist.",
   a,b,
   'Perform this completion check and save the actual observations: '+test,
   f"Save the deliverable as {output}. Include revision R0.2, actual date, accountable owner Faisal Farouq, your actual role, source references, results and unresolved limitations. Preserve prior evidence.",
   'Record PASS, REWORK or BLOCKED for this day with the actual evidence reference and time spent. PASS means the stated task was evidenced; it does not release a gate, certify safety or prove the whole robot works.'
  ]
  inputs=[w['inputs']]
  if n>1:inputs.append(f"Review Day {n-1:03d}'s output and unresolved items. If unavailable, identify the missing input rather than inventing it.")
  alternative=fallbacks.get(w['phase'],['Inspect the named input documents and list missing evidence for this exact daily objective.','Complete only the safe reversible analysis or fictional software case possible with confirmed available inputs.','Record the blocker, required decision/reviewer, next action and follow-up date without claiming the original task passed.'])
  days.append(dict(id=n,week=wi,weekDay=di,title=title,weekTitle=w['title'],phase=w['phase'],mode=mode,minutes=duration,objective=f"Complete {title.lower()} and produce {file} with traceable evidence.",inputs=inputs,steps=steps,stepMinutes=times,acceptance=[test,'The named deliverable contains actual evidence, source/revision/date/owner and limitations.','Required permissions and prior releases are evidenced; unknown, failed and unexecuted results stay visible.'],output=output,calculation=w['calculation'],stop=stop,gates=gates,stages=stages,requirements=[f'ASTRO-R-{r:03d}' for r in w['requirements']],alternative=alternative,alternativeOutput=f'ProjectASTRO/revision_history/day_{n:03d}_blocked_work.md',dependencyDays=[n-1] if n>1 else []))
days.append(dict(id=365,week=53,weekDay=1,title='Close the year with an honest owner decision',weekTitle='Year one closeout',phase='Closeout',mode='Owner decision and archive',minutes=120,objective='Record the evidence-based Year 1 outcome and the next authorized dependency with Faisal Farouq.',inputs=['Owner year-end decision packet, G8 disposition or explicit pending status, actual spend, mass and accepted verification evidence.','Day 364 archive recovery and owner packet.'],steps=[
 'Open the archived requirement matrix, final budget and mass report. List which Year 1 outcomes are accepted, partially achieved or unmet, each with its evidence reference.',
 'Review the actual outcome with Faisal Farouq. State precisely whether both three-step trials, their speed targets, stationary 2 kg ten-repetition task and complete fictional caregiver demo were accepted.',
 'Record the owner decision to maintain the accepted research scope, extend the schedule for specific blockers, or authorize a separately reviewed next phase. Do not invent approval if the discussion has not occurred.',
 'Confirm no unresolved critical safety/privacy/clinical-boundary issue is hidden and no real-patient, person-lifting, 5 kg, untethered or public-operation claim has been added.',
 'Save ProjectASTRO/release_archive/day_365_owner_closeout.md with revision R0.2, actual date, Faisal Farouq as accountable owner, actual attendees, budget difference, qualified review references and all limitations.',
 'Export a backup of this website tracker and the final project archive. Record the next dependency and its responsible person. Use REWORK or BLOCKED when required evidence/review remains absent.'
],stepMinutes=[15,35,30,20,10,10],acceptance=['Every outcome is backed by actual applicable reviewed evidence or marked unmet.','Owner decisions and budget changes are recorded only if they actually occurred.','The archive is recoverable and the next authorized dependency is explicit.'],output='ProjectASTRO/release_archive/day_365_owner_closeout.md',calculation='365 planned days represent approximately 886 owner-hours at this schedule. They exclude qualified specialist/fabrication time and do not guarantee technical feasibility or completion.',stop=DEFAULTS['Closeout'][1],gates=[],stages=[],requirements=['ASTRO-R-043','ASTRO-R-044','ASTRO-R-045','ASTRO-R-064'],alternative=['Audit the final evidence packet without claiming release.','Write the exact owner/reviewer decisions still missing and who must supply them.','Archive an honest incomplete research status and revised dependency list.'],alternativeOutput='ProjectASTRO/revision_history/day_365_pending_closeout.md',dependencyDays=[364]))
assert len(days)==365
for i,d in enumerate(days):d['next']=f"Day {i+2:03d}: {days[i+1]['title']}" if i<364 else 'Only the next scope actually authorized by Faisal and the applicable qualified reviewers.'
gates=[
 dict(id='G0',name='Baseline and owner decisions',day=7,requires=[],stages=[],checks=['Mission and exclusions accepted for this revision','D-01 through D-05 have actual dispositions or explicitly accepted scope restrictions','Budget accounting and spending authority recorded','Qualified role appointments and unresolved roles recorded']),
 dict(id='G1',name='Software baseline',day=83,requires=['G0'],stages=['S1'],checks=['Fictional-data and no-live-EHR boundary tested','Consent, medication, audit and exact-preview send cases reviewed','Privacy/accessibility/clinical-boundary defects dispositioned','Reviewed software revision and limitations archived']),
 dict(id='G2',name='Architecture and facility review',day=180,requires=['G0'],stages=[],checks=['Ten-joint topology and interfaces reviewed/frozen','Mass, COM, duty, power/thermal and simulation evidence reviewed','Independent safety and gravity-retention concept reviewed','Actual facility, qualified people and rated robot-arrest route evidenced']),
 dict(id='G3',name='Exact procurement release',day=195,requires=['G2'],stages=[],checks=['All required sizing, vendor and simulation evidence accepted','Landed complete BOM and reserve reconciled to funding','Independent reviewer and named fabricator recorded','Owner authorization covers exact order lines, amounts and revision']),
 dict(id='G4',name='Exact fabrication release',day=205,requires=['G3'],stages=[],checks=['Qualified-reviewed load-bearing drawings and materials released','Actual authorized qualified fabricator named','Fixture, support and stop design dependencies accepted','Fabrication and incoming-inspection plans accepted']),
 dict(id='G5',name='Fixture and electrical acceptance',day=252,requires=['G4'],stages=['S2','S3','S4','S5','S6','S7'],checks=['Sensor/module/power/safety/joint/leg evidence accepted','Actual response budget and gravity retention verified','Reviewed operating limits and calibration in force','Qualified next-stage test authority recorded']),
 dict(id='G6',name='Supported locomotion acceptance',day=294,requires=['G5'],stages=['S8','S9','S10','S11','S12','S13'],checks=['Lower body through repeated three-step progression accepted in order','Both three-step trials individually evidenced','Speed achievement, support assistance and stops accurately reported','As-tested configuration and qualified limitations recorded']),
 dict(id='G7',name='Handling and enclosure acceptance',day=322,requires=['G6'],stages=['S14','S15'],checks=['Stationary supported 2 kg handling evidence accepted','Ten repetitions and limits/retention documented','Panel clearance, thermal, service and actual mass evidence accepted','Payload/walking and support interlocks verified']),
 dict(id='G8',name='Controlled research release',day=360,requires=['G7'],stages=['S16'],checks=['Complete demonstration and all required evidence reviewed','Actual budget, mass and as-built revisions reconciled','Risks, failed tests and limitations disclosed','Release is controlled research only with actual independent disposition']),
]
stage_names=['Software-only caregiver demonstration','Individual sensors','Individual actuator module','Power system','Safety controller and emergency stops','One joint on fixture','One leg on fixture','Lower body without walking','Supported standing','Weight shifting','Single tethered step','Three consecutive tethered steps','Repeated three-step sequence','Stationary supported handling','Panel clearance and thermal tests','Complete caregiver demonstration']
stage_days=[83,217,224,231,238,245,252,259,266,273,280,287,294,308,322,343]
stages=[]
for i,(name,day) in enumerate(zip(stage_names,stage_days),1):
 gate='G0' if i==1 else 'G4' if i<=7 else 'G5' if i<=13 else 'G6' if i<=15 else 'G7'
 stages.append(dict(id=f'S{i}',name=name,day=day,requires=[f'S{i-1}'] if i>1 else [],gate=gate,checks=['Actual approved protocol and exact configuration identified','Required calibration and raw logs retained','Failures/stops and limitations disclosed','Qualified reviewer disposition recorded for this scope']))
phase_descriptions={
 'Foundation':'Set scope, decisions, roles and traceability before committing resources.',
 'Software':'Build and verify a fictional caregiver experience on a laptop first.',
 'Engineering':'Develop geometry, loads, mass, power, safety and facility evidence.',
 'Simulation':'Run versioned models, bounded controllers, uncertainty sweeps and failure injection.',
 'Procurement':'Qualify exact components and reconcile the whole-system budget before spending.',
 'Fabrication':'Release drawings to named qualified services and inspect actual parts.',
 'Hardware':'Follow the required sensor-to-gait physical validation sequence under signed permits.',
 'Handling':'Validate the separate stationary supported 2 kg task without cargo walking.',
 'Enclosure':'Fit and verify the removable rigid body with clearance, service and thermal evidence.',
 'Integration':'Combine accepted subsystems for a controlled fictional caregiver demonstration.',
 'Closeout':'Reconcile claims, risks, costs and evidence; archive the actual research outcome.',
 'Buffer':'Resolve actual blockers without compressing physical validation or adding scope.'}
for d in days:
 for key in ['steps','inputs']:
  d[key]=[s.replace('Software/care_app','software/care_app').replace('Requirements, Architecture, CAD, Simulation, Software, Tests, Evidence, Budget, Procurement, Risks, Workflows, FictionalData, Revisions and Releases','requirements, architecture, cad_specifications, simulation, software, tests, evidence, budget, procurement, risk_records, caregiver_workflows, simulated_patient_data, revision_history and release_archive').replace('Releases/R0_1','release_archive/R0_1') for s in d[key]]
data={'meta':{'owner':'Faisal Farouq','revision':'R0.2','date':'2026-10-24','baselineRevision':'R0.1','defaultStart':'2026-10-24','days':365,'ownerHours':sum(d['minutes'] for d in days)/60,'note':'Provisional dependency plan; physical completion and budget feasibility are unproven. Progress is browser-local and is not a safety approval.'},'weeks':[{'id':i+1,'title':w['title'],'phase':w['phase'],'start':i*7+1,'end':i*7+7} for i,w in enumerate(WEEKS)],'days':days,'gates':gates,'stages':stages,'phaseDescriptions':phase_descriptions,'requirements':baseline['requirements'],'hazards':baseline['hazards'],'verification':baseline['verification'],'decisions':baseline['decisions'],'budget':baseline['budget'],'mass':baseline['mass'],'sources':baseline['sources'],'artifacts':[{k:s[k] for k in ['number','title','path','control','body']} for s in baseline['sections']]}
(ROOT/'dist/plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
with (ROOT/'dist/resources/ASTRO_365_Daily_Plan.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['Day','Week','Phase','Title','Minutes','Objective','Required inputs','Exact steps','Completion checks','Output','Calculation or check','Stop conditions','Required gates','Prior test stages','Next dependency','Owner','Revision'])
 for d in days:writer.writerow([d['id'],d['week'],d['phase'],d['title'],d['minutes'],d['objective'],'\n'.join(d['inputs']),'\n'.join(f'{i+1}. {s}' for i,s in enumerate(d['steps'])),'\n'.join(d['acceptance']),d['output'],d['calculation'],d['stop'],','.join(d['gates']),','.join(d['stages']),d['next'],'Faisal Farouq','R0.2'])
for name,key,headers in [('Requirements','requirements',['ID','Phase','Requirement','Verification','Hazards','Evidence','Owner','Revision','Date']),('Hazards','hazards',baseline['hazard_headers']),('Verification','verification',baseline['verification_headers'])]:
 with (ROOT/f'dist/resources/{name}_R0_1.csv').open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(headers);writer.writerows(data[key])
assert len({d['title'] for d in days})==365
assert len({d['output'] for d in days})==365
assert all(sum(d['stepMinutes'])==d['minutes'] for d in days)
assert all(len(d['steps'])==6 for d in days)
assert all(len(d['steps'][1])>70 and len(d['steps'][2])>70 for d in days)
print(json.dumps({'days':len(days),'weeks':len(WEEKS),'owner_hours':data['meta']['ownerHours'],'unique_outputs':365,'daily_steps':sum(len(d['steps']) for d in days),'plan_bytes':(ROOT/'dist/plan.json').stat().st_size}))
