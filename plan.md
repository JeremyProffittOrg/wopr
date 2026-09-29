# WOPR first-draft model

## Locked decisions (user-confirmed; do not revisit)
- 2026-09-27: "create a single filament version and a multi-color version of the body, both 3mf files"
- 2026-09-27: "great the lcd fits perfect." confirms the current LCD fit coupon.
- 2026-09-27: "create a two color / two filament test pannel for the wopr working and open as a 3mf file in bambulabs, for dual color printing"
- 2026-09-27: "open the 3mf test when done"
- 2026-09-27: "okay, the lcd cut out requries adjustmeent, bring the left side in 4.5mm, top 2mm down and the right side 1mm in."
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
- 2026-09-26: "the bottom needs to be inset inside of the body and leave 3mm clearance from the bottom of the base plate to the bottom edge of the body for the scre heads. Also, add a divider horizontally and vertically in cup-tower, and in cup-main, half of that should only be 1.5 inches deep, and have 3 dividers in it, the other half should have a horizontal and veritcal divider in it as well. update these and show me a new pdf"
- 2026-09-26: "create stl's for both" confirms both shallow-left and shallow-right main-cup alternatives.

## Verified facts
- C:/dev/wopr/deploy.md: delivery through main only. Repository currently has no GitHub workflow.
- C:/Users/Jeremy/tools/openscad-nightly/openscad.com --version: OpenSCAD 2026.09.11.
- Adafruit https://www.adafruit.com/product/3315: V2 2.4-inch TFT touchscreen, nominal 65 x 53 x 9.5 mm.
- Seeed Eagle board from https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip: outline 20.955 x 17.780 mm; 60 LEDs per board.
- Visual reference: https://www.miniatua.com/work/wopr/; proportions are an interpretation, not measured film-prop dimensions.
- Existing C:/dev/adafruit-pannel/scripts/send_case_pdf_mail.py configures jeremy@jeremy.ninja to proffitt.jeremy@gmail.com, reply to proffitt.jeremy@gmail.com, SES us-east-1.

## Assumptions
- Current draft 07: fourteen Seeed boards total, seven adjacent boards per side. Shell and inset base remain one piece each. Main cup has shallow-left and shallow-right alternatives, one piece each; tower cup has crossed dividers. The front LCD window is50.1 x39.6 mm with the requested asymmetric edge trims. See lcd-aperture-adjustment and divided-cups-inset-base for verified dimensions.
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
- [x] longer-bank-push — superseded by draft 05 delivery, committed and pushed through the verified private-desktop chain. Retired shell launchers remain prohibited.
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

## two-filament-wording-test — print the production lettering on a small test panel
depends on: front-window-trim
### wording-panel-geometry — reuse production lettering and inlay depth
- [x] lettering-panel — 90 x34 x3 mm gray panel with production font/size, white wording flush at Z2.2..3.0; both meshes watertight and combined volume fills the blank panel.
- [x] native-filament-assignments — native Bambu 3MF round-trip retains one object with gray part on filament1 and white part on filament2. H2D0.4 standard-nozzle profile and Generic PLA match the selected application setup.
- [x] wording-slice-proof — builder-integrated Bambu slice exited0, used both filaments for the object, and reported no outside-area paths. Four top layers contain both colors.
### wording-test-delivery — open the verified editable project
- [x] wording-test-open — final slice-verified project opened alone in Bambu Studio; gray=filament1, white=filament2.
- [x] wording-test-push — c862532 pushed to main; diff checks passed and gh run list returned [] (no workflow).

Scope: wording test modules in cad/wopr.scad, focused cad/build-wording-test.py, README/plan and output/wording-test only. Main enclosure geometry stays unchanged; no print command is sent to the printer. Direct GUI launch is authorized for Bambu Studio; all CAD/slicer/CLI work stays on WoprBuildPrivate. Native export and slicing have 180-second ceilings; deterministic failures require a correction before retry, at most two corrected retries per failing stage.

## lcd-aperture-adjustment — trim the visible opening to the measured screen
depends on: inset-organizer-geometry
### front-window-trim — apply the three requested edge changes
- [x] lcd-front-edges — front view left +4.5 mm, right -1 mm, top -2 mm, bottom fixed. Result50.1 x39.6 mm, X212.7..262.8, Z103.2..142.8. Preserve 2 mm glass inset, rear glass relief, board pocket and screw positions.
- [x] lcd-window-proof — python C:/dev/wopr/cad/build.py on verified private desktop exits0; slice of actual fit-coupon front lip verifies new dimensions and offsets; existing mesh/clearance checks pass.
- [x] lcd-window-delivery — draft07 PDF and parts reviewed; commit1c2f991 pushed to main; Bambu import and diff checks passed; no workflow configured.

Scope: cad/wopr.scad, relevant checks/labels in cad/build.py, cad/README.md, plan.md and derived exports. No change to cups, base, LED layout or rear mounting dimensions. Front aperture is the interpretation of "LCD cut out"; no unnecessary hardware relocation.

## divided-cups-inset-base — recess the removable base and partition storage
depends on: unsplit-exports
### inset-organizer-geometry — meet the new dimensions
- [x] recessed-base — 6 mm plate seated at Z=3..9 inside a shell whose bottom edge is Z=0; 3.3 mm XY inset (3 mm wall plus 0.3 mm clearance). Shift screw bosses to Z=9, remove old head counterbores; overall envelope stays 279.4 x155 x165.
- [x] tower-cross-dividers — 3 mm horizontal and vertical dividers form four deep cells.
- [x] main-cup-alternatives — export shallow-left and shallow-right STLs. A level Z=128 main-cup rim gives exactly 38.1 mm depth above the raised shallow floor; three dividers form four shallow cells, crossed dividers form four 85 mm deep cells. Main cup remains one piece per alternative; print one alternative.
- [x] organizer-proof — python C:/dev/wopr/cad/build.py through the verified private desktop exits 0; mesh ray checks prove compartment depths, CSG probes prove dividers, base seating/head clearance and unchanged electronics clearances.
### organizer-pdf-delivery — show the revised organizer and base section
depends on: inset-organizer-geometry
- [x] organizer-pdf — all eight rendered pages inspected, including both cup variants and the 3 mm base recess section.
- [x] organizer-push — 9a0a321 pushed to main; gh run list returned [] (no workflow configured).

