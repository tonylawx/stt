# Agent Handoff

- Boundary update: `/Users/tonylaw/Documents/stt` is now responsible for audio/video transcription only. Do not start new RhinoFinance / 美股分析师 content-production work in this repository.
- The current 美股分析师 workflow lives in `/Users/tonylaw/Documents/us-stock-analyst`. Agents asked to write, render, publish, validate, or queue RhinoFinance daily articles must switch there first.
- The analyst repo calls this repo only through `RHF_STT_REPO`, `RHF_STT_BIN`, or `RHF_STT_COMMAND` for transcript generation.
- The blog/distribution/archive boundary lives in `/Users/tonylaw/Documents/blog`; WeChat daily drafts are normally created by that repo's `.github/workflows/wechat.yml` from `wechat-runs/**`.
- Legacy notes below are retained only for migration/debugging old runs. Do not treat `private/scripts/` in this repo as the active content workflow source of truth.

- RhinoFinance daily WeChat articles must use the current approved blue fresh template implemented in `private/scripts/rhino_daily_brief.py`: centered blue SEO line `美股 · 期权 · 资讯 · 观点`, blue `#2763e9` section labels with an adaptive flex blue rule, header ad image, and full-width QR footer card. Do not revive the old gold `#8a6c2a`/`theta.jpg` template.
- RhinoFinance daily writing must explicitly run the `humanizer-zh` pass after the initial Markdown draft and before title/render/publish. The run report must contain `humanizer_zh_applied: true` and a `.pre-humanizer.md` snapshot; do not publish a daily draft that bypasses this pass.
- The fixed daily publish order is: source/check -> initial Markdown -> `humanizer-zh` -> final Markdown -> one run-folder `abstract_cover.png` -> rendered HTML -> `.wechat.html` -> bilingual blog push -> blog repo GitHub Action creates the WeChat draft from `wechat-runs/**` -> X -> reports -> validator.
- Before queueing a WeChat draft, rendered RhinoFinance HTML must be processed through the project-local `html-to-wechat-article` skill/script into a sibling `.wechat.html`; the blog repo Action must receive that `.wechat.html`, not raw `.html` and not blog-cleaned HTML.
- Do not default to direct local `wechat_draft_via_droplet.py` publication for the daily flow. The normal WeChat draft path is the blog repo's `.github/workflows/wechat.yml`, triggered by pushing `wechat-runs/<slug>/` from `publish_to_blog.py`.
- Every daily WeChat draft must use a title-driven abstract cover saved as `abstract_cover.png` in the run folder. If OpenAI image generation is unavailable, the agent must generate one with the available image tool before publishing; do not silently fall back to `workflow_runs/rhino_finance/assets/wechat-cover.jpg` for the final draft.
- The main workflow now fails before publishing if the final cover is not the run-folder `abstract_cover.png`; do not bypass that guard unless Tony explicitly asks for a temporary diagnostic draft.
- Before reporting success, run `./.venv/bin/python private/scripts/validate_rhino_daily_run.py <run_dir>` and fix any failure.
- This checkout is exposed through DevSpace from Tony's Mac. Use the real local path `/Users/tonylaw/Documents/stt`, not `/workspace/stt` or `/opt/tonylaw/stt`.
- Start workflow work by reading `.codex/README.md`, then read the relevant project-local skill under `.codex/skills/`.
- The RhinoFinance daily workflow may depend on ignored local directories such as `private/`, `workflow_state/`, and `workflow_runs/`; inspect the live filesystem instead of relying only on git-tracked files.
- Before running timed or publishing workflows, confirm `pwd`, current date/time, and the active workflow state.
