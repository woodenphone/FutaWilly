#-------------------------------------------------------------------------------
# Name:        unittests_common
# Purpose:
#
# Author:      Ctrl-S
#
# Created:     04-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import unittest
import common






class testmd5(unittest.testcase):# WIP TODO
    def test_nonexistant_file(self):
        """Expected result if no file exists to calculate a hash of at the given path"""
        filepath = os.path.join('tests', 'hash_md5_notreallythere.test')
        self.assertRaises(hash_file_md5(filepath), ValueError)

    def test_known_value_a(self):
        """Expected result with given file data"""
        filepath = os.path.join('tests', 'hash_md5_a.test')
        self.assertEqual(hash_file_md5(filepath), 'some_hash_result')# TODO

    def test_known_value_b(self)
        """Expected result with given file data"""
        filepath = os.path.join('tests', 'hash_md5_b.test')
        self.assertEqual(hash_file_md5(filepath), 'some_hash_result')# TODO





def main():
    unittest.main()

if __name__ == '__main__':
    main()
