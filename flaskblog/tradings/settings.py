import config
import ccxt


exchanges = {}

########
# bitbay #
########

exchanges['bitbay'] = {}
exchanges['bitbay']['init'] = ccxt.bitbay(config.bitbay)
exchanges['bitbay']['limit'] = 100
exchanges['bitbay']['currency'] = 'pln'
exchanges['bitbay']['name'] = 'bitbay'
exchanges['bitbay']['name_trader'] = 'bitbay'
###############
# indodax #
###############

exchanges['indodax'] = {}
exchanges['indodax']['init'] = ccxt.indodax(config.indodax)
exchanges['indodax']['limit'] = 500
exchanges['indodax']['currency'] = 'idr'
exchanges['indodax']['name'] = 'indodax'
exchanges['indodax']['name_trader'] = 'indodax'

###############
# Coinbasepro GBP #
###############

exchanges['coinbasepro_gbp'] = {}
exchanges['coinbasepro_gbp']['init'] = ccxt.coinbasepro(config.gdax_gbp)
exchanges['coinbasepro_gbp']['limit'] = 500
exchanges['coinbasepro_gbp']['currency'] = 'gbp'
exchanges['coinbasepro_gbp']['name'] = 'coinbasepro'
exchanges['coinbasepro_gbp']['name_trader'] = 'coinbasepro_gbp'

###############
# Coinbasepro EUR #
###############

exchanges['coinbasepro_eur'] = {}
exchanges['coinbasepro_eur']['init'] = ccxt.coinbasepro(config.gdax_eur)
exchanges['coinbasepro_eur']['limit'] = 500
exchanges['coinbasepro_eur']['currency'] = 'eur'
exchanges['coinbasepro_eur']['name'] = 'coinbasepro'
exchanges['coinbasepro_eur']['name_trader'] = 'coinbasepro_eur'
