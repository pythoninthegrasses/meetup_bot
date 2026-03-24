# Changelog

## [1.0.0](https://github.com/pythoninthegrasses/meetup_bot/compare/v1.1.2...v1.0.0) (2026-03-24)


### ⚠ BREAKING CHANGES

* PostgreSQL is no longer supported. SQLite is the sole database provider, configured via DB_PATH env var (default: /data/meetup_bot.db).

### Features

* add e2e test suite with testcontainers for TASK-006 ([8d704ee](https://github.com/pythoninthegrasses/meetup_bot/commit/8d704eefeff083bba95c37aa4b4c0e17f0cb387d))
* add integration test suite with TestClient and pytest markers ([6d08754](https://github.com/pythoninthegrasses/meetup_bot/commit/6d08754eefc6e0bcf4981719ea02dcf5174fe4e6))
* add property-based tests with Hypothesis for TASK-007 ([a1c88d3](https://github.com/pythoninthegrasses/meetup_bot/commit/a1c88d3e48a76c982d107144a16039962907f3bd))
* add pytest taskfile with test categories and server lifecycle ([8470405](https://github.com/pythoninthegrasses/meetup_bot/commit/84704056f9873607f8052622a993f215c84aea03))
* add pytest unit test markers and fix all test failures ([5cb0366](https://github.com/pythoninthegrasses/meetup_bot/commit/5cb0366ca3496b8971ba2cc2f450a47d3718793b))
* add scheduling ([800acda](https://github.com/pythoninthegrasses/meetup_bot/commit/800acda371006760724ca67e6b0a70260b39b0b1))
* Add scheduling functionality ([fa2cd46](https://github.com/pythoninthegrasses/meetup_bot/commit/fa2cd46d1ca05d11625c31ed70b2e4cd629af397))
* add shared db module with SQLite support for local development ([5e4ba37](https://github.com/pythoninthegrasses/meetup_bot/commit/5e4ba373f9d151800a3d073f03c5e5ef10bf68ef))
* **auth:** add PUBLIC_IPS env var and cookie-based session auth ([1c5e71c](https://github.com/pythoninthegrasses/meetup_bot/commit/1c5e71c3bdbc3d7142a03d30f0505ddd41809446))
* migrate from PostgreSQL to SQLite with persistent Docker volume ([c685523](https://github.com/pythoninthegrasses/meetup_bot/commit/c685523aadf5ebe88a1f6921534ed5c1cd316ebd))
* replace Node.js with Deno for JS/TS tooling ([985c65a](https://github.com/pythoninthegrasses/meetup_bot/commit/985c65aee2c8e1b2dbd22d8f56221aa2fdb466c1))


### Bug Fixes

* add `raise ... from err` in except clauses, add B904 rule ([2679341](https://github.com/pythoninthegrasses/meetup_bot/commit/267934146d0185ae856987f980267a4ffcbe5aba))
* add topicCategoryId filter to groupSearch query ([5e02468](https://github.com/pythoninthegrasses/meetup_bot/commit/5e0246878627fae58c611a38f8bc174a42b80533))
* **auth:** increase default token expiration from 30m to 8h ([c83de20](https://github.com/pythoninthegrasses/meetup_bot/commit/c83de20f66a3ade86d70da83e8bd97943734c638))
* **auth:** persist Swagger UI authorization across page refreshes ([8e676a1](https://github.com/pythoninthegrasses/meetup_bot/commit/8e676a1a42930cb60b87d1337d2201e34779ff30))
* bypass auth for local requests when DEV=True ([4f6d1b0](https://github.com/pythoninthegrasses/meetup_bot/commit/4f6d1b009b1fef98133b662791704acd0bb6848e))
* compute time values per-request in check-schedule endpoint ([2d53882](https://github.com/pythoninthegrasses/meetup_bot/commit/2d538822c4dc8e696c74332b1c13958e7543a060))
* docker ([be44104](https://github.com/pythoninthegrasses/meetup_bot/commit/be44104c8caa7197eeb12123873ab64aa7677ef8))
* **e2e:** set DEV=false in e2e server env and migrate to httpx ([378e77b](https://github.com/pythoninthegrasses/meetup_bot/commit/378e77b1b35efc276d77ab0828ca733eccc75556))
* filters ([f9810df](https://github.com/pythoninthegrasses/meetup_bot/commit/f9810df9964bdbc9ac60ca64db36143c4c9c38a7))
* handle duplicate user on startup and respect WEB_CONCURRENCY in gunicorn config ([13f6630](https://github.com/pythoninthegrasses/meetup_bot/commit/13f663044e520392335c5d9b83bfa016b4296b64))
* handle invalid private/public key gracefully in sign_jwt ([2327d5e](https://github.com/pythoninthegrasses/meetup_bot/commit/2327d5e9312eff1cbf8618c85aa567b42d57b1da))
* handle missing DB_USER/DB_PASS with actionable error and fix Dockerfile port ([45d1a37](https://github.com/pythoninthegrasses/meetup_bot/commit/45d1a37c88575da9ce107f1fea32ad97f220c056))
* handle missing events and imprecise date parsing in meetup_query ([b1ffb41](https://github.com/pythoninthegrasses/meetup_bot/commit/b1ffb41bd6097ef8587e56ff95219aa4abb4c294))
* handle missing json file ([9391c1b](https://github.com/pythoninthegrasses/meetup_bot/commit/9391c1b0e0fd2fac723e258c1b7ba474c5d7b61d))
* heroku stats ([79977ab](https://github.com/pythoninthegrasses/meetup_bot/commit/79977ab5549de6d11d888b229fd3b7f0d1b352e0))
* indentation ([3a47e6c](https://github.com/pythoninthegrasses/meetup_bot/commit/3a47e6c245164d085b69cfc9d27081b75a9f308d))
* migrate capture_groups from keywordSearch to groupSearch API ([52cd8a9](https://github.com/pythoninthegrasses/meetup_bot/commit/52cd8a9fcecdb2b63f68e7f459411007f89691cc))
* migrate sign_jwt and scheduler from requests to httpx ([1ba297f](https://github.com/pythoninthegrasses/meetup_bot/commit/1ba297f427992e9e0de82b6747aacd6cb4077611))
* move entities to db.py and use absolute paths for file I/O ([9b15b65](https://github.com/pythoninthegrasses/meetup_bot/commit/9b15b652d4d6f6c2ba8390fb96e7acb02773d0a3))
* override schedule times ([f18718b](https://github.com/pythoninthegrasses/meetup_bot/commit/f18718b62b403fabf7dce0921c9056dd96defba1))
* pandas formatting ([3b48647](https://github.com/pythoninthegrasses/meetup_bot/commit/3b48647ae1fa23598c7ee70d3efdcfe77070050f))
* pandas formatting ([9f7c5ce](https://github.com/pythoninthegrasses/meetup_bot/commit/9f7c5ce6d53f2f09230a078961f2314e83840964))
* pass auth to get_events in post_slack endpoint ([9dbc547](https://github.com/pythoninthegrasses/meetup_bot/commit/9dbc547b9b8f7b3814156175a7f7ca68660920d7))
* poetry package error ([a9a24ac](https://github.com/pythoninthegrasses/meetup_bot/commit/a9a24ac14d7ef2ce86ed517e744ada7128ebc6d1))
* port matches env ([db78324](https://github.com/pythoninthegrasses/meetup_bot/commit/db78324d5f60f5d6e4361523f590b054fe4a42d2))
* print exception error ([96c3c40](https://github.com/pythoninthegrasses/meetup_bot/commit/96c3c404b1268401f2a4bbfc803f32849cc54d98))
* remove buildkit ([bd7ecc1](https://github.com/pythoninthegrasses/meetup_bot/commit/bd7ecc125d188e5bf4fc526f267282dd5492a19d))
* remove deprecated typing.List/Union import, add UP035 rule ([c036732](https://github.com/pythoninthegrasses/meetup_bot/commit/c03673248c2c4a9d446eb6079c8065dfe1a563ad))
* remove hard-coded .env path ([bc05636](https://github.com/pythoninthegrasses/meetup_bot/commit/bc056360e81968c7d086fce4744f807b9093c0e3))
* replace ParserError catch-all with explicit date type handling in sort_json ([ae2bd73](https://github.com/pythoninthegrasses/meetup_bot/commit/ae2bd7314db6e03050a906c29567a02633a9adf0))
* replace passlib with direct bcrypt and migrate to lifespan events ([8071027](https://github.com/pythoninthegrasses/meetup_bot/commit/8071027035975b57e6c5848d5a9df0b9a25d0184))
* set oauth2 auto_error=False so IP whitelist works without token ([d5e2988](https://github.com/pythoninthegrasses/meetup_bot/commit/d5e298897c1f5a32ce48f31d06902a704f05b091))
* update exclusions ([adb7a7d](https://github.com/pythoninthegrasses/meetup_bot/commit/adb7a7d57cfef266f89edc8aa08a4fa6531905fe))
* use /api/slack path in dokploy cron command ([99d0b63](https://github.com/pythoninthegrasses/meetup_bot/commit/99d0b635fcfb7eee5ac6a6c6187e89d3b328e737))
* use ternary for if/else assignments, add SIM108 rule ([353bab1](https://github.com/pythoninthegrasses/meetup_bot/commit/353bab1107e8e99e9bd425914e8bca7d054752f8))
* use WEB_CONCURRENCY env var for gunicorn workers ([394b54b](https://github.com/pythoninthegrasses/meetup_bot/commit/394b54b7beb4698cd3cd38f409c43aa6cf2810d2))
* wrong dockerfile directory ([b77daf5](https://github.com/pythoninthegrasses/meetup_bot/commit/b77daf51d5b1ae3d4fae406b3513ae8a201bce30))


### Performance Improvements

* add BuildKit cache mounts and bump Python to 3.11.13 ([689ae3d](https://github.com/pythoninthegrasses/meetup_bot/commit/689ae3d9ee8e47a3a646178a87932df4354c8928))
* batch GraphQL queries for /api/events endpoint ([b413825](https://github.com/pythoninthegrasses/meetup_bot/commit/b413825e22b459fd510c97f573a840751e89e786))
* bump dockerfile syntax to 1.17.1, replace pip env vars with uv env vars ([fcbc8d5](https://github.com/pythoninthegrasses/meetup_bot/commit/fcbc8d57410c59350b0671f3d7e85c46f08564f9))


### Documentation

* add [@alex-code4okc](https://github.com/alex-code4okc) as a contributor ([7feccfa](https://github.com/pythoninthegrasses/meetup_bot/commit/7feccfa439115616c7fdb760c15043ff3e6d858e))
* add architecture ([450061e](https://github.com/pythoninthegrasses/meetup_bot/commit/450061ecaaa88023d2efae883d815bbd6a68cb17))
* add backlog tasks, add security.md, update agents.md ([dc3d549](https://github.com/pythoninthegrasses/meetup_bot/commit/dc3d5493360474fe98997d929d15a040382ee583))
* complete task-016 and update task-017 status ([1067c4a](https://github.com/pythoninthegrasses/meetup_bot/commit/1067c4adb61696bc62cdb49dc92963359a31972f))
* contributing ([fd2c294](https://github.com/pythoninthegrasses/meetup_bot/commit/fd2c294a018e6943b4b6b66af74b8eaa14db0c0c))
* fix stale references in architecture.md ([35327d0](https://github.com/pythoninthegrasses/meetup_bot/commit/35327d0f48a7b0c99e4cd68231f1af508fa88170))
* **gql:** validate group discovery queries and fix stale templates ([896dfbe](https://github.com/pythoninthegrasses/meetup_bot/commit/896dfbe03662524ad3b1aa2904e7636e3594694a))
* update .env.example ([5918f91](https://github.com/pythoninthegrasses/meetup_bot/commit/5918f9183d46eea3072a01fdabf1bb161ef5a45b))
* update architecture.md for scheduler removal ([f7834e7](https://github.com/pythoninthegrasses/meetup_bot/commit/f7834e7d275ee39afa04971ca187a38e5282be75))
* update backlog tasks ([e538c80](https://github.com/pythoninthegrasses/meetup_bot/commit/e538c80dbf6fbbe11b43d8d26957808eecbdae24))
* update backlog tasks ([d1d980a](https://github.com/pythoninthegrasses/meetup_bot/commit/d1d980ae9111fba6111881fd7f48f2a4f9d0cb88))
* update backlog tasks ([0624d74](https://github.com/pythoninthegrasses/meetup_bot/commit/0624d74cef4b27d32a9885822a1fff2a8ad537e3))
* update backlog tasks ([f269f45](https://github.com/pythoninthegrasses/meetup_bot/commit/f269f4586d68180fdc3e1fe93eb0927bb564b359))
* update readme ([437d81a](https://github.com/pythoninthegrasses/meetup_bot/commit/437d81a528e7e63b98d8f9ab7e1086d2a11023b7))
* update readme ([899cb27](https://github.com/pythoninthegrasses/meetup_bot/commit/899cb279d2ee87acb154edf612e196b6f9b1b541))
* update README.md ([11239c0](https://github.com/pythoninthegrasses/meetup_bot/commit/11239c098f59acc35ed006610fd8b4031520f953))
* update README.md ([e270e5e](https://github.com/pythoninthegrasses/meetup_bot/commit/e270e5e1bcd2f3a9a7f520ac074c7f687063da27))
* update README.md ([9038532](https://github.com/pythoninthegrasses/meetup_bot/commit/903853252fcf1bfa0d28540eed8e1fb45c6ddaa1))
* update README.md ([a752c67](https://github.com/pythoninthegrasses/meetup_bot/commit/a752c673f073d8cf355bf399416d8b4dcda05b4b))
* update README.md ([489ba54](https://github.com/pythoninthegrasses/meetup_bot/commit/489ba540d873ee79863b57e31ab3fa4fa2f1fcca))
* update README.md ([84e891a](https://github.com/pythoninthegrasses/meetup_bot/commit/84e891a468a74532518c95c26190c0f2ade614be))
* update README.md ([c3013b6](https://github.com/pythoninthegrasses/meetup_bot/commit/c3013b6b2a953f5992bba588d17f4f7d7f43ee36))
* update todo ([990793e](https://github.com/pythoninthegrasses/meetup_bot/commit/990793eba772f638b6c2a8189c6990c8170f78af))


### Miscellaneous Chores

* release 1.0.0 ([116b45f](https://github.com/pythoninthegrasses/meetup_bot/commit/116b45f03d246b7ad5cf11f54bb99330311bf1dd))

## [1.1.2](https://github.com/pythoninthegrass/meetup_bot/compare/v1.1.1...v1.1.2) (2025-05-13)


### Documentation

* add [@alex-code4okc](https://github.com/alex-code4okc) as a contributor ([7feccfa](https://github.com/pythoninthegrass/meetup_bot/commit/7feccfa439115616c7fdb760c15043ff3e6d858e))
* contributing ([fd2c294](https://github.com/pythoninthegrass/meetup_bot/commit/fd2c294a018e6943b4b6b66af74b8eaa14db0c0c))
* update readme ([437d81a](https://github.com/pythoninthegrass/meetup_bot/commit/437d81a528e7e63b98d8f9ab7e1086d2a11023b7))

## [1.1.1](https://github.com/pythoninthegrass/meetup_bot/compare/v1.1.0...v1.1.1) (2024-08-26)


### Bug Fixes

* override schedule times ([f18718b](https://github.com/pythoninthegrass/meetup_bot/commit/f18718b62b403fabf7dce0921c9056dd96defba1))

## [1.1.0](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.4...v1.1.0) (2024-08-21)


### Features

* add scheduling ([800acda](https://github.com/pythoninthegrass/meetup_bot/commit/800acda371006760724ca67e6b0a70260b39b0b1))

## [1.0.4](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.3...v1.0.4) (2024-06-26)


### Bug Fixes

* print exception error ([96c3c40](https://github.com/pythoninthegrass/meetup_bot/commit/96c3c404b1268401f2a4bbfc803f32849cc54d98))
* remove buildkit ([bd7ecc1](https://github.com/pythoninthegrass/meetup_bot/commit/bd7ecc125d188e5bf4fc526f267282dd5492a19d))
* remove hard-coded .env path ([bc05636](https://github.com/pythoninthegrass/meetup_bot/commit/bc056360e81968c7d086fce4744f807b9093c0e3))
* wrong dockerfile directory ([b77daf5](https://github.com/pythoninthegrass/meetup_bot/commit/b77daf51d5b1ae3d4fae406b3513ae8a201bce30))


### Documentation

* update readme ([899cb27](https://github.com/pythoninthegrass/meetup_bot/commit/899cb279d2ee87acb154edf612e196b6f9b1b541))

## [1.0.3](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.2...v1.0.3) (2024-03-22)


### Bug Fixes

* heroku stats ([79977ab](https://github.com/pythoninthegrass/meetup_bot/commit/79977ab5549de6d11d888b229fd3b7f0d1b352e0))


### Documentation

* update README.md ([11239c0](https://github.com/pythoninthegrass/meetup_bot/commit/11239c098f59acc35ed006610fd8b4031520f953))
* update README.md ([9038532](https://github.com/pythoninthegrass/meetup_bot/commit/903853252fcf1bfa0d28540eed8e1fb45c6ddaa1))
* update README.md ([a752c67](https://github.com/pythoninthegrass/meetup_bot/commit/a752c673f073d8cf355bf399416d8b4dcda05b4b))

## [1.0.2](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.1...v1.0.2) (2024-02-24)


### Bug Fixes

* docker ([be44104](https://github.com/pythoninthegrass/meetup_bot/commit/be44104c8caa7197eeb12123873ab64aa7677ef8))

## [1.0.1](https://github.com/pythoninthegrass/meetup_bot/compare/v1.0.0...v1.0.1) (2024-02-19)


### Bug Fixes

* poetry package error ([a9a24ac](https://github.com/pythoninthegrass/meetup_bot/commit/a9a24ac14d7ef2ce86ed517e744ada7128ebc6d1))


### Documentation

* update README.md ([489ba54](https://github.com/pythoninthegrass/meetup_bot/commit/489ba540d873ee79863b57e31ab3fa4fa2f1fcca))
* update README.md ([84e891a](https://github.com/pythoninthegrass/meetup_bot/commit/84e891a468a74532518c95c26190c0f2ade614be))

## 1.0.0 (2024-02-19)


### Bug Fixes

* indentation ([3a47e6c](https://github.com/pythoninthegrass/meetup_bot/commit/3a47e6c245164d085b69cfc9d27081b75a9f308d))


### Miscellaneous Chores

* release 1.0.0 ([116b45f](https://github.com/pythoninthegrass/meetup_bot/commit/116b45f03d246b7ad5cf11f54bb99330311bf1dd))
