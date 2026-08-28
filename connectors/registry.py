"""Connector registry used by status endpoints and release evidence."""

from connectors.clarity.connector import ClarityConnector
from connectors.ga4.connector import GA4Connector
from connectors.google_ads.connector import GoogleAdsConnector
from connectors.merchant.connector import MerchantConnector
from connectors.salla_mcp.connector import SallaMCPConnector
from connectors.search_console.connector import SearchConsoleConnector


def connector_registry():
    return [
        SallaMCPConnector(), GA4Connector(), SearchConsoleConnector(),
        MerchantConnector(), ClarityConnector(), GoogleAdsConnector(),
    ]
