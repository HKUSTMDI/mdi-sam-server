import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root-dir', dest='root_dir', default='.', help='Projects root directory')
parser.add_argument('--option', dest='option', default=False, action='store_true', help='An optional flag')

args, subargs = parser.parse_known_args()

print(args.root_dir)  # 访问已知参数的值
print(args.option)    # 访问已知参数的值

print(subargs)  # 输出未知参数的列表

"""
(rtmdet-sam) ➜  tests git:(master) ✗ python3 test_parse2.py --root-dir zach --go go
zach
False
['--go', 'go']

"""