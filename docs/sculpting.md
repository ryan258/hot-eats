# Sculpt a restaurant and preserve the library

1. Preview a suitable preset through `./he preview --preset cafe` and inspect `/site-kit/`.
2. Create a new destination with `scripts/sculpt.py`. Keep the source master and its examples available.
3. Use the client's wrapper to apply its profile and preset. Edit `data/restaurant.json`, not `data/scenarios.json`.
4. Replace brand copy, images, menu, narrative records, policies and contact information. Set real location schedules, exceptions, and access facts.
5. Configure only verified provider destinations; retain an alternative contact and actual terms. No checkout, booking, email, or analytics backend is implied.
6. Make everyday edits through `./he today`, `./he menu`, and menu CSV tools. Review the diff or save with `--apply`; use history/restore for recovery.
7. Run `./he check` and `./he test`, then the documented browser checks. A disabled module must be absent from fresh output, navigation, and search.
8. Prepare publication separately through its local validation/build mode. Review the exact artifact, domain, policies, permissions, provider behavior, and hosting configuration before authorizing deployment.

The planner requires either catering or private events. Team content can stand alone. Food-truck homepages use a schedule section and omit a fixed-location visit block. Shared feature flags and homepage order are explicit in presets.

Publication approval never transfers through copying or owner edits. Copy receipts establish where the helper came from, not the truth of restaurant information. Existing destinations and unrelated files are never overwritten by the supported copy/build commands.
