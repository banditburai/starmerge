from starmerge import merge


def test_handles_color_conflicts_properly():
    assert merge('bg-grey-5 bg-hotpink') == 'bg-hotpink'
    assert merge('hover:bg-grey-5 hover:bg-hotpink') == 'hover:bg-hotpink'
    assert merge('stroke-[hsl(350_80%_0%)] stroke-[10px]') == 'stroke-[hsl(350_80%_0%)] stroke-[10px]' 
