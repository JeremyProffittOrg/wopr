# WOPR first-draft model

## Locked decisions (user-confirmed; do not revisit)
- 2026-09-26: "create a 3d pirntable mock up of the W.O.P.R. computer in war games"
- 2026-09-26: "4 for the longer side lights"
- 2026-09-26: "Four per long side: eight total"
- 2026-09-26: "perfect" confirms W.O.P.R. / War Operation Plan Response lettering and touchscreen above the logo.
- 2026-09-26: "proffitt.jeremy@gmail.com" is the delivery recipient.
- 2026-09-26: "inset, with 1 inch deep mount cut out ont he back of the led"
- 2026-09-26: "about 11 inches in length and porprtionaql othewise"
- 2026-09-26: "gray and white" and "Create a first draft incliduign both mock ups and drawings from multiple agnles from scad in a pdf, and email it to me"
- 2026-09-26: "DON\"T START CONSOLEE APPS IN THE FORGROUND"
- 2026-09-26: "no, the led arrays need to be side by side and everythign needs to mount from the back, and the top needs to be open for a pen holder"
- 2026-09-26: "I SAID DONT RUN CONSOLE APPS IN THE FORGROUND"
- 2026-09-26: "make it 8 rgb led pannels per side, try that" supersedes the earlier four-per-side count.
- 2026-09-26: "change it to 7 rgb led pannels per side, then email it to me" supersedes the eight-per-side count.
- 2026-09-26: "gray left and grry right should be one piece, and combine base and cup too, redo that and then open at bambu labs"

## Verified facts
- C:/dev/wopr/deploy.md: delivery through main only. Repository currently has no GitHub workflow.
- C:/Users/Jeremy/tools/openscad-nightly/openscad.com --version: OpenSCAD 2026.09.11.
- Adafruit https://www.adafruit.com/product/3315: V2 2.4-inch TFT touchscreen, nominal 65 x 53 x 9.5 mm.
- Seeed Eagle board from https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip: outline 20.955 x 17.780 mm; 60 LEDs per board.
- Visual reference: https://www.miniatua.com/work/wopr/; proportions are an interpretation, not measured film-prop dimensions.
- Existing C:/dev/adafruit-pannel/scripts/send_case_pdf_mail.py configures jeremy@jeremy.ninja to proffitt.jeremy@gmail.com, reply to proffitt.jeremy@gmail.com, SES us-east-1.

## Assumptions
- Current draft 05: fourteen Seeed boards total, seven adjacent boards per side. Centers X=31.235+i*21.255 for i=0 through 6; Z=101. A 0.30 mm assembly gap separates PCB edges. Shell, base and main cup each export as one continuous part; tower cup remains separately removable.
- Side text corrected to War Operation Plan Response. One TFT above primary W.O.P.R. logo.
- Overall 279.4 x 155 x 165 mm. Gray structure and flush white material volumes; colored electronics are render-only.
- First-draft mounts use measured PCB envelopes plus clearance; hardware fit and print tolerance require a physical trial.
- Draft 02 uses rear-loading pockets with hidden rear screws, plus removable main and tower pen cups. Removable cups allow screwdriver access before installation and keep pens away from electronics.

## rear-mount-pen-holder — correct LED layout, mounting direction and open top
depends on: model-export
### revised-geometry — adjacent arrays and open pen storage
- [x] adjacent-led-banks — four adjacent boards behind each continuous window, rear retaining frames and blind pilots.
- [x] rear-tft-mount — rear loading and rear screw heads; closed front bezel.
- [x] open-pen-cups — removable, isolated pen cups with 3 mm floors and vertical removal paths.
- [x] hidden-console-build — OpenSCAD subprocess uses CREATE_NO_WINDOW and openscad.exe; no foreground console.
- [x] revision-proof — python C:/dev/wopr/cad/build.py exits 0, eleven watertight STLs and mechanical clearance probes pass; six PDF pages inspected.
### revised-delivery — publish and email the corrected packet
depends on: revised-geometry
- [x] revision-push — git -C C:/dev/wopr push origin main exits 0 and gh run list returns [] (no workflow configured).
- [x] revision-email — SES accepted updated PDF and kit to proffitt.jeremy@gmail.com; MessageId recorded below.

