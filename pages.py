import time
import json
import data
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import WebDriverException, TimeoutException

#El codigo si me ejecuta bien la prueba hasta el final, corriendo o ejecutando desde el marcador Run 'main' y cumpliendo cada uno de los pasos.
#Ya actualice la URL

# -----------------------------------
# FUNCIONES DE AYUDA
# -----------------------------------
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


# -----------------------------------
# CLASE: UrbanRoutesPage (POM)
# -----------------------------------
class UrbanRoutesPage:
    # Elementos para configurar la ruta:
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    search_taxi_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[1]/div[3]/div[1]/button")

    # Elementos para el flujo de teléfono:
    phone_modal_button = (By.XPATH, "//div[contains(@class, 'np-button') and .//div[text()='Número de teléfono']]")
    phone_input_modal = (By.ID, "phone")
    next_button = (By.XPATH, "//div[contains(@class, 'modal')]//button[normalize-space(text())='Siguiente']")
    phone_code_input = (By.ID, "code")
    confirm_sms_button = (By.XPATH, "//div[contains(@class, 'modal')]//button[normalize-space(text())='Confirmar']")

    # Elementos para el flujo de tarjeta de crédito:
    payment_method_button = (
    By.XPATH, "//div[contains(@class, 'pp-button') and .//div[contains(text(),'Método de pago')]]")
    add_card_option = (By.XPATH, "//div[contains(@class, 'pp-row') and contains(., 'Agregar tarjeta')]")
    card_modal_container = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]")
    card_number_input = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]//input[@id='number']")
    card_code_input = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]//input[@id='code']")
    add_card_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[2]/form/div[3]//button")
    close_card_modal_button = (By.XPATH,
                               "//div[contains(@class, 'modal unusual')]//button[contains(@class, 'close-button') and contains(@class, 'section-close')]")
    close_payment_modal_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")

    # Elementos para el mensaje al conductor:
    message_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[3]")
    message_text_input = (By.ID, "comment")

    # Elementos para los requisitos del pedido:
    # Se usan los XPATH exactos que nos proporcionaste para activar manta y pañuelos y el contador de helados.
    blanket_toggle = (
    By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    ice_cream_plus = (By.XPATH,
                      "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    reserve_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[4]")

    # Otros elementos:
    order_button = (By.CLASS_NAME, "button_confirm")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def set_route(self, from_address, to_address):
        input_from = self.wait.until(EC.visibility_of_element_located(self.from_field))
        input_from.send_keys(from_address)
        input_to = self.wait.until(EC.visibility_of_element_located(self.to_field))
        input_to.send_keys(to_address)
        search_btn = self.wait.until(EC.element_to_be_clickable(self.search_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
        time.sleep(1)
        search_btn.click()
        print(f"Ruta configurada: Desde {from_address} hasta {to_address}")

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property("value")

    def select_comfort_tariff(self):
        comfort_title = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tcard-title') and text()='Comfort']")))
        tcard = comfort_title.find_element(By.XPATH, "..")
        comfort_button = tcard.find_element(By.TAG_NAME, "button")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", comfort_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", comfort_button)
        print("Tarifa Comfort seleccionada.")

    def enter_phone_number(self, phone):
        print("Ingresando número de teléfono...")
        modal_button = self.wait.until(EC.element_to_be_clickable(self.phone_modal_button))
        modal_button.click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.number-picker.open")))
        input_tel = self.wait.until(EC.element_to_be_clickable(self.phone_input_modal))
        input_tel.clear()
        input_tel.send_keys(phone)
        print("Número de teléfono ingresado:", phone)
        next_btn = self.wait.until(EC.element_to_be_clickable(self.next_button))
        next_btn.click()
        print("Clic en 'Siguiente' en el modal de teléfono.")

    def enter_phone_code(self, code):
        print("Ingresando código SMS:", code)
        input_code = self.wait.until(EC.visibility_of_element_located(self.phone_code_input))
        input_code.clear()
        input_code.send_keys(code)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_sms_button))
        confirm_btn.click()
        print("Clic en 'Confirmar' el código SMS.")

    def enter_card_data(self, card_number, card_code):
        print("=== Iniciando la parte de 'Agregar tarjeta' ===")
        # Paso 1: Clic en "Método de pago"
        payment_btn = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", payment_btn)
        time.sleep(1)
        payment_btn.click()
        print("Clic en 'Método de pago' ejecutado.")

        # Paso 2: Clic en "Agregar tarjeta"
        add_card_opt = self.wait.until(EC.element_to_be_clickable(self.add_card_option))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_opt)
        time.sleep(1)
        add_card_opt.click()
        print("Clic en 'Agregar tarjeta' ejecutado en el modal de pago.")

        # Paso 3: Esperar que aparezca el modal de tarjeta
        self.wait.until(EC.visibility_of_element_located(self.card_modal_container))
        print("Modal 'Agregar tarjeta' visible.")

        # Paso 4: Ingresar el número de tarjeta:
        try:
            card_num_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
            card_num_input.clear()
            ActionChains(self.driver).move_to_element(card_num_input).click().perform()
            time.sleep(0.5)
            card_num_input.send_keys(card_number)
            print("Número de tarjeta ingresado:", card_number)
            print("Valor final en el input de tarjeta:", card_num_input.get_attribute("value"))
        except TimeoutException as e:
            raise Exception("Timeout al interactuar con el input del número de tarjeta: " + str(e))

        # Paso 5: Ingresar el CVV (código):
        try:
            card_code_input = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
            card_code_input.clear()
            ActionChains(self.driver).move_to_element(card_code_input).click().perform()
            self.driver.execute_script("arguments[0].focus();", card_code_input)
            time.sleep(0.5)
            card_code_input.send_keys(card_code)
            print("Código (CVV) ingresado:", card_code)
            print("Valor final en el input de CVV:", card_code_input.get_attribute("value"))
        except TimeoutException as e:
            raise Exception("Timeout al interactuar con el input del CVV: " + str(e))

        # Paso 6: Forzar pérdida de foco en el campo CVV:
        try:
            print("Forzando pérdida de foco en el campo CVV (TAB, blur, ESC, clic en contenedor).")
            card_code_input.send_keys(Keys.TAB)
            self.driver.execute_script("arguments[0].blur();", card_code_input)
            card_code_input.send_keys(Keys.ESCAPE)
            time.sleep(3)
            container = self.wait.until(EC.visibility_of_element_located(self.card_modal_container))
            ActionChains(self.driver).move_to_element_with_offset(container, 10, 10).click().perform()
            print("Pérdida de foco forzada en el campo CVV mediante clic en el contenedor.")
        except TimeoutException as e:
            raise Exception("Timeout al forzar el blur en el campo CVV: " + str(e))

        # Paso 7: Esperar que el botón "Agregar" se habilite y hacer clic:
        def add_button_enabled(driver):
            btn = driver.find_element(*self.add_card_button)
            return btn.get_attribute("disabled") is None

        try:
            print("Esperando que el botón 'Agregar' se habilite...")
            self.wait.until(add_button_enabled)
            add_card_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_btn)
            time.sleep(1)
            add_card_btn.click()
            print("Clic en el botón 'Agregar' ejecutado.")
        except TimeoutException as e:
            raise Exception("Timeout al esperar o hacer clic en el botón 'Agregar': " + str(e))

    def close_payment_modal(self):
        """Cierra el cuadro de 'Método de pago' usando el botón de 'X'."""
        print("Cerrando modal de 'Método de pago'...")
        try:
            payment_close = self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button))
            payment_close.click()
            print("Modal de 'Método de pago' cerrado.")
        except TimeoutException:
            print("No se encontró el botón para cerrar el modal de 'Método de pago'. Continuando...")

    def enter_message_for_driver(self, message):
        print("Ingresando mensaje para el conductor...")
        msg_btn = self.wait.until(EC.element_to_be_clickable(self.message_button))
        msg_btn.click()
        print("Clic en el botón de mensaje para el conductor ejecutado.")
        message_input = self.wait.until(EC.visibility_of_element_located(self.message_text_input))
        message_input.clear()
        message_input.send_keys(message)
        print("Mensaje ingresado:", message)

    def select_requirements_and_reserve(self, ice_cream_qty=2):
        print("Seleccionando Requisitos del pedido...")
        # Se asume que el contenedor de requisitos ya está desplegado automáticamente.
        # Paso 1: Activar la opción de manta y pañuelos:
        blanket_toggle = self.wait.until(EC.element_to_be_clickable(self.blanket_toggle))
        blanket_toggle.click()
        print("Opción de manta y pañuelos activada.")
        time.sleep(1)
        # Paso 2: Agregar helado (clic en el botón de "+") la cantidad indicada:
        for i in range(ice_cream_qty):
            ice_cream_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus))
            ice_cream_btn.click()
            print(f"Helado agregado: {i + 1}")
            time.sleep(0.5)
        # Paso 3: Clic en el botón "Reservar":
        reserve_btn = self.wait.until(EC.element_to_be_clickable(self.reserve_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", reserve_btn)
        time.sleep(1)
        reserve_btn.click()
        print("Clic en el botón 'Reservar' ejecutado.")

    def confirm_order(self):
        print("Confirmando pedido...")
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.order_button))
        confirm_btn.click()
        print("Pedido confirmado.")

    def click_order_taxi(self):
        print("Pidiendo taxi...")
        order_taxi = self.wait.until(EC.element_to_be_clickable(self.search_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", order_taxi)
        time.sleep(1)
        order_taxi.click()
        time.sleep(1)
        print("Clic en 'Pedir un taxi' ejecutado.")


# -----------------------------------
# CLASE: TestUrbanRoutes (Pruebas individuales)
# -----------------------------------
class TestUrbanRoutes:
    def __init__(self, driver):
        self.driver = driver
        self.page = UrbanRoutesPage(driver)

    def test_configurar_direccion(self):
        print("PRUEBA: Configurar dirección")
        self.page.set_route(data.address_from, data.address_to)
        assert self.page.get_from() == data.address_from, "La dirección 'from' no coincide"
        assert self.page.get_to() == data.address_to, "La dirección 'to' no coincide"

    def test_seleccionar_tarifa(self):
        print("PRUEBA: Seleccionar tarifa Comfort")
        self.page.select_comfort_tariff()

    def test_ingresar_telefono(self):
        print("PRUEBA: Ingresar número de teléfono")
        self.page.enter_phone_number(data.phone_number)

    def test_ingresar_codigo_sms(self):
        print("PRUEBA: Ingresar código SMS")
        code = retrieve_phone_code(self.driver)
        self.page.enter_phone_code(code)

    def test_agregar_tarjeta(self):
        print("PRUEBA: Agregar tarjeta de crédito")
        self.page.enter_card_data(data.card_number, data.card_code)
        self.page.close_payment_modal()

    def test_ingresar_mensaje(self):
        print("PRUEBA: Ingresar mensaje para el conductor")
        self.page.enter_message_for_driver(data.message_for_driver)

    def test_seleccionar_requisitos(self):
        print("PRUEBA: Seleccionar Requisitos del pedido (manta, pañuelos y 2 helados)")
        self.page.select_requirements_and_reserve(2)

    def test_confirmar_pedido(self):
        print("PRUEBA: Confirmar pedido")
        self.page.confirm_order()

    def test_pedir_taxi(self):
        print("PRUEBA: Pedir taxi")
        self.page.click_order_taxi()


# -----------------------------------
# FUNCIONES DE EJECUCIÓN
# -----------------------------------
def main():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(data.urban_routes_url)
        time.sleep(5)
        tests = TestUrbanRoutes(driver)
        tests.test_configurar_direccion()
        time.sleep(1)
        tests.test_seleccionar_tarifa()
        time.sleep(1)
        tests.test_ingresar_telefono()
        time.sleep(1)
        tests.test_ingresar_codigo_sms()
        time.sleep(1)
        tests.test_agregar_tarjeta()
        time.sleep(1)
        tests.test_ingresar_mensaje()
        time.sleep(1)
        tests.test_seleccionar_requisitos()
        time.sleep(1)
        tests.test_confirmar_pedido()
        time.sleep(1)
        tests.test_pedir_taxi()
        time.sleep(5)
        print("Flujo completo de pedido de taxi ejecutado exitosamente.")
    finally:
        driver.quit()


# -----------------------------------
# EJECUCIÓN
# -----------------------------------
if __name__ == '__main__':
    # Ejecutar el flujo completo de forma única:
    main()












































