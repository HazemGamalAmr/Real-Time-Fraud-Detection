import pandas as pd
import random
from faker import Faker
import uuid
import datetime
#from shapely.geometry import Point, Polygon
import requests





#API_KEY = ''


def get_lat_lon_google_maps(address, api_key):
    try:
        # Define the API endpoint
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        
        # Send a GET request to the Google Maps API
        response = requests.get(endpoint)
        data = response.json()

        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Error geocoding address: {data['status']}")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


# Initialize Faker with localization for global data

fake = Faker('en_US')

currency = "USD"



#Random seed 
random_seed = 42  # You can choose any integer value as the seed
Faker.seed(random_seed)  # Set seed for Faker
random.seed(random_seed)  # Set seed for Python's random module

# Parameters (you can adjust these)
num_customers = 100  # Number of customers



# customer 1000 * 1000 


## 1 million to 2 million 
min_transactions_per_customer = 100  # Minimum number of transactions per customer
max_transactions_per_customer = 200  # Maximum number of transactions per customer
fraud_percentage = 0.10
start_date = datetime.datetime(2023, 9, 1)
end_date = datetime.datetime(2024, 9, 1)

# Calculate total number of transactions
num_rows = sum(random.randint(min_transactions_per_customer, max_transactions_per_customer) for x in range(num_customers))
num_fraudulent = int(num_rows * fraud_percentage)






# Define peak hours and assign more weight to them
peak_hours = list(range(8, 23))  # 8 AM to 8 PM (peak hours)
off_peak_hours = list(range(1, 8))  # 8 PM to 8 AM (off-peak hours)

# Assign weights to hours (e.g., higher weight for peak hours)
hour_weights = [2 if hour in peak_hours else 1 for hour in range(24)]  # Higher weight for peak hours

def generate_transaction_date():
    # Generate a random date using Faker
    random_date = fake.date_between(start_date=start_date, end_date=end_date)

    # Generate a random hour with bias towards peak hours
    hour = random.choices(range(24), weights=hour_weights, k=1)[0]
    
    # Generate random minutes and seconds
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    # Combine date and time
    transaction_datetime = datetime.datetime(
        year=random_date.year,
        month=random_date.month,
        day=random_date.day,
        hour=hour,
        minute=minute,
        second=second
    )
    
    return transaction_datetime





# Function to generate a transaction amount based on customer balance
def generate_transaction_amount(customer_balance):
    # Set minimum and maximum transaction amount relative to current balance
    min_transaction = (customer_balance * 0.03)  # Set a minimum transaction amount (e.g., $1)
    max_transaction = customer_balance * 0.3  # Ensure max is half of balance, leaving a min of $1
    return round(random.uniform(min_transaction, max_transaction), 2)

# Function to update the balance after a transaction
def update_balance(customer_balance, transaction_amount):
    # Deduct the transaction amount from the balance, but ensure balance never goes below $1
    new_balance = customer_balance - transaction_amount
    return max(new_balance, 200)  # Ensure balance never drops below $200


def generate_credit_card_type():
    card_types = ['Visa', 'MasterCard', 'American Express', 'Discover']
    return random.choice(card_types)




# Function to generate a random account balance based on income bracket
def generate_balance(income_bracket):
    if income_bracket == "Low":
        return round(random.uniform(1000, 5000), 2)  # Low income, smaller balance
    elif income_bracket == "Middle":
        return round(random.uniform(5000, 20000), 2)  # Mid income, medium balance
    elif income_bracket == "High":
        return round(random.uniform(20000, 50000), 2)  # High income, larger balance
    else:
        # Handle unexpected values by returning a default range
        return round(random.uniform(2000, 50000), 2)    

'''def Credit_Limit(income_bracket):
    if income_bracket == "Low":
        return round(random.uniform(1500, 7500), 2)  # Low income, smaller balance
    elif income_bracket == "Middle":
        return round(random.uniform(7500, 30000), 2)  # Mid income, medium balance
    elif income_bracket == "High":
        return round(random.uniform(30000, 75000), 2)  # High income, larger balance'''


