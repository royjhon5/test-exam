from django.test import Client, SimpleTestCase


class AlertsApiTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_tenant_scoped_alerts(self):
        response = self.client.get("/api/alerts", **{"HTTP_X_TENANT_ID": "tenant-acme", "HTTP_X_USER_ROLE": "analyst"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["tenant_id"], "tenant-acme")
        self.assertTrue(all(item["tenant_id"] == "tenant-acme" for item in payload["items"]))
        self.assertIn("enrichment", payload["items"][0])

    def test_requires_tenant_header(self):
        response = self.client.get("/api/alerts")
        self.assertEqual(response.status_code, 401)

    def test_rejects_unknown_tenant(self):
        response = self.client.get("/api/alerts", **{"HTTP_X_TENANT_ID": "tenant-unknown", "HTTP_X_USER_ROLE": "admin"})
        self.assertEqual(response.status_code, 403)
