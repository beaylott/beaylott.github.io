title: TIL: (almost) auto venv like pyenv-virtualenv in mise
date: 2025-01-12
tags: ["til","mise","python","venv"]
author: "Ben Aylott"
filename: til_misevenv.html
draft: false

# TIL: (almost) auto venv like pyenv-virtualenv in mise

[mise](https://mise.jdx.dev/templates.html#variables) provides some instructions to auto-configure the python venv. This didn't work quite how I was used to with pyenv-virtualenv where the venv would be placed in a separate cache folder in $HOME.

This is actually possible in mise using the below config using [Template Variables](https://mise.jdx.dev/templates.html#variables) as below:

```{.toml title="mise.toml"}
[tools]
python = "3.13"

[env]
_.python.venv = { path = "{{env.HOME}}/.cache/venv{{config_root}}", create = true }
```

I am copying this into each project configuration. This could be setup system wide as well using the global mise.toml file although if planning to check this in to a project repo it would be better to have the project specific config in the repo IMO.