# Generate customer data
def generate_customer():
    customer_id = str(uuid.uuid4())
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email() if random.random() > 0.05 else None  # Introduce some missing emails
    phone_number = fake.phone_number()
    #address = fake.address()
    #city = fake.city()
    #country = fake.country()
    birth_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=80)
    income_bracket = random.choices(["Low", "Middle", "High"] , weights=[3,6,1])   
    bank_name = ["JPMorgan Chase & Co.","Bank of America Corp.","Wells Fargo & Co.","Citigroup Inc.","Goldman Sachs Group Inc.","Morgan Stanley","U.S. Bancorp","Truist Financial Corp.","PNC Financial Services Group Inc.",
    "TD Group US Holdings LLC","Capital One Financial Corp.","Charles Schwab Corp.","Fifth Third Bancorp","BMO Financial Corp.","Ally Financial Inc.","American Express Co.","Citizens Financial Group Inc.","KeyCorp",
    "Huntington Bancshares Inc.","Regions Financial Corp.","M&T Bank Corp.","First Republic Bank","SVB Financial Group","Discover Financial Services","Comerica Inc.",]
    card_issuer_country = fake.country()
    transaction_channel = random.choice(["Online", "In-store", "Mobile"])
    cardholder_age = (datetime.datetime.now().year - birth_date.year)  # min_age 18  maximum 
    cardholder_gender = fake.random_element(elements=("Male", "Female")) 
    #lat, lon = generate_us_lat_lon()
    #account_balance = float(generate_balance(income_bracket))

    #address=fake.street_address()
    
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zip_code = fake.zipcode()
    formatted_address = f"{street_address}, {city}, {state} {zip_code}, USA"
    
    #region="Midwest"
    #lat, lon = generate_us_lat_lon(region=random.choice(regions))
    #lat,lan = get_lat_lon_google_maps(formatted_address,API_KEY)
    return {
        "Customer ID": customer_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Email": email,
        "Phone Number": phone_number,
        "Country": "United States",

        "City": city,

        "Latitude": fake.latitude(),
        "Longitude": fake.longitude(),
        "Birth Date": birth_date,
        "Income Bracket": income_bracket,
        "Bank Name": random.choice(bank_name),
        "Card Issuer Country": "United States",
        "Transaction Channel": transaction_channel,
        "Cardholder's Age": cardholder_age,
        "Cardholder's Gender": cardholder_gender,
        "Account Balance": float(generate_balance(income_bracket)) ,

        "street_address":street_address ,
        "Customer State": state,
        "Customer Zip Code": zip_code,

        "Card Type": generate_credit_card_type(),
        "Card Expiration Date": fake.credit_card_expire(start="now", end="+5y", date_format="%m/%y"),
        "Card Number": fake.credit_card_number(card_type=None),
        "Card CVV": fake.credit_card_security_code(card_type=None),
        #"Credit Limit": round(random.uniform(5000, 50000), 2),

    }











'''
check date.day 
if  transaction count<2 add random transaction in date.day 

''' 






