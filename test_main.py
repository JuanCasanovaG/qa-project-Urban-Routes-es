import time
import pytest
import data
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.page = UrbanRoutesPage(cls.driver)
        cls.driver.get(data.urban_routes_url)
        time.sleep(5)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

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


#if __name__ == '__main__':
    #pytest.main()














































