# thanks to https://github.com/svbnet/diezel, https://gist.github.com/svbnet/b79b705a4c19d74896670c1ac7ad627e

from typing import Any

from requests import (
	post as req_post
)

from .exceptions.bad_credentials import Bad_Credentials

from .utils import (
	aes_enc, aes_dec
)


class API_Mobile:
	__API_URL = 'https://api.deezer.com/1.0/gateway.php'
	__MOBILE_GW_KEY = 'VBK1FSUEXHTSDBJJ'
	__MOBILE_API_KEY = '4VCYIJUCDLOUELGD1V8WBVYBNVDYOXEWSLLZDONGBBDFVXTZJRXPR29JRLQFO6ZE'


	def __init__(self, mail: str, password: str) -> None:
		self.__mail = mail
		self.__password = password


	def make_req(
		self,
		params: dict[str, str | int],
		json: dict[str, str] | None = None
	) -> dict[str, Any]:

		req = req_post(
			self.__API_URL,
			params = params,
			json = json
		).json()

		return req


	def login(self) -> str:
		__decrypted = aes_dec(self.__MOBILE_GW_KEY, self.__encrypted_token)
		self.__token = __decrypted[0:64]
		self.__token_key = __decrypted[64:80]
		__user_key = __decrypted[80:96]
		padded_password = self.__password.encode().ljust(16, b'\0')
		p = aes_enc(__user_key, padded_password)
		self.__login(self.__mail, p)

		return self.ARL


	@property
	def __encrypted_token(self) -> str:
		params = {
			'method': 'mobile_auth',
			'api_key': self.__MOBILE_API_KEY,
			'output': 3,
		}

		return self.make_req(params)['results']['TOKEN']
	

	@property
	def __sid(self) -> str:
		tok = aes_enc(
			self.__token_key, self.__token.encode()
		)

		params = {
			'method': 'api_checkToken',
			'api_key': self.__MOBILE_API_KEY,
			'output': 3,
			'auth_token': tok,
		}
	
		return self.make_req(params)['results']


	def __login(self, mail: str, hashed_password: str) -> str:
		params = {
			'method': 'mobile_userAuth',
			'api_key': self.__MOBILE_API_KEY,
			'output': 3,
			#'input': 3,
			'sid': self.__sid
		}

		json = {
			'mail': mail,
			'password': hashed_password,
			# 'device_serial': '',
			# 'platform': 'innotek GmbH_x86_64_9',
			# 'custo_version_id': '',
			# 'custo_partner': '',
			# 'model': 'VirtualBox',
			# 'device_name': 'VirtualBox',
			# 'device_os': 'Android',
			# 'device_type': 'tablet',
			# 'google_play_services_availability': '1',
			# 'consent_string': ''
		}

		res = self.make_req(
			params = params,
			json = json
		)

		
		if res['error']:
			raise Bad_Credentials(res, self.__mail)

		self.ARL = res['results']['ARL']

		return self.ARL