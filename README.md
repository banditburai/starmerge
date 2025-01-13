# tw_merge

A Python port of [tailwind-merge v2.5.4](https://github.com/dcastil/tailwind-merge/tree/v2.5.4)

⚠️ **EXPERIMENTAL STATUS** ⚠️
This is an experimental port of the JavaScript tailwind-merge library to Python. It may not work as expected and should not be used in production for anything except for funsies.

## Description

`tw_merge` is a utility function to efficiently merge Tailwind CSS classes in Python without style conflicts. This is a direct port of the JavaScript library `tailwind-merge` version 2.5.4.

```python
from tw_merge import tw_merge

tw_merge("px-2 py-1 bg-red hover:bg-dark-red", "p-3 bg-[#B91C1C]")
# → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

## Installation

```bash
pip install git+https://github.com/promptsiren/tw-merge.git
```

## Current Status

- ✅ Basic class merging functionality
- ✅ Support for Tailwind v3.x syntax
- ⚠️ Not all edge cases may be handled
- ⚠️ Performance may differ from the JS version

## Future Plans

- This package will likely need a major update when Tailwind v4 is released
- Currently tracking version 2.5.4 of the JS library
- May be completely rewritten

## Requirements

- Python 3.11+
- Works with Tailwind CSS v3.x

## Contributing

This is an experimental project. Feel free to open issues for bugs or unexpected behavior, but be aware that this is not a production-ready library.

## Credits

This is a port of [tailwind-merge](https://github.com/dcastil/tailwind-merge) by Dany Castillo. All credit for the original implementation goes to the original authors.

## License

This is a port of [tailwind-merge](https://github.com/dcastil/tailwind-merge/tree/v2.5.4) which is also licensed under the [MIT License](https://github.com/dcastil/tailwind-merge/blob/v2.5.4/LICENSE.md).

## Disclaimer

This is an unofficial port and is not affiliated with or endorsed by the original tailwind-merge project or Tailwind CSS.