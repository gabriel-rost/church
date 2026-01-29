# [1.1.0](https://github.com/gabriel-rost/church/compare/v1.0.0...v1.1.0) (2026-01-29)


### Bug Fixes

* correct redirect parameter in create_post function ([51193f1](https://github.com/gabriel-rost/church/commit/51193f16b3e86f94e0fc5db0a7933529ac5869fb))
* restore DEBUG setting to use environment variable ([5ea4b67](https://github.com/gabriel-rost/church/commit/5ea4b6783d0bbf8118ed10977dd65324e6434b58))
* update home view test to expect 200 status for anonymous users ([bbe07c0](https://github.com/gabriel-rost/church/commit/bbe07c0eb06a5cfbf01bc9d969e3770d4e955655))
* update page title to reflect correct application name ([6dc9d4b](https://github.com/gabriel-rost/church/commit/6dc9d4b6c7ec2385c322b0295e3bc78ba9275db1))
* update post detail template to restrict edit permissions to post owner ([6099680](https://github.com/gabriel-rost/church/commit/609968002eb7043b70e0d86ecb1466455ecf0a9e))


### Features

* Add Bible models and reading plan functionality ([677a1da](https://github.com/gabriel-rost/church/commit/677a1dad62aa0baad4531e6189064ee70b6b0975))
* add Docker build configuration for static file storage ([280d2bf](https://github.com/gabriel-rost/church/commit/280d2bfa13c4f40069d8bbab3b93fd94ea174633))
* add Dockerfile for containerized Django application ([432b2c3](https://github.com/gabriel-rost/church/commit/432b2c399fe145f15d4f6d210f02ee68426e22ff))
* Add likers modal and functionality to display users who liked a post ([4ba244e](https://github.com/gabriel-rost/church/commit/4ba244e5895ee2245975e40df756aeaa00fbabe8))
* add Role model and enhance Channel and ChannelMember models with additional fields ([122f97b](https://github.com/gabriel-rost/church/commit/122f97b23bcb88bc2044dd5d7901d38156fb3f82))
* add search button to navbar ([9f57fbc](https://github.com/gabriel-rost/church/commit/9f57fbc12ef12143861556d9bb36f5d97a8e3b1a))
* Enhance Bible reading functionality with verse range support and search feature ([6929d45](https://github.com/gabriel-rost/church/commit/6929d457ed34a794f361b5eba4ac57928ce5267e))
* enhance channel and post functionalities, add featured post feature, and improve templates ([7fd5ce4](https://github.com/gabriel-rost/church/commit/7fd5ce4e0a97dd28e2ef771380073b3dbb1991c4))
* enhance login and signup forms with icon and password toggle functionality ([0f5f833](https://github.com/gabriel-rost/church/commit/0f5f83328dad64e1b77f63e6f8c22ce7cd72a23a))
* Enhance Open Graph and Twitter meta tags for improved post sharing ([99848e6](https://github.com/gabriel-rost/church/commit/99848e607a44c48bb8585129e242dab1dc832a7b))
* enhance user profile editing functionality with avatar upload and URL fix ([378ab42](https://github.com/gabriel-rost/church/commit/378ab420da0ca735a586ca86acd56970e3a47946))
* ensure post_detail view requires user authentication ([82f7ac3](https://github.com/gabriel-rost/church/commit/82f7ac3b3cde8e488324461085adb0274389af86))
* expose post_detail route to share preview ([0b6dbaa](https://github.com/gabriel-rost/church/commit/0b6dbaab0162307238e75dfbe16668277d37c03e))
* implement advanced search functionality with results page ([42e6bf9](https://github.com/gabriel-rost/church/commit/42e6bf92dbc8662d34487c3830a4993eba06cb69))
* implement channel management features including add, edit, and delete functionalities ([7781c12](https://github.com/gabriel-rost/church/commit/7781c120d449460b06d97dd62f2fd60cd6ab6ffe))
* implement infinite scroll for post listing with AJAX loading ([53f3c55](https://github.com/gabriel-rost/church/commit/53f3c559d9455d728a06feda2d1c7fcc37e7136f))
* Implement like functionality for posts with toggle feature and update UI ([926c286](https://github.com/gabriel-rost/church/commit/926c2860d44c4b4511a7787b3eb958373439c158))
* Implement notification system with web push support and user signup email welcome ([0f346cd](https://github.com/gabriel-rost/church/commit/0f346cd10ed7e7db964d4800399119f9e4d79ab1))
* implement password reset functionality with corresponding templates and routing ([cc9bb15](https://github.com/gabriel-rost/church/commit/cc9bb158d806381c91b5b257f928e544fc67d95f))
* Improve Nginx configuration with enhanced gzip settings and SSL headers ([75edc8e](https://github.com/gabriel-rost/church/commit/75edc8e0e97d8a7dddfbd91f337e60aac0e9be3d))
* improve Open Graph image handling for post attachments ([1dd8158](https://github.com/gabriel-rost/church/commit/1dd81587fdbb5b4bf130ef99337377de6fc2becf))
* improve post list view with channel existence check and permission validation ([c244d60](https://github.com/gabriel-rost/church/commit/c244d6081768c446bae6ff4ac4b5224a2c7149b9))
* refactor channel model to remove Role and update members relationship ([94c5c4c](https://github.com/gabriel-rost/church/commit/94c5c4cf522aa758e198909a18679a050fea5a83))
* Refactor Cloudflare R2 settings for production environment ([2c172a1](https://github.com/gabriel-rost/church/commit/2c172a1e41ef97de1c9ddfd10dcdcf1b3641646a))
* Remove mock AWS credentials from Django CI workflow ([4ebe0f2](https://github.com/gabriel-rost/church/commit/4ebe0f2cea5f821d674fcfa959fc3f9f03c89318))
* update Dockerfile and add docker-compose for improved container management ([20e29af](https://github.com/gabriel-rost/church/commit/20e29af8a8172f1343184cff1981681d5db1c624))
* update post creation logic to include channel visibility check and redirect to post list ([692b588](https://github.com/gabriel-rost/church/commit/692b5888691c8b3f15a0a7582dadd99bc9d908df))
* update requirements.txt to include gunicorn and packaging dependencies ([03d4e95](https://github.com/gabriel-rost/church/commit/03d4e9517c025cdde96d6f6f541933dedc552219))
* Update requirements.txt with additional dependencies for improved functionality ([40a04a8](https://github.com/gabriel-rost/church/commit/40a04a8c3fc268d60be979c9a9f37ea1c14d86a6))
* Update STATIC_URL configuration and add email backend settings for local and production environments ([4e98a79](https://github.com/gabriel-rost/church/commit/4e98a79d2fc14ff8c35b5dac2fe87b09ff813a04))
* update storage backend to use S3Boto3Storage for static files; configure static URL and ACL settings ([f5aa062](https://github.com/gabriel-rost/church/commit/f5aa062bc3777ad126c0cc73c072e6906670d56e))

# 1.0.0 (2025-11-18)


### Bug Fixes

* add CSRF_TRUSTED_ORIGINS configuration from environment variable ([1add629](https://github.com/gabriel-rost/church/commit/1add629c9ad30fadae1628f666ead8a014a5f588))
* restore DEBUG setting and configure ALLOWED_HOSTS from environment ([3629960](https://github.com/gabriel-rost/church/commit/36299606d5c94a7bf3bb4c8e914e2e4c36529a7c))
* settings.py to run correcly the CI Workflow ([ba0c0ee](https://github.com/gabriel-rost/church/commit/ba0c0ee943dd16ffb6b72ece20d5a6924dd52a37))
* update Content model fields to allow blank title and enforce non-blank text; modify __str__ method to return first 50 characters of text ([026304a](https://github.com/gabriel-rost/church/commit/026304a1c3b46b13f5aca75c9bda50a30eebd90a))
* update deployment path to target church_project directory ([5ff4a0c](https://github.com/gabriel-rost/church/commit/5ff4a0c37a9feaff8e9368565b9ac86b96ab721b))


### Features

* add back navigation button to create post template for improved user experience ([dd924e3](https://github.com/gabriel-rost/church/commit/dd924e369b0a66775bf86d1c1223eb80fd0090ba))
* add changelog feature with markdown rendering; implement changelog view and template, and update home page to display latest updates ([e3e2751](https://github.com/gabriel-rost/church/commit/e3e2751baf214008be5610f08def488f604b0e1a))
* add release workflow and semantic release configuration; initialize changelog and version files ([c3c368c](https://github.com/gabriel-rost/church/commit/c3c368c5a7c8eff7556fc6bf87b6991fb69bdb54))
* add user profile editing functionality with forms and templates ([4afe46b](https://github.com/gabriel-rost/church/commit/4afe46bf936e8df48bd1e2aff81ecfd2adce699f))
* enhance comment and post templates with improved styling and functionality; add responsive design elements and user-friendly features ([6d51b52](https://github.com/gabriel-rost/church/commit/6d51b5286db019faa6f8ae83ed8bf1a59cc910b6))
* enhance user interface and experience across templates, improve login and signup forms, and update profile display ([f46e150](https://github.com/gabriel-rost/church/commit/f46e1502729ac20e990ba3de8446247a3d98e676))
* implement user profile, post editing, and comment features; update storage settings ([284d151](https://github.com/gabriel-rost/church/commit/284d151b0e22faef34d163c7b8453fdec90110d5))
