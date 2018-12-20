#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'


class TestClass:

    name = 'terry'

    def run(self):
        print(self.name)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    test_class = TestClass()
    print(test_class)