Scope: base seating, cup storage and their derived files only. LED/TFT layout, colors and outer dimensions remain. Files: cad/wopr.scad, cad/build.py, cad/README.md, plan.md and current generated outputs. Proof: existing mesh checks plus targeted physical-depth/clearance probes and visual PDF review. No dependencies or services added.

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
- [x] continuous-email — SES accepted draft 05 PDF and full kit; receipt recorded below.
- [x] continuous-push — e3fd24a pushed to main; workflow check returned [] and worktree clean.

## bambu-import-handoff — fix mixed-suffix GUI import failure
depends on: unsplit-exports
### single-file-import — one geometry-only project containing all parts
- [x] import-reproduction — Bambu GUI reproduced "Please import multiple files with the same suffix." for the six-file mixed .3mf/.stl batch; CLI geometry checks passed, proving the failing boundary is GUI batch handling.
- [x] combined-project — builder creates output/model/wopr-parts.3mf with seven spaced build items, grouped gray/white shell, two retainers and no printer presets.
- [x] import-verification — private GUI probe accepts the standard geometry-only confirmation, sees "wopr-parts - BambuStudio", and reports import_pass=true; parent PID43128 exited 0.
- [x] corrected-open — Bambu Studio PID39996 launched with wopr-parts.3mf as its only file argument.
- [x] import-fix-delivery — dbd93ae pushed; corrected PDF/kit accepted by SES, receipt recorded below.

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
- 2026-09-26: Bambu Studio launched directly as the user-requested GUI (PID38956) with shell-two-color.3mf, base.stl, cup-main.stl, cup-tower.stl, led-retainer.stl and fit-coupon.stl. No slicing or printing was started. Native build plate fit must be checked by the user; full-size shell/base need 279.4 x155 mm plus brim.
- 2026-09-26: SES accepted regenerated draft 05 PDF and complete kit to proffitt.jeremy@gmail.com. MessageId 010001a0dfb18ba6-30511bb8-3578-4878-8181-3422786953b0-000000; receipt read at tmp/pdfs/email-receipt-draft05.json. Email sent entirely through SDK/HTTPS without local processes.
- 2026-09-26: Commit e3fd24a pushed to main. git diff --cached --check passed. Private workflow-check parent PID16428 exited 0; gh run list returned []; git status --short returned no entries. GitHub CLI used existing configuration at C:/Users/Jeremy/AppData/Roaming/GitHub CLI without exposing credentials. No workflow is configured.
- 2026-09-26: Import diagnosis: bambu-studio.exe --info succeeded for each input and the complete original batch. Private GUI reproduction captured "Please import multiple files with the same suffix." Replaced the mixed GUI handoff with one geometry-only 3MF. The builder now verifies seven build items and excludes printer presets. Final private GUI probe (tmp/pdfs/gui-import-probe.py via desktop-launch.py) reported import_pass=true and title "wopr-parts - BambuStudio" after geometry-only confirmation. Opened the verified file on the interactive desktop only through the explicitly authorized Bambu GUI. No console windows used.
- 2026-09-26: Import fix committed/pushed as dbd93ae. git diff --cached --check passed; gh run list returned []. Bambu CLI's generated result.json was identified by timestamp and export fields and removed. SES accepted the corrected PDF and 13-file kit, MessageId 010001a0dfc4d49b-64207c92-1ad0-4fc3-bb38-f2b7e0f7d517-000000; receipt read at tmp/pdfs/email-receipt-import-fix.json.
- 2026-09-26: Operator could not see LCD mounting holes. File-only ray intersections against the actual gray-shell.stl verified all four: centers at X=206.155/265.845, print-coordinate Z=94.251/141.749; bore floors at Y=1 and surrounding seats at Y=4. Thus all four blind holes are present and 3 mm deep (SCAD diameter1.8 mm). No design changes were needed. Rendered output/views/lcd-rear-mounts.png as an angled rear detail with the deep clearance walls cut away so the holes can be seen. Private render parent PID28632 exited 0, manifold NoError.
- 2026-09-26: Draft 06 private build parent PID38048 exited 0 with "PASS: all geometry and document checks". Eight watertight STLs; structural parts each one component. Measured base272.8 x148.4 x6 and 3.00 mm recess. Both main-cup variants measured169 x111 x88, four shallow cells at38.10 mm and four deep cells at85 mm; tower has four nominal97 mm cells. CSG probes verified divider material, cell voids, plate insertion and screw-head clearance; only the intentional zero-volume seating contact at Z=9 is excluded from collision checks. All eight PDF pages visually inspected. Removed superseded cup-main.stl after replacement passed; ZIP14entries match current sources/meshes and contains both alternatives. Physical print/fit remains untested.
- 2026-09-26: Bambu Studio --info output/model/wopr-parts.3mf completed successfully on the private desktop and reported manifold=yes for the imported items. Commit9a0a321 pushed to main. git diff --cached --check passed; gh run list returned []. Removed Bambu's generated root result.json after inspecting its return_code. Delivered PDF contains eight pages, both layout alternatives on page5 and dimensioned base clearance on page6.
- 2026-09-27: LCD revision build parent PID10980 exited0 with "PASS: all geometry and document checks". Section of the exported front lip measured50.10 x39.60 mm, at coupon-local lower corner13.7 x10.2 (global X212.7,Z103.2); this proves the requested left/right/top trims and fixed bottom edge. Preserved glass relief behind the2 mm front lip, rear PCB pocket and screw positions. All eight STLs watertight; existing base/cup/depth/electronics clearance probes pass. All eight updated PDF pages visually reviewed. Physical fit remains untested.
- 2026-09-27: Bambu --info accepted updated wopr-parts.3mf (return_code0). Commit1c2f991 pushed to main; git diff --cached --check passed and gh run list returned []. Kit14entries match current source files and meshes. Removed generated root result.json after checking its successful status.
- 2026-09-27: Wording panel meshes and native filament assignments verified. Bambu CLI capture changed to files to avoid waiting on inherited pipe handles after export. Explicit H2D standard-nozzle counts and a prime-tower location in the common printable area resolved the actual slice failures without disabling checks. Slice parent PID26224 exited0; report confirms filament1 gray7.68 g and filament2 white0.59 g, both used for the object, outside=false, estimated1506 seconds. The slicer logs diagnostics for factory H2D special T commands but reports successful validated export; factory G-code is preserved. Physical printing has not started. Final builder now contains these slice assertions.
- 2026-09-27: Final integrated wording builder parent PID34840 exited0. Geometry, native Bambu round-trip and slice assertions all passed. Layer ranges0..10 use gray; layers11..14 use gray and white. Output/wording-test contains the editable two-filament 3MF, separate material STLs, preview and verification/estimated-usage summary. Final project reopened in Bambu Studio after verification. Printer output was not started; actual spool/AMS mapping remains the operator's choice.
- 2026-09-27: Final Bambu GUI PID19924 opened wopr-two-filament-test.3mf alone. Commitc862532 pushed successfully; gh run list returned[]. Bambu-created runtime data under output/model/%SystemDrive%/ProgramData/Microsoft is excluded from source control and preserved locally; no runtime/identity data was read or committed.

