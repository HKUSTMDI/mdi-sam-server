import argparse

# 创建主解析器
parser = argparse.ArgumentParser()

# 创建子解析器
subparsers = parser.add_subparsers(dest='command', help='Available commands')
subparsers.required = True

# 子命令 1: init
parser_init = subparsers.add_parser('init', help='Initialize something')
parser_init.add_argument('--name', help='Name parameter for init command')

# 子命令 2: process
parser_process = subparsers.add_parser('process', help='Process something')
parser_process.add_argument('--input', help='Input file for process command')
parser_process.add_argument('--output', help='Output file for process command')

# 解析命令行参数
args = parser.parse_args()

# 根据所选的命令执行相应的逻辑
if args.command == 'init':
    print('Running init command...')
    if args.name:
        print(f'Initializing with name: {args.name}')
elif args.command == 'process':
    print('Running process command...')
    if args.input and args.output:
        print(f'Processing input file: {args.input} and writing output file: {args.output}')
else:
    print('Invalid command')


args, subargs = parser.parse_known_args()

print(args)
print(subargs)
"""
(1)先添加子解析器 add_subparsers
(2)添加子命令 add_parser
(3)添加参数 add_argument

测试
>>>python3 test_parsar.p init --name zachczhang      
Initializing with name: zachczhang
Namespace(command='init', name='zachczhang')
[]

>>>python3 test_parsar.py process --input in --output out
Processing input file: in and writing output file: out
Namespace(command='process', input='in', output='out')
[]
"""