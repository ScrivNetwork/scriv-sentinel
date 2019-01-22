import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from scrivd import ScrivDaemon
from scriv_config import ScrivConfig


def test_scrivd():
    config_text = ScrivConfig.slurp_config_file(config.scriv_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000341742751657129c08995d46795094e9e9e48ac1b0908f6ca1ffae197c7'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000003e4498531ba1f89172241bbb76325fc212aa5932c95d7fa273cd31830bf'

    creds = ScrivConfig.get_rpc_creds(config_text, network)
    scrivd = ScrivDaemon(**creds)
    assert scrivd.rpc_command is not None

    assert hasattr(scrivd, 'rpc_connection')

    # scriv testnet block 0 hash == 000003e4498531ba1f89172241bbb76325fc212aa5932c95d7fa273cd31830bf
    # test commands without arguments
    info = scrivd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert scrivd.rpc_command('getblockhash', 0) == genesis_hash
