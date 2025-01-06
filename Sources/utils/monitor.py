#
#  monitor.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 02/01/25.
#

import time
from os import environ # Environment Variables
from prometheus_client import start_http_server, Counter, Gauge
from utils.logger import logger

class Monitor:
    def __init__(self, service, node, port=None):
        self.service = str(service)
        self.node = str(node)
        if port is not None:
            self.port = int(port)
            start_http_server(self.port)
        else:
            self.port = None
    #-------------------------------------------------------------------------------------
    def _parse_labels(self, *kargs, **kwargs):
        labels = dict()
        for key in kargs:
            if type(key) is str:
                labels[key] = ""
        for key, value in kwargs.items():
            if (type(key) is str) and (type(value) is str):
                labels[key] = value
        labels["service"] = self.service
        labels["node"] = self.node
        return labels
    #-------------------------------------------------------------------------------------
    def counter(self, name, description, *kargs, **kwargs):
        labels = self._parse_labels(*kargs, **kwargs)
        return Counter(name, description, labels.keys()).labels(**labels)
    #-------------------------------------------------------------------------------------
    def gauge(self, name, description, *kargs, **kwargs):
        labels = self._parse_labels(*kargs, **kwargs)
        return Gauge(name, description, labels.keys()).labels(**labels)
    #-------------------------------------------------------------------------------------
    class Context:
        def __init__(self, monitor, name, description, *kargs, **kwargs):
            self.start_time = time.time()
            self.manual = True if ('manual' in kwargs) and (kwargs['manual'] == True) else False
            del kwargs['manual']
            def parse_string(string, counter_suffix = "", gauge_suffix = ""):
                counter = ""
                gauge = ""
                if type(string) is str:
                    counter = string + counter_suffix
                    gauge = string + gauge_suffix
                elif (type(string) is dict) and "counter" in string and "gauge" in string:
                    counter = str(string["counter"])
                    gauge = str(string["gauge"])
                else:
                    raise ValueError("Provide either a single string or a dictionary with 'counter' and 'gauge' strings")
                return counter, gauge
            counter_name, gauge_name = parse_string(name, "_counter", "_gauge")
            counter_description, gauge_description = parse_string(description)
            self.labels = monitor._parse_labels(*kargs, **kwargs)
            self.counter = Counter(counter_name, counter_description, self.labels.keys())
            self.gauge = Gauge(gauge_name, gauge_description, self.labels.keys())
            self.reported = False
        #---------------------------------------------------------------------------------
        def _metrics_with_updated_labels(self, **kwargs):
            def metric_updater(metric, new_labels):
                labels = dict(zip(metric._labelnames, metric._labelvalues))
                for key, value in new_labels.items():
                    if (type(key) is str) and (type(value) is str) and (key in labels):
                        labels[key] = value
                _labelvalues = metric._labelvalues
                metric._labelvalues = ()
                new_metric = metric.labels(**labels)
                metric._labelvalues = _labelvalues
                return new_metric
            return metric_updater(self.counter, kwargs), metric_updater(self.gauge, kwargs)
        #---------------------------------------------------------------------------------
        def report(self, **kwargs):
            self.reported = True
            duration = time.time() - self.start_time
            if len(kwargs) > 0:
                labels = self.labels.copy()
                for key, value in kwargs.items():
                    if (type(key) is str) and (type(value) is str) and (key in labels):
                        labels[key] = value
                labels[key] = value
                labels[key] = value
                labels["service"] = self.labels["service"]
                labels["node"] = self.labels["node"]
                self.counter.labels(**labels).inc()
                self.gauge.labels(**labels).set(duration)
            else:
                self.counter.labels(**self.labels).inc()
                self.gauge.labels(**self.labels).set(duration)
        #---------------------------------------------------------------------------------
        def __enter__(self):
            self.reported = False
            return self
        #---------------------------------------------------------------------------------
        def __exit__(self, exc_type, exc, exc_tb):
            if (self.reported is False) and (self.manual is False):
                if exc is None:
                    self.report()
            return False # Rethrow exceptions
        #---------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------
    def context(self, name, description, *kargs, **kwargs):
        return self.__class__.Context(self, name, description, *kargs, **kwargs)
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

monitor = None
_service = str(environ.get('MONITOR_SERVICE_NAME', ''))
_node = str(environ.get('MONITOR_SERVICE_NODE', ''))
if (len(_service) > 0) and (len(_node) > 0):
    _port = str(environ.get('MONITOR_SERVICE_PORT', ''))
    if len(_port) > 0:
        logger.info(f"MONITOR PORT: {_port}")
        monitor = Monitor(_service, _node, _port)
#-----------------------------------------------------------------------------------------