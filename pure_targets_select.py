import fileinput
import argparse

vars_file = 'group_vars/all/vars_file.yml'


def change_target(target):
    """Change target_servers variable in vars_file based on selection
    
    Args:
        target (str): One of 'test','nonprod','prod', and 'all' selections
    
    """
    if target == 'test':
        newline = '              <<: *test_arrays_opts'
    elif target == 'nonprod':
        newline = '              <<: *pure_arrays_nonprod_opts'
    elif target == 'prod':
        newline = '              <<: *pure_arrays_prod_opts'
    elif target == 'all':
        newline = '              <<: *pure_arrays_all_opts'
    else:
        return
    with fileinput.FileInput(files=(vars_file), inplace=True) as f:
        marker = 0
        for line in f:
            if marker == 1 and '<<:' in line:
                line = newline
                marker = 0
                print(line)
            else:
                print(line, end='')
            if 'target_arrays:' in line:
                marker = 1
    return


def simplified_target(target):
    """ Returns two values based on contents of target string

    Args:
        target (str): string value of target_arrays variable in vars_file.yml

    Returns:
        str, str: Simplied values of alias found in target_arrays variable

    """
    if '_prod_' in target:
        return 'Production', 'prod'
    elif 'test' in target:
        return 'Test', 'test'
    elif 'nonprod' in target:
        return 'Non-Production', 'nonprod'
    elif 'all' in target:
        return 'All', 'all'
    else:
        return 'Target not found!', None


def display_current_target():
    """Display current target_arrays variable setting in vars_file

    Returns:
        str, str: String values for simplified version of the value found in target_arrays variable
        
    """
    marker = 0
    target = ""
    with open(vars_file) as f:
        for line in f:
            if marker == 1 and '<<:' in line:
                line_list = line.split(':')
                target = line_list[1].strip()
                marker = 0
            if 'target_arrays:' in line:
                marker = 1
    simple_target, current_selection = simplified_target(target)
    print(f'Current target setting: {simple_target}')
    return simple_target, current_selection


def main():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--t", dest='value', action='store_const', const='test', help="Select Test Pure Arrays list for Ansible")
    g.add_argument("--n", dest='value', action='store_const', const='nonprod', help="Select Non-Prod Pure Arrays list for Ansible")
    g.add_argument("--p", dest='value', action='store_const', const='prod', help="Select Prod Pure Arrays list for Ansible")
    g.add_argument("--a", dest='value', action='store_const', const='all', help="Select ALL Pure Arrays list for Ansible")
    args = parser.parse_args()
    print()
    simple_target, current_selection = display_current_target()
    print(f'Switching to: [{args.value.capitalize()}]')
    changed = False
    if (args.value == None):
        parser.error('Error: No selection made!')
    elif args.value == current_selection:
        print(f'{simple_target} already currently selected in file.')
    elif 'test' in args.value:
        change_target(args.value)
        changed = True
    elif 'nonprod' in args.value:
        change_target(args.value)
        changed = True
    elif 'prod' in args.value:
        change_target(args.value)
        changed = True
    elif 'all' in args.value:
        change_target(args.value)
        changed = True
    else:
        print('No valid choice selected')
    if changed:
        simple_target, current_selection = display_current_target()    
    print()

if __name__ == '__main__':
    main()
