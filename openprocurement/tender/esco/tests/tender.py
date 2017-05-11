# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy
from datetime import datetime, timedelta
from openprocurement.api import ROUTE_PREFIX
from openprocurement.api.models import get_now, SANDBOX_MODE
from openprocurement.tender.openeu.models import TENDERING_DAYS
from openprocurement.tender.esco.tests.base import (
    test_tender_eu_data,
    test_organization,
    BaseESCOWebTest, BaseESCOEUContentWebTest,
    snitch
)
from openprocurement.tender.esco.models import TenderESCOEU

from openprocurement.tender.esco.tests.tender_blanks import (
    simple_add_tender,
    empty_listing, listing, listing_changes,
    listing_draft, create_tender, get_tender,
    patch_tender, dateModified_tender,
    tender_not_found, guarantee,
    tender_Administrator_change
)


class TenderESCOEUTest(BaseESCOWebTest):
    initial_auth = ('Basic', ('broker', ''))

    test_simple_add_tender = snitch(simple_add_tender)


class TenderESCOTestCommon():

    test_empty_listing = snitch(empty_listing)
    test_listing = snitch(listing)
    test_listing_changes = snitch(listing_changes)
    test_listing_draft = snitch(listing_draft)
    test_create_tender = snitch(create_tender)
    test_get_tender = snitch(get_tender)
    test_patch_tender = snitch(patch_tender)
    test_dateModified_tender = snitch(dateModified_tender)
    test_tender_not_found = snitch(tender_not_found)
    test_guarantee = snitch(guarantee)
    test_tender_Administrator_change = snitch(tender_Administrator_change)


class TestTenderEU(TenderESCOTestCommon, BaseESCOEUContentWebTest):
    """ ESCO EU tender test """
    initialize_initial_data = False
    initial_data = test_tender_eu_data
    tender_period_duration = TENDERING_DAYS
