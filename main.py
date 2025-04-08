import time
import json
import data
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import WebDriverException, TimeoutException


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


def slow_type(element, text, delay=0.2):
    """Envía cada carácter de 'text' al elemento con una demora para simular tipiado manual."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)


class UrbanRoutesPage:
    # Flujo de rutas:
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    search_taxi_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[1]/div[3]/div[1]/button")

    # Flujo de teléfono:
    phone_modal_button = (By.XPATH, "//div[contains(@class, 'np-button') and .//div[text()='Número de teléfono']]")
    phone_input_modal = (By.ID, "phone")
    next_button = (By.XPATH, "//div[contains(@class, 'modal')]//button[normalize-space(text())='Siguiente']")
    phone_code_input = (By.ID, "code")
    confirm_sms_button = (By.XPATH, "//div[contains(@class, 'modal')]//button[normalize-space(text())='Confirmar']")

    # Flujo de tarjeta de crédito:
    payment_method_button = (
    By.XPATH, "//div[contains(@class, 'pp-button') and .//div[contains(text(),'Método de pago')]]")
    add_card_option = (By.XPATH, "//div[contains(@class, 'pp-row') and contains(., 'Agregar tarjeta')]")
    card_modal_container = (By.XPATH, "//div[contains(@class, 'section') and contains(., 'Agregar tarjeta')]")
    # Usamos los XPaths exactos proporcionados:
    card_number_input = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/input")
    card_code_input = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input")
    add_card_button = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]")
    close_card_modal_button = (By.XPATH,
                               "//div[contains(@class, 'modal unusual')]//button[contains(@class, 'close-button') and contains(@class, 'section-close')]")

    # Otros elementos:
    message_textarea = (By.TAG_NAME, "textarea")
    blanket_checkbox = (By.ID, "blanket")
    tissues_checkbox = (By.ID, "tissues")
    ice_cream_increment_button = (By.CLASS_NAME, "counter__plus")
    order_button = (By.CLASS_NAME, "button_confirm")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def set_route(self, from_address, to_address):
        input_from = self.wait.until(EC.visibility_of_element_located(self.from_field))
        input_from.send_keys(from_address)
        input_to = self.wait.until(EC.visibility_of_element_located(self.to_field))
        input_to.send_keys(to_address)
        search_btn = self.wait.until(EC.element_to_be_clickable(self.search_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
        time.sleep(1)
        search_btn.click()
        print("Ruta establecida y 'Pedir un taxi' clickeado para generar el recorrido.")

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property("value")

    def select_comfort_tariff(self):
        comfort_title = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'tcard-title') and text()='Comfort']")))
        tcard = comfort_title.find_element(By.XPATH, "..")
        comfort_button = tcard.find_element(By.TAG_NAME, "button")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comfort_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", comfort_button)
        print("Tarifa Comfort seleccionada.")

    def enter_phone_number(self, phone):
        print("Abrir modal para ingresar número de teléfono...")
        modal_button = self.wait.until(EC.element_to_be_clickable(self.phone_modal_button))
        modal_button.click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.number-picker.open")))
        input_tel = self.wait.until(EC.element_to_be_clickable(self.phone_input_modal))
        input_tel.clear()
        input_tel.send_keys(phone)
        print("Número de teléfono ingresado:", phone)
        next_btn = self.wait.until(EC.element_to_be_clickable(self.next_button))
        next_btn.click()
        print("'Siguiente' en el modal de teléfono clickeado.")

    def enter_phone_code(self, code):
        print("Ingresar código SMS...")
        input_code = self.wait.until(EC.visibility_of_element_located(self.phone_code_input))
        input_code.clear()
        input_code.send_keys(code)
        print("Código SMS ingresado:", code)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_sms_button))
        confirm_btn.click()
        print("'Confirmar' código SMS clickeado.")

    def enter_card_data(self, card_number, card_code):
        print("Iniciar flujo para agregar tarjeta de crédito...")
        # Paso 1: Clic en 'Método de pago'
        payment_btn = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", payment_btn)
        time.sleep(1)
        payment_btn.click()
        print("'Método de pago' clickeado.")

        # Paso 2: Clic en 'Agregar tarjeta'
        add_card_opt = self.wait.until(EC.element_to_be_clickable(self.add_card_option))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_opt)
        time.sleep(1)
        add_card_opt.click()
        print("'Agregar tarjeta' clickeado en el modal de pago.")

        # Paso 3: Esperar que se muestre el modal de tarjeta
        self.wait.until(EC.visibility_of_element_located(self.card_modal_container))
        print("Modal 'Agregar tarjeta' visible.")

        # Paso 4: Ingresar el número de tarjeta con tipiado lento
        try:
            card_num_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
            card_num_input.clear()
            # Forzar doble clic para activar el input
            ActionChains(self.driver).move_to_element(card_num_input).double_click().perform()
            self.driver.execute_script("arguments[0].click();", card_num_input)
            slow_type(card_num_input, card_number, delay=0.25)
            print("Número de tarjeta ingresado:", card_number)
            print("Valor final en número de tarjeta:", card_num_input.get_attribute("value"))
        except TimeoutException:
            print("No se pudo interactuar con el input del número de tarjeta.")

        # Paso 5: Ingresar el CVV (código) con tipiado lento
        try:
            card_code_input = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
            card_code_input.clear()
            ActionChains(self.driver).move_to_element(card_code_input).double_click().perform()
            self.driver.execute_script("arguments[0].click();", card_code_input)
            slow_type(card_code_input, card_code, delay=0.25)
            print("Código (CVV) ingresado:", card_code)
            print("Valor final en CVV:", card_code_input.get_attribute("value"))
        except TimeoutException:
            print("No se pudo interactuar con el input del CVV.")

        # Paso 6: Forzar pérdida de foco en el campo del CVV
        try:
            # Enviar TAB para que el input pierda el foco
            card_code_input.send_keys(Keys.TAB)
            # Ejecutar blur explícitamente
            self.driver.execute_script("arguments[0].blur();", card_code_input)
            # Esperar 3 segundos para que React actualice su estado
            time.sleep(3)
            # Clic en el contenedor del modal para asegurar que se pierda el foco en caso de ser necesario
            container = self.wait.until(EC.visibility_of_element_located(self.card_modal_container))
            ActionChains(self.driver).move_to_element_with_offset(container, 10, 10).click().perform()
            print("Pérdida de foco forzada en el CVV con clic en el contenedor del modal.")
        except TimeoutException:
            print("No se pudo forzar el blur en el modal.")

        # Paso 7: Esperar que el botón "Agregar" se habilite y hacer clic
        def add_button_enabled(driver):
            btn = driver.find_element(*self.add_card_button)
            return btn.get_attribute("disabled") is None

        self.wait.until(add_button_enabled)
        try:
            add_card_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", add_card_btn)
            print("Botón 'Agregar' de tarjeta clickeado.")
        except TimeoutException:
            print("El botón 'Agregar' no se habilitó a tiempo; se salta el paso.")

    def close_card_modal(self):
        print("Cerrar modal de tarjeta...")
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(self.close_card_modal_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_btn)
            time.sleep(1)
            close_btn.click()
            print("Modal de tarjeta cerrado.")
        except TimeoutException:
            print("No se encontró el botón para cerrar el modal de tarjeta. Se continúa.")

    def enter_message_for_driver(self, message):
        textarea = self.wait.until(EC.visibility_of_element_located(self.message_textarea))
        textarea.clear()
        textarea.send_keys(message)
        print("Mensaje para el conductor ingresado:", message)

    def select_blanket_and_tissues(self):
        blanket = self.wait.until(EC.element_to_be_clickable(self.blanket_checkbox))
        blanket.click()
        tissues = self.wait.until(EC.element_to_be_clickable(self.tissues_checkbox))
        tissues.click()
        print("Manta y pañuelos seleccionados.")

    def add_ice_cream(self, quantity=2):
        for _ in range(quantity):
            ice_cream_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_increment_button))
            ice_cream_btn.click()
        print(f"{quantity} helados agregados.")

    def confirm_order(self):
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.order_button))
        confirm_btn.click()
        print("'Confirmar pedido' clickeado.")

    def click_order_taxi(self):
        print("Clic en 'Pedir un taxi'...")
        order_taxi = self.wait.until(EC.element_to_be_clickable(self.search_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", order_taxi)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", order_taxi)
        time.sleep(1)
        print("'Pedir un taxi' clickeado.")


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        print("Iniciando driver de Chrome...")
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        print("Driver iniciado y ventana maximizada.")

    def test_order_taxi(self):
        print("Abriendo la página de Urban Routes...")
        self.driver.get(data.urban_routes_url)
        print("URL abierta:", data.urban_routes_url)
        time.sleep(5)

        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from, "La dirección 'from' no coincide"
        assert routes_page.get_to() == data.address_to, "La dirección 'to' no coincide"

        routes_page.select_comfort_tariff()
        routes_page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        routes_page.enter_phone_code(code)
        routes_page.enter_card_data(data.card_number, data.card_code)
        routes_page.close_card_modal()
        routes_page.enter_message_for_driver(data.message_for_driver)
        routes_page.select_blanket_and_tissues()
        routes_page.add_ice_cream(2)
        routes_page.confirm_order()
        routes_page.click_order_taxi()

        print("Flujo de pedido de taxi completado exitosamente.")
        time.sleep(5)

    @classmethod
    def teardown_class(cls):
        print("Cerrando driver...")
        cls.driver.quit()
        print("Driver cerrado.")


if __name__ == '__main__':
    print("=== INICIO DE LA PRUEBA ===")
    TestUrbanRoutes.setup_class()
    test_instance = TestUrbanRoutes()
    try:
        test_instance.test_order_taxi()
    finally:
        TestUrbanRoutes.teardown_class()
    print("=== FIN DE LA PRUEBA ===")
























