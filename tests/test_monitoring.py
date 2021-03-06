# Author: FL42

"""
Tests for main file
"""

import unittest

from monitoring import ServicesMonitoring
from tools import Message


class ServicesMonitoringTest(ServicesMonitoring):
    """
    Subclass of ServicesMonitoring used for testing without a config file
    """
    # We don't want to call the __init__ of the mother class
    # pylint: disable=W0231
    def __init__(self):
        """
        Define useful self variables
        """
        self.down_services = []
    # pylint: enable=W0231


class TestNotificationManagementLogic(unittest.TestCase):
    """
    Test self.manage_notifications()
    """

    def setUp(self):
        """
        Instantiate ServicesMonitoringTest class
        """
        self.services_monitoring = ServicesMonitoringTest()

    def test_one_notification(self):
        """
        Test with one notification
        """
        message1 = Message('Service 1', 'Message 1', Message.ERROR)
        notifications = [message1]
        self.services_monitoring.down_services = []

        notifications_to_send = \
            self.services_monitoring.manage_notifications(notifications)

        self.assertTrue(notifications_to_send == [message1])
        self.assertTrue(
            self.services_monitoring.down_services == [message1]
        )

    def test_back_online(self):
        """
        Test if a service was down but it's now up
        """
        message1 = Message('Service 1', 'Message 1', Message.ERROR)
        expected_notifications = [
            Message(
                'Service 1',
                'Message 1',
                Message.ERROR,
                'back online'
            )
        ]
        notifications = []
        self.services_monitoring.down_services = [message1]

        notifications_to_send = \
            self.services_monitoring.manage_notifications(notifications)

        self.assertTrue(notifications_to_send == expected_notifications)
        self.assertTrue(not self.services_monitoring.down_services)

    def test_still_down(self):
        """
        Test if a service is still down
        """
        message1 = Message('Service 1', 'Message 1', Message.ERROR)
        notifications = [message1]
        self.services_monitoring.down_services = [message1]

        notifications_to_send = \
            self.services_monitoring.manage_notifications(notifications)

        self.assertTrue(not notifications_to_send)
        self.assertTrue(
            self.services_monitoring.down_services == [message1]
        )