## body-filament-projects — body-only Bambu projects
- [x] body-project-export — python cad/build-body-projects.py exits0; one gray body with recessed lettering and one gray/white body with flush lettering. Preserve current mechanical geometry.
- [x] body-project-delivery — native Bambu round-trip preserves part assignments and geometry; both editable files saved under output/body-projects.

Files: cad/build-body-projects.py, cad/README.md, plan.md, output/body-projects. Use existing checked body meshes and the same factory H2D profiles as the wording test. No base/cup changes, PDF, email, or physical print. Native exports have180-second timeouts, maximum two corrected retries; tracked private-desktop worker logs success and failure.

- 2026-09-27: Body-project builder private parent PID38040 exited0. Both native Bambu round-trips exited0. Single version contains one gray part with recessed lettering; multi-color contains gray1/white2 parts. Packaged meshes are watertight and retain source extents and volume within decimal-coordinate precision (single volume425301.001 versus425300.687 mm3). Both projects are unsliced, H2D0.4 Generic PLA with three walls and automatic supports. No physical print or foreground application launch.

## robot-variants — six-per-side replica and eight-wheel robot
2026-09-28. Depends on: front-window-trim.
Outcome: preserve base design in a six-per-side RGB replica; robot has no pen wells, main removable lid, fixed LCD tower, four upright #3777 motors and eight #3766 wheels, battery/controller space, eight-angle PDF and assembly instructions emailed to proffitt.jeremy@gmail.com.
Non-goals: original geometry changes, physical fabrication, cloud changes.
Files: cad/wopr-variants.scad, cad/build-variants.py, cad/VARIANTS.md, firmware/wopr-robot/wopr-robot.ino, output/variants, output/pdf/wopr-variants.pdf, plan.md.
Locked scope: six modules per side; phone Wi-Fi control through WOPR AP and captive portal. Selected ESP32-DevKitC V4, two DRV8833 drivers and Anker A1259 pack.
Verified facts: original CAD 279.4 x155 x165; motor manufacturer drawing 70 x22.44 x18.6, shaft span36.6; wheels63 x29. Worktree main; preserve modified output/wording-test/wopr-two-filament-test.3mf.
### variant-solids — create and check printable models
- [x] variant-geometry — python cad/build-variants.py exits0 with watertight solids and clearance probes.
### variant-packet — eight views and build guide
- [x] variant-pdf — same build exits0; every rendered PDF page inspected.
### variant-delivery — publish and email
- [x] variant-push — focused git commit/push succeeds; workflow terminal state checked.
- [x] variant-email — SES MessageId recorded for attached PDF.
Runtime: existing Node -> pythonw -> desktop-launch.py -> WoprBuildPrivate child assertion. No exec_command. Track parent PID and log; each CAD export180s max; failed result or traceback halts batch; deterministic failures fixed first; at most two corrected retries per stage. No automatic restart.
Stop conditions remain those above; physical fit/durability explicitly unverified.

## Locked decisions (user-confirmed; do not revisit)
- 2026-09-28: "Six per side". Supersedes six-total assumption above. Both new variants use twelve modules.
- 2026-09-28: "Select parts; phone over Wi-Fi".

## Execution log
- 2026-09-28: variant geometry passed: 17 watertight STL files; all structural parts one component. Wheel/shell/floor/lid/tray/battery interference probe exactly1mm3 sentinel. Replica retainer139.23 x23.78 x2.4 and six-per-side bank127.23 verified. PDF22pages built; visual review improved top/bottom angles and lettering face isolation.
- 2026-09-28: firmware compile through private desktop parent31100 / worker33868 exited0. Arduino CLI compile --fqbn esp32:esp32:esp32 --build-path C:/dev/wopr/tmp/variants/firmware-build C:/dev/wopr/firmware/wopr-robot. Existing core3.3.8; program936987 bytes, global47108 bytes. No hardware flashed. Temporary official portable compiler used; no machine PATH or project dependency changed.

## Locked decisions (user-confirmed; do not revisit)
- 2026-09-28: "the esp32 firmware needs to have an AP called WOPR you connect to". Access-point SSID is exactly WOPR.
- 2026-09-28: "and use dns and that approval page you can pop up when attaching to wifi, to put the controller on it". Add wildcard DNS, DHCP captive-portal advertisement and controller at /portal; preserve manual IP access. Reuse installed core3.3.8 DNSServer example/API; no new runtime dependency.

