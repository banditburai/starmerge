"""Default configuration for tailwind-merge, converted from TypeScript."""

from typing import Dict, List, Any, Union, Callable, Optional

from starmerge.lib.from_theme import from_theme
from starmerge.lib.types import Config
from starmerge.lib.validators import (
    is_any,
    is_any_non_arbitrary,
    is_arbitrary_image,
    is_arbitrary_length,
    is_arbitrary_number,
    is_arbitrary_position,
    is_arbitrary_shadow,
    is_arbitrary_size,
    is_arbitrary_value,
    is_arbitrary_variable,
    is_arbitrary_variable_family_name,
    is_arbitrary_variable_image,
    is_arbitrary_variable_length,
    is_arbitrary_variable_position,
    is_arbitrary_variable_shadow,
    is_arbitrary_variable_size,
    is_fraction,
    is_integer,
    is_number,
    is_percent,
    is_tshirt_size,
)


def get_default_config(previous_config=None):
    # =========================================================================
    # SECTION 1: Theme Getters
    # =========================================================================
    theme_color = from_theme('color')
    theme_font = from_theme('font')
    theme_text = from_theme('text')
    theme_font_weight = from_theme('font-weight')
    theme_tracking = from_theme('tracking')
    theme_leading = from_theme('leading')
    theme_breakpoint = from_theme('breakpoint')
    theme_container = from_theme('container')
    theme_spacing = from_theme('spacing')
    theme_radius = from_theme('radius')
    theme_shadow = from_theme('shadow')
    theme_inset_shadow = from_theme('inset-shadow')
    theme_drop_shadow = from_theme('drop-shadow')
    theme_blur = from_theme('blur')
    theme_perspective = from_theme('perspective')
    theme_aspect = from_theme('aspect')
    theme_ease = from_theme('ease')
    theme_animate = from_theme('animate')
    
    # =========================================================================
    # SECTION 2: Scale Functions
    # =========================================================================

    def scale_break():
        return ['auto', 'avoid', 'all', 'avoid-page', 'page', 'left', 'right', 'column']

    def scale_position():
        return [
            'bottom',
            'center',
            'left',
            'left-bottom',
            'left-top',
            'right',
            'right-bottom',
            'right-top',
            'top',
        ]
    
    def scale_overflow():
        return ['auto', 'hidden', 'clip', 'visible', 'scroll']
    
    def scale_overscroll():
        return ['auto', 'contain', 'none']
    
    def scale_unambiguous_spacing():
        return [is_arbitrary_variable, is_arbitrary_value, 'px', is_number, theme_spacing]
    
    def scale_inset():
        return [is_fraction, 'full', 'auto', *scale_unambiguous_spacing()]
    
    def scale_grid_template_cols_rows():
        return [is_integer, 'none', 'subgrid', is_arbitrary_variable, is_arbitrary_value]
    
    def scale_grid_col_row_start_and_end():
        return [
            'auto',
            {'span': ['full', is_integer, is_arbitrary_variable, is_arbitrary_value]},
            is_arbitrary_variable,
            is_arbitrary_value,
        ]
    
    def scale_grid_col_row_start_or_end():
        return [is_integer, 'auto', is_arbitrary_variable, is_arbitrary_value]
    
    def scale_grid_auto_cols_rows():
        return ['auto', 'min', 'max', 'fr', is_arbitrary_variable, is_arbitrary_value]
    
    def scale_align_primary_axis():
        return ['start', 'end', 'center', 'between', 'around', 'evenly', 'stretch', 'baseline']
    
    def scale_align_secondary_axis():
        return ['start', 'end', 'center', 'stretch']
    
    def scale_margin():
        return ['auto', *scale_unambiguous_spacing()]
    
    def scale_sizing():
        return [
            is_fraction,
            is_number,
            'auto',
            'full',
            'dvw',
            'dvh',
            'lvw',
            'lvh',
            'svw',
            'svh',
            'min',
            'max',
            'fit',
            *scale_unambiguous_spacing(),
        ]
    
    def scale_color():
        return [theme_color, is_arbitrary_variable, is_arbitrary_value]
    
    def scale_gradient_stop_position():
        return [is_percent, is_arbitrary_length]
    
    def scale_radius():
        return [
            '',
            'none',
            'full',
            theme_radius,
            is_arbitrary_variable,
            is_arbitrary_value,
        ]
    
    def scale_border_width():
        return ['', is_number, is_arbitrary_variable_length, is_arbitrary_length]
    
    def scale_line_style():
        return ['solid', 'dashed', 'dotted', 'double']
    
    def scale_blend_mode():
        return [
            'normal',
            'multiply',
            'screen',
            'overlay',
            'darken',
            'lighten',
            'color-dodge',
            'color-burn',
            'hard-light',
            'soft-light',
            'difference',
            'exclusion',
            'hue',
            'saturation',
            'color',
            'luminosity',
        ]
    
    def scale_blur():
        return [
            '',
            'none',
            theme_blur,
            is_arbitrary_variable,
            is_arbitrary_value,
        ]
    
    def scale_origin():
        return [
            'center',
            'top',
            'top-right',
            'right',
            'bottom-right',
            'bottom',
            'bottom-left',
            'left',
            'top-left',
            is_arbitrary_variable,
            is_arbitrary_value,
        ]
    
    def scale_rotate():
        return ['none', is_number, is_arbitrary_variable, is_arbitrary_value]
    
    def scale_scale():
        return ['none', is_number, is_arbitrary_variable, is_arbitrary_value]
    
    def scale_skew():
        return [is_number, is_arbitrary_variable, is_arbitrary_value]
    
    def scale_translate():
        return [is_fraction, 'full', *scale_unambiguous_spacing()]
    
    # =========================================================================
    # SECTION 3: Return Configuration Object
    # =========================================================================

    return {
        'cache_size': 500,

        'theme': {
            'animate': ['spin', 'ping', 'pulse', 'bounce'],
            'aspect': ['video'],
            'blur': [is_tshirt_size],
            'breakpoint': [is_tshirt_size],
            'color': [is_any],
            'container': [is_tshirt_size],
            'drop-shadow': [is_tshirt_size],
            'ease': ['in', 'out', 'in-out'],
            'font': [is_any_non_arbitrary],
            'font-weight': [
                'thin',
                'extralight',
                'light',
                'normal',
                'medium',
                'semibold',
                'bold',
                'extrabold',
                'black'
            ],
            'inset-shadow': [is_tshirt_size],
            'leading': ['none', 'tight', 'snug', 'normal', 'relaxed', 'loose'],
            'perspective': ['dramatic', 'near', 'normal', 'midrange', 'distant', 'none'],
            'radius': [is_tshirt_size],
            'shadow': ['sm', '', 'md', 'lg', 'xl', '2xl'],
            'spacing': ['px', is_number],
            'text': [is_tshirt_size],
            'tracking': ['tighter', 'tight', 'normal', 'wide', 'wider', 'widest'],
        },

        'class_groups': {
            'aspect': [
                {
                    'aspect': [
                        'auto',
                        'square',
                        is_fraction,
                        is_arbitrary_value,
                        is_arbitrary_variable,
                        theme_aspect,
                    ],
                },
            ],
            'container': ['container'],
            'columns': [
                { 'columns': [is_number, is_arbitrary_value, is_arbitrary_variable, theme_container] },
            ],
            'break-after': [{ 'break-after': scale_break() }],
            'break-before': [{ 'break-before': scale_break() }],
            'break-inside': [{ 'break-inside': ['auto', 'avoid', 'avoid-page', 'avoid-column'] }],
            'box-decoration': [{ 'box-decoration': ['slice', 'clone'] }],
            'box': [{ 'box': ['border', 'content'] }],
            'display': [
                'block',
                'inline-block',
                'inline',
                'flex',
                'inline-flex',
                'table',
                'inline-table',
                'table-caption',
                'table-cell',
                'table-column',
                'table-column-group',
                'table-footer-group',
                'table-header-group',
                'table-row-group',
                'table-row',
                'flow-root',
                'grid',
                'inline-grid',
                'contents',
                'list-item',
                'hidden',
            ],
            'sr': ['sr-only', 'not-sr-only'],
            'float': [{ 'float': ['right', 'left', 'none', 'start', 'end'] }],
            'clear': [{ 'clear': ['left', 'right', 'both', 'none', 'start', 'end'] }],
            'isolation': ['isolate', 'isolation-auto'],
            'object-fit': [{ 'object': ['contain', 'cover', 'fill', 'none', 'scale-down'] }],
            'object-position': [
                { 'object': [*scale_position(), is_arbitrary_value, is_arbitrary_variable] },
            ],
            'overflow': [{ 'overflow': scale_overflow() }],
            'overflow-x': [{ 'overflow-x': scale_overflow() }],
            'overflow-y': [{ 'overflow-y': scale_overflow() }],
            'overscroll': [{ 'overscroll': scale_overscroll() }],
            'overscroll-x': [{ 'overscroll-x': scale_overscroll() }],
            'overscroll-y': [{ 'overscroll-y': scale_overscroll() }],
            'position': ['static', 'fixed', 'absolute', 'relative', 'sticky'],
            'inset': [{ 'inset': scale_inset() }],
            'inset-x': [{ 'inset-x': scale_inset() }],
            'inset-y': [{ 'inset-y': scale_inset() }],
            'start': [{ 'start': scale_inset() }],
            'end': [{ 'end': scale_inset() }],
            'top': [{ 'top': scale_inset() }],
            'right': [{ 'right': scale_inset() }],
            'bottom': [{ 'bottom': scale_inset() }],
            'left': [{ 'left': scale_inset() }],
            'visibility': ['visible', 'invisible', 'collapse'],
            'z': [{ 'z': [is_integer, 'auto', is_arbitrary_variable, is_arbitrary_value] }],
            'basis': [
                {
                    'basis': [
                        is_fraction,
                        'full',
                        'auto',
                        theme_container,
                        *scale_unambiguous_spacing(),
                    ],
                },
            ],
            'flex-direction': [{ 'flex': ['row', 'row-reverse', 'col', 'col-reverse'] }],
            'flex-wrap': [{ 'flex': ['nowrap', 'wrap', 'wrap-reverse'] }],
            'flex': [{ 'flex': [is_number, is_fraction, 'auto', 'initial', 'none', is_arbitrary_value] }],
            'grow': [{ 'grow': ['', is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'shrink': [{ 'shrink': ['', is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'order': [
                {
                    'order': [
                        is_integer,
                        'first',
                        'last',
                        'none',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'grid-cols': [{ 'grid-cols': scale_grid_template_cols_rows() }],
            'col-start-end': [{ 'col': scale_grid_col_row_start_and_end() }],
            'col-start': [{ 'col-start': scale_grid_col_row_start_or_end() }],
            'col-end': [{ 'col-end': scale_grid_col_row_start_or_end() }],
            'grid-rows': [{ 'grid-rows': scale_grid_template_cols_rows() }],
            'row-start-end': [{ 'row': scale_grid_col_row_start_and_end() }],
            'row-start': [{ 'row-start': scale_grid_col_row_start_or_end() }],
            'row-end': [{ 'row-end': scale_grid_col_row_start_or_end() }],
            'grid-flow': [{ 'grid-flow': ['row', 'col', 'dense', 'row-dense', 'col-dense'] }],
            'auto-cols': [{ 'auto-cols': scale_grid_auto_cols_rows() }],
            'auto-rows': [{ 'auto-rows': scale_grid_auto_cols_rows() }],
            'gap': [{ 'gap': scale_unambiguous_spacing() }],
            'gap-x': [{ 'gap-x': scale_unambiguous_spacing() }],
            'gap-y': [{ 'gap-y': scale_unambiguous_spacing() }],
            'justify-content': [{ 'justify': [*scale_align_primary_axis(), 'normal'] }],
            'justify-items': [{ 'justify-items': [*scale_align_secondary_axis(), 'normal'] }],
            'justify-self': [{ 'justify-self': ['auto', *scale_align_secondary_axis()] }],
            'align-content': [{ 'content': ['normal', *scale_align_primary_axis()] }],
            'align-items': [{ 'items': [*scale_align_secondary_axis(), 'baseline'] }],
            'align-self': [{ 'self': ['auto', *scale_align_secondary_axis(), 'baseline'] }],
            'place-content': [{ 'place-content': scale_align_primary_axis() }],
            'place-items': [{ 'place-items': [*scale_align_secondary_axis(), 'baseline'] }],
            'place-self': [{ 'place-self': ['auto', *scale_align_secondary_axis()] }],
            'p': [{ 'p': scale_unambiguous_spacing() }],
            'px': [{ 'px': scale_unambiguous_spacing() }],
            'py': [{ 'py': scale_unambiguous_spacing() }],
            'ps': [{ 'ps': scale_unambiguous_spacing() }],
            'pe': [{ 'pe': scale_unambiguous_spacing() }],
            'pt': [{ 'pt': scale_unambiguous_spacing() }],
            'pr': [{ 'pr': scale_unambiguous_spacing() }],
            'pb': [{ 'pb': scale_unambiguous_spacing() }],
            'pl': [{ 'pl': scale_unambiguous_spacing() }],
            'm': [{ 'm': scale_margin() }],
            'mx': [{ 'mx': scale_margin() }],
            'my': [{ 'my': scale_margin() }],
            'ms': [{ 'ms': scale_margin() }],
            'me': [{ 'me': scale_margin() }],
            'mt': [{ 'mt': scale_margin() }],
            'mr': [{ 'mr': scale_margin() }],
            'mb': [{ 'mb': scale_margin() }],
            'ml': [{ 'ml': scale_margin() }],
            'space-x': [{ 'space-x': scale_unambiguous_spacing() }],
            'space-x-reverse': ['space-x-reverse'],
            'space-y': [{ 'space-y': scale_unambiguous_spacing() }],
            'space-y-reverse': ['space-y-reverse'],
            'size': [{ 'size': scale_sizing() }],
            'w': [{ 'w': [theme_container, 'screen', *scale_sizing()] }],
            'min-w': [
                {
                    'min-w': [
                        theme_container,
                        'screen',
                        'none',
                        *scale_sizing(),
                    ],
                },
            ],
            'max-w': [
                {
                    'max-w': [
                        theme_container,
                        'screen',
                        'none',
                        'prose',
                        { 'screen': [theme_breakpoint] },
                        *scale_sizing(),
                    ],
                },
            ],
            'h': [{ 'h': ['screen', *scale_sizing()] }],
            'min-h': [{ 'min-h': ['screen', 'none', *scale_sizing()] }],
            'max-h': [{ 'max-h': ['screen', *scale_sizing()] }],
            'font-size': [
                { 'text': ['base', theme_text, is_arbitrary_variable_length, is_arbitrary_length] },
            ],
            'font-smoothing': ['antialiased', 'subpixel-antialiased'],
            'font-style': ['italic', 'not-italic'],
            'font-weight': [{ 'font': [theme_font_weight, is_arbitrary_variable, is_arbitrary_number] }],
            'font-stretch': [
                {
                    'font-stretch': [
                        'ultra-condensed',
                        'extra-condensed',
                        'condensed',
                        'semi-condensed',
                        'normal',
                        'semi-expanded',
                        'expanded',
                        'extra-expanded',
                        'ultra-expanded',
                        is_percent,
                        is_arbitrary_value,
                    ],
                },
            ],
            'font-family': [{ 'font': [is_arbitrary_variable_family_name, is_arbitrary_value, theme_font] }],
            'fvn-normal': ['normal-nums'],
            'fvn-ordinal': ['ordinal'],
            'fvn-slashed-zero': ['slashed-zero'],
            'fvn-figure': ['lining-nums', 'oldstyle-nums'],
            'fvn-spacing': ['proportional-nums', 'tabular-nums'],
            'fvn-fraction': ['diagonal-fractions', 'stacked-fractions'],
            'tracking': [{ 'tracking': [theme_tracking, is_arbitrary_variable, is_arbitrary_value] }],
            'line-clamp': [
                { 'line-clamp': [is_number, 'none', is_arbitrary_variable, is_arbitrary_number] },
            ],
            'leading': [
                {
                    'leading': [
                        theme_leading,
                        *scale_unambiguous_spacing(),
                    ],
                },
            ],
            'list-image': [{ 'list-image': ['none', is_arbitrary_variable, is_arbitrary_value] }],
            'list-style-position': [{ 'list': ['inside', 'outside'] }],
            'list-style-type': [
                { 'list': ['disc', 'decimal', 'none', is_arbitrary_variable, is_arbitrary_value] },
            ],
            'text-alignment': [{ 'text': ['left', 'center', 'right', 'justify', 'start', 'end'] }],
            'placeholder-color': [{ 'placeholder': scale_color() }],
            'text-color': [{ 'text': scale_color() }],
            'text-decoration': ['underline', 'overline', 'line-through', 'no-underline'],
            'text-decoration-style': [{ 'decoration': [*scale_line_style(), 'wavy'] }],
            'text-decoration-thickness': [
                {
                    'decoration': [
                        is_number,
                        'from-font',
                        'auto',
                        is_arbitrary_variable,
                        is_arbitrary_length,
                    ],
                },
            ],
            'text-decoration-color': [{ 'decoration': scale_color() }],
            'underline-offset': [
                { 'underline-offset': [is_number, 'auto', is_arbitrary_variable, is_arbitrary_value] },
            ],
            'text-transform': ['uppercase', 'lowercase', 'capitalize', 'normal-case'],
            'text-overflow': ['truncate', 'text-ellipsis', 'text-clip'],
            'text-wrap': [{ 'text': ['wrap', 'nowrap', 'balance', 'pretty'] }],
            'indent': [{ 'indent': scale_unambiguous_spacing() }],
            'vertical-align': [
                {
                    'align': [
                        'baseline',
                        'top',
                        'middle',
                        'bottom',
                        'text-top',
                        'text-bottom',
                        'sub',
                        'super',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'whitespace': [
                { 'whitespace': ['normal', 'nowrap', 'pre', 'pre-line', 'pre-wrap', 'break-spaces'] },
            ],
            'break': [{ 'break': ['normal', 'words', 'all', 'keep'] }],
            'hyphens': [{ 'hyphens': ['none', 'manual', 'auto'] }],
            'content': [{ 'content': ['none', is_arbitrary_variable, is_arbitrary_value] }],
            'bg-attachment': [{ 'bg': ['fixed', 'local', 'scroll'] }],
            'bg-clip': [{ 'bg-clip': ['border', 'padding', 'content', 'text'] }],
            'bg-origin': [{ 'bg-origin': ['border', 'padding', 'content'] }],
            'bg-position': [
                { 'bg': [*scale_position(), is_arbitrary_variable_position, is_arbitrary_position] },
            ],
            'bg-repeat': [{ 'bg': ['no-repeat', { 'repeat': ['', 'x', 'y', 'space', 'round'] }] }],
            'bg-size': [
                { 'bg': ['auto', 'cover', 'contain', is_arbitrary_variable_size, is_arbitrary_size] },
            ],
            'bg-image': [
                {
                    'bg': [
                        'none',
                        {
                            'linear': [
                                { 'to': ['t', 'tr', 'r', 'br', 'b', 'bl', 'l', 'tl'] },
                                is_integer,
                                is_arbitrary_variable,
                                is_arbitrary_value,
                            ],
                            'radial': ['', is_arbitrary_variable, is_arbitrary_value],
                            'conic': [is_integer, is_arbitrary_variable, is_arbitrary_value],
                        },
                        is_arbitrary_variable_image,
                        is_arbitrary_image,
                    ],
                },
            ],
            'bg-color': [{ 'bg': scale_color() }],
            'gradient-from-pos': [{ 'from': scale_gradient_stop_position() }],
            'gradient-via-pos': [{ 'via': scale_gradient_stop_position() }],
            'gradient-to-pos': [{ 'to': scale_gradient_stop_position() }],
            'gradient-from': [{ 'from': scale_color() }],
            'gradient-via': [{ 'via': scale_color() }],
            'gradient-to': [{ 'to': scale_color() }],
            'rounded': [{ 'rounded': scale_radius() }],
            'rounded-s': [{ 'rounded-s': scale_radius() }],
            'rounded-e': [{ 'rounded-e': scale_radius() }],
            'rounded-t': [{ 'rounded-t': scale_radius() }],
            'rounded-r': [{ 'rounded-r': scale_radius() }],
            'rounded-b': [{ 'rounded-b': scale_radius() }],
            'rounded-l': [{ 'rounded-l': scale_radius() }],
            'rounded-ss': [{ 'rounded-ss': scale_radius() }],
            'rounded-se': [{ 'rounded-se': scale_radius() }],
            'rounded-ee': [{ 'rounded-ee': scale_radius() }],
            'rounded-es': [{ 'rounded-es': scale_radius() }],
            'rounded-tl': [{ 'rounded-tl': scale_radius() }],
            'rounded-tr': [{ 'rounded-tr': scale_radius() }],
            'rounded-br': [{ 'rounded-br': scale_radius() }],
            'rounded-bl': [{ 'rounded-bl': scale_radius() }],
            'border-w': [{ 'border': scale_border_width() }],
            'border-w-x': [{ 'border-x': scale_border_width() }],
            'border-w-y': [{ 'border-y': scale_border_width() }],
            'border-w-s': [{ 'border-s': scale_border_width() }],
            'border-w-e': [{ 'border-e': scale_border_width() }],
            'border-w-t': [{ 'border-t': scale_border_width() }],
            'border-w-r': [{ 'border-r': scale_border_width() }],
            'border-w-b': [{ 'border-b': scale_border_width() }],
            'border-w-l': [{ 'border-l': scale_border_width() }],
            'divide-x': [{ 'divide-x': scale_border_width() }],
            'divide-x-reverse': ['divide-x-reverse'],
            'divide-y': [{ 'divide-y': scale_border_width() }],
            'divide-y-reverse': ['divide-y-reverse'],
            'border-style': [{ 'border': [*scale_line_style(), 'hidden', 'none'] }],
            'divide-style': [{ 'divide': [*scale_line_style(), 'hidden', 'none'] }],
            'border-color': [{ 'border': scale_color() }],
            'border-color-x': [{ 'border-x': scale_color() }],
            'border-color-y': [{ 'border-y': scale_color() }],
            'border-color-s': [{ 'border-s': scale_color() }],
            'border-color-e': [{ 'border-e': scale_color() }],
            'border-color-t': [{ 'border-t': scale_color() }],
            'border-color-r': [{ 'border-r': scale_color() }],
            'border-color-b': [{ 'border-b': scale_color() }],
            'border-color-l': [{ 'border-l': scale_color() }],
            'divide-color': [{ 'divide': scale_color() }],
            'outline-style': [{ 'outline': [*scale_line_style(), 'none', 'hidden'] }],
            'outline-offset': [
                { 'outline-offset': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'outline-w': [
                { 'outline': ['', is_number, is_arbitrary_variable_length, is_arbitrary_length] },
            ],
            'outline-color': [{ 'outline': scale_color() }],
            'shadow': [
                {
                    'shadow': [
                        '',
                        'none',
                        theme_shadow,
                        is_arbitrary_variable_shadow,
                        is_arbitrary_shadow,
                    ],
                },
            ],
            'shadow-color': [{ 'shadow': scale_color() }],
            'inset-shadow': [
                {
                    'inset-shadow': [
                        'none',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                        theme_inset_shadow,
                    ],
                },
            ],
            'inset-shadow-color': [{ 'inset-shadow': scale_color() }],
            'ring-w': [{ 'ring': scale_border_width() }],
            'ring-w-inset': ['ring-inset'],
            'ring-color': [{ 'ring': scale_color() }],
            'ring-offset-w': [{ 'ring-offset': [is_number, is_arbitrary_length] }],
            'ring-offset-color': [{ 'ring-offset': scale_color() }],
            'inset-ring-w': [{ 'inset-ring': scale_border_width() }],
            'inset-ring-color': [{ 'inset-ring': scale_color() }],
            'opacity': [{ 'opacity': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'mix-blend': [{ 'mix-blend': [*scale_blend_mode(), 'plus-darker', 'plus-lighter'] }],
            'bg-blend': [{ 'bg-blend': scale_blend_mode() }],
            'filter': [
                {
                    'filter': [
                        '',
                        'none',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'blur': [{ 'blur': scale_blur() }],
            'brightness': [{ 'brightness': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'contrast': [{ 'contrast': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'drop-shadow': [
                {
                    'drop-shadow': [
                        '',
                        'none',
                        theme_drop_shadow,
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'grayscale': [{ 'grayscale': ['', is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'hue-rotate': [{ 'hue-rotate': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'invert': [{ 'invert': ['', is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'saturate': [{ 'saturate': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'sepia': [{ 'sepia': ['', is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'backdrop-filter': [
                {
                    'backdrop-filter': [
                        '',
                        'none',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'backdrop-blur': [{ 'backdrop-blur': scale_blur() }],
            'backdrop-brightness': [
                { 'backdrop-brightness': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-contrast': [
                { 'backdrop-contrast': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-grayscale': [
                { 'backdrop-grayscale': ['', is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-hue-rotate': [
                { 'backdrop-hue-rotate': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-invert': [
                { 'backdrop-invert': ['', is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-opacity': [
                { 'backdrop-opacity': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-saturate': [
                { 'backdrop-saturate': [is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'backdrop-sepia': [
                { 'backdrop-sepia': ['', is_number, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'border-collapse': [{ 'border': ['collapse', 'separate'] }],
            'border-spacing': [{ 'border-spacing': scale_unambiguous_spacing() }],
            'border-spacing-x': [{ 'border-spacing-x': scale_unambiguous_spacing() }],
            'border-spacing-y': [{ 'border-spacing-y': scale_unambiguous_spacing() }],
            'table-layout': [{ 'table': ['auto', 'fixed'] }],
            'caption': [{ 'caption': ['top', 'bottom'] }],
            'transition': [
                {
                    'transition': [
                        '',
                        'all',
                        'colors',
                        'opacity',
                        'shadow',
                        'transform',
                        'none',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'transition-behavior': [{ 'transition': ['normal', 'discrete'] }],
            'duration': [{ 'duration': [is_number, 'initial', is_arbitrary_variable, is_arbitrary_value] }],
            'ease': [
                { 'ease': ['linear', 'initial', theme_ease, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'delay': [{ 'delay': [is_number, is_arbitrary_variable, is_arbitrary_value] }],
            'animate': [{ 'animate': ['none', theme_animate, is_arbitrary_variable, is_arbitrary_value] }],
            'backface': [{ 'backface': ['hidden', 'visible'] }],
            'perspective': [
                { 'perspective': [theme_perspective, is_arbitrary_variable, is_arbitrary_value] },
            ],
            'perspective-origin': [{ 'perspective-origin': scale_origin() }],
            'rotate': [{ 'rotate': scale_rotate() }],
            'rotate-x': [{ 'rotate-x': scale_rotate() }],
            'rotate-y': [{ 'rotate-y': scale_rotate() }],
            'rotate-z': [{ 'rotate-z': scale_rotate() }],
            'scale': [{ 'scale': scale_scale() }],
            'scale-x': [{ 'scale-x': scale_scale() }],
            'scale-y': [{ 'scale-y': scale_scale() }],
            'scale-z': [{ 'scale-z': scale_scale() }],
            'scale-3d': ['scale-3d'],
            'skew': [{ 'skew': scale_skew() }],
            'skew-x': [{ 'skew-x': scale_skew() }],
            'skew-y': [{ 'skew-y': scale_skew() }],
            'transform': [
                { 'transform': [is_arbitrary_variable, is_arbitrary_value, '', 'none', 'gpu', 'cpu'] },
            ],
            'transform-origin': [{ 'origin': scale_origin() }],
            'transform-style': [{ 'transform': ['3d', 'flat'] }],
            'translate': [{ 'translate': scale_translate() }],
            'translate-x': [{ 'translate-x': scale_translate() }],
            'translate-y': [{ 'translate-y': scale_translate() }],
            'translate-z': [{ 'translate-z': scale_translate() }],
            'translate-none': ['translate-none'],
            'accent': [{ 'accent': scale_color() }],
            'appearance': [{ 'appearance': ['none', 'auto'] }],
            'caret-color': [{ 'caret': scale_color() }],
            'color-scheme': [
                { 'scheme': ['normal', 'dark', 'light', 'light-dark', 'only-dark', 'only-light'] },
            ],
            'cursor': [
                {
                    'cursor': [
                        'auto',
                        'default',
                        'pointer',
                        'wait',
                        'text',
                        'move',
                        'help',
                        'not-allowed',
                        'none',
                        'context-menu',
                        'progress',
                        'cell',
                        'crosshair',
                        'vertical-text',
                        'alias',
                        'copy',
                        'no-drop',
                        'grab',
                        'grabbing',
                        'all-scroll',
                        'col-resize',
                        'row-resize',
                        'n-resize',
                        'e-resize',
                        's-resize',
                        'w-resize',
                        'ne-resize',
                        'nw-resize',
                        'se-resize',
                        'sw-resize',
                        'ew-resize',
                        'ns-resize',
                        'nesw-resize',
                        'nwse-resize',
                        'zoom-in',
                        'zoom-out',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'field-sizing': [{ 'field-sizing': ['fixed', 'content'] }],
            'pointer-events': [{ 'pointer-events': ['auto', 'none'] }],
            'resize': [{ 'resize': ['none', '', 'y', 'x'] }],
            'scroll-behavior': [{ 'scroll': ['auto', 'smooth'] }],
            'scroll-m': [{ 'scroll-m': scale_unambiguous_spacing() }],
            'scroll-mx': [{ 'scroll-mx': scale_unambiguous_spacing() }],
            'scroll-my': [{ 'scroll-my': scale_unambiguous_spacing() }],
            'scroll-ms': [{ 'scroll-ms': scale_unambiguous_spacing() }],
            'scroll-me': [{ 'scroll-me': scale_unambiguous_spacing() }],
            'scroll-mt': [{ 'scroll-mt': scale_unambiguous_spacing() }],
            'scroll-mr': [{ 'scroll-mr': scale_unambiguous_spacing() }],
            'scroll-mb': [{ 'scroll-mb': scale_unambiguous_spacing() }],
            'scroll-ml': [{ 'scroll-ml': scale_unambiguous_spacing() }],
            'scroll-p': [{ 'scroll-p': scale_unambiguous_spacing() }],
            'scroll-px': [{ 'scroll-px': scale_unambiguous_spacing() }],
            'scroll-py': [{ 'scroll-py': scale_unambiguous_spacing() }],
            'scroll-ps': [{ 'scroll-ps': scale_unambiguous_spacing() }],
            'scroll-pe': [{ 'scroll-pe': scale_unambiguous_spacing() }],
            'scroll-pt': [{ 'scroll-pt': scale_unambiguous_spacing() }],
            'scroll-pr': [{ 'scroll-pr': scale_unambiguous_spacing() }],
            'scroll-pb': [{ 'scroll-pb': scale_unambiguous_spacing() }],
            'scroll-pl': [{ 'scroll-pl': scale_unambiguous_spacing() }],
            'snap-align': [{ 'snap': ['start', 'end', 'center', 'align-none'] }],
            'snap-stop': [{ 'snap': ['normal', 'always'] }],
            'snap-type': [{ 'snap': ['none', 'x', 'y', 'both'] }],
            'snap-strictness': [{ 'snap': ['mandatory', 'proximity'] }],
            'touch': [{ 'touch': ['auto', 'none', 'manipulation'] }],
            'touch-x': [{ 'touch-pan': ['x', 'left', 'right'] }],
            'touch-y': [{ 'touch-pan': ['y', 'up', 'down'] }],
            'touch-pz': ['touch-pinch-zoom'],
            'select': [{ 'select': ['none', 'text', 'all', 'auto'] }],
            'will-change': [
                {
                    'will-change': [
                        'auto',
                        'scroll',
                        'contents',
                        'transform',
                        is_arbitrary_variable,
                        is_arbitrary_value,
                    ],
                },
            ],
            'fill': [{ 'fill': ['none', *scale_color()] }],
            'stroke-w': [
                {
                    'stroke': [
                        is_number,
                        is_arbitrary_variable_length,
                        is_arbitrary_length,
                        is_arbitrary_number,
                    ],
                },
            ],
            'stroke': [{ 'stroke': ['none', *scale_color()] }],
            'forced-color-adjust': [{ 'forced-color-adjust': ['auto', 'none'] }],
        },

        'conflicting_class_groups': {
            'overflow': ['overflow-x', 'overflow-y'],
            'overscroll': ['overscroll-x', 'overscroll-y'],
            'inset': ['inset-x', 'inset-y', 'start', 'end', 'top', 'right', 'bottom', 'left'],
            'inset-x': ['right', 'left'],
            'inset-y': ['top', 'bottom'],
            'flex': ['basis', 'grow', 'shrink'],
            'gap': ['gap-x', 'gap-y'],
            'p': ['px', 'py', 'ps', 'pe', 'pt', 'pr', 'pb', 'pl'],
            'px': ['pr', 'pl'],
            'py': ['pt', 'pb'],
            'm': ['mx', 'my', 'ms', 'me', 'mt', 'mr', 'mb', 'ml'],
            'mx': ['mr', 'ml'],
            'my': ['mt', 'mb'],
            'size': ['w', 'h'],
            'font-size': ['leading'],
            'fvn-normal': [
                'fvn-ordinal',
                'fvn-slashed-zero',
                'fvn-figure',
                'fvn-spacing',
                'fvn-fraction',
            ],
            'fvn-ordinal': ['fvn-normal'],
            'fvn-slashed-zero': ['fvn-normal'],
            'fvn-figure': ['fvn-normal'],
            'fvn-spacing': ['fvn-normal'],
            'fvn-fraction': ['fvn-normal'],
            'line-clamp': ['display', 'overflow'],
            'rounded': [
                'rounded-s',
                'rounded-e',
                'rounded-t',
                'rounded-r',
                'rounded-b',
                'rounded-l',
                'rounded-ss',
                'rounded-se',
                'rounded-ee',
                'rounded-es',
                'rounded-tl',
                'rounded-tr',
                'rounded-br',
                'rounded-bl',
            ],
            'rounded-s': ['rounded-ss', 'rounded-es'],
            'rounded-e': ['rounded-se', 'rounded-ee'],
            'rounded-t': ['rounded-tl', 'rounded-tr'],
            'rounded-r': ['rounded-tr', 'rounded-br'],
            'rounded-b': ['rounded-br', 'rounded-bl'],
            'rounded-l': ['rounded-tl', 'rounded-bl'],
            'border-spacing': ['border-spacing-x', 'border-spacing-y'],
            'border-w': [
                'border-w-s',
                'border-w-e',
                'border-w-t',
                'border-w-r',
                'border-w-b',
                'border-w-l',
            ],
            'border-w-x': ['border-w-r', 'border-w-l'],
            'border-w-y': ['border-w-t', 'border-w-b'],
            'border-color': [
                'border-color-s',
                'border-color-e',
                'border-color-t',
                'border-color-r',
                'border-color-b',
                'border-color-l',
            ],
            'border-color-x': ['border-color-r', 'border-color-l'],
            'border-color-y': ['border-color-t', 'border-color-b'],
            'translate': ['translate-x', 'translate-y', 'translate-none'],
            'translate-none': ['translate', 'translate-x', 'translate-y', 'translate-z'],
            'scroll-m': [
                'scroll-mx',
                'scroll-my',
                'scroll-ms',
                'scroll-me',
                'scroll-mt',
                'scroll-mr',
                'scroll-mb',
                'scroll-ml',
            ],
            'scroll-mx': ['scroll-mr', 'scroll-ml'],
            'scroll-my': ['scroll-mt', 'scroll-mb'],
            'scroll-p': [
                'scroll-px',
                'scroll-py',
                'scroll-ps',
                'scroll-pe',
                'scroll-pt',
                'scroll-pr',
                'scroll-pb',
                'scroll-pl',
            ],
            'scroll-px': ['scroll-pr', 'scroll-pl'],
            'scroll-py': ['scroll-pt', 'scroll-pb'],
            'touch': ['touch-x', 'touch-y', 'touch-pz'],
            'touch-x': ['touch'],
            'touch-y': ['touch'],
            'touch-pz': ['touch'],
        },

        'conflicting_class_group_modifiers': {
            'font-size': ['leading'],
        },

        'order_sensitive_modifiers': [
            'before',
            'after',
            'placeholder',
            'file',
            'marker',
            'selection',
            'first-line',
            'first-letter',
            'backdrop',
            '*',
            '**',
        ],
    }
