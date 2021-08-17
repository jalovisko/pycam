"""
  2 Copyright (c) 2021 Nikita Letov (letovnn@gmail.com)
  3 Distributed under the MIT software license, see the accompanying
  4 file COPYING or http://www.opensource.org/licenses/mit-license.php.
  5 
  6 This script converts STEP files to STL file.
  7 Usage:
  8     python main.py -i input.dxf -o output.png
  9 or
 10     python main.py --input input.dxf --output output.png
 11 
 12 For more info see the PythonOCC Tutorial:
 13 https://pythonocc-doc.readthedocs.io/en/latest/convert/
 14 """

import json
import yaml

from optparse import OptionParser

def read_json(json_file_name: str) -> dict:
    """
    Opens and reads a JSON file
    """
    with open(json_file_name) as reader:
        data = json.load(reader)
        return data

def format_data(data: dict) -> dict:
    """
    Formats the imported data (dictionary) to another dictionary which is
    closer to the YAML file format + fills the data gaps that are not present
    in the initial JSON.
    """
    # Filling the bounds data
    bounds_data = {'bounds': {
        'minimal': {
            'X-Application':  {
                'pycam-gtk': {
                    'name': 'minimal'}
                },
            'lower': [5, 5, 0],
            'reference_models': ['model'],
            'specification': 'margins',
            'tool_boundary': 'along',
            'upper': [5, 5, 1]
            }
        }
    }
    # Filling the export settings data
    export_settings = {'export_settings': {
            'milling': {
                'X-Application': {
                    'pycam-gtk': {
                        'name': 'Milling Settings'
                        }
                    },
                'gcode': {
                    'corner_style': {
                        'mode': 'optimize_tolerance',
                        'motion_tolerance': 0.0,
                        'naive_tolerance': 0.0
                        },
                    'plunge_feedrate': data.get('plunge_feedrate'),
                    'safety_height': data.get('safety_height'),
                    'step_width': {
                        'x': 0.0001,
                        'y': 0.0001,
                        'z': 0.0001
                        },
                    'unit': data.get('unit')
                    }
                }
            }
        }
    # Filling the exports data
    exports = { 'exports': {
        # The following line and other similar lines in this script are
        # hash sums generated by PyCAM. Ideally, they should vary per
        # output but this is a TODO
        '728de392bf74440486fb862eb9692eff': {
            'format': {
                'comment': 'Generated by PyCAM 0.7.0~pre0~requirements.589.gc127f00a.dirty: 2021-07-29',
                'dialect': 'linuxcnc',
                'export_settings': 'milling',
                'type': 'gcode'
                },
            'source': {
                'items': ['819bdee87f134ca9a23ba05af4258972',
                    'bab6daf625d94288ad8caf134736eb5e'],
                'type': 'toolpath'
                },
            'target': {
                'location': data.get('ngs_output'),
                'type': 'file'
                }
            }
        }
    }
    # Filling the models data
    models = { 'models': {
        'model': {
            'X-Application': {
                'pycam-gtk': {
                    'color': {
                        'alpha': 0.8,
                        'blue': 1.0,
                        'green': 0.4,
                        'red': 0.1
                        },
                 'name': 'cli_part'
                 }
            },
            'source': {
                'location': data.get('model_input'),
               'type': 'file'
                },
            'transformations': []
            }
        }
    }
    # Filling the processes data
    processes = { 'processes': {
        'process_slicing': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Slice (rough)'
                    }
                },
            'grid_direction': 'y',
            'milling_style': 'ignore',
            'overlap': 0.1,
            'path_pattern': 'grid',
            'radius_compensation': 'false',
            'rounded_corners': 'true',
            'spiral_direction': 'out',
            'step_down': 3.0,
            'strategy': 'slice'
            },
        'process_surfacing': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Surface (fine)'
                    }
                },
            'grid_direction': 'x',
            'milling_style': 'ignore',
            'overlap': 0.8,
            'path_pattern': 'grid',
            'radius_compensation': 'false',
            'rounded_corners': 'true',
            'spiral_direction': 'out',
            'step_down': 1.0,
            'strategy': 'surface'
            }
        }
    }
    # Filling the tasks data
    tasks = { 'tasks': {
        'fine': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Finishing'
                    }
                },
            'bounds': 'minimal',
            'collision_models': ['model'],
            'process': 'process_surfacing',
            'tool': 'fine',
            'type': 'milling'
            },
        'rough': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Quick Removal'
                    }
                },
            'bounds': 'minimal',
            'collision_models': ['model'],
            'process': 'process_slicing',
            'tool': 'rough',
            'type': 'milling'
            }
        }
    }
    # Filling the toolpaths data
    toolpaths = { 'toolpaths': {
        '819bdee87f134ca9a23ba05af4258972': {
            'source': {
                'item': 'rough',
                'type': 'task'
                },
            'transformations': []
            },
        'bab6daf625d94288ad8caf134736eb5e': {
            'source': {
                'item': 'fine',
                'type': 'task'
                },
            'transformations': []
            }
        }
    }
    # Filling the tools data
    tools = { 'tools': {
        'fine': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Small Tool'
                    }
                },
            'feed': data.get('fine_feed'),
            'height': data.get('fine_height'),
            'radius': data.get('fine_radius'),
            'shape': data.get('fine_shape'),
            'spindle': {
                'speed': data.get('fine_spindle_speed'),
                'spin_up_delay': '2.0',
                'spin_up_enabled': 'true'
                },
            'tool_id': 2
            },
        'rough': {
            'X-Application': {
                'pycam-gtk': {
                    'name': 'Big Tool'
                    }
                },
            'feed': data.get('rough_feed'),
            'height': data.get('rough_height'),
            'radius': data.get('rough_radius'),
            'shape': data.get('rough_shape'),
            'spindle': {
                'speed': data.get('rough_spindle_speed'),
                'spin_up_delay': '2.0',
                'spin_up_enabled': 'true'
                },
            'tool_id': 1
            }
        }
    }
    # ** operator for packing and unpacking items in order
    data = {**bounds_data, **export_settings, **exports, **models,
            **processes, **tasks, **toolpaths, **tools}
    return data

def write_to_yml(yml_file_name: str, dict_file: dict) -> None:
    """
    Writes the formated data to the YAML file
    """
    with open(yml_file_name, 'w') as writer:
        documents = yaml.dump(dict_file, writer)
        print("Data written to " + yml_file_name)

def main():
    # Setting up the parser
    parser = OptionParser()
    parser.add_option("-i", "--input", dest = "input_filename",
            help = "Input STEP file name")
    parser.add_option("-o", "--output", dest = "output_filename",
            help = "Output stl file name")
    (options, args) = parser.parse_args()
    input_filename = str(options.input_filename)
    output_filename = str(options.output_filename)
    data = read_json(input_filename)
    data = format_data(data)
    write_to_yml(output_filename, data)

if __name__ == '__main__':
    main()