## Execution log
- 2026-09-28: final captive-portal compile parent29248 / worker9084 exited0: "Sketch uses 960055 bytes (73%) of program storage space. Maximum is 1310720 bytes." and "Global variables use 47252 bytes (14%) of dynamic memory, leaving 280428 bytes for local variables. Maximum is 327680 bytes." Core3.3.8, WOPR SSID, wildcard DNS, DHCP captive-portal advertisement and /portal controller. Hardware popup/driving untested.
- 2026-09-28: full CAD builder parent3856 exited0; all17STLs and interference checks passed, two aligned shell3MFs and standalone default-correct SCADs generated. Eight views for both assembled variants and each unique printed part. Final packet refreshed from verified renders after AP/captive portal steering;22pages visually reviewed. Final archive checks require WOPR, DNSServer, DHCP portal and validZIP.

- 2026-09-28: commit5b4d0b0a8215a6a820ac38cbcd99908262801f45 pushed to main. git diff --cached --check exited0; gh run list --limit3 --json status,conclusion,headSha returned[]. Repository has no workflow. Preserved unrelated modified output/wording-test/wopr-two-filament-test.3mf.
- 2026-09-28: delegated /root/email_variants sent final22-page PDF plus2.2MB kit via SES us-east-1 to proffitt.jeremy@gmail.com. SES MessageId010001a0ea106eb4-3880f089-eaa1-4e93-927a-31dd26474675-000000; receipt output/variants/email-receipt.json read back. Email states physical fit, durability and phone popup/driving remain untested.

## concealed-drive — add two robots with wheels recessed inside the body
Depends on: variant-geometry.
## Locked decisions (user-confirmed; do not revisit)
- 2026-09-28: "keep that variant, but make one with only 4 wheels and 4 motors and the wheels tucked up under the unit".
- 2026-09-28: "and make one more variant with 4 motors, 8 wheels with all the wheels under the unit, but widden the unit to hide all the wheels".
Outcome: preserve existing exports; add155mm-wide four-wheel and210mm-wide eight-wheel robots, four upright motors each, axle18mm above skirt and13.5mm tire projection below. Keep six RGB modules per side, LCD dimensions and WOPR captive-portal firmware.
Non-goals: new electronics, firmware changes, physical fabrication, changing delivered eight-wheel variant.
Files: minimal shared CAD parameter changes in cad/wopr.scad and cad/wopr-variants.scad; cad/wopr-concealed.scad, cad/build-concealed.py, cad/CONCEALED.md, output/concealed, output/pdf/wopr-concealed.pdf, plan.md.
Verified facts: existing #3766 wheel63x29mm and #3777 motor/shaft geometry are retained from earlier checked manufacturer drawings. Existing windowless Node->pythonw->desktop-launch.py->WoprBuildPrivate assertion remains the required launch path.
Assumptions:13.5mm ground clearance is suitable for a low indoor model; no hardware test is available.
### concealed-geometry — printable solids and collision proof
- [x] concealed-solids — python C:/dev/wopr/cad/build-concealed.py exits0; all structural meshes watertight/single component; probes prove wheel/motor/electronics clearance, wheel count and width. Existing eight-wheel shell and lid regression comparison passes.
### concealed-packet — drawings and assembly differences
- [x] concealed-drawings — same builder exits0; eight-angle views and all PDF pages visually reviewed.
### concealed-delivery — commit, push and email
- [x] concealed-push — focused commit/push exits0; workflow terminal state checked.
- [x] concealed-email — SES MessageId for final PDF/kit recorded.
Restart policy: each export180s; watcher checks exit/log for both PASS and traceback/errors; deterministic fixes precede retries; two corrected retries per failing check. Existing stop conditions apply. No scheduling or foreground applications.

- 2026-09-28: Assembly-path review requires removable upper wheel hoods and open shaft slots. Keep lower tubs and reinforced cradles on floor; insert motors with wheels already fitted from above, then screw on hoods and motor clamps. Two M3x12 fasteners per hood. Add wheel top-insertion probes; nominal tire clearance1mm. No new electronics or firmware.

## Execution log
- 2026-09-28: concealed final build parent34148 ran C:/Python314/pythonw.exe C:/dev/wopr/tmp/pdfs/desktop-launch.py C:/dev/wopr/tmp/pdfs/concealed-worker.py and exited0. Worker ran cad/build-concealed.py on WoprBuildPrivate.22 watertight STL exports; each structural mesh one connected component. Four-wheel width155, wide-eight-wheel width210; all wheels inside body;13.5mm tire projection. Motor/shaft/wheel top-insertion and removable hood placement probes passed, excluding intentional zero-area motor shoulder seating at Z42. Previous eight-wheel shell/lid volume, extents and face counts unchanged; every prior deliverable and firmware file byte-for-byte preserved.
- 2026-09-28: final output/pdf/wopr-concealed.pdf has26pages; every rendered page inspected. Both matching print folders, aligned shell3MFs, standalone SCADs, motor-fit coupons, instructions and unchanged WOPR captive-portal firmware are in output/concealed/wopr-concealed-kit.zip; ZIP check passed. Physical fit, driving and durability remain untested.

- 2026-09-28: commit af87dd3c503add324abbf97060e65225b65f7656 pushed to main; git diff --cached --check exited0. gh run list --limit3 --json status,conclusion,headSha returned[] (no workflow). Unrelated modified output/wording-test/wopr-two-filament-test.3mf preserved.
- 2026-09-28: /root/email_concealed sent26-page PDF and print kit via SES to proffitt.jeremy@gmail.com; MessageId010001a0ea282e30-8cabe41e-1953-4d4d-a046-3a4a51c53011-000000. Receipt output/concealed/email-receipt.json read back. Email explicitly states physical fit, driving and durability remain untested.

