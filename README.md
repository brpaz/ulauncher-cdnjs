# Ulauncher cdnjs

> [ulauncher](https://ulauncher.io/) Extension to quickly search frontend libraries on [cndjs](https://cdnjs.com).

## Usage

![demo](demo.gif)

## Requirements

* [ulauncher](https://ulauncher.io/)
* Python >= 2.7

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```https://github.com/brpaz/ulauncher-cdnjs```

## Usage

* Just type ```cdnjs <your searh query>```

Clickling on a result will copy the latest version url to the clipboard, while  "Alt+Enter" will open the respective library page on GitHub

## Development

```
git clone https://github.com/brpaz/ulauncher-cdnjs
cd ~/.cache/ulauncher_cache/extensions/ulauncher-cdnjs
ln -s <repo_location> ulauncher-cdnjs
```

To see your changes, stop ulauncher and run it from the command line with: ```ulauncher -v```.

## License 

MIT
