# Page templates (engine)

Shared page markup with `{{name}}` placeholders, rendered by `tools/shell.py`.
Single braces (`{privacy}`) are left for the calling builder to `.format()`.
To change markup for one market only, copy the file to `markets/<market>/templates/<same name>`.
Build-time only; not deployed.
