import time
import json
from selenium.common import WebDriverException

def slow_type(element, text, delay=0.25):
    """Envía cada carácter de 'text' al elemento con una demora para emular tipiado manual."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def retrieve_phone_code(driver) -> str:
    """Intercepta el código de confirmación del teléfono desde los logs de rendimiento."""
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log("performance")
                    if log.get("message") and "api/v1/number?number" in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd("Network.getResponseBody",
                                              {"requestId": message_data["params"]["requestId"]})
                code = "".join([x for x in body["body"] if x.isdigit()])
                if code:
                    break
        except WebDriverException:
            time.sleep(1)
            continue
        if code:
            return code
    raise Exception("No se encontró el código de confirmación del teléfono.")