## full-reinforcement — reinforce every organizer and robot variant
Depends on: concealed-solids.
## Locked decisions (user-confirmed; do not revisit)
- 2026-09-29: "reinfoce the entire model structure on them all 5mm walls, and an even thicker 10mm base for the motor bases, adn reinforce everything!"
Outcome: five reinforced replacements (seven-per-side organizer, six-per-side organizer, exposed eight-wheel robot, tucked four-wheel robot, wide tucked eight-wheel robot). Nominal structural walls/panels5mm; robot chassis and motor bearing feet10mm. Necessary holes/hardware relief remain openings. Load-bearing motor cheeks remain5mm by using open-sided cradles, not shaving walls against wheels.
Non-goals: new electronics or firmware, physical strength certification, overwriting historical exports or user-owned Bambu edits. New reinforced kits are the current print recommendations.
Files: cad/wopr-reinforced.scad, cad/build-reinforced.py, cad/REINFORCED.md, current-kit notices in existing CAD guides, output/reinforced, output/pdf/wopr-reinforced.pdf, plan.md. Reuse existing silhouette/mount positions and document/render workflow.
Verified facts: structural walls are currently3mm, base6mm, tray3mm, caps4mm, hood end walls3mm; motor shaft span36.6mm and paired wheels constrain front/rear cradle walls. Existing Node->pythonw->WoprBuildPrivate launch chain is verified.
Assumptions: nominal5mm applies to structural sections, not empty fastener bores, assembly seams, lettering volumes or hardware openings. Dimensions may grow where necessary for reinforcement and actual hardware clearance; report final envelopes.
### reinforced-solids — build thick sections and verify interfaces
- [x] reinforced-geometry — python C:/dev/wopr/cad/build-reinforced.py exits0: watertight connected structures, measured5mm/10mm sections, component/assembly path probes, correct wheel/module counts.
### reinforced-packet — export and review instructions
- [x] reinforced-drawings — same build exits0, all PDF pages visually reviewed; updated print files and hardware instructions match CAD.
### reinforced-delivery — publish and send the updated packet
- [x] reinforced-push — focused commit/push exits0; workflow terminal state checked.
- [x] reinforced-email — final PDF/kit SES MessageId recorded.
Stop conditions: unavailable credentials/resources; unapproved scope expansion; hidden execution cannot be guaranteed. Physical testing remains explicitly unverified and does not block a CAD draft. Per-export timeout180s; tracebacks/errors as well as PASS are monitored; two corrected retries per failing check; no automatic restart or scheduled automation.

## Execution log
- 2026-09-29: reinforcement covers all five editions; organizer bases also increased to10mm so no existing6mm base was weakened. Wide tucked body increased to220mm; exposed platform196mm. Hidden motor flanges leave6.5mm ground clearance; exposed motor feet7.1mm. Retain hardware/module counts and unchanged WOPR firmware.
- 2026-09-29: final CAD export/clearance phase via reinforced-worker.py on WoprBuildPrivate produced47 watertight STL meshes; each structural part is one component. Thickness-validation continuation (parent29728) measured exported5mm shell/LCD/letter backing/cup/lid/tray/cap/hood sections and10mm base/foot/flange sections; foot/flange overlap exceeds10mm where joined. All five assembly and sampled installation-path probes passed.
- 2026-09-29: reinforced-final-packet.py parent44204 / worker44012 exited0. All38 PDF pages visually reviewed; five aligned two-color3MF projects and47 STL archive entries validated. Final output/pdf/wopr-reinforced.pdf and output/reinforced/wopr-reinforced-kit.zip contain current matching parts and updated assembly/screw guidance. Historical guides now point to reinforced kits. Physical fit, load, drop, torque and driving remain untested.

- 2026-09-29: commit d80eaeede3af0e1519453574ff8baa690669d6ab pushed to main. git diff --cached --check exited0; gh run list --limit3 --json status,conclusion,headSha returned[] (no workflow). Unrelated output/wording-test/wopr-two-filament-test.3mf remains untouched and modified.
- 2026-09-29: /root/email_reinforced sent the38-page PDF and an immutable GitHub print-kit download link to proffitt.jeremy@gmail.com. SES MessageId010001a0ec9004df-56f2aab8-15a9-496b-b71d-17ae961afc9e-000000; output/reinforced/email-receipt.json read back. PDF-only attachment avoids combined MIME size exceeding the legacy raw-email limit. Physical testing limitations and matching-parts requirement were included.

## unified-chassis — fuse motor mounts and wheel wells into each robot chassis
## Locked decisions (user-confirmed; do not revisit)
- 2026-09-29: "that's not going to wsork, the motor mount and the wheel wells needs to be a sikngle piece".
- 2026-09-29: "One piece with the whole chassis".
Outcome: one continuous structural chassis for all three robot editions, integrating four motor mounts and all wheel wells. Only motor-retaining caps remain removable. Preserve5mm walls and10mm bases, existing motors/wheels, electronics and firmware.
Files: cad/wopr-reinforced.scad, cad/build-reinforced.py, cad/REINFORCED.md, native Bambu project builder/exports, output/reinforced and PDF, plan.md. Organizer geometry and user-owned Bambu edits are non-goals.
Assembly approach: bare motors insert from above; wheels insert from below at an axial service offset, then slide onto their shafts. Wheel wells include the real installation sweep, not only running clearance. Case reliefs accept the integrated housings; tucked tires remain inside the body outline.
### unified-solids — one solid and practical installation
- [x] unified-geometry — reinforced builder passes single-component chassis,5mm/10mm thickness, motor/wheel insertion sweeps, electronics and case clearance.
### unified-delivery — correct native Bambu projects and guide
- [x] unified-projects — Bambu native import/export roundtrip passes; projects contain one chassis and no loose motor-mount/wheel-well parts; open all four eight-wheel/retention choices in separate windows.
- [x] unified-packet — updated PDF pages reviewed and kit verified.
- [x] unified-push — scoped commit/push passes; workflow terminal state checked.
- [x] unified-email — SES receipt for updated PDF recorded.
Process policy: verified Node->pythonw->WoprBuildPrivate chain; direct Bambu GUI only as authorized by current session. Per-export180s timeout; failures and success monitored; deterministic fixes before retries, two corrected retries per failing check. No print command. Previous stop conditions apply.

