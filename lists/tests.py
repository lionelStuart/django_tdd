from django.http import HttpRequest
from django.test import TestCase

# Create your tests here.
from django.urls import resolve

from .models import Item, List
from .views import home_page


class HomepageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_post_request(self):
        response = self.client.post('/', data={'item_text': 'a new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "a new list item")

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'a new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item.objects.create(text="the first item", list=list_)
        second_item = Item.objects.create(text="the second item", list=list_)

        first_item.save()
        second_item.save()
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'a new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a new list item')

        print("res  {}".format(response))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displays_all_list_item(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")

        response = self.client.get("/")

        self.assertIn("item 1", response.content.decode())
        self.assertIn("item 2", response.content.decode())


class ListViewTest(TestCase):
    def test_uses_list_templates(self):
        response = self.client.get("/list/the-only-list/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_item(self):
        list_ = List.objects.create()
        Item.objects.create(text="item 1", list=list_)
        Item.objects.create(text="item 2", list=list_)

        response = self.client.get("/list/the-only-list/")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/list/new/", data={"item_text": "a new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "a new list item")

    def test_redirect_after_post(self):
        response = self.client.post("/list/new/", data={"item_text": "a new list item"})
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        # self.assertEqual(response['location'], 'list/the-only-list')
        self.assertRedirects(response, f"/list/{new_list.id}/")
