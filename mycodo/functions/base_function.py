# coding=utf-8
"""
This module contains the AbstractFunction Class which acts as a template
for all functions.  It is not to be used directly. The AbstractFunction Class
ensures that certain methods and instance variables are included in each
Function.

All Functions should inherit from this class and overwrite methods that raise
NotImplementedErrors
"""
import json
import logging
import time

from mycodo.abstract_base_controller import AbstractBaseController
from mycodo.config import SQL_DATABASE_MYCODO
from mycodo.databases.models import Conversion
from mycodo.databases.models import DeviceMeasurements
from mycodo.databases.models import CustomController
from mycodo.databases.utils import session_scope
from mycodo.utils.database import db_retrieve_table_daemon

MYCODO_DB_PATH = 'sqlite:///' + SQL_DATABASE_MYCODO


class AbstractFunction(AbstractBaseController):
    """
    Base Function class that ensures certain methods and values are present
    in functions.
    """
    def __init__(self, function, testing=False, name=__name__):
        if not testing:
            super(AbstractFunction, self).__init__(function.unique_id, testing=testing, name=__name__)
        else:
            super(AbstractFunction, self).__init__(None, testing=testing, name=__name__)

        self.logger = None
        self.setup_logger(testing=testing, name=name, function=function)
        self.function = function
        self.channels_conversion = {}
        self.channels_measurement = {}
        self.running = True
        self.device_measurements = None

        if not testing:
            self.unique_id = function.unique_id
            self.initialize_measurements()

    def initialize_measurements(self):
        try:
            if self.device_measurements:
                return
        except:
            pass
        self.setup_device_measurement()

    def is_enabled(self, channel):
        try:
            return self.channels_measurement[channel].is_enabled
        except:
            self.setup_device_measurement()
            return self.channels_measurement[channel].is_enabled

    def setup_device_measurement(self):
        # Make 5 attempts to access database
        for _ in range(5):
            try:
                self.device_measurements = db_retrieve_table_daemon(
                    DeviceMeasurements).filter(
                    DeviceMeasurements.device_id == self.function.unique_id)

                for each_measure in self.device_measurements.all():
                    self.channels_measurement[each_measure.channel] = each_measure
                    self.channels_conversion[each_measure.channel] = db_retrieve_table_daemon(
                        Conversion, unique_id=each_measure.conversion_id)
                return
            except Exception as msg:
                self.logger.debug("Error: {}".format(msg))
            time.sleep(1)

    def setup_logger(self, testing=None, name=None, function=None):
        name = name if name else __name__
        if not testing and function:
            log_name = "{}_{}".format(name, function.unique_id.split('-')[0])
        else:
            log_name = name
        self.logger = logging.getLogger(log_name)
        if not testing and function:
            if function.log_level_debug:
                self.logger.setLevel(logging.DEBUG)
            else:
                self.logger.setLevel(logging.INFO)

    def start_function(self):
        """ Not used yet """
        self.running = True

    def stop_function(self):
        """ Called when Function is deactivated """
        self.running = False
        try:
            # Release all locks
            for lockfile, lock_state in self.lockfile.locked.items():
                if lock_state:
                    self.lock_release(lockfile)
        except:
            pass

    #
    # Accessory functions
    #

    def set_custom_option(self, option, value):
        try:
            with session_scope(MYCODO_DB_PATH) as new_session:
                mod_function = new_session.query(CustomController).filter(
                    CustomController.unique_id == self.unique_id).first()
                try:
                    dict_custom_options = json.loads(mod_function.custom_options)
                except:
                    dict_custom_options = {}
                dict_custom_options[option] = value
                mod_function.custom_options = json.dumps(dict_custom_options)
                new_session.commit()
        except Exception:
            self.logger.exception("set_custom_option")

    def get_custom_option(self, option):
        try:
            dict_custom_options = json.loads(self.function.custom_options)
        except:
            dict_custom_options = {}
        if option in dict_custom_options:
            return dict_custom_options[option]

    def delete_custom_option(self, option):
        try:
            with session_scope(MYCODO_DB_PATH) as new_session:
                mod_function = new_session.query(CustomController).filter(
                    CustomController.unique_id == self.unique_id).first()
                try:
                    dict_custom_options = json.loads(mod_function.custom_options)
                except:
                    dict_custom_options = {}
                dict_custom_options.pop(option)
                mod_function.custom_options = json.dumps(dict_custom_options)
                new_session.commit()
        except Exception:
            self.logger.exception("delete_custom_option")