- 2026-09-29 (locked user decision): "open in bambu labs wqhen done, and make a second version of the base that allows me to use zip ties to secure the motors". Create screw-cap and zip-tie editions of the integrated chassis for all three robots; open both retention choices of both eight-wheel models in Bambu Studio. Zip-tie slots are1.8mm x4.6mm through reinforced motor posts at two motor-can heights, leaving5.4mm or more vertical webs. Use two3.6mm ties per motor; physical retention remains untested.

## Execution log
- 2026-09-29: reinforced geometry and section checks passed for43 STL exports. All six robot chassis are watertight single solids. Motor/wheel insertion sweeps, wheel-well roofs/end walls5mm, motor feet/base10mm and zip-slot web5.4mm passed. Exposed chassis width209mm; tucked widths155/220mm; motor feet ground clearance7.1mm. Organizers retain identical geometry.
- 2026-09-29: cad/build-eight-wheel-projects.py via WoprBuildPrivate exited0: all four native Bambu import/export roundtrips passed, cap projects10 objects and zip projects6, unsliced. Native --info printed mesh details but failed to exit; native export roundtrip now proves a complete successful load/save. GUI windows verified for exposed cap PID536, exposed zip PID46908, wide cap PID35836, wide zip PID11524. Earlier open projects preserved.
- 2026-09-29: updated37-page PDF fully visually reviewed; eight angles per unique printed part, integrated chassis and zip alternatives included. ZIP integrity passed. Physical fit, zip retention, durability and driving remain untested.

- 2026-09-29: commit ddb40c461e3c87d01970e97fd5c9f20f7bc5dfed pushed to main. git diff --cached --check exited0; gh run list --limit3 --json status,conclusion,headSha returned[] (no workflow). Existing modified wording-test3MF, old untracked Bambu projects and root result.json preserved.

- 2026-09-29: /root/email_reinforced sent updated37-page PDF and immutable kit/native-project links to proffitt.jeremy@gmail.com. SES MessageId010001a0ed2d3c6c-b275de76-c090-4aba-b605-0d42a0732cbd-000000; receipt read back. Parent48676 exited0 on verified private desktop.

## external-tie-routing — wrap ties around the motor
- 2026-09-29 locked correction: "The zip tie loops are in the wrong place, they need to enc asuplate the motor, now they would go through the motor which doesn't work".
Outcome: front-to-back channels through the two side supports; full loops surround motor and supports. Widen zip-only cheeks to12.7mm, leaving5mm outside and5.9mm inside the1.8mm tunnel. Keep5.4mm vertical webs,10mm base, two ties per motor. Use1mm rubber pads on motor front/rear for preload.
Non-goals: screw-cap geometry, motor locations, firmware, new hardware types.
Files: reinforced CAD/builder/guide, three zip chassis exports, affected drawings/PDF/kit, two zip Bambu projects, plan and delivery receipt.
Proof: r-check-zip includes complete belt/lock-head versus actual motor and chassis intersections; exported connected meshes and tunnel wall sections; native Bambu import/export roundtrip. Prior slot-only check did not prove a feasible tie loop.
- [x] external-tie-geometry — clearance and thickness probes pass for all three robots.
- [x] external-tie-delivery — update guide/kit, open corrected zip projects, commit/push and send corrected PDF.
Use verified private-desktop launch chain only. Per-command180s; at most two corrected retries. Existing stop conditions apply.

## Execution log
- 2026-09-29: corrected front-to-back tie tunnels pass r-check-zip for exposed/four/wide, including complete3.6x1.2mm external bands and6x6x5mm lock heads against actual motors, chassis, wheels and enclosure. Each chassis is a watertight connected solid. Measured tunnel side walls5.0/5.9mm and vertical web5.4mm. Standard frame meshes match prior vertices/bounds/volume.
- 2026-09-29: regression probe restoring old cross-motor slots is rejected by the full-loop check, with1465.344mm3 interference. Correction supersedes the earlier empty-slot-only clearance claim.
- 2026-09-29: corrected zip native Bambu import/export roundtrips exited0, six objects each. Opened corrected exposed PID11052 and wide PID33548; exact project titles verified. Updated38-page PDF includes eight-angle loop routing page34; changed chassis views and reflowed instructions visually reviewed. ZIP integrity and corrected STL byte equality passed.

- 2026-09-29: correction commit1cbc59adcdeaba11c0f9cb318f3d3975c3f627ba pushed to main; git diff --cached --check exited0 and gh run list --limit3 --json status,conclusion,headSha returned[]. Unrelated wording-test change and old untracked files preserved.

- 2026-09-29: /root/email_reinforced sent corrected38-page PDF plus immutable kit/Bambu links, explicitly correcting the old slot-only check claim. SES MessageId010001a0ed527b74-2cafc993-7079-4927-b373-250d14825b53-000000; receipt read back; parent17112 exited0 on WoprBuildPrivate.

## slim-pillars-top-tie — clamp the seated motor with three ties
Locked decisions2026-09-29: "Better, but the pillars the zip ties go in need to be skinner so the zip ties connect better, and there should be a cap between the pillars so the motor stops when in place"; corrected by "nevermind, the motirs top at the bottom, they insert fromt he top"; then "that means we need a zip tie over the top of the motor too". No added cap.
Outcome: zip-only upper supports10mm deep instead23mm,11.8mm wide instead12.7mm; tie paths turn inward to motor faces. Third2.5mm-wide tie (<=1mm thick) passes over motor and under existing10mm foot, offset6mm from shaft centerline. Existing two side ties remain3.6mm (<=1.2mm thick).
Non-goals: screw-cap geometry, motor/shaft/wheel locations, firmware. Files: reinforced CAD/checks/guide, zip exports/views/PDF/kit and zip Bambu projects.
- [x] slim-pillars-proof — all three chassis pass motor insertion, complete three-tie clearance,5mm tunnel walls and10mm foot; screw frames unchanged.
- [x] slim-pillars-delivery — drawings reviewed, corrected zip projects opened, commit/push and updated email receipt.
Verified private-desktop launch chain, per-command180s, two corrected retries per failing check; existing stop conditions apply.

