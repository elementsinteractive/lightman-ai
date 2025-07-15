## v0.19.2 (2025-07-14)

### Tests

- add test checking SD from cli

## v0.19.1 (2025-07-10)

### Fix

- service desk env variables can be empty string

## v0.19.0 (2025-07-10)

### Feat

- --env-file flag

## v0.18.4 (2025-07-10)

### Docs

- readme and cotntributing

## v0.18.3 (2025-07-10)

### Docs

- Readme update

## v0.18.2 (2025-07-09)

### Technical

- clean toml and results

## v0.18.1 (2025-07-09)

### Technical

- inject context as system prompt

## v0.18.0 (2025-07-08)

### Feat

- break: replace --model by --agent

## v0.17.0 (2025-07-04)

### Feat

- break: remove iterations

## v0.16.1 (2025-07-03)

### Technical

- rename 'eval' prompt to 'development'

## v0.16.0 (2025-07-03)

### Feat

- rename

## v0.15.0 (2025-07-03)

### Feat

- ServiceDesk integration

## v0.14.1 (2025-07-02)

### Technical

- Create Dockerfile

## v0.14.0 (2025-06-25)

### Feat

- load prompts from prompt file

## v0.13.0 (2025-06-25)

### Feat

- create prompts in toml file

## v0.12.1 (2025-06-23)

### Technical

- change lgtm model

## v0.12.0 (2025-06-20)

### Feat

- allow config file in eval

## v0.11.0 (2025-06-20)

### Feat

- rename --config and accept different configs per file

## v0.10.2 (2025-06-20)

### Technical

- drop vcr usage

## v0.10.1 (2025-06-19)

### Fix

- let pydantic validate iterations and score

## v0.10.0 (2025-06-18)

### Feat

- read config from file

## v0.9.2 (2025-06-04)

### Technical

- **#38**: refine prompt

## v0.9.1 (2025-06-04)

### Refactor

- Refator eval

## v0.9.0 (2025-06-03)

### Feat

- add 95% confidence interval and F1 score to eval

## v0.8.4 (2025-06-02)

### Technical

- run calls in parallele when possible

## v0.8.3 (2025-06-02)

### Fix

- **deps**: update dependency click to v8.2.1

## v0.8.2 (2025-06-02)

### Fix

- **deps**: update dependency pydantic-ai to ^0.2.0

## v0.8.1 (2025-06-02)

### Technical

- **deps**: update dependency ruff to v0.11.12

## v0.8.0 (2025-05-30)

### Feat

- **#83**: filter out articles in python by its score

## v0.7.7 (2025-05-29)

### Technical

- **#83**: show score and why each article was selected

## v0.7.6 (2025-05-29)

### Refactor

- **#83**: directly return SelectedArticles instead of selecting original Articles

## v0.7.5 (2025-05-29)

### Technical

- **#82**: add the amount of time it takes to run an eval

## v0.7.4 (2025-05-28)

### Technical

- **deps**: update dependency commitizen to v4

## v0.7.3 (2025-05-28)

### Technical

- Improve prompt and do a minor refactor

## v0.7.2 (2025-05-23)

### Fix

- remove breakpoint

## v0.7.1 (2025-05-23)

### Fix

- **#76**: make implementation sync

## v0.7.0 (2025-05-22)

### Feat

- **#76**: Gemini agent

## v0.6.9 (2025-05-22)

### Refactor

- **#76**: move base agent tests to another directory

## v0.6.8 (2025-05-21)

### Technical

- **#76**: Abstract common method from OpenAI Agent to Base Agent

## v0.6.7 (2025-05-21)

### Technical

- **#73**: Allow to run multiple samples

## v0.6.6 (2025-05-20)

### Technical

- refactor template

## v0.6.5 (2025-05-20)

### Technical

- **#72**: Create tooling for the agent to run multiple times

## v0.6.4 (2025-05-20)

### Technical

- **deps**: update dependency ruff to v0.11.10

## v0.6.3 (2025-05-19)

### Technical

- change the way the agent is instantiated

## v0.6.2 (2025-05-19)

### Technical

- switch to gemini for lgtm

## v0.6.1 (2025-05-16)

### Technical

- **#74**: Handle insufficient quota error

## v0.6.0 (2025-05-16)

### Feat

- **#39**: introduce evaluator

### Technical

- **#71**: Use gpt-4.1 model

## v0.5.0 (2025-05-16)

### Feat

- **#39**: introduce evaluator

## v0.4.3 (2025-05-14)

### Technical

- switch back to openai

## v0.4.2 (2025-05-13)

### Technical

- swap openai for gemini

## v0.4.1 (2025-05-13)

### Technical

- run poetry update

## v0.4.0 (2025-05-13)

### Feat

- **#67**: allow to introduce the model through the cli

## v0.3.15 (2025-05-13)

### Refactor

- move OpenAI implementation to its directory

## v0.3.14 (2025-05-09)

### Technical

- **#41**: Articles have now number_of_tokens property

## v0.3.13 (2025-05-09)

### CI

- Add lgtm to the pipeline

## v0.3.12 (2025-05-08)

## v0.3.11 (2025-05-08)

### Fix

- **deps**: update dependency pydantic-ai to ^0.1.0

## v0.3.10 (2025-05-08)

### Technical

- Delay subsequent calls to the model based on model response

## v0.3.9 (2025-05-08)

### Fix

- **deps**: update dependency httpx to ^0.28.0

## v0.3.8 (2025-05-06)

### Technical

- **WBSOAI-62**: Reduce number of tokens

## v0.3.7 (2025-05-02)

### Technical

- **deps**: update dependency pytest-asyncio to ^0.26.0

## v0.3.6 (2025-05-02)

### Technical

- **deps**: update dependency pytest-recording to v0.13.3

## v0.3.5 (2025-05-02)

### Technical

- **deps**: update dependency mkdocs-material to v9.6.12

## v0.3.4 (2025-05-02)

### Technical

- update httpcore to get rid of vulnerability

## v0.3.3 (2025-04-24)

### Technical

- **WBSOAI-40**: Remove xml form prompt

## v0.3.2 (2025-04-24)

### Docs

- **WBSOAI-58**: update readme

## v0.3.1 (2025-04-24)

### Technical

- **WBSOAI-57**: add renovate

## v0.3.0 (2025-04-24)

### Feat

- **WBSOAI-55**: run prompt multiple times and introduce pydantic settings

## v0.2.3 (2025-04-10)

### Technical

- improve prompt and some minor improvements

## v0.2.2 (2025-04-03)

### Technical

- bump to python 3.13

## v0.2.1 (2025-04-03)

### Technical

- change to openai

## v0.2.0 (2025-01-17)

### Feat

- allow apikey to be introduced via envvars + refactor

## v0.1.1 (2024-12-19)

### Technical

- remove unused dependency and gitlab stage

## v0.1.0 (2024-12-19)

### Feat

- first version