# Generate transactions with customer references
def generate_combined_transaction(is_fraudulent, customer):


    
    transaction_id = str(uuid.uuid4())
    #card_number = fake.credit_card_number(card_type=None)
    #card_type = fake.credit_card_provider(card_type=None)
    card_expiry_date = fake.credit_card_expire(start="now", end="+5y", date_format="%m/%y")
    transaction_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    #amount = round(random.uniform(10 ''' change with amount < 0.5 % of  balance   ''', 5000'''   amount >  70 % of balance '''), 2) 

    #account_balance = round(random.uniform(1000, 20000), 2)
    
    #amount = round(random.uniform(customer["Account Balance"]*(0.03), customer["Account Balance"]*(0.6)), 2) # amount feh correlation with credit_balance 
    

    current_balance = customer["Account Balance"]

    amount=generate_transaction_amount(current_balance)

    #calc=(max_ number_of_transaction _customer * maxmum amount ) < balance_customer 
 
    merchant_name = fake.company()   # Introduce missing merchant names
    merchant_category_code = fake.random_int(min=4000, max=6000)
    transaction_type = random.choice(["Purchase", "Refund", "Withdrawal"])  
    authorization_code = fake.random_number(digits=6, fix_len=True)
     #    ["Low", "Middle", "High"] for each catogery  min & max 


    '''
    if cust_income == low 
        balance in range(,)
    elif cust_income == Middle  
        balance in range(,)
    else 
        blah blah blah 
    '''



    fraud_flag = is_fraudulent
    transaction_status = random.choices(["Approved", "Declined", "Pending"],weights=[90,9,1]) 
    pos_entry_mode = random.choice(["Chip", "Swipe", "Online", "Contactless"])  
    installment_plan = None
    if random.random() < 0.1:  # 10% chance of installment
        installment_plan = {
            "installments": random.randint(2, 12),
            "installment_amount": round(amount / random.randint(2, 12), 2)
        }
    merchant_id = str(uuid.uuid4())
    terminal_id = str(uuid.uuid4())
    #bank_name = fake.company() ##  give more than 100k bank _name  must ####be assure that every cust have only credit from one bank 
    #bank_name=[fake.unique.company() for i in range(25)]
    card_issuer_country = fake.country()
    #card_issuer_country=[fake.unique.country() for i in range(40)]
    transaction_channel = random.choice(["Online", "In-store", "Mobile"])  # Introduce missing transaction channels
    ip_address = fake.ipv4()
    device_info = {
        "device_type": random.choice(["Smartphone", "Laptop", "Tablet", "Desktop"]),
        "os": fake.user_agent().split()[0],
        "browser": fake.user_agent().split()[1]
    }
    transaction_risk_score = round(random.uniform(0, 1), 2)##  machine learing model 
    loyalty_points_earned = random.randint(0, 500)
    cardholder_age = (datetime.datetime.now().year - customer["Birth Date"].year)  # min_age 18  maximum 
    cardholder_gender = fake.random_element(elements=("Male", "Female"))  
    transaction_notes = random.choice(["High-value purchase", "First-time purchase", "Suspicious location"])
    fraud_detection_method = random.choice(["Machine Learning Model", "Rule-based System", "Manual Review"])  
    response_time = round(random.uniform(0.1, 5.0), 2)  # In seconds
    merchant_rating = round(random.uniform(1.0, 5.0), 1)
    recurring_transaction_flag = random.choice([True, False])
    

    #added=(amount*random.randint(1, 5)*0.01) #from 1% to 25%
    #customer["Account Balance"]=customer["Account Balance"]+ (amount-added)
    #customer["Account Balance"]=customer["Account Balance"]-amount
    


    # Combine customer info with transaction data


    return {
        "Transaction ID": transaction_id,
        "Transaction Date/Time": generate_transaction_date(),
        "Transaction Amount": amount,
        "Currency": currency ,  # Use different currencies
        "Merchant Name": merchant_name,
        "Merchant Category Code (MCC)": merchant_category_code,
        "Location": customer["City"] + ", " + customer["Country"],  # Use customer's location
        "Latitude": customer["Latitude"],
        "Longitude": customer["Longitude"],
        "Transaction Type": transaction_type,
        "Authorization Code": authorization_code,
        
        "Fraud Flag": fraud_flag,
        "Transaction Status": transaction_status,
        "POS Entry Mode": pos_entry_mode,
        "Installment Information": installment_plan,
        "Merchant ID": merchant_id,
        "Terminal ID": terminal_id,
        
        "IP Address": ip_address,
        "Device Information": device_info,
        "Transaction Risk Score": transaction_risk_score,
        "Loyalty Points Earned": loyalty_points_earned,
        
        "Transaction Notes": transaction_notes,
        "Cardholder's Income Bracket": customer["Income Bracket"],
        "Fraud Detection Method": fraud_detection_method,
        "Response Time": response_time,
        "Merchant Rating": merchant_rating,
        "Recurring Transaction Flag": recurring_transaction_flag,


        # Customer information
        "Customer ID": customer["Customer ID"],
        "First Name": customer["First Name"],
        "Last Name": customer["Last Name"],
        "Email": customer["Email"],
        "Phone Number": customer["Phone Number"],
        "Address": customer["street_address"],
        "Latitude": customer["Latitude"],
        "Longitude": customer["Longitude"],
        "City": customer["City"],
        "Country": customer["Country"],
        "Birth Date": customer["Birth Date"],
        "Income Bracket": customer["Income Bracket"],
        "Bank Name": customer["Bank Name"],
        "Card Issuer Country": customer["Card Issuer Country"],
        "Transaction Channel": customer["Transaction Channel"],
        "Cardholder's Age": customer["Cardholder's Age"],
        "Cardholder's Gender": customer["Cardholder's Gender"],
        "Account Balance": customer["Account Balance"],
        "Remaining Balance": update_balance(current_balance, amount),


        "Customer State": customer["Customer State"],
        "Customer Zip Code": customer["Customer Zip Code"],

        "Card Type":customer["Card Type"],
        "Card Expiration Date": customer["Card Expiration Date"],
        "Card Number":customer["Card Number"],
        "Card CVV": customer["Card CVV"],
        #"Credit Limit": customer["Credit Limit"],

    }

# Generate customers
customers = [generate_customer() for x in range(num_customers)]



# Select a subset of customers who will have fraudulent transactions
fraudulent_customers = random.sample(customers, k=int(num_customers * 0.3))  # e.g., 30% of customers can have fraud transactions

# Generate combined transactions
combined_transactions = []

'''# Ensure each customer has a minimum and maximum number of transactions
for customer in customers:
    num_transactions = random.randint(min_transactions_per_customer, max_transactions_per_customer)
    for x in range(num_transactions):
        combined_transactions.append(generate_combined_transaction(is_fraudulent=False, customer=customer))

'''
# Ensure each customer has a minimum and maximum number of transactions
for customer in customers:
    num_transactions = random.randint(min_transactions_per_customer, max_transactions_per_customer)
    
    # Determine if the customer is in the fraudulent customer subset
    is_customer_fraudulent = customer in fraudulent_customers
    for x in range(num_transactions):
        # Only assign fraudulent transactions if the customer is in the fraudulent subset
        if is_customer_fraudulent and random.random() < fraud_percentage:
            combined_transactions.append(generate_combined_transaction(is_fraudulent=True, customer=customer))
        else:
            combined_transactions.append(generate_combined_transaction(is_fraudulent=False, customer=customer))

'''
# Add fraudulent transactions
for x in range(num_fraudulent):
    customer = random.choice(customers)
    combined_transactions.append(generate_combined_transaction(is_fraudulent=True, customer=customer))
'''



random.shuffle(combined_transactions)  # Shuffle to mix fraudulent and non-fraudulent transactions

# Convert to DataFrame
combined_df = pd.DataFrame(combined_transactions)

# Save to CSV
combined_df.to_csv("Data_Set.csv", index=False)

print("Global combined data generation complete.")
