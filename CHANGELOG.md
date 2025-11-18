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
