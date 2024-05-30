import pytest
from asyncmock import AsyncMock
from src.alpha_api_demo import AlphaESSAPI



@pytest.mark.asyncio
async def test_et_ess_list_one_device_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': [{'sysSn': 'SN1', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'}], 'extra': None}

    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__get_request", AsyncMock(return_value=mock_response))

    alpha_instance = AlphaESSAPI()
    results = await alpha_instance.get_ess_list()

    assert results[0]['sysSn'] == 'SN1'


@pytest.mark.asyncio
async def test_et_ess_list_three_devices_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': [], 'extra': None}
    for i in range(3):
        mock_response['data'].append({'sysSn': f'SN{i}', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'})

    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__get_request", AsyncMock(return_value=mock_response))

    alpha_instance = AlphaESSAPI()
    results = await alpha_instance.get_ess_list()

    for i, result in enumerate(results):
        assert result['sysSn'] == f'SN{i}'


@pytest.mark.asyncio
async def test_et_ess_list_one_device_not_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_response = {'code': 400, 'msg': 'Success', 'expMsg': None, 'data': [{'sysSn': 'SN1', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'}], 'extra': None}
    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__get_request", AsyncMock(return_value=mock_response))

    alpha_instance = AlphaESSAPI()
    results = await alpha_instance.get_ess_list()
    assert results == None

    mock_response = None
    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__get_request", AsyncMock(return_value=mock_response))

    alpha_instance = AlphaESSAPI()
    results = await alpha_instance.get_ess_list()
    assert results == None

