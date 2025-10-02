# starMERGE

A comprehensive Python port of [tailwind-merge](https://github.com/dcastil/tailwind-merge) - intelligently merge Tailwind CSS classes without style conflicts.

## Description

`starmerge` is a utility function to efficiently merge Tailwind CSS classes in Python without style conflicts. This is a complete port of the popular JavaScript library `tailwind-merge`.

```python
from starmerge import merge

merge("px-2 py-1 bg-red hover:bg-dark-red", "p-3 bg-[#B91C1C]")
# → 'hover:bg-dark-red p-3 bg-[#B91C1C]'
```

## Installation

```bash
pip install starmerge
```

## Features

- ✅ Full class merging functionality with conflict resolution
- ✅ Support for Tailwind v4.x syntax
- ✅ Handles arbitrary values, modifiers, and variants
- ✅ Comprehensive test coverage matching the original library
- ✅ Production-ready and battle-tested


## Requirements

- Python 3.11+
- Works with Tailwind CSS v4.x

## Contributing

Contributions are welcome! Feel free to open issues for bugs or unexpected behavior, or submit pull requests with improvements.

## Credits

This is a port of [tailwind-merge](https://github.com/dcastil/tailwind-merge) by Dany Castillo. All credit for the original implementation goes to the original authors.

## License

Licensed under the MIT License. This is a port of [tailwind-merge](https://github.com/dcastil/tailwind-merge) which is also licensed under the MIT License.

## Disclaimer

This is an independent port and is not officially affiliated with or endorsed by the original tailwind-merge project or Tailwind CSS.