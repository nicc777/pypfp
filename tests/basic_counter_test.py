import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import unittest
import random
from src.pypfp.pfp import MultiProcessor
from src.pypfp import Result
import traceback
import inspect
import time


CONTEXT = {
    'counter1': [0,9,8,7,6,5],  # SUM=35
    'counter2': [2,4,6,8]       # PRODUCT=384
}


def counter1(q, context: dict, args: dict):
    r = Result(function_name=inspect.currentframe().f_code.co_name)
    r.result = dict()
    r.result['Count'] = 0
    r.result['Answer'] = None
    elements = list()
    if inspect.currentframe().f_code.co_name in context:
        elements = context[inspect.currentframe().f_code.co_name]
    count = len(elements)
    r.result['Count'] = count
    if args is not None:
        if 'Operation' in args:
            if args['Operation'].upper() == 'ADD':
                r.result['Answer'] = 0
                for num in elements:
                    r.result['Answer'] += num
            elif args['Operation'].upper() == 'MULTIPLY':
                r.result['Answer'] = 1
                for num in elements:
                    r.result['Answer'] *= num
    time.sleep(0.3)
    try:
        q.put(r)
    except:
        traceback.print_exc()


def counter2(q, context: dict, args: dict):
    r = Result(function_name=inspect.currentframe().f_code.co_name)
    r.result = dict()
    r.result['Count'] = 0
    r.result['Answer'] = None
    elements = list()
    if inspect.currentframe().f_code.co_name in context:
        elements = context[inspect.currentframe().f_code.co_name]
    count = len(elements)
    r.result['Count'] = count
    if args is not None:
        if 'Operation' in args:
            if args['Operation'].upper() == 'ADD':
                r.result['Answer'] = 0
                for num in elements:
                    r.result['Answer'] += num
            elif args['Operation'].upper() == 'MULTIPLY':
                r.result['Answer'] = 1
                for num in elements:
                    r.result['Answer'] *= num
    try:
        q.put(r)
    except:
        traceback.print_exc()


class DummyQueue:

    def __init__(self):
        self.result = None

    def put(self, result):
        self.result = result


class TestBasicMultiProcessing(unittest.TestCase):

    def test_counter1_basic_test(self):
        q = DummyQueue()
        counter1(q=q, context=CONTEXT, args=None)
        self.assertIsNotNone(q.result.result)
        self.assertIsInstance(q.result, Result)
        self.assertIsInstance(q.result.result, dict)
        self.assertTrue('Count' in q.result.result)
        self.assertTrue('Answer' in q.result.result)
        self.assertIsInstance(q.result.result['Count'], int)
        self.assertTrue(q.result.result['Count'] > 0)
        self.assertEqual(6, q.result.result['Count'])

    def test_counter2_basic_test(self):
        q = DummyQueue()
        counter2(q=q, context=CONTEXT, args=None)
        self.assertIsNotNone(q.result.result)
        self.assertIsInstance(q.result, Result)
        self.assertIsInstance(q.result.result, dict)
        self.assertTrue('Count' in q.result.result)
        self.assertTrue('Answer' in q.result.result)
        self.assertIsInstance(q.result.result['Count'], int)
        self.assertTrue(q.result.result['Count'] > 0)
        self.assertEqual(4, q.result.result['Count'])

    def test_multiprocessing(self):
        m = MultiProcessor(context=CONTEXT)
        m.register_function(f=counter1, f_args={'Operation': 'ADD'})
        m.register_function(f=counter2, f_args={'Operation': 'MULTIPLY'})
        m.execute_parallel()
        self.assertEqual(len(m.results), 2)
        for result in m.results:
            self.assertIsInstance(result, Result)
            self.assertTrue(result.function_name in CONTEXT)
            expected_count = len(CONTEXT[result.function_name])
            expected_answer = 0
            if result.function_name == 'counter1':
                expected_answer = 35
            elif result.function_name == 'counter2':
                expected_answer = 384
            self.assertEqual(expected_count, result.result['Count'])
            self.assertEqual(expected_answer, result.result['Answer'])



# EOF
