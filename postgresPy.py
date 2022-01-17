import psycopg2
import random
import datetime
import json

suppliers_names = ['Rapidplante', 'Outliermind', 'Nutripack', 'Strategist Nutrition', 'Paretsky', 'Neuzegroup Bv',
                   'Eryf Holdings', 'Carmel Mills', 'Norfast', 'Hipro', 'Pratfalla', 'Subsula', 'Sd2trol', 'Melotte']

customers_names = ['Verrolu', 'Lydore', 'Dairy Queen', 'Ationiml', 'Sharma Foods', 'Highfive', 'One Dollar Store',
                   'Nettwinder', 'La Vie En Chilombe', '123 Thrift Store', 'The Woodward', 'Cityfresh', 'Tin Vault']

cities_names = ['Ardbridge', 'Ariofield', 'Zierenhausen', 'Lieskirch', 'Diersingen', 'Kremly', 'Rahavinsk', 'Tvarru',
                'Walensiedeln', 'Freiendris', 'Grennois', 'Arnningen', 'Kaiserstadt', 'Arterio', 'Monterica','Dokshyvinsk',
                'Zhdadivka', 'Liuhanov', 'Yenalynska', 'Sosnochowa', 'Lipastovo', 'Nuremheim', 'Catadorm', 'Kapisaarsuk',
                'Fordstone', 'Stamborough', 'Cliffdwell', 'Newingport', 'Kapitalik', 'Cumberbury', 'Stockhampton', 'Kangerrapaluk',
                'Aladon', 'Harphampton', 'Bellgus', 'Brightmark', 'Petrowick', 'Putford', 'Hasville', 'Confolk', 'Summerdale',
                'Dettelscheid', 'Bellingarten', 'Mistelbruck', 'Paraschato', 'Caltanigliari', 'Kremeryska', 'Seretanka']

streets_names = ['Anchor Route', 'Adams Avenue', 'Highland Drive', 'Warren Street', 'Myrtle Street', 'Front Street North',
                 'Brandywine Drive', 'Cedar Lane', 'Route 41', 'Oak Avenue', 'Valley View Road', 'Lincoln Avenue', '10th Street',
                 'Elmwood Avenue', 'Cedar Avenue', 'Heather Court', '12th Street', '4th Street', 'Moskovskaya ul.', 'Lenina pr.',
                 '3 Internatsionala ul.', 'Normandii-Neman ul.', 'Gagarina pr.', 'Kennedy Orchards', 'Kerry Copse', 'Bradleys Lane',
                 'Silverton Road', 'Nemirovicha-Danchenko ul.', 'Znamenskaya ul.', 'Scharnweberstrasse', 'Hoheluftchaussee',
                 'Knesebeckstrasse', 'Neuer Jungfernstieg', 'Schoenebergerstrasse', 'Wallstrasse', 'Messedamm', 'boulevard de la Liberation',
                 'Rue du Palais', 'boulevard Amiral Courbe', 'Chemin Des Bateliers', 'ul. Rataja Macieja', 'ul. Dworcowa', 'ul. Dzwonki']

class Product:

    name: str
    unit: str
    unit_weight: float
    
    def __init__(self, name: str, unit: str, unit_weight: float):
        self.name = name
        self.unit = unit
        self.unit_weight = unit_weight

products = [Product('Sugar', 'kg', 1.0), Product('Flour', 'kg', 1.0),
            Product('Salt', 'kg', 0.5), Product('Butter', 'kg', 0.2),
            Product('Olive oil', 'l', 0.5), Product('Sunflower oil', 'l', 1),
            Product('White bread', 'g', 300), Product('Rye bread', 'g', 300),
            Product('Pasta', 'g', 450), Product('Pasta', 'g', 900),
            Product('Ketchup', 'g', 320), Product('Mayonnaise', 'g', 320),
            Product('Milk', 'l', 1), Product('Milk', 'l', 0.5),
            Product('Milk', 'l', 0.2), Product('Cream 35%', 'l', 1),
            Product('Cream 35%', 'l', 0.5), Product('Cream 35%', 'l', 0.25),
            Product('Cream 20%', 'l', 0.35), Product('Cream 20%', 'l', 0.5),
            Product('Cottage cheese 9%', 'g', 900), Product('Cottage cheese 9%', 'g', 250),
            Product('Cottage cheese 5%', 'g', 900), Product('Cottage cheese 5%', 'g', 250),
            Product('Sour cream 20%', 'g', 350), Product('Sour cream 20%', 'g', 500),
            Product('Sour cream 30%', 'g', 350), Product('Sour cream 30%', 'g', 500),
            Product('Cheese 48%', 'g', 150), Product('Cheese 52%', 'g', 150),
            Product('Cheese 60%', 'g', 150), Product('Mozzarella 45%', 'g', 100),
            Product('Mozzarella 45%', 'g', 250), Product('Still water', 'ml', 250),
            Product('Still water', 'ml', 500), Product('Still water', 'ml', 1000),
            Product('Sparkling water', 'ml', 250), Product('Sparkling water', 'ml', 500),
            Product('Sparkling water', 'ml', 1000), Product('Apple juice', 'ml', 500),
            Product('Apple juice', 'ml', 1000), Product('Orange juice', 'ml', 500),
            Product('Orange juice', 'ml', 1000), Product('Pineapple juice', 'ml', 500),
            Product('Pineapple juice', 'ml', 1000), Product('Tomato juice', 'ml', 500),
            Product('Tomato juice', 'ml', 1000), Product('Black tea', 'g', 200),
            Product('Black tea', 'g', 500), Product('Green tea', 'g', 200),
            Product('Green tea', 'g', 500), Product('Soap', 'g', 90),
            Product('Bleach', 'g', 300), Product('Washing powder', 'kg', 1)]

