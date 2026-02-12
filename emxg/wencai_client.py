import logging
import requests
import json
import math
import pydash as _
from typing import List, Dict, Any, Optional, Union
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_exponential
from functools import lru_cache
from traceback import format_exc
from .data_adapter import DataFrame, concat, DataProcessor
from .device_info import wencai_session, wencai_headers, random_useragent
from .wencai_converter import parse_url_params, xuangu_tableV1_handler, multi_show_type_handler


logger = logging.getLogger(__package__)


class WencaiStockClient:
    ''' iWencai条件选股查询客户端
    '''
    def __init__(self):
        self.session = wencai_session()
        self.data_processor = DataProcessor()

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((requests.Timeout, requests.HTTPError, requests.ConnectionError))
    )
    def post(self, url, json=None, data=None, headers=None, **kwargs):
        if json is not None:
            return self.session.post(url, json=json, headers=headers, **kwargs)
        return self.session.post(url, data=data, headers=headers, **kwargs)

    def get_robot_data(self, **kwargs):
        question = kwargs.get('query')
        query_type = kwargs.get('query_type', 'stock')
        user_agent = kwargs.get('user_agent', None)
        request_params = kwargs.get('request_params', {})
        data = {
            'add_info': "{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}",
            'perpage': '10',
            'page': 1,
            'source': 'Ths_iwencai_Xuangu',
            'log_info': "{\"input_type\":\"click\"}",
            'version': '2.0',
            'secondary_intent': query_type,
            'question': question
        }

        pro = kwargs.get('pro', False)

        if pro:
            data['iwcpro'] = 1

        logger.debug(f'获取condition开始')

        result = self.post(
            'http://www.iwencai.com/customized/chart/get-robot-data',
            json=data, headers=wencai_headers(user_agent), **request_params)
        result = self.convert(result)

        if result:
            logger.debug(f'获取get_robot_data成功')
        else:
            logger.info(f'获取get_robot_data失败')

        return result

    def get_page(self, url_params, **kwargs):
        '''获取每页数据'''
        user_agent = kwargs.get('user_agent', None)
        find = kwargs.pop('find', None)
        query_type = kwargs.get('query_type', 'stock')
        request_params = kwargs.get('request_params', {})
        pro = kwargs.get('pro', False)
        if find is None:
            data = {
                **url_params,
                'perpage': 100,
                'page': 1,
                **kwargs
            }
            target_url = 'http://www.iwencai.com/gateway/urp/v7/landing/getDataList'
            if pro:
                target_url = f'{target_url}?iwcpro=1'
            path = 'answer.components.0.data.datas'
            colpath = 'answer.components.0.data.columns'
        else:
            if isinstance(find, List):
                # 传入股票代码列表时，拼接
                find = ','.join(find)
            data = {
                **url_params,
                'perpage': 100,
                'page': 1,
                'query_type': query_type,
                'question': find,
                **kwargs
            }
            target_url = 'http://www.iwencai.com/unifiedwap/unified-wap/v2/stock-pick/find'
            path = 'data.data.datas'
            colpath = 'data.data.columns'

        logger.debug(f'第{data.get("page")}页开始')

        request_params['timeout'] = (5, 10)
        res = self.post(target_url, data=data, headers=wencai_headers(user_agent), **request_params)
        result = json.loads(res.text)
        data_list = _.get(result, path)
        columns = _.get(result, colpath)
        if len(data_list) > 0:
            logger.debug(f'第{data.get("page")}页成功')
            result = self.data_processor.process_data(data_list, columns)
        else:
            logger.error(f'第{data.get("page")}页返回空！')
            raise Exception("data_list is empty!")

        if result is None:
            logger.error(f'第{data.get("page")}页失败')

        return result

    def loop_page(self, loop, row_count, url_params, **kwargs):
        '''循环分页'''
        count = 0
        perpage = kwargs.pop('perpage', 100)
        max_page = math.ceil(row_count / perpage)
        result = None
        if 'page' not in kwargs:
            kwargs['page'] = 1
        initPage = kwargs['page']
        loop_count = max_page if loop is True else loop
        while count < loop_count:
            kwargs['page'] = initPage + count
            resultPage = self.get_page(url_params, **kwargs)
            count = count + 1
            if result is None:
                result = resultPage
            else:
                result = concat([result, resultPage], ignore_index=True)

        return result

    def convert(self, res):
        '''处理get_robot_data的结果'''
        logger.debug(res.text)
        result = json.loads(res.text)
        content = _.get(result, 'data.answer.0.txt.0.content')
        if type(content) == str:
            content = json.loads(content)
        components = content['components']
        params = {}

        url = _.get(components[0], 'config.other_info.footer_info.url')
        if (len(components) == 1 and _.get(components[0], 'show_type') == 'xuangu_tableV1'):
            params = {
                'data': xuangu_tableV1_handler(components[0], components),
                'row_count': _.get(components[0], 'data.meta.extra.row_count'),
                'url': url,
                'url_params': parse_url_params(url)
            }
        else:
            params = {
                'data': multi_show_type_handler(components),
                'url': url,
                'url_params': parse_url_params(url)
            }
        return params

    def search(self, loop=False, **kwargs):
        params = self.get_robot_data(**kwargs)
        data = params.get('data')
        url_params = params.get('url_params')
        condition = data.get('condition', None)

        if condition is not None:
            kwargs = {**kwargs, **data}
            find = kwargs.get('find', None)
            if loop and find is None:
                row_count = params.get('row_count')
                return self.loop_page(loop, row_count, url_params, **kwargs)
            else:
                return self.get_page(url_params, **kwargs)
        else:
            no_detail = kwargs.get('no_detail')
            if no_detail != True:
                return data
            else:
                return None


@lru_cache(maxsize=1)
def create_client() -> WencaiStockClient:
    """创建并缓存EMStockClient实例"""
    return WencaiStockClient()


def search_wencai(keyword: str, max_count: Optional[int] = None,
               max_page: Optional[int] = None) -> Union[DataFrame, List[Dict[str, Any]]]:
    """使用i问财接口搜索股票数据"""
    loop = True
    if max_count is None and max_page is None:
        loop = True
    elif max_page is not None and max_page <= 1:
        loop = False
    elif max_count is not None and max_count <= 100:
        loop = False
    try:
        return create_client().search(loop=loop, query=keyword)
    except Exception as e:
        logger.error('获取i问财数据失败', e)
        logger.debug(format_exc())
        random_useragent.cache_clear()
    return None
