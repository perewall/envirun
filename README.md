## Sublime Envirun

Plugin for Sublime-Text 3, that helps to run any Python command in SublimeREPL inside project-specified environment, which created by `python3 -m venv <dir>` (Python >= 3.3)

**[SublimeREPL](https://packagecontrol.io/packages/SublimeREPL) must be installed for use this plugin!**

### Installation

Download [Package Control](https://packagecontrol.io/) and use the *Package Control: Install Package* command from the command palette. Using Package Control ensures plugin will stay up to date automatically.

### Settings

The default settings can be viewed by accessing the ***Preferences > Package Settings > Envirun > Settings – Default*** menu entry. To ensure settings are not lost when the package is upgraded, make sure all edits are saved to ***Settings – User***.

### Usage

Create file ***.envirun*** (by default, can be changed in settings) in root of your project, this file must contain a valid JSON object with two keys: ***env*** and ***run***

* The ***env*** key must be a *string* with name of environment directory, located in project root
* The ***run*** key must be a *list* with arguments, that be passed to environment's Python interpreter (without *'python'*)

### Example

```json
{
    "env": "venv",
    "run": ["manage.py", "run"]
}
```
