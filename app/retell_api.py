from __future__ import annotations

import requests


BASE_URL = "https://api.retellai.com"


class RetellAPIError(RuntimeError):
    pass


class RetellAPI:
    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def create_phone_call(
        self,
        *,
        from_number: str,
        to_number: str,
        metadata: dict | None = None,
        retell_llm_dynamic_variables: dict[str, str] | None = None,
        override_agent_id: str | None = None,
    ) -> dict:
        payload: dict = {
            "from_number": from_number,
            "to_number": to_number,
        }

        if metadata:
            payload["metadata"] = metadata
        if retell_llm_dynamic_variables:
            payload["retell_llm_dynamic_variables"] = retell_llm_dynamic_variables
        if override_agent_id:
            payload["override_agent_id"] = override_agent_id

        resp = self.session.post(f"{BASE_URL}/v2/create-phone-call", json=payload, timeout=30)
        if not resp.ok:
            raise RetellAPIError(
                f"Create phone call failed: {resp.status_code} {resp.text}"
            )
        return resp.json()

    def get_call(self, call_id: str) -> dict:
        resp = self.session.get(f"{BASE_URL}/v2/get-call/{call_id}", timeout=30)
        if not resp.ok:
            raise RetellAPIError(
                f"Get call failed: {resp.status_code} {resp.text}"
            )
        return resp.json()