tel_numbers = []

def generate_telnum() -> str:
    res = '8'
    for i in range(10):
        res += str(random.randint(0, 9))
    if res not in tel_numbers:
        tel_numbers.append(res)
        return res
    else:
        return generate_telnum()

def generate_supplier_name() -> str:
    index = random.randrange(len(suppliers_names))
    result = suppliers_names.pop(index)
    return result

def generate_customer_name() -> str:
    index = random.randrange(len(customers_names))
    result = customers_names.pop(index)
    return result

def generate_client_address() -> str:
    city = random.choice(cities_names)
    cities_names.remove(city)
    street = random.choice(streets_names)
    streets_names.remove(street)
    number = random.randint(1, 100)
    result = city + ', ' + street + ', ' + str(number)
    return result

def generate_storage_number() -> int:
    return random.randint(1, 20)

def generate_quantity_supply() -> int:
    return random.randint(1000, 30000)

def generate_quantity_left(quantity_supply: int) -> int:
    return random.randint(int(quantity_supply*0.25), quantity_supply)

def generate_date(start_date: str = str(datetime.date(2020, 1, 1))) -> str:
    start_date = datetime.date(int(start_date.split('-')[0]),
                               int(start_date.split('-')[1]),
                               int(start_date.split('-')[2]))
    end_date = datetime.date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return str(random_date)

def create_connection():
    with open("credentials.json", "r") as credentials_file:
        credentials = json.load(credentials_file)
    conn = psycopg2.connect(dbname='facility_storage', user=credentials['user'],
                            password=credentials['password'], host='localhost')
    return conn

class Client:

    client_id: int
    name: str
    address: str
    telnum: str

    def __init__(self, client_id: int, name: str, address: str, telnum = ''):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.telnum = telnum

def fill_clients_table(conn):
    cursor = conn.cursor()
    query_clients = 'insert into suppliers_clients values (%s, \'%s\', \'%s\', \'%s\',\'%s\');'
    for i in range(1, len(suppliers_names) + len(customers_names) - 1):
        choice = random.randint(0, 1)
        if choice == 0 or len(customers_names) == 0:
            name = generate_supplier_name()
            client_type = 'S'
        elif choice == 1 or len(suppliers_names) == 0:
            name = generate_customer_name()
            client_type = 'C'
        address = generate_client_address()
        telnum = generate_telnum()
        cursor.execute(query_clients % (i, name, address, telnum, client_type))
    conn.commit()
    cursor.close()

def get_vendor_code(num: int) -> str:
    res = str(num)
    while len(res) < 8:
        res = '0' + res
    return res

def fill_products_table(conn):
    cursor = conn.cursor()
    query_products = 'insert into products values(\'%s\', \'%s\', \'%s\', %s);'
    for i in range(1, len(products)):
        vendor_code = get_vendor_code(i)
        product = products.pop(0)
        name = product.name
        unit = product.unit
        unit_weight = product.unit_weight
        cursor.execute(query_products % (vendor_code, name, unit, unit_weight))
    conn.commit()
    cursor.close()

def fill_storage_table(conn):
    cursor = conn.cursor()
    query_get_suppliers = 'select id from suppliers_clients where client_type = \'S\';'
    cursor.execute(query_get_suppliers)
    suppliers_response = cursor.fetchall()
    query_get_products = 'select vendor_code from products;'
    cursor.execute(query_get_products)
    products_response = cursor.fetchall()
    query_storage = 'insert into products_in_storage values (%s, %s, \'%s\', \'%s\', %s, \'%s\', %s, %s);'
    for i in range(1, len(products)):
        supply_number = i
        supplier = random.choice(suppliers_response)[0]
        date_supply = generate_date()
        vendor_code = products_response[i-1][0]
        storage_number = generate_storage_number()
        line_number = str(random.randint(1, 7))
        quantity_supply = generate_quantity_supply()
        quantity_left = generate_quantity_left(quantity_supply)
        cursor.execute(query_storage
                       % (supply_number, supplier,
                          date_supply, vendor_code,
                          storage_number, line_number,
                          quantity_supply, quantity_left))
    conn.commit()
    cursor.close()

def fill_orders_table(conn):
    cursor = conn.cursor()
    query_get_customers = 'select id from suppliers_clients where client_type = \'C\';'
    cursor.execute(query_get_customers)
    customers_response = cursor.fetchall()
    query_vendor_codes = 'select vendor_code from products;'
    cursor.execute(query_vendor_codes)
    vendor_codes_response = cursor.fetchall()
    for i in range(1, random.randint(50, 100)):
        customer = random.choice(customers_response)[0]
        product = random.choice(vendor_codes_response)[0]
        quantity = random.randint(100, 500)
        date_order = generate_date()
        is_completed = random.choice([True, False])
        if is_completed is True:
            date_complete = generate_date(date_order)
            cursor.execute('insert into orders values (%s, %s, \'%s\', %s, \'%s\', \'%s\');'
                           % (i, customer, product, quantity, date_order, date_complete))
        else:
            cursor.execute('insert into orders values (%s, %s, \'%s\', %s, \'%s\');'
                           % (i, customer, product, quantity, date_order))
    conn.commit()
    cursor.close()
    

if __name__ == '__main__':
    conn = create_connection()

    # fill suppliers/customers table
    fill_clients_table(conn)
    
    # fill products table
    fill_products_table(conn)

    # fill storage table
    fill_storage_table(conn)

    # fill orders table
    fill_orders_table(conn)
    conn.close()
