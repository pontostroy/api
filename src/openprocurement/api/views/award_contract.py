# -*- coding: utf-8 -*-
from logging import getLogger
from cornice.resource import resource, view
from openprocurement.api.models import Contract
from openprocurement.api.utils import (
    apply_patch,
    save_tender,
    error_handler,
)
from openprocurement.api.validation import (
    validate_contract_data,
    validate_patch_contract_data,
)


LOGGER = getLogger(__name__)


@resource(name='Tender Award Contracts',
          collection_path='/tenders/{tender_id}/awards/{award_id}/contracts',
          path='/tenders/{tender_id}/awards/{award_id}/contracts/{contract_id}',
          description="Tender award contracts",
          error_handler=error_handler)
class TenderAwardContractResource(object):

    def __init__(self, request):
        self.request = request
        self.db = request.registry.db

    @view(content_type="application/json", permission='create_award_contract', validators=(validate_contract_data,), renderer='json')
    def collection_post(self):
        """Post a contract for award
        """
        tender = self.request.validated['tender']
        if tender.status not in ['active.awarded', 'complete']:
            self.request.errors.add('body', 'data', 'Can\'t add contract in current ({}) tender status'.format(tender.status))
            self.request.errors.status = 403
            return
        contract_data = self.request.validated['data']
        contract = Contract(contract_data)
        contract.awardID = self.request.validated['award_id']
        self.request.validated['award'].contracts.append(contract)
        save_tender(self.request)
        LOGGER.info('Created tender award contract {}'.format(contract.id), extra={'MESSAGE_ID': 'tender_award_contract_create'})
        self.request.response.status = 201
        self.request.response.headers['Location'] = self.request.route_url('Tender Award Contracts', tender_id=tender.id, award_id=self.request.validated['award_id'], contract_id=contract['id'])
        return {'data': contract.serialize()}

    @view(renderer='json', permission='view_tender')
    def collection_get(self):
        """List contracts for award
        """
        return {'data': [i.serialize() for i in self.request.validated['award'].contracts]}

    @view(renderer='json', permission='view_tender')
    def get(self):
        """Retrieving the contract for award
        """
        return {'data': self.request.validated['contract'].serialize()}

    @view(content_type="application/json", permission='edit_tender', validators=(validate_patch_contract_data,), renderer='json')
    def patch(self):
        """Update of contract
        """
        if self.request.validated['tender_status'] not in ['active.awarded', 'complete']:
            self.request.errors.add('body', 'data', 'Can\'t update contract in current ({}) tender status'.format(self.request.validated['tender_status']))
            self.request.errors.status = 403
            return
        apply_patch(self.request, src=self.request.context.serialize())
        LOGGER.info('Updated tender award contract {}'.format(self.request.context.id), extra={'MESSAGE_ID': 'tender_award_contract_patch'})
        return {'data': self.request.context.serialize()}