## eight-panel-banks — fit eight adjacent RGB panels per long side
depends on: revised-geometry
### sixteen-panel-model — regenerate the same case with longer banks
- [x] longer-bank-proof — draft 03 builder completed and existing eleven-mesh/clearance checks passed before the operator interruption. Eight panels per side confirmed in the regenerated views. Do not reuse exec_command or run-isolated.ps1: the operator reported another foreground window. A hidden child desktop did not prove the tool host stayed hidden.
- [x] longer-bank-pdf — all six draft 03 pages visually inspected; kit contents match current files after file-only ZIP refresh.
### sixteen-panel-delivery — commit and email draft 03
depends on: sixteen-panel-model
- [!] longer-bank-push — needs a process-free delivery path or a full launch chain independently verified to stay hidden. The current launcher is prohibited by the operator's console-visibility rule.
- [x] longer-bank-email — SES accepted draft 03 PDF through process-free SDK signing and HTTPS. Updated ZIP became ready after transmission and was not emailed; it is available locally.

## cad-draft — parametric printable geometry
depends on: none
### model-export — create solids and views
- [x] scad-model — C:/dev/wopr/cad/wopr.scad plus reproducible builder and instructions; generated printable meshes and aligned two-color files.
- [x] geometry-proof — python C:/dev/wopr/cad/build.py verifies watertight meshes and dimensions; exits 0.

## review-delivery — PDF and email
depends on: model-export
### pdf-review — assembled views and dimensioned drawings
- [x] drawing-packet — python C:/dev/wopr/cad/build.py creates C:/dev/wopr/output/pdf/wopr-first-draft.pdf; all rendered pages inspected.
### artifact-delivery — commit, push, email attachments
- [x] repository-delivery — git -C C:/dev/wopr push origin main exits 0; gh run list returned [] (repository has no workflow).
- [x] operator-email — delegated SES send returned MessageId; PDF and model ZIP attached.

## Stop conditions (only these)
- Hidden execution cannot be guaranteed for the entire process chain. Stop process-dependent work; use file-only tools for remaining safe work. Do not test an uncertain launcher on the operator's desktop.
- Missing credentials or delivery recipient that cannot be resolved from existing configuration.
- An unapproved irreversible change or genuine scope expansion.
- Physical fit cannot be verified without actual components; deliver the first draft with that limitation.

## seven-panel-source — revise and email the editable seven-panel model
depends on: sixteen-panel-model
### seven-panel-edit — source change with explicit export limits
- [x] seven-panel-parameters — source read-back confirms panels_per_side=7; arithmetic gives fourteen boards, 840 LEDs, 148.485 mm banks and 160.485 mm retainers. Updated builder labels/assertions and assembly instructions.
- [x] seven-panel-package — file-only ZIP contains four current source/document/check files; saved-byte read-back passes. No stale PDF/STL included.
- [x] seven-panel-render — resolved in draft 05 with the verified launch chain recorded below. Seven-panel PDF and meshes regenerated and checked.
### seven-panel-send — deliver revised source without old exports
- [x] seven-panel-email — SES accepted seven-panel SCAD and source ZIP; MessageId recorded below. No old PDF/STL attached.

## continuous-parts — combine halves and open the verified result
depends on: seven-panel-edit
### unsplit-exports — one shell, one base and one main cup
- [x] continuous-geometry — native builder exits 0; gray-shell, base and cup-main each watertight and one connected solid. No clipping split or splice export remains.
- [x] continuous-pdf — all six draft 05 pages visually inspected; seven panels per side and unsplit parts documented.
- [x] bambu-open — Bambu Studio GUI PID 38956 launched directly with shell-two-color.3mf and five STL files; no shell wrapper.
### continuous-delivery — updated PDF and full print kit
- [~] continuous-email — process-free SES send delegated to /root/email_draft.
- [ ] continuous-push — focused commit and main push, then workflow check, from the private desktop.