## tray-shelves-lighting — tie mounts and lighting provisions
Locked2026-09-29: "the rtray should be zip tied in place as well, adn there should be a  platform over each of the center wheel wells that matches to the height of the r-tray when attched, and it should have zip tie loops on it so we can zip tie in batterey packs"; "And on the bottom and in the wheel wells, add 5mm led holes so we can add some led's , 4 between the wheels, two in each wheel well, 8 under the r-tray on the bottom in a grid".
All robot chassis receive tray tie tunnels, bottom LED holes and wheel-well LED holes. Both eight-wheel robots receive two shelves over their shared inner wheel cavities; shelf and tray surfaces Z72.3mm. Four-wheel robot has no inner wheel cavity. Shelf tie slots accommodate3.6mm ties; useful pack envelopes54x62x40mm exposed,54x75x40mm wide. Existing central battery bay gets8mm rails for LED lead clearance.
Pending optional LED-count clarification defaults to two per actual cavity:12 wheel-well LEDs on eight-wheel robots,8 on four-wheel, plus4 between wheels and8 in a4x2 bottom grid.5mm bores; reinforced wheel-roof bosses seat lenses recessed from tire clearance.
- [x] tray-shelves-proof — tray ties, pack envelopes and LED wiring clearances pass alongside motor/wheel checks.
- [x] tray-shelves-delivery — refresh all affected exports/drawings/projects, verify and publish.

- 2026-09-29 locked LED answer: "Two per wheel: 16 wheel-well LEDs". Eight-wheel count28 total:16 wheel-well +4 between +8 below tray. Four-wheel count20 total:8 wheel-well +4 between +8 below tray.

## perimeter-sensors — eight internal Adafruit3967 mounts
Locked2026-09-29: "add mounts for https://www.adafruit.com/product/3967 (4 hole on the inside, hole in center for sensor), two on the front, two on the back, two on each side.  On the front and back, centered below the sensor, add 8mm led holes as well."
Verified from Adafruit-VL53L1X-PCB/main/Adafruit VL53L1X.brd: PCB25.4x17.78; holes(2.54,2.54),(22.86,2.54),(2.54,15.24),(22.86,15.24),2.5mm drill; sensor centered(12.7,8.89). Source https://github.com/adafruit/Adafruit-VL53L1X-PCB . Mount pitch20.32x12.70, four blind M2 pilots1.6mm each, sensor aperture10mm. Four8mm LED holes20mm below end-face sensors.
Front=low X end, rear=tower X end. End sensors Y40/W-40,Z64; side sensors X85/170,Z64. Connector routing and board space checked. Mechanical mounts only; firmware does not yet read these sensors.
- [x] sensor-proof — all eight PCB/connector spaces clear and holes/pilots verified.
- [x] sensor-delivery — exported cases, drawings, guide and Bambu projects updated.
- 2026-09-29 locked skirt request: "The side of the woper case should go all the way down, the wheel cut outs should not been seen from the side". Tucked models will get continuous side walls and inset chassis; optional scope question for exposed version pending.

- 2026-09-29 locked skirt scope: "Also widen the exposed version". Both eight-wheel bodies220mm wide; four-wheel155mm. Motor centers59.3mm from each side, outer wheel-well faces5.3mm inset. Preserve5mm unbroken side skins; internal ledge relief only. Base width now W-10.6mm. Eight-wheel shelf depth66.4mm, verified pack envelope54x62.4x40mm. Low-axle model retains its lower axle height.

- 2026-09-29: continuous skirts require inset wheel wells. Rotate the existing104x52.3x26mm central USB pack90degrees so it clears the four-wheel housings; retain8mm risers for LED leads. Replace tall center strap anchors with four base slots10.6x2.4mm, two strap rows atX125/154, endsYcenter+/-54; no change to selected battery or firmware.

## Execution log
- 2026-09-29: OpenSCAD r-check and r-check-zip pass for all three final robot editions.43 exported STL meshes pass watertight/positive-volume checks; structural parts are single solids. Existing thickness checks pass, including5mm continuous lower side skins,5mm tie-tunnel walls,10mm motor feet/base and72.3mm level shelf/tray surfaces. Motor/wheel insertion, all three motor ties, tray ties, shelf pack volumes, sensor/connector spaces and LED lead clearances pass.
- 2026-09-29: exported subtractive-solid counts verified independently:28 five-mm bores on both eight-wheel models;20 on four-wheel;44 sensor/end-face bores per robot (32 blind mounting pilots,8 optical ports,4 eight-mm LED holes). Final paired shelf supports overlap instead of touching; robot base edge overlaps the well ends by0.1mm. Frame widths209.6/144.6mm. Organizer frames match prior exported vertices/bounds/volume at STL precision.
- 2026-09-29: cad/build-eight-wheel-projects.py passed native import/export roundtrip for all four projects,10 cap objects or6 zip objects. Four new GUI windows verified:50036 exposed-cap,25624 exposed-zip,37864 wide-cap,50028 wide-zip. All39 PDF pages visually checked; final text reflow removes single-line paragraph tails. ZIP integrity and current exported STL byte matching pass.

- 2026-09-29: committed5867ea70df1af8e40677681150ca35e2de0772aa and pushed main. git diff --cached --check exited0. gh run list --limit3 --json status,conclusion,headSha returned[] (no workflow). Final39-page PDF and archive reviewed; unrelated wording-test edit, old untracked Bambu projects and root result.json preserved.

