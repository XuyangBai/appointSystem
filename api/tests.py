# coding=utf-8
import datetime

from testing.testcase import TestCase


class ApiTests(TestCase):
    def setUp(self):
        self.bxy = self.createAccount('BXY', "123456789")
        self.classroom1 = self.createClassroom("500")
        self.classroom2 = self.createClassroom("400A")
        self.url = "/api/classroom/"
        self.today = datetime.date.today()

    def test_list(self):
        self.createAppointment(self.bxy, self.classroom1)
        response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(len(response.data['appointments']), 1)
        # get a wrong name
        response = self.client.get(self.url + "/" + self.classroom1.name + "12", decode=False)
        self.assertEqual(response.status_code, 404)

    def test_create_conflict_time(self):
        with self.logged_in_user(self.bxy.user):
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            init_size = response.data['size']
            data = {
                "classroom": self.classroom1.name,
                "start": 8,
                "end": 10,
                "date": str(self.today),
                "reason": "test",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 201)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)
            # 预约一个冲突的时间
            data = {
                "classroom": self.classroom1.name,
                "start": 9,
                "end": 11,
                "date": str(self.today),
                "reason": "test",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)

    def test_create_other_circumstance(self):
        with self.logged_in_user(self.bxy.user):
            # post with start < end
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "8",
                "date": str(self.today),
                "reason": "test",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('non_field_errors' in response.data, True)

            # post without reason
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "10",
                "date": str(self.today),
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('reason' in response.data, True)

            # post without before date
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "10",
                "date": str(self.today - datetime.timedelta(1)),
                "reason": "test"
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('non_field_errors' in response.data, True)
