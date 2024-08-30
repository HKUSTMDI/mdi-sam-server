# run_tests.py
import unittest

# 自动发现并运行 tests 目录下的所有测试
loader = unittest.TestLoader()
suite = loader.discover('tests')

runner = unittest.TextTestRunner()
runner.run(suite)
