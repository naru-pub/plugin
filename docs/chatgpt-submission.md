# ChatGPT submission

Publisher: Jihyeok Seo, ji@hyeok.org. Availability: all supported countries.
An existing Naru supporter subscription is required; the plugin does not sell
products, process payments, or require additional purchases. This requirement
is recorded in review.commerce_description, not the public listing description.

The root plugin.json includes five positive and three negative cases under
extensions.com.openai.review.test_cases. Keep these fields in the submission
ZIP; the private package made earlier did not contain review cases.

The recorded demo visually shows site lookup, homepage reading, page creation,
rename, deletion, and a billing limitation response. Full tool arguments and
the other two negative cases have not been independently verified. Finish all
cases on a dedicated supporter-enabled test site before submission. Never put
reviewer credentials in Git or the ZIP; use secure portal fields.

The demo still needs a reviewer-accessible hosted URL. Once verified, set
extensions.com.openai.review.demo_recording_url and rebuild. No recording URL
is currently declared. Keep videos outside the source tree or attach them to
a release rather than committing them.

Verify the four listing URLs, complete developer and domain verification,
deploy the server's latest tool annotations, and rescan MCP tools in the portal.
The privacy-policy automated assessment previously failed without a specific
policy defect; additional review remains available. This repository does not
claim that public submission or approval is complete.

Run python3 scripts/package.py and upload dist/naru-chatgpt-1.1.0.zip as the
next draft. Uploading, submitting for review, and publishing are separate steps.
