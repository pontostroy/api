# -*- coding: utf-8 -*-


def lot_create_tender_question(self):
    response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id, self.tender_token), {'data': {
        'title': 'question title',
        'description': 'question description',
        "questionOf": "lot",
        "relatedItem": self.initial_lots[0]['id'],
        'author': self.author_data
    }})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    question = response.json['data']
    self.assertEqual(question['author']['name'], self.author_data['name'])
    self.assertIn('id', question)
    self.assertIn(question['id'], response.headers['Location'])


def lot_create_tender_cancellations_and_questions(self):
    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id, self.tender_token), {'data': {
        'title': 'question title',
        'description': 'question description',
        "questionOf": "lot",
        "relatedItem": self.initial_lots[0]['id'],
        'author': self.author_data
    }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can add question only in active lot status")


def lot_patch_tender_question(self):
    response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id, self.tender_token), {'data': {
        'title': 'question title',
        'description': 'question description',
        "questionOf": "lot",
        "relatedItem": self.initial_lots[0]['id'],
        'author': self.author_data
    }})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    question = response.json['data']

    response = self.app.patch_json('/tenders/{}/questions/{}?acc_token={}'.format(
        self.tender_id, question['id'], self.tender_token), {"data": {"answer": "answer"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["answer"], "answer")
    self.assertIn('dateAnswered', response.json['data'])

    response = self.app.get(
        '/tenders/{}/questions/{}?acc_token={}'.format(self.tender_id, question['id'], self.tender_token))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["answer"], "answer")
    self.assertIn('dateAnswered', response.json['data'])

    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.patch_json('/tenders/{}/questions/{}?acc_token={}'.format(self.tender_id, question['id'], self.tender_token),
                                   {"data": {"answer": "answer"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update question in current (cancelled) tender status")

    response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id, self.tender_token), {'data': {
        'title': 'question title',
        'description': 'question description',
        "questionOf": "lot",
        "relatedItem": self.initial_lots[0]['id'],
        'author': self.author_data
    }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"],
                     "Can add question only in active lot status")