## Job policy
- OpenSCAD subprocesses: captured exit code, stderr and a 180-second timeout per export; deterministic failure gets a code correction, at most two corrected retries. No background scheduler.
- Builder is tracked by exec session ID; poll until success or failure. No silent retries.
- Email: delegate tracked by agent ID; require SES MessageId. One transient retry after 5 seconds; ambiguous send timeout is investigated before resending.

## Execution log
- 2026-09-26: Read repository instructions and deployment guide; clean main initially. Confirmed local OpenSCAD, Python PDF/mesh tools, GitHub access, and manufacturer CAD dimensions. No dependency installation needed.
- 2026-09-26: Builder sessions 59785 and 49901 completed with exit 0. User confirmed eight boards; final geometry has four per long side. Seven STL exports passed watertight/winding/positive-volume checks, structural parts passed single-component checks, and 3MF passed ZIP/XML/material-part checks. All six PDF page images inspected at C:/dev/wopr/tmp/pdfs/page-1.png through page-6.png. No clipping or text overlap. Physical fit and slicer toolpaths remain unverified as explicitly stated in the packet.
- 2026-09-26: Final builder session 20668: exit 0, "PASS: all geometry and document checks". Final section and coupon pages visually checked. Trimesh loaded the 3MF with 2 geometries; bounds [[0,0,0],[139.371094,155,158.951843]]. Initial artifact commit a611cc5. gh workflow list returned no configured workflows. Font cache moved into ignored temporary directory; no scratch files staged.
- 2026-09-26: Pushed main at 59d07c7a4bf9a4199fe1b4e0441948a0bb492a9d; git ls-remote confirmed the remote SHA. gh run list --limit 5 --json databaseId,status,conclusion,headSha returned []. git diff --check passed. PDF and ZIP committed bytes match local attachments; ZIP integrity and SCAD source match passed (12 entries).
- 2026-09-26: Agent /root/email_draft sent HTML mail through SES us-east-1 to proffitt.jeremy@gmail.com, with PDF and printable ZIP attached. SES accepted message 010001a0dd695595-c8b70668-057d-437d-bc55-073aa580f00e-000000. Receipt read from C:/dev/wopr/tmp/pdfs/email-receipt.json. This confirms SES acceptance, not inbox delivery.
- 2026-09-26: Draft 02 replaces spaced LED clusters with adjacent 84.72 mm banks, front-loading mounts with rear-loading pockets and blind screws, and closed roofs with removable pen cups. Hidden OpenSCAD build session 36630 exited 0: "PASS: all geometry and document checks". Eleven meshes are watertight; SCAD collision probes passed rear insertion, cup lift, pen well openness, 25.4 mm display clearance and hidden pilot checks. All six regenerated PDF pages visually reviewed. Physical fit and toolpaths remain unverified. No dependencies or cloud resources changed.
- 2026-09-26: Draft 02 artifact commit 0595cdd pushed to main; gh run list returned []. ZIP integrity passed, all 16 entries match the current files. PDF and ZIP bytes match their Git blobs. PDF SHA256 ed135301334bedce4dc7f112057dcc6bedb473ac2ba382b4e548822ca9e5788f; ZIP SHA256 c12c3c66703863ca550d838f943b0a8a9c235dded53ceff8ec2cc14b2c7a158d.
- 2026-09-26: /root/email_draft sent the corrected HTML email and attachments. SES accepted MessageId 010001a0dd7b3bc9-18b919f4-d6de-41d1-bdaf-d1bb042ffe82-000000. Receipt checked at C:/dev/wopr/tmp/pdfs/email-receipt-draft02.json. The email identifies the draft 01 corrections and physical-fit limit. No foreground console was requested; subprocesses use CREATE_NO_WINDOW.
- 2026-09-26: Draft 03 source now specifies eight panels per side, sixteen total, 169.74 mm banks and 181.74 mm retainers. C:/dev/wopr/tmp/pdfs/build-draft03.log contains "PASS: all geometry and document checks". The operator then reported another foreground window and required formal rules. All subsequent edits used file-only tools. Updated C:/Users/Jeremy/.codex/AGENTS.md, C:/dev/dotfiles/rules/portable.md, C:/dev/wopr/agents.md and the CLAUDE.md pointer; read-back verified the saved rules. The previous launch method is retired. These edits and draft 03 remain uncommitted; draft 03 has not been emailed. The ZIP was built before the latest README edits and needs repackaging before delivery.
- 2026-09-26: User requested "email me the latest copy". Reviewed all six draft 03 page images through file-only image tools. Rebuilt ZIP with Node fs/zlib in the existing tool runtime; 16 current files, 976006 bytes, SHA256 beb8173cbaecde845a1e9db61bf17f2a3f28a53f344c2fed979a0aa5915ee8de. Compression round trips and saved-byte read-back passed. No shell or subprocess launched. Agent /root/email_draft established a process-free SES SDK route and received send authorization for the PDF plus updated ZIP.
- 2026-09-26: Read receipt C:/dev/wopr/tmp/pdfs/email-receipt-draft03.json. SES accepted draft 03 PDF to proffitt.jeremy@gmail.com with MessageId 010001a0df7a2093-7a4911f1-633f-45f5-a934-90dc98f6d697-000000. Send used the existing Node runtime, AWS SDK signing and HTTPS; no local process launched. PDF was transmitted before the ZIP-ready message arrived; no duplicate email sent. Acceptance does not confirm inbox delivery.
- 2026-09-26: Draft 04 request changed source to seven panels per side. Downloaded official OpenSCAD WebAssembly files into ignored temporary storage and inspected the runtime before evaluation; all subprocess imports blocked. Evaluation failed because the tool runtime disallows WebAssembly code generation. No native process launched and no renderer workaround was attempted after that denial. Updated SCAD, builder expectations, and README via file-only tools. Source/arithmetic check saved to output/draft04-source-check.json. Packaged output/wopr-seven-panel-source.zip (four entries, 34598 bytes) and standalone output/wopr-seven-panels-per-side.scad. Explicitly excluded draft 03 exports. Send delegated through the established process-free SES route.
- 2026-09-26: SES accepted draft 04 source email to proffitt.jeremy@gmail.com: MessageId 010001a0df8864dc-f060276d-aa62-4f58-a8a2-226d5f57b0cd-000000. Receipt read at tmp/pdfs/email-receipt-draft04-source.json. Attached only the seven-panel SCAD and source ZIP. Email prominently states PDF/STL regeneration and validation remain pending. No local processes were launched.
- 2026-09-26: Verified a new full launch chain without the retired shell/tool wrapper: existing Node runtime -> direct C:/Python314/pythonw.exe (PE subsystem 2; no AllocConsole import in executable or Python DLL) -> CreateDesktop/CreateProcess on WoprBuildPrivate -> child assertion of desktop name before any renderer launch. Only the explicitly requested Bambu Studio GUI runs on the interactive desktop. The old exec_command/PowerShell launcher remains prohibited.
- 2026-09-26: Private build parent PID 15880 exited 0. tmp/pdfs/one-piece-build.log reports "PASS: all geometry and document checks". Gray shell 279.342 x155 x158.952 mm; base279.4 x155 x6; main cup169 x111 x96.952. All seven STLs watertight; each structural mesh one connected component. Mechanical probes passed. All six PDF pages visually reviewed. Obsolete generated split STLs and source-only draft04 package removed after successful replacement; current kit explicitly includes only new exports.
