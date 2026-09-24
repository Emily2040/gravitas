# Module 04 - Runtime Verification

## Purpose

This module covers verification for anything with a running or rendered surface: applications, web pages, 3D scenes, charts, generated images and laid-out documents. It is one field's instance of the general rule in `03-domain-checks.md`, which is to find the check that does not route through your own reasoning. For software, that check is running the thing and looking at it.

## Check The Toolset First

Plan verification around the tools that exist in this session, and confirm them before writing the plan.

| Surface | Browser And Runtime Tools |
| :--- | :--- |
| agy CLI | None. A tool listing taken on agy 1.2.9 on 2026-09-24 had `run_command`, `view_file`, `read_url_content`, `search_web`, `generate_image` and the subagent tools, and no browser tools |
| Antigravity desktop app | `open_browser_url`, `capture_browser_screenshot`, `capture_browser_console_logs`, `browser_list_network_requests`, `browser_get_network_request`, `execute_browser_javascript`, `browser_click_element`, `browser_input`, `browser_select_option`, `browser_resize_window`, `read_browser_page`, `browser_subagent`, when browser integration is on |
| Either, with a plugin | Browser control exposed as `mcp_` tools by the Chrome DevTools plugin, when it is installed and enabled |
| Either, always | A Playwright or Puppeteer harness written to a file and run through `run_command` |

A recorded run in the desktop app had no browser tools at all. Its whole toolset was `view_file`, `grep_search`, `list_dir`, `find_by_name`, `run_command`, `replace_file_content`, `write_to_file`, `schedule` and `manage_task`. The agent built a Playwright harness through `run_command` and captured screenshots anyway, which was the right move. The harness was never the problem; what it checked was, and `06-perceptual-gates.md` covers that part.

## Observe First

This is the default for anything with a rendered or running surface. Text review answers whether the code looks correct. The question that matters is whether the thing does the right thing, and that can be looked at directly.

1. Get it running: `restart_dev_server` then `open_browser_url`, or start the server with `run_command` and open it from the harness.
2. Capture the baseline before the change: a screenshot and the console log.
3. Make the change.
4. Capture the same surfaces, at the same viewport, after.
5. Hand both captures to `gravitas-visual-critic`, which has not seen the code and cannot edit anything, and ask it to describe what differs and whether the difference is the intended one.

`view_file` hands an image to the model as an image: on agy 1.2.9 the critic described a test PNG correctly, including a shape that was asked about and was not there. A critic that looks catches a class of defect that code review cannot see: overlapping elements, text clipped by its container, colour that fails contrast, an element rendered off-screen, a layout that collapses at 400 px, a spinner that never resolves, and a control that exists in the DOM and cannot be seen by a person.

Read the console every time. A runtime exception inside a component that rendered correctly is the defect a screenshot-only check misses most often.

## Contract Verification

For any API call, fetch, form submission or request, exercise the path and read the wire instead of reading the client and the handler and reasoning about whether they agree.

- `browser_list_network_requests` shows what fired, in what order and how many times.
- `browser_get_network_request` shows the method, headers, payload, status and response body.
- Without browser tools, a harness can record the same traffic, or `run_command` can call the endpoint directly with `curl`.

This settles what text review can only guess: the double submit, the request that never fires, the field the client sends and the server ignores, the 200 that carries an error body, the retry storm.

## State Exercise

Static review reasons about empty states, error states and loading states, and is frequently wrong about them, because those paths get the least exercise during development. Drive them instead.

- `execute_browser_javascript` forces a state directly.
- `browser_input`, `browser_click_element` and `browser_select_option` walk the real flow.
- `browser_resize_window` tests breakpoints instead of reading media queries.

Capture each state and have the visual critic look at it.

## Target Diff

When a visual specification exists, such as a mock, a design file or a reference implementation, give the visual critic the target and a capture of the implementation and ask for a list of concrete differences in spacing, weight, alignment, colour and proportion. `generate_image` can produce a target where none exists, labelled as generated. This converts "does it look right", which a text agent cannot answer, into a comparison with a list of results.

## Images, Documents And Audio As Evidence

Gemini reads images, PDFs, Office files and audio natively, so treat anything the user supplies as evidence rather than context to acknowledge. A screenshot of a bug is a reproduction. A design mock is a specification to diff against. A photo of a whiteboard is an architecture document. A chart is data. When a user pastes an error screenshot, read the error out of it and act on it; asking them to retype it throws away the anchor.

When a task has a visual anchor, pass the image itself to the critic. Describing an image in words to a model that could have looked at it discards information for no reason.

## Parallel Browser And Code

When work spans implementation and behaviour, one agent observes the running application while implementation proceeds, and the two reconcile at each round through `send_message`. The observer holds ground truth about what the application does; the implementer changes what it should do.

Keep the charters apart. An observer that starts editing code, or an implementer that starts guessing at rendering, has lost the independence that made the split worth having.

## When Observation Is Impossible

Some claims have no runtime surface: architectural judgements, security reasoning about paths that cannot be safely triggered, code that does not run yet. These stay at tiers 3 and 4, and only here is adversarial review of text the right tool.

1. Send the claim to independent refuters, each told to refute it and to default to refuted when uncertain.
2. When a claim could be wrong in several ways, give each verifier a different lens: correctness, security, performance, reproducibility.
3. Require a majority to clear it.
4. Report the survivor as a hypothesis with its tier.

Before accepting that a claim cannot be observed, check whether a cheap harness would make it observable: a scratch script, one test, a single query. Building it is almost always cheaper than a five-agent debate about what the code probably does, and it produces a result rather than a vote.
