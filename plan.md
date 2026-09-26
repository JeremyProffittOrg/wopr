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

## Verified facts
- C:/dev/wopr/deploy.md: delivery through main only. Repository currently has no GitHub workflow.
- C:/Users/Jeremy/tools/openscad-nightly/openscad.com --version: OpenSCAD 2026.09.11.
- Adafruit https://www.adafruit.com/product/3315: V2 2.4-inch TFT touchscreen, nominal 65 x 53 x 9.5 mm.
- Seeed Eagle board from https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip: outline 20.955 x 17.780 mm; 60 LEDs per board.
- Visual reference: https://www.miniatua.com/work/wopr/; proportions are an interpretation, not measured film-prop dimensions.
- Existing C:/dev/adafruit-pannel/scripts/send_case_pdf_mail.py configures jeremy@jeremy.ninja to proffitt.jeremy@gmail.com, reply to proffitt.jeremy@gmail.com, SES us-east-1.

## Assumptions
- Eight Seeed boards total, four per long side, confirmed by user. Centers X=37,79,121,163; Z=101.
- Side text corrected to War Operation Plan Response. One TFT above primary W.O.P.R. logo.
- Overall 279.4 x 155 x 165 mm. Gray structure and flush white material volumes; colored electronics are render-only.
- First-draft mounts use measured PCB envelopes plus clearance; hardware fit and print tolerance require a physical trial.

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
- Missing credentials or delivery recipient that cannot be resolved from existing configuration.
- An unapproved irreversible change or genuine scope expansion.
- Physical fit cannot be verified without actual components; deliver the first draft with that limitation.

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
