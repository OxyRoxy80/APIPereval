import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pereval_app.models import Pereval, User, Coords, Level, Images
from pereval_app.serializers import PerevalSerializer


class PerevalAPITestCase(APITestCase):

    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            beauty_title="ПЕРЕВАЛ-1",
            title="ПЕРЕВАЛ-1",
            other_titles="ПЕРЕВАЛ-1",
            connect="",
            add_time="2021-09-22T13:18:13Z",
            user=User.objects.create(
                email="email-1@email.ru",
                fam="fam-1",
                name="name-1",
                otc="otc-1",
                phone="89000000001"
            ),
            coords=Coords.objects.create(
                latitude=123.01,
                longitude=456.01,
                height=7891
            ),
            level=Level.objects.create(
                winter="1A",
                summer="1A",
                autumn="1A",
                spring="1A"
            )
        )
        self.image_1_1 = Images.objects.create(
            data="url_image_1_1",
            title="title_1_1",
            pereval=self.pereval_1
        )
        self.image_1_2 = Images.objects.create(
            data="url_image_1_2",
            title="title_1_2",
            pereval=self.pereval_1
        )

        self.pereval_2 = Pereval.objects.create(
            beauty_title="ПЕРЕВАЛ-2",
            title="ПЕРЕВАЛ-2",
            other_titles="ПЕРЕВАЛ-2",
            connect="connect-2",
            add_time="2021-09-22T13:18:13Z",
            user=User.objects.create(
                email="email-1@email.ru",
                fam="fam-2",
                name="name-2",
                otc="otc-2",
                phone="89000000002"
            ),
            coords=Coords.objects.create(
                latitude=123.02,
                longitude=456.02,
                height=7892
            ),
            level=Level.objects.create(
                winter="1B",
                summer="1B",
                autumn="1B",
                spring=""
            ),
            status="pending"
        )
        self.image_2_1 = Images.objects.create(
            data="url_image_2_1",
            title="title_2_1",
            pereval=self.pereval_2
        )
        self.image_2_2 = Images.objects.create(
            data="url_image_2_2",
            title="title_2_2",
            pereval=self.pereval_2
        )

    def test_get_list(self):
        url = reverse("pereval-list")
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(serializer_data))

    def test_get_detail(self):
        url = reverse("pereval-detail", args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post_pereval(self):
        url = reverse("pereval-list")
        data = {
            "beauty_title": "пер 2",
            "title": "Пхия 2",
            "other_titles": "Триев 2",
            "connect": "2",

            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "ivanov@mail.ru",
                     "fam": "Иванов",
                     "name": "Иван",
                     "otc": "Иванович",
                     "phone": "+7 555 55 55"},

            "coords": {
                "latitude": 45.3842,
                "longitude": 7.1525,
                "height": 1200},

            "level": {"winter": "",
                      "summer": "1А",
                      "autumn": "1А",
                      "spring": ""},

            "images": [{"data": "картинка3", "title": "Седловина"}, {"data": "картинка4", "title": "Подъём"}]
        }

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, Pereval.objects.all().count())

    def test_patch_pereval(self):
        url = reverse("pereval-detail", args=(self.pereval_1.id,))
        data = {
            "beauty_title": "ПЕРЕВАЛ-1",
            "title": "ПЕРЕВАЛ-1",
            "other_titles": "ПЕРЕВАЛ-1",
            "connect": "connect-1",

            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "email-1@email.ru",
                     "fam": "fam-1",
                     "name": "name-1",
                     "otc": "otc-1",
                     "phone": "89000000001"},

            "coords": {
                "latitude": 123.01,
                "longitude": 456.01,
                "height": 7891},

            "level": {"winter": "А",
                      "summer": "1А",
                      "autumn": "1А",
                      "spring": "А"},

            "images": [{"data": "картинка3", "title": "Седловина"}, {"data": "картинка4", "title": "Подъём"}]
        }

        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.pereval_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.pereval_1.connect, "connect-1")

    def test_patch_status_not_new(self):
        url = reverse("pereval-detail", args=(self.pereval_2.id,))
        data = {
            "beauty_title": "ПЕРЕВАЛ-1",
            "title": "ПЕРЕВАЛ-1",
            "other_titles": "ПЕРЕВАЛ-1",
            "connect": "",

            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "email-1@email.ru",
                     "fam": "fam-1",
                     "name": "name-1",
                     "otc": "otc-1",
                     "phone": "89000000001"},

            "coords": {
                "latitude": 123.01,
                "longitude": 456.01,
                "height": 7891},

            "level": {"winter": "А",
                      "summer": "1А",
                      "autumn": "1А",
                      "spring": "А"},

            "images": [{"data": "картинка3", "title": "Седловина"}, {"data": "картинка4", "title": "Подъём"}]
        }

        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.pereval_1.refresh_from_db()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(self.pereval_2.beauty_title, "ПЕРЕВАЛ-2")
        self.assertEqual(self.pereval_2.title, "ПЕРЕВАЛ-2")
        self.assertEqual(self.pereval_2.other_titles, "ПЕРЕВАЛ-2")
        self.assertEqual(self.pereval_2.connect, "connect-2")

    def test_patch_edit_user(self):
        url = reverse("pereval-detail", args=(self.pereval_1.id,))
        data = {
            "beauty_title": "ПЕРЕВАЛ-NEW",
            "title": "ПЕРЕВАЛ-1",
            "other_titles": "ПЕРЕВАЛ-1",
            "connect": "",

            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "email-5@email.ru",
                     "fam": "fam-5",
                     "name": "name-5",
                     "otc": "otc-5",
                     "phone": "89000000005"},

            "coords": {
                "latitude": 123.01,
                "longitude": 456.01,
                "height": 7891},

            "level": {"winter": "А",
                      "summer": "1А",
                      "autumn": "1А",
                      "spring": "А"},

            "images": [{"data": "картинка3", "title": "Седловина"}, {"data": "картинка4", "title": "Подъём"}]
        }

        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.pereval_1.refresh_from_db()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(self.pereval_1.user.email, "email-1@email.ru")
        self.assertEqual(self.pereval_1.user.fam, "fam-1")
        self.assertEqual(self.pereval_1.user.name, "name-1")
        self.assertEqual(self.pereval_1.user.otc, "otc-1")
        self.assertEqual(self.pereval_1.user.phone, "89000000001")