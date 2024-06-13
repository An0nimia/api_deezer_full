from api_deezer_full import (
	API_GW, API_Media, API_PIPE
)

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level = logging.DEBUG)

__ARL = 'd1b59217b86abb231097b0fdd2b0e2e03304af8b9d25d9408c9c0cb9fb65a9536b131094fb65a27a5fb52658c518f865119bf6e7dc5a573ad0ac364feca3513c7b7dd332d59e2edc72b3711b306c39f5ac4cd8422ce33828009f50cf418af99b'
__api = API_GW(__ARL)
__api.gw_search('eminem')