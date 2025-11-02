const fs = require('fs');

module.exports = {
  branches: ["main"],
  repositoryUrl: "https://github.com/gabriel-rost/church.git",
  plugins: [
    ["@semantic-release/changelog", {
      "changelogFile": "CHANGELOG.md"
    }],

    ["@semantic-release/exec", {
      prepareCmd: `
        VERSION=${nextRelease.version};
        if [ -f VERSION ]; then
          echo $VERSION > VERSION
        fi
        if [ -f pyproject.toml ]; then
          sed -i "s/^version = \\".*\\"/version = \\"$VERSION\\"/" pyproject.toml
        elif [ -f setup.py ]; then
          sed -i "s/version='.*'/version='$VERSION'/" setup.py
        fi
      `
    }],

    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "pyproject.toml", "setup.py", "VERSION"],
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }],

    "@semantic-release/github"
  ]
};