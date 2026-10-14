# Publication and provider acceptance

`./he build` always produces a new preview artifact outside the source. Its exact path is printed. An existing destination is refused. Old `public/` files are not used, copied, cleaned, or treated as current evidence.

```sh
./he build
./he build --mode publication --destination /tmp/my-restaurant-release
```

Publication mode is a local gate and build, not deployment. It requires client data (`use_examples: false`), approved metadata with source/review dates for relevant records, an actual HTTPS domain, a public contact, reviewed privacy/contact flags, and explicit publication approval. It rejects demo collection states and obvious demo brand copy. It includes canonical/social metadata and a sitemap, omits the operator guide and review bar, and allows crawling. Preview output uses noindex with crawling allowed so crawlers can read it. Neither controls access: keep private previews local or use host access controls.

Review actual facts, image permissions, dietary wording, links, policies, and location access details before approving. A successful gate checks the documented data contract; it cannot establish truth or provider acceptance. Generated Restaurant structured data is limited to approved location pages and never emits invented ratings. Add a raster social image through `params.socialImage`; its use and appearance require review.

## Provider contract

Each action owns a module, location, optional service, state, provider label, HTTPS URL, terms, metadata, and fallback email/phone. Only available actions with an available associated service render a transaction link. A paused pickup service suppresses pickup links without disabling delivery. The integration completes on the provider site; this project does not accept payments or reservations.

For each configured destination, verify the exact location/service, pricing/fees and service boundaries, cancellation/deposit rules, accessible alternative, privacy terms, mobile/keyboard behavior, failure behavior, and a real provider confirmation in an authorized test. Record the check in the action's metadata. A handoff click does not prove completion. No live provider acceptance is inherited from a demo or scaffold receipt.

## Hosting and recovery

`static/_headers` describes headers for compatible hosts; Hugo's local server does not establish deployed behavior. The restrictive CSP supports local scripts/styles/images and external navigation; introducing embedded widgets or intake APIs requires a deliberate host/privacy/CSP review. No backend, D1 database, Turnstile, provider credentials, deployment workflow, or analytics collector is installed by this project.

Use the printed sibling build manifest to associate output with selected data, source hashes, and generated-file hashes. The wrapper compares source hashes before and after a build and refuses a success manifest if they changed. A failed output can remain for diagnosis; choose a new destination for retry and do not use an output without its successful manifest. Keep the prior accepted artifact and hosting rollback route before cutover. Deployment, DNS changes, provider transactions, and external messaging remain owner-controlled actions.

## Structured-hours references

Location metadata includes explicit closures and date-specific overrides. The encoding follows [Google's local-business hours guidance](https://developers.google.com/search/docs/appearance/structured-data/local-business) and [Schema.org special opening hours](https://schema.org/specialOpeningHoursSpecification). The public model retains `24:00` as an end boundary; structured metadata maps a full-day opening to `00:00`–`23:59` and other midnight closes to `00:00`. This is metadata implementation guidance, not confirmation of a Google search appearance. Actual generated metadata still requires the verification and publication review described above.