- 2026-09-29: /root/email_reinforced sent final39-page PDF and immutable kit/native Bambu links. SES MessageId010001a0ed86b805-4222f804-95e8-425a-91dc-409c74927655-000000; receipt read back. Parent36576 exited0 on WoprBuildPrivate. Message states mechanical-only additions for sensors/LEDs and physical fit/retention/driving/durability untested.

- 2026-09-29 correction: final hardware-pair audit identified0.2mm overlap of unused inner shaft tips in the155mm four-wheel layout. Four-wheel body widened to158mm, giving2.8mm shaft-tip gap and preserving5mm skins. Added hardware-pair intersection and >37.2mm insertion-envelope separation assertions. The earlier39-page delivery email stated155mm; a corrected packet and explicit email correction will supersede it. Eight-wheel bodies remain220mm.

- 2026-09-29: corrected four-wheel export passes both retention assembly checks,20 five-mm bores,44 sensor/end-face bores, motor-pair intersections and shaft insertion spacing. Updated STL bounds279.4x158mm case;147.6mm chassis. Eight-wheel hardware-pair checks also pass. All affected drawings and39-page PDF reviewed again; ZIP current-STL equality passes.
- [x] shaft-gap-correction-email — send corrected39-page packet and explicitly supersede155mm four-wheel width.

- 2026-09-29: central battery strap rows set toX121/157, between the bottom LED columns. Added complete10mm strap-envelope checks against chassis, battery, tray, shell and bottom LED lens volumes so the straps cannot cover the LEDs. End slots remain10.6x2.4mm.

- 2026-09-29: all three complete10mm central-strap envelopes pass against the base, battery, shell, tray and bottom LED lens spaces. All six chassis and assembly probes pass again. Updated four native Bambu projects pass import/export roundtrip; final opened PIDs38568/44552/32976/36244.39-page PDF regenerated from matching views.

- 2026-09-29: final artifact commit e1d1900b8beea9096f1813385a6c7a5df49379c4 pushed main. git diff --cached --check exited0; gh run list --limit3 --json status,conclusion,headSha returned[]. Final four-wheel body158mm, eight-wheel bodies220mm. Native four-project verification and current kit ZIP check pass.

- 2026-09-29: corrected final39-page packet sent by /root/email_reinforced; explicitly supersedes155mm four-wheel statement with158mm and2.8mm shaft clearance. SES MessageId010001a0ed926f32-478473aa-9df0-43cf-81d8-b23d3ac13d04-000000; receipt read back; parent53732 exited0 on WoprBuildPrivate.

## solid-battery-blocks — narrow and fill the inner-well battery supports
Locked request2026-09-29: "remove the led holders from the inside wheel wells, add 2 more led's on the sides between the wheels, and bring the platform for the batteries overr the inside wheel wells down so it's a complete block from the wheel wells to the bottom of the platform, solid.  and reduce the width of that platform by 20 percent".
Assumption after optional width question: reduce across-case66.4mm width to53.12mm; keep56mm length and72.3mm top height. Add two LEDs total, one per side, producing six between wheels. Remove inner-wheel LED bosses and bores, retain eight outer-wheel LEDs and eight bottom-grid LEDs:22 five-mm LEDs per robot plus four8mm end LEDs.
Outcome: solid CAD blocks from curved wheel roofs to shelf tops, with horizontal tie tunnels preserving5mm top skins and external wrap clearance. New platform infill regions in native Bambu projects will make these blocks100percent infill.
Non-goals: outer body dimensions, motors/sensors/controller changes, physical printing. Files: reinforced CAD/builders/guide, affected chassis views/PDF/kit/native projects, plan and email receipt.
- [x] solid-block-proof — connected watertight meshes, solid vertical sections,53.12mm width,22 LED bores and assembly/tie clearances pass.
- [x] solid-block-delivery — reviewed drawings, dense platform modifiers verified in Bambu, latest wide zip model opened, commit/push/email.
Same verified private-desktop launch chain. Per-command180s; two corrected retries per failing check; existing stop conditions apply.

- 2026-09-29 user clarification: "the platform oavboce the wheel wells". Applied the20percent reduction to those two platforms across the case (66.4 to53.12mm); their top remains72.3mm.

- Native modifier format verified against BambuStudio src/libslic3r/Model.cpp and PrintConfig.cpp: subtype modifier_part; Rectilinear serializes as zig-zag. Roundtrip must retain both100percent densities and that pattern. Imported source-volume indices and centroids are checked to prevent marking the chassis itself as a modifier.

## Execution log
- 2026-09-29: all six modified chassis pass watertight single-solid checks and r-check/r-check-zip. Exported solid-section samples show uninterrupted material from curved cavity roofs to72.3mm; platform width53.12mm verified. Shelf tie tunnels and full wrap/head envelopes clear all hardware.22 five-mm bores per robot confirmed;44 sensor/end-face bores unchanged. All three outer shell meshes match their previous vertices/bounds/volumes.
- 2026-09-29: all four native Bambu projects pass import/export roundtrip with exactly two aligned modifier_part volumes,100percent infill and native zig-zag(Rectilinear) pattern. One post-export CLI shutdown timed out; a fresh-output retry exited successfully. Print-object counts remain10 cap/6 zip, with one actual chassis mesh. Latest wide zip model opened and title verified atPID47224.

- 2026-09-29: revision1b784febcf8ca2e880e7fb20ff654fd113b33030 committed and pushed main. git diff --cached --check exited0; gh run list --limit3 --json status,conclusion,headSha returned[].39-page PDF visually reviewed, source text includes53.12mm/22 LED holes/100percent block infill. ZIP integrity and all six current chassis byte equality passed. Unrelated user files preserved.

- 2026-09-29: final39-page solid-block packet sent by /root/email_reinforced. SES MessageId010001a0eeb93ebc-a34466e7-d42e-4012-91b2-f68e0480a544-000000; receipt read back; parent9568 exited0 on WoprBuildPrivate.
