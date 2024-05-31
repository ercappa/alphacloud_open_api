import pytest
from asyncmock import AsyncMock
from src.alpha_api_demo import AlphaESSAPI


async def __http_get_helper(mocker, mock_response, method_name, *args):
    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__get_request", AsyncMock(return_value=mock_response))
    alpha_instance = AlphaESSAPI()
    return await getattr(alpha_instance, method_name)(*args) 


async def __http_post_helper(mocker, mock_response, method_name, *args):
    mocker.patch.object(AlphaESSAPI, "_AlphaESSAPI__post_request", AsyncMock(return_value=mock_response))
    alpha_instance = AlphaESSAPI()
    return await getattr(alpha_instance, method_name)(*args) 


@pytest.mark.asyncio
async def test_get_ess_list_one_device_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_data = [{'sysSn': 'SN1', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'}]
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    results = await __http_get_helper(mocker, mock_response, 'get_ess_list')
    assert results[0] == mock_data[0]


@pytest.mark.asyncio
async def test_get_ess_list_three_devices_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': [], 'extra': None}
    mock_data = []
    for i in range(3):
        mock_data.append({'sysSn': f'SN{i}', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'})
    mock_response['data'] = mock_data

    results = await __http_get_helper(mocker, mock_response, 'get_ess_list')
    for i, result in enumerate(results):
        assert result == mock_data[i]



@pytest.mark.asyncio
async def test_get_ess_list_one_device_not_ok(mocker):
    
    # Mock the get_last_power_data AlphaESSAPI
    mock_data = [{'sysSn': 'SN1', 'popv': 6.1, 'minv': 'MODEL', 'poinv': 1.0, 'cobat': 30, 'mbat': 'MOD_BATT', 'surplusCobat': 10, 'usCapacity': 100.0, 'emsStatus': 'Normal'}]
    mock_response = {'code': 400, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_ess_list')
    assert results == None

    mock_response = None
    results = await __http_get_helper(mocker, mock_response, 'get_ess_list')
    assert results == None



@pytest.mark.asyncio
async def test_get_last_power_data_ok(mocker):

    mock_data = {'ppv': 757.0, 'ppvDetail': {'ppv1': 405.0, 'ppv2': 352.0, 'ppv3': 0.0, 'ppv4': 0.0, 'pmeterDc': 0.0}, 'soc': 100.0, 'pev': 0, 'pevDetail': {'ev1Power': 0, 'ev2Power': 0, 'ev3Power': 0, 'ev4Power': 0}, 'prealL1': 746.0, 'prealL2': 0.0, 'prealL3': 0.0, 'pbat': 0.0, 'pload': 313.0, 'pgrid': -444.0, 'pgridDetail': {'pmeterL1': -703.0, 'pmeterL2': 26.0, 'pmeterL3': 233.0}}
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_last_power_data', 'sv')
    assert results == mock_data




@pytest.mark.asyncio
async def test_get_last_power_data_wrong_app_id(mocker):

    mock_response = {'code': 6007, 'msg': 'Sign check error'}
    
    results = await __http_get_helper(mocker, mock_response, 'get_last_power_data', 'sv')
    assert results == None


@pytest.mark.asyncio
async def test_get_last_power_data_wrong_app_secret(mocker):

    mock_response = {'code': 6007, 'msg': 'Sign check error'}
    
    results = await __http_get_helper(mocker, mock_response, 'get_last_power_data', 'sv')
    assert results == None


@pytest.mark.asyncio
async def test_get_last_power_data_wrong_sn(mocker):

    mock_response = {'code': 6005, 'msg': 'This appId is not bound to the SN', 'expMsg': None, 'data': None, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_last_power_data', 'sv')
    assert results == None


@pytest.mark.asyncio
async def test_get_one_date_energy_by_sn_ok(mocker):

    mock_data = {'sysSn': 'SN1', 'theDate': '2023-06-10', 'eCharge': 10.1, 'epv': 30.6, 'eOutput': 1.77, 'eInput': 0.46, 'eGridCharge': 0.0, 'eDischarge': 7.4, 'eChargingPile': 11.25}
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_one_date_energy_by_sn', 'sv', '2023-06-23')
    assert results == mock_data


@pytest.mark.asyncio
async def test_get_one_date_power_by_sn_ok(mocker):

    #this is only a part of the data ... 
    mock_data = [{'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:57:34', 'ppv': 0, 'load': 272.0, 'cbat': 85.2, 'feedIn': 0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:52:33', 'ppv': 0, 'load': 276.0, 'cbat': 85.2, 'feedIn': 0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:47:32', 'ppv': 0, 'load': 280.0, 'cbat': 85.6, 'feedIn': 0, 'gridCharge': 1.0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:42:31', 'ppv': 0, 'load': 369.0, 'cbat': 86.0, 'feedIn': 0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:37:30', 'ppv': 0, 'load': 368.0, 'cbat': 86.4, 'feedIn': 0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:32:30', 'ppv': 0, 'load': 284.0, 'cbat': 86.8, 'feedIn': 11.0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:27:35', 'ppv': 0, 'load': 280.0, 'cbat': 87.2, 'feedIn': 1.0, 'gridCharge': 0, 'pchargingPile': 0},
                 {'sysSn': 'SN1', 'uploadTime': '2023-06-10 23:26:35', 'ppv': 0, 'load': 279.0, 'cbat': 87.2, 'feedIn': 1.0, 'gridCharge': 0, 'pchargingPile': 0}] 
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_one_date_power_by_sn', 'sv', '2023-06-23')
    assert results == mock_data


@pytest.mark.asyncio
async def test_get_in_charge_config_info_ok(mocker):

    mock_data = {'gridCharge': 0, 'timeChaf1': '07:00', 'timeChae1': '12:00', 'timeChaf2': '00:00', 'timeChae2': '00:00', 'batHighCap': 100.0}
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_in_charge_config_info', 'sn')
    assert results == mock_data


@pytest.mark.asyncio
async def test_get_out_charge_config_info_ok(mocker):

    mock_data = {'ctrDis': 0, 'timeDisf1': '17:00', 'timeDise1': '00:00', 'timeDisf2': '00:00', 'timeDise2': '08:00', 'batUseCap': 10.0}
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_get_helper(mocker, mock_response, 'get_out_charge_config_info', 'sn')
    assert results == mock_data


@pytest.mark.asyncio
async def test_update_in_charge_config_info_ok(mocker):

    mock_data = None
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_post_helper(mocker, mock_response, 'update_in_charge_config_info', 'sn', 100.0, 0, '12:00', '00:00', '00:00', '00:00')
    assert results == 200



@pytest.mark.asyncio
async def test_update_out_charge_config_info_ok(mocker):

    mock_data = None
    mock_response = {'code': 200, 'msg': 'Success', 'expMsg': None, 'data': mock_data, 'extra': None}
    
    results = await __http_post_helper(mocker, mock_response, 'update_out_charge_config_info', 'sn', 100.0, 0, '12:00', '00:00', '00:00', '00:00')
    assert results == 200
