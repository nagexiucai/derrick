#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


class DetectorReport(object):
    """
    construct a dict with complex structure is very difficult
    especially when you need to construct the detect dict with
    many detectors.


    DEMO:

    {
        "Dockerfile.j2":{
            "version":"1.0"
            "content":"content"
        }
    }

    dr = DetectorReport()
    dockerfile_node = dr.create_node("Dockerfile.j2")
    dockerfile_node.extend_content({"version":"1.0"})
    dockerfile_node.extend_content({"content":"content"})

    report = dr.generate_report()

    """

    def __init__(self, name=None):
        self.name = name
        self.nodes = dict()
        self.store = dict()

    def get_name(self):
        return self.name

    def create_node(self, node_name):
        dr = DetectorReport(node_name)
        self.nodes[node_name] = dr
        return dr

    def extend_content(self, detect_content=None):
        self.store.update(detect_content)

    def register_detector(self, detector, *args, **kwargs):
        result = detector.execute(*args, **kwargs)
        self.extend_content(result)

    def generate_report(self):
        return DetectorReport.recursive_generate_store(self)

    @staticmethod
    def recursive_generate_store(report_node):
        nodes = report_node.nodes
        store = report_node.store
        if len(nodes.keys()) > 0:
            for node_name in nodes.keys():
                store[node_name] = dict()
                node_store = store[node_name]
                node_store_item = DetectorReport.recursive_generate_store(nodes[node_name])
                node_store.update(node_store_item)
            return store
        else:
            return report_node.store
