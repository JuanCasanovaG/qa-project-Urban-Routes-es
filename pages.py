import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
    # (Se omite el clic en el botón "Requisitos del pedido" porque se despliega automáticamente)
    blanket_toggle = (
    By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    ice_cream_plus = (By.XPATH,
                      "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    reserve_button = (By.XPATH, "//*[@id='root']/div/div[3]/div[4]")

    # Elementos para confirmar el pedido:
    order_button = (By.CLASS_NAME, "button_confirm")

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def set_route(self, from_address: str, to_address: str):
        input_from = self.wait.until(EC.visibility_of_element_located(self.from_field))
        input_from.send_keys(from_address)
        input_to = self.wait.until(EC.visibility_of_element_located(self.to_field))
        input_to.send_keys(to_address)
        search_btn = self.wait.until(EC.element_to_be_clickable(self.search_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
        time.sleep(1)
        search_btn.click()
        print(f"Ruta configurada: Desde {from_address} hasta {to_address}")

    def get_from(self) -> str:
        return self.driver.find_element(*self.from_field).get_property("value")

    def get_to(self) -> str:
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

    def enter_phone_number(self, phone: str):
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

    def enter_phone_code(self, code: str):
        print("Ingresando código SMS:", code)
        input_code = self.wait.until(EC.visibility_of_element_located(self.phone_code_input))
        input_code.clear()
        input_code.send_keys(code)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_sms_button))
        confirm_btn.click()
        print("Clic en 'Confirmar' el código SMS.")

    def enter_card_data(self, card_number: str, card_code: str):
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            raise Exception("Timeout al esperar o hacer clic en el botón 'Agregar': " + str(e))

    def close_payment_modal(self):
        """Cierra el cuadro de 'Método de pago' usando el botón de 'X'."""
        print("Cerrando modal de 'Método de pago'...")
        try:
            payment_close = self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button))
            payment_close.click()
            print("Modal de 'Método de pago' cerrado.")
        except Exception:
            print("No se encontró el botón para cerrar el modal de 'Método de pago'. Continuando...")

    def enter_message_for_driver(self, message: str):
        print("Ingresando mensaje para el conductor...")
        msg_btn = self.wait.until(EC.element_to_be_clickable(self.message_button))
        msg_btn.click()
        print("Clic en el botón de mensaje para el conductor ejecutado.")
        message_input = self.wait.until(EC.visibility_of_element_located(self.message_text_input))
        message_input.clear()
        message_input.send_keys(message)
        print("Mensaje ingresado:", message)

    def select_requirements_and_reserve(self, ice_cream_qty: int = 2):
        print("Seleccionando Requisitos del pedido...")
        blanket_toggle = self.wait.until(EC.element_to_be_clickable(self.blanket_toggle))
        blanket_toggle.click()
        print("Opción de manta y pañuelos activada.")
        time.sleep(1)
        for i in range(ice_cream_qty):
            ice_cream_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus))
            ice_cream_btn.click()
            print(f"Helado agregado: {i + 1}")
            time.sleep(0.5)
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
