## v1.2.1 (2026-01-12)

### CI

- use twyn action (#158)

### Technical

- bump actions/cache from 4.3.0 to 5.0.1 (#165)
- bump dependabot/fetch-metadata from 2.4.0 to 2.5.0 (#166)
- bump astral-sh/setup-uv from 7.1.6 to 7.2.0 (#167)
- bump dependencies (#168)
- bump softprops/action-gh-release from 2.4.2 to 2.5.0 (#163)
- bump the patch-updates group with 3 updates (#162)
- bump deps (#164)
- bump actions/checkout from 5.0.0 to 6.0.0 (#161)
- bump actions/create-github-app-token from 2.1.4 to 2.2.0 (#160)
- bump astral-sh/setup-uv from 7.1.2 to 7.1.4 in the patch-updates group (#159)

## v1.2.0 (2025-11-11)

### Docs

- fix supported python version in badge (#156)

### Technical

- update dependencies (#157)
- bump softprops/action-gh-release from 2.4.1 to 2.4.2 in the patch-updates group (#155)

## v1.1.4 (2025-11-06)

### CI

- Do not tag with major version (#154)
- only tag once with latest (#152)

## v1.1.3 (2025-11-06)

### CI

- delete remote major tag (#151)

## v1.1.2 (2025-11-06)

### Technical

- add docker tags (#150)

## v1.1.1 (2025-11-06)

### CI

- fix non valid syntax on GH action (#149)
- Create major version tag (#148)

### Technical

- minor changes (#147)

## v1.1.0 (2025-11-06)

### Feat

- add `-v` option and improve logging (#146)

### Refactor

- update default gemini model and replace deprecated OpenAIModel class usage (#144)

### CI

- use lgtm github action (#145)

## v1.0.3 (2025-10-30)

### CI

- pin python version in ci jobs (#142)
- periodically scan for vulnerabilities (#132)
- adapt to breaking change in lgtm-ai (#129)

### Technical

- Bump dependencies (#143)
- bump astral-sh/setup-uv from 6.8.0 to 7.1.2 (#140)
- bump softprops/action-gh-release from 2.3.4 to 2.4.1 (#138)
- bump softprops/action-gh-release from 2.3.3 to 2.3.4 in the patch-updates group (#135)
- bump astral-sh/setup-uv from 6.7.0 to 6.8.0 (#136)
- bump docker/login-action from 3.5.0 to 3.6.0 (#134)
- bump actions/cache from 4.2.4 to 4.3.0 (#133)
- bump actions/create-github-app-token from 2.1.1 to 2.1.4 in the patch-updates group (#131)
- bump astral-sh/setup-uv from 6.6.1 to 6.7.0 in the minor-updates group (#130)

## v1.0.2 (2025-09-08)

### CI

- preview-version-bump job (#127)
- update actions through dependabot (#117)

### Docs

- add more examples (#124)

### Technical

- includes badges in README.md (#128)
- bump pydantic-ai to v1 (#126)
- bump the patch-updates group with 2 updates (#125)
- add scastlara as author (#123)
- bump dependabot/fetch-metadata from 1.1.1 to 2.4.0 (#121)
- bump actions/create-github-app-token from 1.12.0 to 2.1.1 (#120)
- bump actions/checkout from 4.2.2 to 5.0.0 (#122)
- bump astral-sh/setup-uv in the minor-updates group (#119)
- bump actions/cache from 4.2.3 to 4.2.4 in the patch-updates group (#118)

## v1.0.1 (2025-08-22)

### CI

- Create docker-build action (#116)

## v1.0.0 (2025-08-22)

### Feat

- open source release (#115)

### CI

- Run twyn in our pipelines (#113)

### Technical

- run ensurepip before copying dependency files (#114)

## v0.22.0 (2025-08-01)

### Feat

- provide settings with default values (#111)
- --yesterday flag (#106)

### Fix

- rename breaking to BREAKING CHANGE in conventional-label workflow (#108)

### Docs

- update README.md (#110)

### Tests

- add test for mutually exclusive fields (#107)

## v0.21.2 (2025-07-29)

### Docs

- fix defaults in docs (#105)
- Update readme with sentry and start-date changes (#104)

## v0.21.1 (2025-07-29)

### Fix

- replace time when running with --today (#103)

## v0.21.0 (2025-07-29)

### Feat

- allow to retrieve articles from specific date onwards (#100)

### Refactor

- save publication date of the Articles (#99)

## v0.20.2 (2025-07-28)

### Fix

- remove caching from latest (#97)

## v0.20.1 (2025-07-28)

### CI

- publish package with uv (#96)
- test docker build (#94)
- improve docker cache (#95)
- test build in ci (#93)

## v0.20.0 (2025-07-28)

### Feat

- replace setuptools with hatchling (#92)

## v0.19.0 (2025-07-28)

### Feat

- --version option (#91)

## v0.18.6 (2025-07-28)

### CI

- delete old docker cache entries (#83)

### Technical

- improve docker cache by copying VERSION later

## v0.18.5 (2025-07-24)

### Fix

- push tags (#68)

## v0.18.4 (2025-07-24)

### Fix

- push commits together with tags (#67)
- Allow bump job to push commits (#66)
- fix bump job (#65)

### CI

- udpate package dependency after bump (#64)

## v0.18.2 (2025-07-23)

### Technical

- pin python version with its sha (#62)

## v0.18.1 (2025-07-23)

### CI

- pin commitizen version (#61)

### Technical

- fix justfile (#60)

## v0.18.0 (2025-07-23)

### Feat

- add Sentry integration (#59)

## v0.17.0 (2025-07-23)

### Feat

- allow to introduce any model for supported agents (#54)
- Add more information in SD description (#44)

### Refactor

- remove number_of_tokens (#43)
- format lightman output (#41)

### CI

- pin actions (#55)
- cache mypy to speed up runs (#48)

### Technical

- compile libraries at installation time (#47)
- do not update dependencies when installing venv (#46)
- swap pydantic-ai with pydantic-ai-slim (#45)
- automatically create venv (#42)
- bump pdbpp from 0.11.6 to 0.11.7 in the patch-updates group (#40)

## v0.16.13 (2025-07-21)

### CI

- Build image for arm64 and amd64 architechtures (#39)

## v0.16.12 (2025-07-21)

### CI

- bump osv-scanner version (#38)

### Technical

- migrate from poetry to uv (#37)
- bump the minor-updates group with 5 updates (#35)

## v0.16.11 (2025-07-17)

### CI

- readme change (#34)

## v0.16.10 (2025-07-17)

### CI

- install poetry via pip (#33)

## v0.16.9 (2025-07-17)

### CI

- install poetry via pip (#32)

## v0.16.8 (2025-07-17)

### CI

- readme update to test cache (#31)

## v0.16.7 (2025-07-17)

### CI

- Add description to published pypi package (#30)

## v0.16.6 (2025-07-17)

### CI

- Group poetry steps to improve caching (#29)

## v0.16.5 (2025-07-17)

### CI

- Make release_notes depend on all publish jobs (#28)

## v0.16.4 (2025-07-17)

### CI

- refactor Dockerfile (#27)

## v0.16.3 (2025-07-17)

### CI

- Make push_to_docker_hub not dependant on push_to_pypi (#26)

## v0.16.2 (2025-07-17)

### Fix

- add missing permissions to docker job (#25)

## v0.16.1 (2025-07-17)

### CI

- cache docker build (#24)

## v0.16.0 (2025-07-17)

### Feat

- --env-file flag
- break: replace --model by --agent
- break: remove iterations
- rename
- ServiceDesk integration
- load prompts from prompt file
- create prompts in toml file
- allow config file in eval
- rename --config and accept different configs per file
- read config from file
- add 95% confidence interval and F1 score to eval
- filter out articles in python by its score
- Gemini agent
- introduce evaluator
- introduce evaluator
- allow to introduce the model thorugh the cli
- run prompt multiple times and introduce pydantic settings
- allow apikey to be introduced via envvars + refactor
- first version

### Fix

- service desk env variables can be empty string
- let pydantic validate iterations and score
- update dependency click to v8.2.1
- update dependency pydantic-ai to ^0.2.0
- remove breakpoint
- make implementation sync
- update dependency pydantic-ai to ^0.1.0
- update dependency httpx to ^0.28.0

### Refactor

- Refator eval
- directly return SelectedArticles instead of selecting original Articles
- move base agent tests to another directory
- move OpenAI implementation to its directory

### CI

- Add GitHub workflows (#17)
- Add lgtm to the pipeline

### Docs

- add README.md and update LICENSE

### Technical

- Update dependencies (#23)
- bump the patch-updates group with 2 updates (#18)
- CODEOWNERS (#13)
- clean toml and results
- inject context as system prompt
- rename 'eval' prompt to 'development'
- Create Dockerfile
- change lgtm model
- drop vcr usage
- refine prompt
- run calls in parallele when possible
- update dependency ruff to v0.11.12
- show score and why each article was selected
- add the amount of time it takes to run an eval
- update dependency commitizen to v4
- Improve prompt and do a minor refactor
- Abstract common method from OpenAI Agent to Base Agent
- Allow to run multiple samples
- refactor template
- Create tooling for the agent to run multiple times
- update dependency ruff to v0.11.10
- change the way the agent is instantiated
- switch to gemini for lgtm
- Handle insufficient quota error
- Use gpt-4.1 model
- switch back to openai
- swap openai for gemini
- run poetry update
- Articles have now number_of_tokens property
- Delay subsequent calls to the model based on model response
- Reduce number of tokens
- update dependency pytest-asyncio to ^0.26.0
- update dependency pytest-recording to v0.13.3
- update dependency mkdocs-material to v9.6.12
- update httpcore to get rid of vulnerability
- Remove xml form prompt
- add renovate
- improve prompt and some minor improvements
- bump to python 3.13
- change to openai
- remove unused dependency and gitlab stage

### Tests

- add test checking SD from cli
